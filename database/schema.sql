CREATE DATABASE IF NOT EXISTS scheduler_agent_db;
USE scheduler_agent_db;

-- Users and their preferences
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    work_start_time TIME DEFAULT '09:00:00',
    work_end_time TIME DEFAULT '17:00:00',
    preferred_meeting_buffer_minutes INT DEFAULT 15,
    timezone VARCHAR(50) DEFAULT 'UTC'
);

-- Main Meetings Table
CREATE TABLE IF NOT EXISTS meetings (
    meeting_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    organizer_id INT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    location VARCHAR(100),
    status ENUM('scheduled', 'cancelled', 'compressed') DEFAULT 'scheduled',
    is_recurring BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (organizer_id) REFERENCES users(user_id)
);

-- Participants mapping
CREATE TABLE IF NOT EXISTS participants (
    meeting_id INT,
    user_id INT,
    status ENUM('accepted', 'declined', 'pending') DEFAULT 'pending',
    PRIMARY KEY (meeting_id, user_id),
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Compressed History (ScaleDown Storage)
-- Stores aggregated stats instead of individual rows for old data
CREATE TABLE IF NOT EXISTS scaledown_history (
    user_id INT,
    month_year VARCHAR(7), -- Format: YYYY-MM
    total_meetings INT,
    total_hours DECIMAL(10,2),
    primary_collaborators TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

select*from scaledown_history;