import sqlite3
from datetime import datetime, timedelta
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# Connect to (or create) the database file in this directory
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Disable foreign key checks while dropping tables to avoid dependency errors
cursor.execute('PRAGMA foreign_keys = OFF;')

# --- DROP existing tables (order doesn't need to be strict when FK checks are off) ---
cursor.execute('DROP TABLE IF EXISTS tracking_tokens;')
cursor.execute('DROP TABLE IF EXISTS scheduled_emails;')
cursor.execute('DROP TABLE IF EXISTS email_templates;')
cursor.execute('DROP TABLE IF EXISTS campaigns;')
cursor.execute('DROP TABLE IF EXISTS metrics;')
cursor.execute('DROP TABLE IF EXISTS user_responses;')
cursor.execute('DROP TABLE IF EXISTS simulations;')
cursor.execute('DROP TABLE IF EXISTS users;')

# --- CREATE TABLES ---

# Create Users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employer_id INTEGER,
    name TEXT NOT NULL CHECK(LENGTH(name) > 0 AND LENGTH(trim(name)) > 0),
    email TEXT NOT NULL UNIQUE,
    department TEXT,
    role TEXT DEFAULT 'employee' CHECK(role IN ('employer', 'employee')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# Create Simulations table
cursor.execute('''
CREATE TABLE simulations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    email_content TEXT NOT NULL,
    simulation_type TEXT CHECK(LENGTH(simulation_type) > 0),
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
''')

# Create User Responses table
cursor.execute('''
CREATE TABLE user_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    action_taken TEXT CHECK(LENGTH(action_taken) > 0),
    response_time REAL CHECK(response_time >= 0),
    correct BOOLEAN NOT NULL CHECK(correct IN (0,1)),
    FOREIGN KEY (simulation_id) REFERENCES simulations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
''')

# Create Metrics table
cursor.execute('''
CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    click_rate REAL CHECK(click_rate >= 0 AND click_rate <= 1),
    report_rate REAL CHECK(report_rate >= 0 AND report_rate <= 1),
    ignore_rate REAL CHECK(ignore_rate >= 0 AND ignore_rate <= 1),
    accuracy_rate REAL CHECK(accuracy_rate >= 0 AND accuracy_rate <= 1),
    score REAL CHECK(score >= 0 AND score <= 100),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
''')

# Create Campaigns table (for employer management)
cursor.execute('''
CREATE TABLE campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employer_id INTEGER NOT NULL,
    campaign_name TEXT NOT NULL,
    target_department TEXT,
    start_date DATETIME,
    end_date DATETIME,
    status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'active', 'completed', 'paused')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES users(id) ON DELETE CASCADE
);
''')

# Create Email Templates table (for phishing samples)
cursor.execute('''
CREATE TABLE email_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    difficulty_level TEXT CHECK(difficulty_level IN ('easy', 'medium', 'hard', 'complex','complex+')),
    target_department TEXT,
    red_flags TEXT,
    is_phishing BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# Create Scheduled Emails table
cursor.execute('''
CREATE TABLE scheduled_emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,
    scheduled_time DATETIME NOT NULL,
    sent BOOLEAN DEFAULT 0,
    sent_at DATETIME,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES email_templates(id) ON DELETE CASCADE
);
''')

# Create Tracking Tokens table
cursor.execute('''
CREATE TABLE tracking_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    action TEXT NOT NULL CHECK(action IN ('clicked', 'reported')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    acted_at DATETIME,
    FOREIGN KEY (simulation_id) REFERENCES simulations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
''')

connection.commit()
connection.close()

print("Database reset and initialized successfully with all tables.")
