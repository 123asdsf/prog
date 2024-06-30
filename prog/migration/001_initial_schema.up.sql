CREATE TABLE Routes (
    id_route SERIAL NOT NULL,
    name VARCHAR(60) NOT NULL UNIQUE,
    CONSTRAINT K2 PRIMARY KEY (id_route)
);

CREATE TABLE Groups (
    peer_ids INTEGER NOT NULL,
    group_number VARCHAR(60) NOT NULL UNIQUE,
    route INTEGER NOT NULL,
    course INTEGER NOT NULL,
    CONSTRAINT K1 PRIMARY KEY (peer_ids),
    CONSTRAINT C1 FOREIGN KEY (route) REFERENCES Routes (id_route)
);

CREATE TABLE Rules (
    id_rule SERIAL NOT NULL,
    name VARCHAR(60) NOT NULL,
    functional VARCHAR(120) NOT NULL,
    CONSTRAINT K4 PRIMARY KEY (id_rule)
);

CREATE TABLE Users (
    peer_id INTEGER NOT NULL UNIQUE,
    name VARCHAR(60) NOT NULL,
    surname VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    rule INTEGER NOT NULL,
    CONSTRAINT K3 PRIMARY KEY (peer_id),
    CONSTRAINT C2 FOREIGN KEY (rule) REFERENCES Rules (id_rule)
);

