import sqlite3
from datetime import datetime, timedelta
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def _connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def record_employee_action(simulation_id, user_id, action_taken, response_time):
    """
    Record an employee action on a simulation and update metrics.
    action_taken: 'clicked_link', 'reported', 'ignored', 'deleted'
    response_time: seconds to act (float or int)
    """
    con = _connect()
    cur = con.cursor()

    cur.execute('SELECT simulation_type FROM simulations WHERE id = ?', (simulation_id,))
    row = cur.fetchone()
    sim_type = row["simulation_type"] if row else None

    correct = int(action_taken == 'reported' and sim_type == 'phishing_test')

    cur.execute(
        '''
        INSERT INTO user_responses (simulation_id, user_id, action_taken, response_time, correct)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (simulation_id, user_id, action_taken, response_time, correct),
    )
    con.commit()

    # Snapshot metrics after each action
    update_user_metrics_snapshot(user_id, con=con)
    con.close()


def _rates_from_counts(total, clicks, reports, correct):
    if not total:
        return 0.0, 0.0, 0.0
    return clicks / total, reports / total, correct / total


def compute_user_metrics(user_id, con=None):
    """Return per-user metrics and counts without mutating the DB."""
    owns_con = con is None
    if owns_con:
        con = _connect()
    cur = con.cursor()

    # Totals across all responses
    cur.execute(
        '''
        SELECT
            COUNT(*) AS total_responses,
            SUM(CASE WHEN action_taken = 'clicked_link' THEN 1 ELSE 0 END) AS clicks,
            SUM(CASE WHEN action_taken = 'reported' THEN 1 ELSE 0 END) AS reports,
            SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) AS correct
        FROM user_responses
        WHERE user_id = ?
        ''',
        (user_id,),
    )
    r = cur.fetchone()
    total = r["total_responses"] or 0
    clicks = r["clicks"] or 0
    reports = r["reports"] or 0
    correct = r["correct"] or 0

    click_rate, report_rate, accuracy_rate = _rates_from_counts(total, clicks, reports, correct)

    # Failure is clicking a phishing link
    failure_count = clicks
    failure_rate = click_rate

    result = {
        "user_id": user_id,
        "total_responses": total,
        "clicks": clicks,
        "reports": reports,
        "correct": correct,
        "click_rate": click_rate,
        "report_rate": report_rate,
        "accuracy_rate": accuracy_rate,
        "failure_count": failure_count,
        "failure_rate": failure_rate,
        "score": round(accuracy_rate * 100),
    }

    if owns_con:
        con.close()
    return result


def update_user_metrics_snapshot(user_id, con=None):
    """Compute metrics and insert a snapshot row into metrics table."""
    owns_con = con is None
    if owns_con:
        con = _connect()
    cur = con.cursor()

    m = compute_user_metrics(user_id, con=con)
    cur.execute(
        '''
        INSERT INTO metrics (user_id, click_rate, report_rate, accuracy_rate)
        VALUES (?, ?, ?, ?)
        ''',
        (user_id, m["click_rate"], m["report_rate"], m["accuracy_rate"]),
    )
    con.commit()
    if owns_con:
        con.close()
    return m


def update_user_metrics(user_id):
    """Back-compat alias: snapshot metrics for the given user."""
    return update_user_metrics_snapshot(user_id)


def compute_employer_rollup(employer_id):
    """
    Aggregate metrics across all employees under an employer.
    Returns totals, rates, and per-user breakdown.
    """
    con = _connect()
    cur = con.cursor()

    cur.execute("SELECT id FROM users WHERE employer_id = ? AND role = 'employee'", (employer_id,))
    user_ids = [row[0] for row in cur.fetchall()]

    per_user = [compute_user_metrics(uid, con=con) for uid in user_ids]

    # Aggregate counts
    total_responses = sum(u["total_responses"] for u in per_user)
    total_clicks = sum(u["clicks"] for u in per_user)
    total_reports = sum(u["reports"] for u in per_user)
    total_correct = sum(u["correct"] for u in per_user)

    click_rate, report_rate, accuracy_rate = _rates_from_counts(
        total_responses, total_clicks, total_reports, total_correct
    )

    summary = {
        "employer_id": employer_id,
        "total_responses": total_responses,
        "clicks": total_clicks,
        "reports": total_reports,
        "correct": total_correct,
        "click_rate": click_rate,
        "report_rate": report_rate,
        "accuracy_rate": accuracy_rate,
        "failure_count": total_clicks,
        "failure_rate": click_rate,
        "score": round(accuracy_rate * 100),
        "users": per_user,
    }

    con.close()
    return summary


def user_failures_timeseries(user_id, days=30):
    """Return daily failure (clicked_link) counts for the last N days."""
    con = _connect()
    cur = con.cursor()

    cur.execute(
        '''
        SELECT DATE(s.sent_at) AS day, COUNT(1) AS failures
        FROM user_responses ur
        JOIN simulations s ON ur.simulation_id = s.id
        WHERE ur.user_id = ?
        AND ur.action_taken = 'clicked_link'
        AND s.sent_at >= DATETIME('now', ?)
        GROUP BY DATE(s.sent_at)
        ORDER BY day ASC
        ''',
        (user_id, f'-{int(days)} days'),
    )
    rows = cur.fetchall()
    con.close()
    return [{"day": r["day"], "failures": r["failures"]} for r in rows]


print("Response tracker ready: metrics helpers loaded.")
