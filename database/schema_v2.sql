DROP DATABASE IF EXISTS scheduler_agent_v2_db;
CREATE DATABASE scheduler_agent_v2_db;
USE scheduler_agent_v2_db;

-- 1. Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    organization VARCHAR(100) DEFAULT 'Freelancer',
    default_location VARCHAR(100) DEFAULT 'Office'
);

-- 2. Meetings Table (With invite_type)
CREATE TABLE meetings (
    meeting_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    organizer_id INT,
    participant_id INT,
    start_time DATETIME,
    end_time DATETIME,
    location VARCHAR(100),
    status VARCHAR(20) DEFAULT 'scheduled',
    cancellation_reason VARCHAR(255),
    invite_type VARCHAR(20) DEFAULT 'person', -- Stores 'person' or 'org'
    FOREIGN KEY (organizer_id) REFERENCES users(user_id),
    FOREIGN KEY (participant_id) REFERENCES users(user_id)
);

-- 3. Analytics Table
CREATE TABLE system_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(100),
    value VARCHAR(50),
    icon VARCHAR(50),
    color VARCHAR(20)
);

-- 4. Seed Data
INSERT INTO system_analytics (metric_name, value, icon, color) VALUES 
('Schedule Compression', '0%', 'fa-compress-arrows-alt', '#10b981'),
('Overhead Reduced', '0%', 'fa-stopwatch', '#f59e0b'),
('Max Coordination', '0 Users', 'fa-users-viewfinder', '#0ea5e9'),
('Projected Time Saved', '0 Hrs', 'fa-chart-line', '#8b5cf6');




USE scheduler_agent_v2_db;

-- 1. Unlock Safety Mode
SET SQL_SAFE_UPDATES = 0;

-- 2. Run the Fix (Now it will work)
UPDATE meetings 
SET invite_type = 'person' 
WHERE invite_type IS NULL OR invite_type = '';

-- 3. Lock it back up (Optional but good practice)
SET SQL_SAFE_UPDATES = 1;