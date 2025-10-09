import sqlite3

# Connect to (or create) the database file in the same directory
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Enable foreign key support
cursor.execute('PRAGMA foreign_keys = ON;')

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(LENGTH(name) > 0 AND LENGTH(trim(name)) > 0),
    email TEXT NOT NULL UNIQUE,
    department TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# Create Simulations table
cursor.execute('''
CREATE TABLE IF NOT EXISTS simulations (
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
CREATE TABLE IF NOT EXISTS user_responses (
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
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    click_rate REAL CHECK(click_rate >= 0 AND click_rate <= 1),
    report_rate REAL CHECK(report_rate >= 0 AND report_rate <= 1),
    accuracy_rate REAL CHECK(accuracy_rate >= 0 AND accuracy_rate <= 1),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
''')

connection.commit()
connection.close()

print("Initialized database 'database.db' and created tables.")
