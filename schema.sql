DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS item_list;

CREATE TABLE user
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    password    TEXT        NOT NULL,
    date_joined TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_level  INTEGER     NOT NULL
);

CREATE TABLE items
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL,
    cost        INTEGER NOT NULL
);