SET SQL_SAFE_UPDATES = 0;

DELETE FROM system_analytics;

INSERT INTO system_analytics (metric_name, value) VALUES 
('Conflicts Avoided', 0),
('High Risk Warnings', 0),
('Storage Saved', 0);

SET SQL_SAFE_UPDATES = 1; -- Turn safety back on (optional)