# campaign_manager.py
from datetime import datetime, timedelta
import random
import sqlite3

# Connect to (or create) the database file in the same directory
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# --- Drop related tables to start fresh (optional during testing) ---
cursor.execute('PRAGMA foreign_keys = OFF;')  # Temporarily disable FK checks

cursor.execute('DROP TABLE IF EXISTS scheduled_emails;')
cursor.execute('DROP TABLE IF EXISTS email_templates;')
cursor.execute('DROP TABLE IF EXISTS campaigns;')

cursor.execute('PRAGMA foreign_keys = ON;')  # Re-enable FK enforcement

print("Dropped campaign-related tables (scheduled_emails, email_templates, campaigns).")

# --- Main Functions ---

def create_phishing_campaign(employer_id, campaign_name, target_department=None):
    """Step 4: Create a campaign for specific department or all employees"""
    
    # Create campaign
    cursor.execute('''
        INSERT INTO campaigns (employer_id, campaign_name, target_department, start_date, status) 
        VALUES (?, ?, ?, ?, 'scheduled')
    ''', (employer_id, campaign_name, target_department, datetime.now()))
    
    campaign_id = cursor.lastrowid
    
    # Get target employees
    if target_department:
        cursor.execute('''
            SELECT id, department FROM users 
            WHERE role = 'employee' AND department = ?
        ''', (target_department,))
    else:
        cursor.execute('''
            SELECT id, department FROM users 
            WHERE role = 'employee'
        ''')
    
    employees = cursor.fetchall()
    
    # Schedule 10 emails for each employee over next 30 days
    schedule_emails_for_employees(campaign_id, employees)
    
    connection.commit()
    return campaign_id


def schedule_emails_for_employees(campaign_id, employees):
    """Step 5: Schedule 10 phishing emails per employee"""
    
    for employee_id, department in employees:
        # Get 10 templates (prioritize department-specific ones)
        cursor.execute('''
            SELECT id FROM email_templates 
            WHERE target_department = ? OR target_department IS NULL 
            ORDER BY RANDOM() 
            LIMIT 10
        ''', (department,))
        
        templates = cursor.fetchall()
        
        # Schedule emails over 30 days (~1 every 3 days)
        for i, (template_id,) in enumerate(templates):
            days_offset = i * 3  # Day 0, 3, 6, 9, etc.
            scheduled_time = datetime.now() + timedelta(days=days_offset, hours=random.randint(9, 17))
            
            cursor.execute('''
                INSERT INTO scheduled_emails 
                (campaign_id, user_id, template_id, scheduled_time) 
                VALUES (?, ?, ?, ?)
            ''', (campaign_id, employee_id, template_id, scheduled_time))

connection.commit()
connection.close()
print("Campaign manager initialized successfully.")