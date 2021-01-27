SELECT id FROM agdc.dataset;
BEGIN;
DELETE FROM agdc.dataset_location;
DELETE FROM agdc.dataset_source;
DELETE FROM agdc.dataset;
DELETE FROM agdc.dataset_type;
COMMIT;
