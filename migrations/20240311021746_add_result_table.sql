-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd
CREATE TABLE IF NOT EXISTS "valid_result_type"
(
    "type" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_result_type" (type)
VALUES ('voucher'),
    ('cash');


CREATE TABLE IF NOT EXISTS "valid_result_value_unit"
(
    "unit" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_result_value_unit" (unit)
VALUES ('number'),
        ('percent'),
        ('string');


CREATE TABLE IF NOT EXISTS "result" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "updated_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),

    "campaign_id" INT NOT NULL REFERENCES "campaign" ("id"),
    "type" VARCHAR(32) NOT NULL REFERENCES "valid_result_type" ("type"),
    "value" VARCHAR(256),
    "value_unit" VARCHAR(32) NOT NULL REFERENCES "valid_result_value_unit" ("unit")
);
ALTER TABLE "result" ALTER "created_at" TYPE timestamptz USING "created_at" AT TIME ZONE 'UTC';
ALTER TABLE "result" ALTER "updated_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
DROP TABLE IF EXISTS "result";

DROP TABLE IF EXISTS "valid_result_type";
DROP TABLE IF EXISTS "valid_result_value_unit";
