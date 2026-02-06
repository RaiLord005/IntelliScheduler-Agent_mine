DROP DATABASE IF EXISTS scheduler_agent_v2_db;
CREATE DATABASE scheduler_agent_v2_db;
USE scheduler_agent_v2_db;

-- 1. USERS TABLE (Now with 'default_location')
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255) DEFAULT 'Pass123!',
    email VARCHAR(100),
    risk_score FLOAT DEFAULT 0.0,
    preferred_slot VARCHAR(20) DEFAULT 'morning',
    default_location VARCHAR(100) DEFAULT 'Office' -- NEW COLUMN
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
    status VARCHAR(20) DEFAULT 'scheduled',
    cancellation_risk FLOAT DEFAULT 0.0,
    cancellation_reason VARCHAR(255),
    FOREIGN KEY (organizer_id) REFERENCES users(user_id)
);

-- 3. ANALYTICS TABLE
CREATE TABLE system_analytics (
    metric_name VARCHAR(50),
    value DECIMAL(10,2)
);
INSERT INTO system_analytics VALUES ('Conflicts Avoided', 0), ('High Risk Warnings', 0), ('Storage Saved', 0);

-- 4. INSERT 10+ DIVERSE USERS (The "Smart" Data)
INSERT INTO users (username, risk_score, default_location) VALUES 
('Alice Manager', 0.1, 'Conference Room A'),
('Bob Remote', 0.05, 'Online (Zoom)'),
('Charlie CEO', 0.8, 'Boardroom'),
('David Engineer', 0.2, 'Dev Lab 1'),
('Eva Designer', 0.1, 'Creative Studio'),
('Frank Sales', 0.6, 'Client Site (Travel)'),
('Grace HR', 0.1, 'Interview Room 4'),
('Henry Intern', 0.3, 'Cafeteria Huddle'),
('Ivy Consultant', 0.5, 'Online (Teams)'),
('Jack Director', 0.2, 'Executive Suite');

-- 5. CREATE YOUR LOGIN
INSERT INTO users (username, password, default_location) VALUES ('admin', 'admin123', 'Office');