-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "updated_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "deleted_at" TIMESTAMP,
    "is_active" BOOLEAN NOT NULL DEFAULT True,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "password" VARCHAR(256) NOT NULL,
    "email" VARCHAR(128) NOT NULL UNIQUE,
    "phone" VARCHAR(12) NOT NULL UNIQUE,
    "full_name" VARCHAR(128) NOT NULL,
    "birthday" DATE,
    "last_login" TIMESTAMP
);
ALTER TABLE "user" ALTER "created_at" TYPE timestamptz USING "created_at" AT TIME ZONE 'UTC';
ALTER TABLE "user" ALTER "updated_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';
ALTER TABLE "user" ALTER "deleted_at" TYPE timestamptz USING "deleted_at" AT TIME ZONE 'UTC';
ALTER TABLE "user" ALTER "last_login" TYPE timestamptz USING "last_login" AT TIME ZONE 'UTC';

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
DROP TABLE IF EXISTS "user";
