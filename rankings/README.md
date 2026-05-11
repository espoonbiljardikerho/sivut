# EBK Ranking — schema + sample frontend

A working prototype for storing and displaying the rankings currently
published as JPEGs at
https://www.espoonbiljardikerho.com/tulospalvelu/ranking/.

## What's here

| File | Purpose |
| ---- | ------- |
| `schema.sql`         | SQLite schema (3 tables + 1 view) |
| `build_db.py`        | Creates `ebk_rankings.db` and seeds it with sample data |
| `export_json.py`     | Dumps the DB into a single `rankings.json` |
| `template.html`      | The frontend with a `/*__DATA__*/null` placeholder |
| `build_html.py`      | Inlines `rankings.json` into the template |
| `ebk_rankings.html`  | **The final standalone viewer** — open in a browser |

## Schema

Three tables, one view:

- **`players`** — `id, name, slug, first_year, notes`
- **`competitions`** — one row per *discipline + year* (e.g. "Pool 2025"),
  plus a combined `kind='ebk'` overall ranking per year.  Stores the
  source JPEG URL and an `is_current` flag for the in-progress season.
- **`results`** — one row per player per competition season, with
  `rank`, `total_points`, `events_played`, and `event_points` (a JSON
  array of per-week scores so the schema doesn't pin the number of
  events).
- **`v_rankings`** — flat view joining everything, which the frontend
  reads from.

## Sample data

The seed script uses real EBK member names from the club's roster but
fabricated points / rankings.  Five years (2022–2026) × five disciplines
(kaisa, pool, kara, pyramid, plus combined ebk) = 25 competitions,
~870 result rows, 46 players.

## Frontend

Three views, all in `ebk_rankings.html`:

1. **Current standings** — pick a discipline, see this year's leaderboard.
   Marked "live" and links back to the live Dropbox JPEG as a
   verification source.
2. **Archive** — pick any year + discipline from history.
3. **Player profile** — pick any player, get total seasons, best finish,
   podium / title counts, a per-discipline rank chart over time, and
   the full list of seasons.  Clicking a player name in any leaderboard
   jumps straight to their profile.

Aesthetic: billiard-cloth green + cream paper, Fraunces serif for
display, JetBrains Mono for labels.  No build tools, no framework —
just a single HTML file with the data inlined.

## Production path

For a real deployment you'd:

1. Replace `build_db.py` seed data with real ingestion — either ask the
   club for the source spreadsheet behind the JPEG exports (likely
   exists), or OCR the archive JPEGs.
2. Serve `rankings.json` from an endpoint (or split it per year) instead
   of inlining, so updates don't require a rebuild.
3. Add a small admin form (or a Google Sheet sync) to enter new weekly
   results, then regenerate the JPEG *from* the database for backward
   compatibility with the existing site.
