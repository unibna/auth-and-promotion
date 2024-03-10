-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd
CREATE TABLE IF NOT EXISTS "valid_voucher_type"
(
    "type" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_voucher_type" (type)
VALUES ('direct_discount'),
    ('gift');


CREATE TABLE IF NOT EXISTS "valid_voucher_value_unit"
(
    "unit" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_voucher_value_unit" (unit)
VALUES ('number'),
        ('percent'),
        ('string');


CREATE TABLE IF NOT EXISTS "voucher" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "updated_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),

    "expired_at" TIMESTAMP,
    "claimed_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "used_at" TIMESTAMP,

    "campaign_id" INT NOT NULL REFERENCES "campaign" ("id"),
    "user_id" INT NOT NULL REFERENCES "user" ("id"),
    "type" VARCHAR(32) NOT NULL REFERENCES "valid_voucher_type" ("type"),
    "value" VARCHAR(256),
    "value_unit" VARCHAR(32) NOT NULL REFERENCES "valid_voucher_value_unit" ("unit")
);
ALTER TABLE "voucher" ALTER "created_at" TYPE timestamptz USING "created_at" AT TIME ZONE 'UTC';
ALTER TABLE "voucher" ALTER "updated_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';
ALTER TABLE "voucher" ALTER "expired_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';
ALTER TABLE "voucher" ALTER "claimed_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';
ALTER TABLE "voucher" ALTER "used_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
DROP TABLE IF EXISTS "voucher";

DROP TABLE IF EXISTS "valid_voucher_type";
DROP TABLE IF EXISTS "valid_voucher_value_unit";
