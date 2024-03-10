-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

CREATE TABLE IF NOT EXISTS "valid_campaign_type"
(
    "type" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_campaign_type" (type)
VALUES ('direct_apply'),
       ('issue_voucher');

CREATE TABLE IF NOT EXISTS "valid_campaign_status"
(
    "status" VARCHAR(16) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_campaign_status" (status)
VALUES ('draft'),
        ('waiting'),
        ('running'),
        ('pause'),
        ('completed'),
        ('deleted');

CREATE TABLE IF NOT EXISTS "campaign" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "updated_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "deleted_at" TIMESTAMP,
    
    "start_at" TIMESTAMP,
    "end_at" TIMESTAMP,

    "name" VARCHAR(128) NOT NULL UNIQUE,
    "status" VARCHAR(16) NOT NULL REFERENCES "valid_campaign_status" ("status") DEFAULT 'draft',
    "type" VARCHAR(32) NOT NULL REFERENCES "valid_campaign_type" ("type") DEFAULT 'direct_apply',
    "total_vouchers" INT NOT NULL DEFAULT 0
);
ALTER TABLE "campaign" ALTER "created_at" TYPE timestamptz USING "created_at" AT TIME ZONE 'UTC';
ALTER TABLE "campaign" ALTER "updated_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';
ALTER TABLE "campaign" ALTER "deleted_at" TYPE timestamptz USING "deleted_at" AT TIME ZONE 'UTC';
ALTER TABLE "campaign" ALTER "start_at" TYPE timestamptz USING "start_at" AT TIME ZONE 'UTC';
ALTER TABLE "campaign" ALTER "end_at" TYPE timestamptz USING "end_at" AT TIME ZONE 'UTC';

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
DROP TABLE IF EXISTS "campaign";

DROP TABLE IF EXISTS "valid_campaign_type";
DROP TABLE IF EXISTS "valid_campaign_status";
