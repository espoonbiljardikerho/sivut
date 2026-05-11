"""
Build ebk_rankings.db from schema.sql and seed it with sample data.

The sample data uses real EBK member names (from the club's members
page) but the rankings/points are entirely fabricated - this is a
demo dataset, not the actual standings.
"""

import json
import random
import sqlite3
import unicodedata
from pathlib import Path

HERE = Path(__file__).parent
SCHEMA = HERE / "schema.sql"
DB = HERE / "ebk_rankings.db"


def slugify(name: str) -> str:
    """'Lindroos Tomi' -> 'lindroos-tomi'."""
    norm = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return norm.lower().replace(" ", "-")


# A subset of real members from espoonbiljardikerho.com/jasenet/.
PLAYERS = [
    "Lindroos Tomi", "Lindroos Hannu", "Träff Teemu", "Träff Tuomo",
    "Ahola Jarno", "Ahola Joni", "Ahola Risto", "Pekkala Panu",
    "Saarinen Santeri", "Latvala Samuel", "Latvala Santeri",
    "Kauppinen Mikko", "Sutinen Mikko", "Ranta Mikko", "Paajanen Mikko",
    "Lahelma Mikko", "Komi Tuomas", "Hyvönen Tuomas", "Ronkainen Tuomas",
    "Kronbäck Tuomo", "Kahima Jaakko", "Vähäsarja Jaakko", "Noponen Jaakko",
    "Lukkari Juuso", "Lounamaa Joonas", "Asp Niklas", "Asp Kaj",
    "Grönberg Markku", "Grönholm Max", "Hällström Jukka", "Hällström Niko",
    "Kalliomäki Pentti", "Wigelius Pauli", "Verho Pekka", "Räisänen Pekka",
    "Pesäkivi Pekka", "Narvanto Pekka", "Peltonen Tommi",
    "Fredriksson Tommi", "Janzon Tor", "Jansson Jari", "Sironen Jari",
    "Muhonen Timo", "Montonen Timo", "Kuosmanen Timo", "Pöyhönen Aki",
]

DISCIPLINES = ["kaisa", "pool", "kara", "pyramid"]
YEARS = [2022, 2023, 2024, 2025, 2026]

# Live JPEG URLs from the EBK ranking page for the in-progress year.
CURRENT_IMAGES = {
    "kaisa":   "https://www.dropbox.com/scl/fi/9n1mtf2hrbyl7iy2gpjuo/ranking_kaisa.jpg?rlkey=o9hswo2e84rbelb1yer094edo&raw=1",
    "pool":    "https://www.dropbox.com/scl/fi/dbwnt0zbd4zoz4mqvyoor/ranking_pool.jpg?rlkey=2apniefb5rrptncwi1rnszapj&raw=1",
    "kara":    "https://www.dropbox.com/scl/fi/vi5qamf887xrc2d4z6cme/ranking_kara.jpg?rlkey=wkta0e0hakjbagn7tugf0oloj&raw=1",
    "pyramid": "https://www.dropbox.com/scl/fi/8czkh3j2iq7gi21myj5vu/ranking_pyramidi.jpg?rlkey=7s93t6v6qdaurv1n9317lqt2h&raw=1",
    "ebk":     "https://www.dropbox.com/scl/fi/p8go97pj4et2yn78rv811/ranking_EBK.jpg?rlkey=a0dj81gemm1qdleyaczxyb47l&raw=1",
}


def archived_image(year: int, kind: str) -> str:
    """Best-effort URL for an archived year's JPEG.

    Real archive URLs include opaque IDs we don't have; this fakes a
    plausible path. In a real ingestion pipeline you'd grab the actual
    URL from the page when you scrape that year.
    """
    suffix = "pyramidi" if kind == "pyramid" else kind
    suffix = "EBK" if kind == "ebk" else suffix
    return f"https://example.invalid/ranking_{suffix}_{year}.jpg"


def make_results(players, n_events: int, rng: random.Random):
    """Generate plausible per-event scores for each player, then rank
    them by total. Each player skips some events (None entries)."""
    rows = []
    for p in players:
        # Base skill level per player, perturbed per event.
        skill = rng.gauss(50, 15)
        events = []
        for _ in range(n_events):
            if rng.random() < 0.25:
                events.append(None)  # didn't show up
            else:
                events.append(max(0, round(rng.gauss(skill, 8))))
        played = sum(1 for e in events if e is not None)
        total = sum(e for e in events if e is not None)
        rows.append({
            "player": p,
            "events": events,
            "events_played": played,
            "total": total,
        })
    rows.sort(key=lambda r: (-r["total"], -r["events_played"]))
    for i, r in enumerate(rows, start=1):
        r["rank"] = i
    return rows


def main():
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA.read_text())

    # ---- players ---------------------------------------------------
    player_ids = {}
    for name in PLAYERS:
        cur = conn.execute(
            "INSERT INTO players(name, slug, first_year) VALUES (?, ?, ?)",
            (name, slugify(name), min(YEARS)),
        )
        player_ids[name] = cur.lastrowid

    # ---- competitions + results -----------------------------------
    rng = random.Random(42)  # deterministic sample data
    for year in YEARS:
        is_current = 1 if year == max(YEARS) else 0
        per_discipline_totals = {p: 0.0 for p in PLAYERS}

        for kind in DISCIPLINES:
            title = f"{kind.capitalize()} {year}"
            image = CURRENT_IMAGES[kind] if is_current else archived_image(year, kind)
            cur = conn.execute(
                """INSERT INTO competitions(year, kind, title, source_image, is_current)
                   VALUES (?, ?, ?, ?, ?)""",
                (year, kind, title, image, is_current),
            )
            comp_id = cur.lastrowid

            # Not every player plays every discipline.
            participants = [p for p in PLAYERS if rng.random() > 0.3]
            n_events = rng.randint(20, 30)
            rows = make_results(participants, n_events, rng)

            for r in rows:
                conn.execute(
                    """INSERT INTO results
                       (competition_id, player_id, rank, total_points,
                        event_points, events_played)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (comp_id, player_ids[r["player"]], r["rank"],
                     r["total"], json.dumps(r["events"]), r["events_played"]),
                )
                # Accumulate toward combined EBK ranking.
                # Rough weighting: better rank in a discipline = more EBK points.
                ebk_pts = max(0, 100 - r["rank"] * 3) + r["total"] * 0.2
                per_discipline_totals[r["player"]] += ebk_pts

        # ---- combined EBK ranking for the year ---------------------
        title = f"EBK Ranking {year}"
        image = CURRENT_IMAGES["ebk"] if is_current else archived_image(year, "ebk")
        cur = conn.execute(
            """INSERT INTO competitions(year, kind, title, source_image, is_current)
               VALUES (?, ?, ?, ?, ?)""",
            (year, "ebk", title, image, is_current),
        )
        ebk_comp_id = cur.lastrowid

        ranked = sorted(per_discipline_totals.items(),
                        key=lambda kv: -kv[1])
        for i, (name, pts) in enumerate(ranked, start=1):
            if pts <= 0:
                continue
            conn.execute(
                """INSERT INTO results
                   (competition_id, player_id, rank, total_points,
                    event_points, events_played)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (ebk_comp_id, player_ids[name], i, round(pts, 1), None, None),
            )

    conn.commit()
    conn.close()
    print(f"Wrote {DB}  ({DB.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
