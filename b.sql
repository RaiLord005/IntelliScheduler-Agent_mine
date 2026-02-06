USE scheduler_agent_v2_db;

-- Add a column to store why the meeting was cancelled
ALTER TABLE meetings ADD COLUMN cancellation_reason VARCHAR(255);


USE scheduler_agent_v2_db;

-- 1. Add Password Column
ALTER TABLE users ADD COLUMN password VARCHAR(255) DEFAULT 'password';

-- 2. Insert a new test user if you want (Optional)
-- You can log in as 'Alice Manager' with password 'password'


