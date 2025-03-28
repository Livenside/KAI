-- migrate:up
ALTER TABLE study_materials
ADD topic VARCHAR(255) NOT NULL DEFAULT 'default';

-- migrate:down
ALTER TABLE study_materials
DROP COLUMN topic;

