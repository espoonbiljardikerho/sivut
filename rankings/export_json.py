"""Export the SQLite DB to a single JSON file for the static frontend.

For a real site you'd serve this from an API endpoint or generate one
JSON file per discipline+year. Bundling everything works fine at this
scale (a few thousand rows).
"""

import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "ebk_rankings.db"
OUT = HERE / "rankings.json"


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    players = [dict(r) for r in con.execute(
        "SELECT id, name, slug, first_year FROM players ORDER BY name")]

    competitions = [dict(r) for r in con.execute(
        "SELECT id, year, kind, title, source_image, is_current "
        "FROM competitions ORDER BY year, kind")]

    results = []
    for r in con.execute(
        "SELECT competition_id, player_id, rank, total_points, "
        "       event_points, events_played "
        "FROM results ORDER BY competition_id, rank"):
        d = dict(r)
        # Parse the JSON event list now so the frontend doesn't have to.
        if d["event_points"]:
            d["event_points"] = json.loads(d["event_points"])
        results.append(d)

    data = {
        "generated_from": str(DB.name),
        "players": players,
        "competitions": competitions,
        "results": results,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT}  ({OUT.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
