-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd
CREATE TABLE IF NOT EXISTS "valid_condition_type"
(
    "type" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_condition_type" (type)
VALUES ('event');


CREATE TABLE IF NOT EXISTS "valid_condition_operator"
(
    "operator" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_condition_operator" (operator)
VALUES ('equal'),
        ('not_equal');


CREATE TABLE IF NOT EXISTS "valid_condition_value_type"
(
    "type" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_condition_value_type" (type)
VALUES ('int'),
        ('float'),
        ('string');


CREATE TABLE IF NOT EXISTS "valid_condition_value_unit"
(
    "unit" VARCHAR(32) NOT NULL PRIMARY KEY
);
INSERT INTO "valid_condition_value_unit" (unit)
VALUES ('number'),
        ('percent'),
        ('string');


CREATE TABLE IF NOT EXISTS "condition" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    "updated_at" TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),

    "campaign_id" INT NOT NULL REFERENCES "campaign" ("id"),
    "type" VARCHAR(32) NOT NULL REFERENCES "valid_condition_type" ("type"),
    "operator" VARCHAR(32) NOT NULL REFERENCES "valid_condition_operator" ("operator"),
    "value_type" VARCHAR(32) NOT NULL REFERENCES "valid_condition_value_type" ("type"),
    "value" VARCHAR(256),
    "value_unit" VARCHAR(32) NOT NULL REFERENCES "valid_condition_value_unit" ("unit")
);
ALTER TABLE "condition" ALTER "created_at" TYPE timestamptz USING "created_at" AT TIME ZONE 'UTC';
ALTER TABLE "condition" ALTER "updated_at" TYPE timestamptz USING "updated_at" AT TIME ZONE 'UTC';

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
DROP TABLE IF EXISTS "condition";

DROP TABLE IF EXISTS "valid_condition_type";
DROP TABLE IF EXISTS "valid_condition_operator";
DROP TABLE IF EXISTS "valid_condition_value_type";
DROP TABLE IF EXISTS "valid_condition_value_unit";
