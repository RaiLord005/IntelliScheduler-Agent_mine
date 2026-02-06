DROP DATABASE IF EXISTS scheduler_agent_v2_db;
CREATE DATABASE scheduler_agent_v2_db;
USE scheduler_agent_v2_db;

-- 1. USERS TABLE
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,  -- 'UNIQUE' prevents duplicate names
    password VARCHAR(255),        -- Stores the password
    email VARCHAR(100),
    risk_score FLOAT DEFAULT 0.0,
    preferred_slot VARCHAR(20) DEFAULT 'morning'
);

-- 2. MEETINGS TABLE
CREATE TABLE meetings (
    meeting_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    organizer_id INT,
    start_time DATETIME,
    end_time DATETIME,
    location VARCHAR(100),
    travel_time_mins INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'scheduled', -- 'scheduled' or 'cancelled'
    cancellation_risk FLOAT DEFAULT 0.0,
    cancellation_reason VARCHAR(255),
    FOREIGN KEY (organizer_id) REFERENCES users(user_id)
);

-- 3. ANALYTICS TABLE
CREATE TABLE system_analytics (
    metric_name VARCHAR(50),
    value DECIMAL(10,2)
);

-- Initialize Stats
INSERT INTO system_analytics (metric_name, value) VALUES 
('Conflicts Avoided', 0), ('High Risk Warnings', 0), ('Storage Saved', 0);