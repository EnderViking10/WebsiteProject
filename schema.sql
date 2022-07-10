DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS item_list;

CREATE TABLE user
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    username          TEXT UNIQUE NOT NULL,
    password          TEXT        NOT NULL,
    date_joined       TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_level        INTEGER     NOT NULL,
    restriction_level INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE items
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL,
    cost        INTEGER NOT NULL
);

CREATE TABLE tickets
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id   INTEGER   NOT NULL,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title       TEXT      NOT NULL,
    description TEXT      NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users (id)
)