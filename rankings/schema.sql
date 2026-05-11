-- =============================================================
-- EBK Ranking database schema (SQLite)
-- =============================================================
-- Models the rankings currently published as JPEGs at
-- https://www.espoonbiljardikerho.com/tulospalvelu/ranking/
--
-- Design notes:
--  * One row in `results` = one player's standing in one competition
--    season (a discipline + year, e.g. "Pool 2025").
--  * Individual weekly-event points are kept as JSON in
--    `results.event_points` so the schema isn't tied to the
--    number of weeks, which varies year to year.
--  * `competitions.kind` distinguishes the per-discipline
--    rankings ("kaisa", "pool", "kara", "pyramid", "snooker")
--    from the combined club ranking ("ebk").
-- =============================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS competitions;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
    id         INTEGER PRIMARY KEY,
    -- Stored "Lastname Firstname" to match how EBK lists members.
    name       TEXT NOT NULL UNIQUE,
    -- Slug for URLs / lookups, e.g. "lindroos-tomi".
    slug       TEXT NOT NULL UNIQUE,
    -- Optional: when the player first appears in a ranking.
    first_year INTEGER,
    notes      TEXT
);

CREATE TABLE competitions (
    id            INTEGER PRIMARY KEY,
    year          INTEGER NOT NULL,
    -- One of: 'kaisa', 'pool', 'kara', 'pyramid', 'snooker', 'ebk'.
    kind          TEXT NOT NULL CHECK (kind IN
                  ('kaisa','pool','kara','pyramid','snooker','ebk')),
    -- Human-readable label, e.g. "Pool 2025" or "EBK Ranking 2025".
    title         TEXT NOT NULL,
    -- Where the source JPEG lives (Dropbox for current year,
    -- yhdistysavain.fi for archived years).
    source_image  TEXT,
    -- True for the year currently in progress; lets the frontend
    -- mark it as "live" and hit the Dropbox link for the latest pic.
    is_current    INTEGER NOT NULL DEFAULT 0,
    UNIQUE (year, kind)
);

CREATE TABLE results (
    id              INTEGER PRIMARY KEY,
    competition_id  INTEGER NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
    player_id       INTEGER NOT NULL REFERENCES players(id)      ON DELETE CASCADE,
    rank            INTEGER NOT NULL,
    total_points    REAL    NOT NULL,
    -- Per-event points as a JSON array, e.g. "[12, 8, null, 15, 10]".
    -- null = player didn't participate that week.
    event_points    TEXT,
    -- How many events the player actually showed up to.
    events_played   INTEGER,
    UNIQUE (competition_id, player_id),
    UNIQUE (competition_id, rank)
);

-- Helpful indexes for the three frontend views.
CREATE INDEX idx_results_player      ON results(player_id);
CREATE INDEX idx_results_competition ON results(competition_id);
CREATE INDEX idx_competitions_year   ON competitions(year);
CREATE INDEX idx_competitions_kind   ON competitions(kind);

-- =============================================================
-- Convenience view: flat ranking rows with names/years attached.
-- The frontend mostly reads from this.
-- =============================================================
DROP VIEW IF EXISTS v_rankings;
CREATE VIEW v_rankings AS
SELECT
    c.year            AS year,
    c.kind            AS discipline,
    c.title           AS competition_title,
    c.is_current      AS is_current,
    r.rank            AS rank,
    p.name            AS player,
    p.slug            AS player_slug,
    r.total_points    AS total_points,
    r.events_played   AS events_played,
    r.event_points    AS event_points
FROM results r
JOIN competitions c ON c.id = r.competition_id
JOIN players      p ON p.id = r.player_id;
