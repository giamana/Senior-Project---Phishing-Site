import sqlite3
from datetime import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# TODO: move these to environment variables for security
SENDER_EMAIL = "airline.itdesk@gmail.com"
SENDER_PASSWORD = "bktjqkfrgnmthusd"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def _connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def _send_email(receiver_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    try:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    finally:
        server.quit()


def create_employer_account(name, email, company_name):
    """Create employer account then send 10 random demo emails."""
    con = _connect()
    cur = con.cursor()

    cur.execute(
        '''
        INSERT INTO users (name, email, department, role)
        VALUES (?, ?, ?, 'employer')
        ''',
        (name, email, company_name),
    )
    employer_id = cur.lastrowid
    con.commit()

    # Send demo emails (non-blocking concerns out of scope; simple loop)
    send_demo_emails_to_employer(employer_id, count=10)

    con.close()
    return employer_id


def show_sample_phishing_emails(employer_id):
    """Return 10 random templates for UI preview (no sending)."""
    con = _connect()
    cur = con.cursor()
    cur.execute(
        '''
        SELECT id, template_name, subject, body, difficulty_level
        FROM email_templates
        ORDER BY RANDOM()
        LIMIT 10
        '''
    )
    samples = cur.fetchall()
    con.close()
    return samples


def send_demo_emails_to_employer(employer_id, count=10):
    """Send N random templates to the employer's email as a demo."""
    con = _connect()
    cur = con.cursor()

    cur.execute("SELECT email FROM users WHERE id = ? AND role = 'employer'", (employer_id,))
    row = cur.fetchone()
    if not row:
        con.close()
        return 0
    receiver_email = row["email"]

    cur.execute(
        '''
        SELECT subject, body
        FROM email_templates
        ORDER BY RANDOM()
        LIMIT ?
        ''',
        (int(count),),
    )
    templates = cur.fetchall()

    sent = 0
    for tpl in templates:
        subject, body = tpl["subject"], tpl["body"]
        try:
            _send_email(receiver_email, subject, body)
            sent += 1
        except Exception as e:
            # Log/print if needed; keep loop going
            print(f"[demo] Failed to send to employer {employer_id}: {e}")

    con.close()
    return sent


print("Employer signup module ready: demo sender wired.")
