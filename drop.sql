BEGIN;

-- Running downgrade c6ec6d05af2d -> 

DROP TABLE book;

DELETE FROM alembic_version WHERE alembic_version.version_num = 'c6ec6d05af2d';

DROP TABLE alembic_version;

COMMIT;
