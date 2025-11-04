import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import schedule
import time

# Use file-relative DB path so it works from any CWD
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# TODO: move these to environment variables for security
SENDER_EMAIL = "axijewere@gmail.com"
SENDER_PASSWORD = "agboga2014"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# --- Function: send email ---
def send_email(receiver_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[{datetime.now()}] Email sent to {receiver_email}: {subject}")
    except Exception as e:
        print(f"[ERROR] Failed to send email to {receiver_email}: {e}")


def _pick_template_for_department(cur, department):
    # Try department-specific template
    cur.execute(
        """
        SELECT id, subject, body
        FROM email_templates
        WHERE target_department = ?
        ORDER BY RANDOM()
        LIMIT 1
        """,
        (department,),
    )
    row = cur.fetchone()
    if row:
        return row

    # Fallback: any template
    cur.execute(
        """
        SELECT id, subject, body
        FROM email_templates
        ORDER BY RANDOM()
        LIMIT 1
        """
    )
    return cur.fetchone()


def send_department_emails():
    """
    Every minute: for each user, pick a template that matches their department
    and send exactly one email if they haven't received one in the last minute.
    Records a row in simulations for tracking.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    now = datetime.now()
    one_min_ago = now - timedelta(minutes=1)
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    one_min_ago_str = one_min_ago.strftime("%Y-%m-%d %H:%M:%S")

    # Fetch all users
    cur.execute("SELECT id, email, department FROM users")
    users = cur.fetchall()

    for user in users:
        user_id = user["id"]
        receiver_email = user["email"]
        department = user["department"]

        # Skip if user received a simulation email in the last minute
        cur.execute(
            """
            SELECT COUNT(1)
            FROM simulations
            WHERE user_id = ? AND sent_at >= ?
            """,
            (user_id, one_min_ago_str),
        )
        if cur.fetchone()[0] > 0:
            continue

        tpl = _pick_template_for_department(cur, department)
        if not tpl:
            # No templates available, skip gracefully
            continue

        _, subject, body = tpl

        # Send email
        send_email(receiver_email, subject, body)

        # Record simulation
        cur.execute(
            """
            INSERT INTO simulations (user_id, email_content, simulation_type, sent_at)
            VALUES (?, ?, 'phishing_test', ?)
            """,
            (user_id, body, now_str),
        )
        conn.commit()

    conn.close()


# --- Schedule job to run every minute ---
schedule.every(1).minutes.do(send_department_emails)

print("Email scheduler running... Press CTRL+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(5)

