import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import schedule
import time
import sys

# Ensure project root is importable when run as a script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.db.tracking_utils import (
    build_tracking_url,
    generate_tracking_token,
    render_body_with_tracking_links,
)

# Use file-relative DB path so it works from any CWD
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# TODO: move these to environment variables for security
SENDER_EMAIL = "airline.itdesk@gmail.com"
#this is the app password for the email account
SENDER_PASSWORD = "bktjqkfrgnmthusd"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173").rstrip("/")
VIRUS_PAGE_URL = f"{FRONTEND_BASE_URL}/virus"


# --- Function: send email ---
def send_email(receiver_email, subject, body):
    """Send a plain-text email using the configured SMTP credentials."""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[{datetime.now()}] Email sent to {receiver_email}: {subject}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email to {receiver_email}: {e}")
        return False


def _random_template(cur, allowed_template_ids=None):
    """Pick any template (optionally constrained to a provided id list)."""
    if allowed_template_ids:
        placeholders = ",".join("?" * len(allowed_template_ids))
        cur.execute(
            f"""
            SELECT id, subject, body
            FROM email_templates
            WHERE id IN ({placeholders})
            ORDER BY RANDOM()
            LIMIT 1
            """,
            tuple(allowed_template_ids),
        )
        row = cur.fetchone()
        if row:
            return row
    cur.execute(
        """
        SELECT id, subject, body
        FROM email_templates
        ORDER BY RANDOM()
        LIMIT 1
        """
    )
    return cur.fetchone()


def _pick_template_for_department(cur, department, allowed_template_ids=None):
    """
    Prefer a template that matches the user's department; fall back to any
    allowed template when no departmental match exists.
    """
    # Try department-specific template
    where_clauses = []
    params = []
    if department:
        where_clauses.append("(target_department = ? OR target_department IS NULL)")
        params.append(department)
    if allowed_template_ids:
        placeholders = ",".join("?" * len(allowed_template_ids))
        where_clauses.append(f"id IN ({placeholders})")
        params.extend(allowed_template_ids)

    query = """
        SELECT id, subject, body
        FROM email_templates
    """
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += "\n        ORDER BY RANDOM()\n        LIMIT 1\n        "

    cur.execute(query, tuple(params))
    row = cur.fetchone()
    if row:
        return row

    return _random_template(cur, allowed_template_ids)


def send_department_emails(allowed_template_ids=None):
    """
    For each user, pick a template that matches their department
    and send exactly one email if they haven't received one in the last minute.
    Records simulations, tracking tokens, and returns a delivery summary.
    allowed_template_ids: Only consider the provided template ids (optional).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    now = datetime.now()
    one_min_ago = now - timedelta(minutes=1)
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    one_min_ago_str = one_min_ago.strftime("%Y-%m-%d %H:%M:%S")

    allowed_ids = (
        [int(tid) for tid in allowed_template_ids if str(tid).isdigit()]
        if allowed_template_ids
        else None
    )

    # Fetch all users (employers and employees alike) to send the simulation email.
    cur.execute("SELECT id, name, email, department FROM users")
    users = cur.fetchall()
    deliveries = []

    for user in users:
        user_id = user["id"]
        receiver_email = user["email"]
        user_name = user["name"] or "Team Member"
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

        tpl = _pick_template_for_department(cur, department, allowed_ids)
        if not tpl:
            # No templates available, skip gracefully
            continue

        template_id, subject, body = tpl
        personalized_body = body.replace("{name}", user_name)

        # Unique tokens let us distinguish clicks vs reports for this simulation.
        click_token = generate_tracking_token()
        report_token = generate_tracking_token()
        # Track clicks and then redirect users to the virus page for awareness.
        click_url = f"{build_tracking_url(click_token, action='clicked')}&redirect={VIRUS_PAGE_URL}"
        report_url = build_tracking_url(report_token, action="reported")
        final_body = render_body_with_tracking_links(personalized_body, click_url, report_url)

        # Record simulation
        cur.execute(
            """
            INSERT INTO simulations (user_id, email_content, simulation_type, sent_at)
            VALUES (?, ?, 'phishing_test', ?)
            """,
            (user_id, final_body, now_str),
        )
        simulation_id = cur.lastrowid

        cur.executemany(
            """
            INSERT INTO tracking_tokens (simulation_id, user_id, token, action)
            VALUES (?, ?, ?, ?)
            """,
            [
                (simulation_id, user_id, click_token, "clicked"),
                (simulation_id, user_id, report_token, "reported"),
            ],
        )

        # Send email
        if send_email(receiver_email, subject, final_body):
            deliveries.append(
                {
                    "simulation_id": simulation_id,
                    "user_id": user_id,
                    "template_id": template_id,
                    "email": receiver_email,
                }
            )
            conn.commit()

    conn.close()
    return deliveries


def start_scheduler():
    """Background loop to send a batch every minute when run as a script."""
    schedule.every(1).minutes.do(send_department_emails)
    print("Email scheduler running... Press CTRL+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == "__main__":
    start_scheduler()
