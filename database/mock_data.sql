USE scheduler_agent_db;

-- 1. Insert Users
INSERT INTO users (username, email, work_start_time, work_end_time) VALUES 
('Alice Manager', 'alice@company.com', '08:00:00', '16:00:00'),
('Bob Engineer', 'bob@company.com', '10:00:00', '18:00:00'),
('Charlie Designer', 'charlie@company.com', '09:00:00', '17:00:00');

-- 2. Insert Past Meetings (To be tested with ScaleDown)
-- Dates are examples; ensure they are in the past relative to when you run this
INSERT INTO meetings (title, organizer_id, start_time, end_time, status) VALUES 
('Q1 Planning', 1, DATE_SUB(NOW(), INTERVAL 2 MONTH), DATE_ADD(DATE_SUB(NOW(), INTERVAL 2 MONTH), INTERVAL 1 HOUR), 'scheduled'),
('Team Sync', 1, DATE_SUB(NOW(), INTERVAL 2 MONTH), DATE_ADD(DATE_SUB(NOW(), INTERVAL 2 MONTH), INTERVAL 30 MINUTE), 'scheduled'),
('Project Review', 2, DATE_SUB(NOW(), INTERVAL 40 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 40 DAY), INTERVAL 1 HOUR), 'scheduled');

-- 3. Insert Future Meetings (To test conflict resolution)
INSERT INTO meetings (title, organizer_id, start_time, end_time, status) 
VALUES 
('Client Demo', 1, DATE_ADD(NOW(), INTERVAL 1 DAY), DATE_ADD(DATE_ADD(NOW(), INTERVAL 1 DAY), INTERVAL 1 HOUR), 'scheduled');

-- 4. Participants
INSERT INTO participants (meeting_id, user_id, status) VALUES 
(4, 1, 'accepted'), (4, 2, 'pending');

select*from meetings;