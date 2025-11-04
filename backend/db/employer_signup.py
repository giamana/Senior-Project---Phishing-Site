import sqlite3
from datetime import datetime, timedelta
import json


# Connect to (or create) the database file in the same directory
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

def create_employer_account(name, email, company_name):
    """Step 1: Employer creates account"""
    cursor.execute('''
        INSERT INTO users (name, email, department, role) 
        VALUES (?, ?, ?, 'employer')
    ''', (name, email, company_name))
    employer_id = cursor.lastrowid
    connection.commit()
    
    # Automatically show them 10 sample phishing emails
    show_sample_phishing_emails(employer_id)
    
    return employer_id

def show_sample_phishing_emails(employer_id):
    """Step 2: Show 10 sample emails to employer"""
    cursor.execute('''
        SELECT id, template_name, subject, body, difficulty_level 
        FROM email_templates 
        LIMIT 10
    ''')
    samples = cursor.fetchall()
    return samples  # Display these in the UI


connection.commit()
connection.close()
print("Employer signup module initialized successfully.")