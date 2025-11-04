import sqlite3
from datetime import datetime, timedelta
import random


# Connect to (or create) the database file in the same directory
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

def add_employees(employer_id, employee_list):
    """
    Step 3: Employer enters employee data
    employee_list = [
        {'name': 'Test one', 'email': 'testone@airline.com', 'department': 'Flight Operations'},
        
    ]
    """
    for emp in employee_list:
        cursor.execute('''
            INSERT INTO users (name, email, department, role)
            VALUES (?, ?, ?, 'employee')
        ''', (emp['name'], emp['email'], emp['department']))
    
    connection.commit()
    print(f"Added {len(employee_list)} employees")
