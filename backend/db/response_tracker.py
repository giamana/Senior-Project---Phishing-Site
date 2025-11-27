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


def _rates_from_counts(total, clicks, reports, ignores, correct):
    if not total:
        return 0.0, 0.0, 0.0, 0.0
    return (
        clicks / total,
        reports / total,
        ignores / total,
        correct / total,
    )


def _score_from_rates(click_rate, report_rate, ignore_rate):
    # Start at 100. Penalize clicks, reward reports/ignores, and clamp.
    score = 1 - click_rate + (0.5 * report_rate) + (0.2 * ignore_rate)
    score = max(0.0, min(score, 1.0))
    return round(score * 100) if (click_rate or report_rate or ignore_rate) else 100


def _grade_from_score(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


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
            SUM(CASE WHEN action_taken = 'ignored' THEN 1 ELSE 0 END) AS ignores,
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
    ignores = r["ignores"] or 0
    correct = r["correct"] or 0

    click_rate, report_rate, ignore_rate, accuracy_rate = _rates_from_counts(
        total, clicks, reports, ignores, correct
    )

    # Failure is clicking a phishing link
    failure_count = clicks
    failure_rate = click_rate
    score = _score_from_rates(click_rate, report_rate, ignore_rate)

    result = {
        "user_id": user_id,
        "total_responses": total,
        "clicks": clicks,
        "reports": reports,
        "ignores": ignores,
        "correct": correct,
        "click_rate": click_rate,
        "report_rate": report_rate,
        "ignore_rate": ignore_rate,
        "accuracy_rate": accuracy_rate,
        "failure_count": failure_count,
        "failure_rate": failure_rate,
        "score": score,
        "grade": _grade_from_score(score),
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
        INSERT INTO metrics (user_id, click_rate, report_rate, ignore_rate, accuracy_rate, score)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (user_id, m["click_rate"], m["report_rate"], m["ignore_rate"], m["accuracy_rate"], m["score"]),
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
    total_ignores = sum(u["ignores"] for u in per_user)
    total_correct = sum(u["correct"] for u in per_user)

    click_rate, report_rate, ignore_rate, accuracy_rate = _rates_from_counts(
        total_responses, total_clicks, total_reports, total_ignores, total_correct
    )
    aggregate_score = _score_from_rates(click_rate, report_rate, ignore_rate)

    summary = {
        "employer_id": employer_id,
        "total_responses": total_responses,
        "clicks": total_clicks,
        "reports": total_reports,
        "ignores": total_ignores,
        "correct": total_correct,
        "click_rate": click_rate,
        "report_rate": report_rate,
        "ignore_rate": ignore_rate,
        "accuracy_rate": accuracy_rate,
        "failure_count": total_clicks,
        "failure_rate": click_rate,
        "score": aggregate_score,
        "grade": _grade_from_score(aggregate_score),
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


def user_metric_history(user_id, limit=30):
    """Return chronological score/report/click history from the metrics snapshot table."""
    con = _connect()
    cur = con.cursor()
    cur.execute(
        '''
        SELECT date, click_rate, report_rate, ignore_rate, score
        FROM metrics
        WHERE user_id = ?
        ORDER BY date ASC
        LIMIT ?
        ''',
        (user_id, limit),
    )
    rows = cur.fetchall()
    con.close()
    return [
        {
            "date": r["date"],
            "click_rate": r["click_rate"],
            "report_rate": r["report_rate"],
            "ignore_rate": r["ignore_rate"],
            "score": r["score"],
        }
        for r in rows
    ]


def mark_expired_simulations_as_ignored(threshold_hours=24):
    """
    Insert ignored responses for simulations that have gone unanswered for
    threshold_hours. Returns the number of simulations marked as ignored.
    """
    con = _connect()
    cur = con.cursor()
    cur.execute(
        '''
        SELECT s.id, s.user_id, s.sent_at
        FROM simulations s
        WHERE s.sent_at <= DATETIME('now', ?)
        AND NOT EXISTS (
            SELECT 1
            FROM user_responses ur
            WHERE ur.simulation_id = s.id AND ur.user_id = s.user_id
        )
        ''',
        (f'-{int(threshold_hours)} hours',),
    )
    rows = cur.fetchall()
    ignored = 0
    now = datetime.utcnow()
    for row in rows:
        sent_at = datetime.fromisoformat(row["sent_at"])
        response_time = max((now - sent_at).total_seconds(), 0.0)
        cur.execute(
            '''
            INSERT INTO user_responses (simulation_id, user_id, action_taken, response_time, correct)
            VALUES (?, ?, 'ignored', ?, 0)
            ''',
            (row["id"], row["user_id"], response_time),
        )
        update_user_metrics_snapshot(row["user_id"], con=con)
        ignored += 1
    con.commit()
    con.close()
    return ignored


print("Response tracker ready: metrics helpers loaded.")
