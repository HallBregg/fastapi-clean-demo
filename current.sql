BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> c6ec6d05af2d

CREATE TABLE book (
    id SERIAL NOT NULL, 
    title VARCHAR, 
    primary_author VARCHAR, 
    PRIMARY KEY (id)
);

INSERT INTO alembic_version (version_num) VALUES ('c6ec6d05af2d') RETURNING alembic_version.version_num;

COMMIT;

