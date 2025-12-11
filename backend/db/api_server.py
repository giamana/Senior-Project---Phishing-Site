import json
import os
import sqlite3
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from .auth_utils import hash_password, verify_password, create_token, invalidate_token



# Ensure project root is importable when run as a script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.db.email_scheduler import send_department_emails, send_email
from backend.db.response_tracker import (
    compute_employer_rollup,
    compute_user_metrics,
    mark_expired_simulations_as_ignored,
    record_employee_action,
    user_failures_timeseries,
    user_metric_history,
)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
DEFAULT_PORT = int(os.getenv("API_SERVER_PORT", "5000"))


def _connect():
    """Open a SQLite connection with Row objects for dict-style access."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def _status_from_metrics(metrics):
    """Translate numeric metrics into the high-level status badge used in the UI."""
    if metrics["click_rate"] >= 0.4:
        return "At Risk"
    if metrics["report_rate"] >= 0.5:
        return "Security Champion"
    if metrics["score"] >= 85:
        return "On Track"
    return "Monitor"


def _grade_from_score(score):
    """Convert a numeric score into the letter grade displayed on dashboards."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def _resolve_employer_id(raw_employer_id, con):
    """
    Normalize employer ids from the request, falling back to an existing employer
    (or a seeded default) so employee records always carry an employer_id.
    """
    if raw_employer_id is not None:
        try:
            return int(raw_employer_id)
        except (TypeError, ValueError):
            return None

    cur = con.cursor()
    cur.execute(
        """
        SELECT employer_id
        FROM users
        WHERE employer_id IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
        """
    )
    row = cur.fetchone()
    if row and row["employer_id"] is not None:
        return int(row["employer_id"])

    cur.execute("SELECT DISTINCT employer_id FROM users WHERE employer_id IS NOT NULL ORDER BY employer_id ASC LIMIT 1")
    row = cur.fetchone()
    if row:
        return int(row["id"])

    cur.execute(
        """
        INSERT INTO users (name, email, department)
        VALUES (?, ?, ?)"
        """,
        ("Default Employer", "default-employer@localhost", "Default Organization"),
    )
    con.commit()
    return cur.lastrowid

class SecurityAwarenessHandler(BaseHTTPRequestHandler):
    """Lightweight HTTP API for employee management and simulation tracking."""

    server_version = "SecurityAwareness/1.0"

    

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self._set_headers(status=status, content_type="application/json")
        self.wfile.write(body)

    def _parse_id(self, prefix, path):
        if not path.startswith(prefix):
            return None
        remainder = path[len(prefix) :]
        if not remainder:
            return None
        try:
            return int(remainder.strip("/"))
        except ValueError:
            return None

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        payload = self.rfile.read(length)
        if not payload:
            return {}
        try:
            return json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/health":
            return self._send_json({"status": "ok"})
        if path == "/api/employees":
            employer_id = query.get("employerId", [None])[0]
            return self._handle_get_employees(employer_id)
        if path.startswith("/api/employees/"):
            employee_id = self._parse_id("/api/employees/", path)
            if employee_id is None:
                return self._send_json({"error": "Invalid employee id"}, status=400)
            return self._handle_get_employee_detail(employee_id)
        if path == "/api/templates":
            return self._handle_get_templates()
        if path.startswith("/track/"):
            token = path.split("/track/", 1)[1]
            if not token:
                return self._send_json({"error": "Missing tracking token"}, status=400)
            action = query.get("action", [None])[0]
            return self._handle_tracking_event(token, action)

        self._send_json({"error": "Not found"}, status=404)

        

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/signup":
            payload = self._read_json()
            return self._handle_signup(payload)

        if path == "/api/login":
            payload = self._read_json()
            return self._handle_login(payload)

        if path == "/api/logout":
            payload = self._read_json()
            return self._handle_logout(payload)

        if path == "/api/employees":
            payload = self._read_json()
            if payload is None:
                return self._send_json({"error": "Invalid JSON body"}, status=400)
            return self._handle_create_employee(payload)
        if path.startswith("/api/employees/") and path.endswith("/delete"):
            trimmed = path[: -len("/delete")]
            employee_id = self._parse_id("/api/employees/", trimmed)
            if employee_id is None:
                return self._send_json({"error": "Invalid employee id"}, status=400)
            payload = self._read_json() or {}
            return self._handle_delete_employee(employee_id, payload)
        if path == "/api/employees/delete_all":
            payload = self._read_json() or {}
            return self._handle_delete_employees(payload)
        if path == "/api/employees/send_metrics":
            payload = self._read_json() or {}
            return self._handle_send_metrics(payload)
        if path == "/api/simulations/run":
            payload = self._read_json() or {}
            template_ids = payload.get("templateIds") or []
            return self._handle_run_simulations(template_ids)
        if path == "/api/simulations/sweep":
            payload = self._read_json() or {}
            threshold = payload.get("thresholdHours", 24)
            return self._handle_sweep(threshold)

        self._send_json({"error": "Not found"}, status=404)

    def log_message(self, format, *args):
        # Quieter console output
        return

    # ---- Route handlers ----
    def _handle_signup(self, payload):
        name = payload.get("name")
        email = payload.get("email")
        password = payload.get("password")
        phone = payload.get("phone")
        employer_id = payload.get("employerId")
        role = payload.get("role", "employer")  # default to employer if not provided

        if not name or not email or not password or not employer_id or not role:
            return self._send_json({"error": "Missing required fields"}, status=400)

        email = email.lower()

        con = _connect()
        cur = con.cursor()
        try:
            cur.execute(
                """
                INSERT INTO users (name, email, hashed_password, phone, employer_id, role)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, email, hash_password(password), phone, employer_id, role),
            )
            con.commit()
            user_id = cur.lastrowid
        except sqlite3.IntegrityError as e:
            con.close()
            return self._send_json({"error": str(e)}, status=400)
        con.close()

        token = create_token(user_id)
        return self._send_json(
            {
                "id": user_id,
                "name": name,
                "email": email,
                "phone": phone,
                "employerId": employer_id,
                "role": role,
                "access_token": token,
            },
            status=201,
        )


    def _handle_login(self, payload):
        email = payload.get("email", "").lower()
        password = payload.get("password")

        con = _connect()
        cur = con.cursor()
        cur.execute("SELECT id, name, email, phone, employer_id, role, hashed_password FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        con.close()

        if not row or not verify_password(password, row[-1]):
            return self._send_json({"error": "Invalid credentials"}, status=401)

        user_id, name, email, phone, employer_id, role, _ = row
        token = create_token(user_id)
        return self._send_json({
            "id": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "employerId": employer_id,
            "role": role,
            "access_token": token,
        })


    def _handle_logout(self, payload):
        token = payload.get("token")
        if not token:
            return self._send_json({"error": "Missing token"}, status=400)
        invalidate_token(token)
        return self._send_json({"logged_out": True})


    def _handle_get_employees(self, employer_id):
        """List employees (optionally scoped to an employer) with computed metrics."""
        employer_filter = None
        if employer_id is not None:
            try:
                employer_filter = int(employer_id)
            except (TypeError, ValueError):
                return self._send_json({"error": "Invalid employer id"}, status=400)

        con = _connect()
        cur = con.cursor()
        query = "SELECT * FROM users"
        params = []
        if employer_filter is not None:
            query += " WHERE employer_id = ?"
            params.append(employer_filter)
        cur.execute(query, tuple(params))

        rows = cur.fetchall()

        employees = []
        rollup_counts = {
            "responses": 0,
            "clicks": 0,
            "reports": 0,
            "ignores": 0,
            "correct": 0,
        }

        for row in rows:
            metrics = compute_user_metrics(row["id"], con=con)
            employees.append(
                {
                    "id": row["id"],
                    "employer_id": row["employer_id"],
                    "name": row["name"],
                    "email": row["email"],
                    "department": row["department"],
                    "created_at": row["created_at"],
                    "score": metrics["score"],
                    "grade": metrics["grade"],
                    "status": _status_from_metrics(metrics),
                    "metrics": {
                        "click_rate": metrics["click_rate"],
                        "report_rate": metrics["report_rate"],
                        "ignore_rate": metrics["ignore_rate"],
                        "total_responses": metrics["total_responses"],
                    },
                }
            )
            rollup_counts["responses"] += metrics["total_responses"]
            rollup_counts["clicks"] += metrics["clicks"]
            rollup_counts["reports"] += metrics["reports"]
            rollup_counts["ignores"] += metrics["ignores"]
            rollup_counts["correct"] += metrics["correct"]

        if employer_filter is not None:
            summary = compute_employer_rollup(employer_filter)
        else:
            summary = self._aggregate_summary(rollup_counts)

        con.close()
        self._send_json({"employees": employees, "summary": summary})

    def _aggregate_summary(self, rollup_counts):
        """Aggregate metrics across all employees when no employer filter is provided."""
        total = rollup_counts["responses"]
        click_rate = (rollup_counts["clicks"] / total) if total else 0
        report_rate = (rollup_counts["reports"] / total) if total else 0
        ignore_rate = (rollup_counts["ignores"] / total) if total else 0
        accuracy_rate = (rollup_counts["correct"] / total) if total else 0
        # Align with backend scoring: start from 100, penalize clicks, reward reports/ignores
        if total:
            raw = 1 - click_rate + (0.5 * report_rate) + (0.2 * ignore_rate)
            score = round(max(0.0, min(raw, 1.0)) * 100)
        else:
            score = 100
        grade = _grade_from_score(score)
        return {
            "employer_id": None,
            "total_responses": total,
            "clicks": rollup_counts["clicks"],
            "reports": rollup_counts["reports"],
            "ignores": rollup_counts["ignores"],
            "correct": rollup_counts["correct"],
            "click_rate": click_rate,
            "report_rate": report_rate,
            "ignore_rate": ignore_rate,
            "accuracy_rate": accuracy_rate,
            "failure_count": rollup_counts["clicks"],
            "failure_rate": click_rate,
            "score": score,
            "grade": grade,
        }

    def _handle_get_employee_detail(self, employee_id):
        """Return detail + history for a single employee."""
        con = _connect()
        cur = con.cursor()
        cur.execute(
            "SELECT id, name, email, department, created_at FROM users WHERE id = ?",
            (employee_id,),
        )
        row = cur.fetchone()
        if not row:
            con.close()
            return self._send_json({"error": "Employee not found"}, status=404)

        metrics = compute_user_metrics(employee_id, con=con)
        history = user_metric_history(employee_id, limit=30)
        failures = user_failures_timeseries(employee_id, days=60)
        con.close()

        payload = {
            "employee": {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "department": row["department"],
                "created_at": row["created_at"],
            },
            "metrics": metrics,
            "history": history,
            "failures": failures,
        }
        self._send_json(payload)

    def _handle_get_templates(self):
        """Return available phishing templates for the UI picker."""
        con = _connect()
        cur = con.cursor()
        cur.execute(
            """
            SELECT id, template_name, subject, target_department, difficulty_level
            FROM email_templates
            ORDER BY template_name ASC
            """
        )
        templates = [
            {
                "id": row["id"],
                "name": row["template_name"],
                "subject": row["subject"],
                "department": row["target_department"],
                "difficulty": row["difficulty_level"],
            }
            for row in cur.fetchall()
        ]
        con.close()
        self._send_json({"templates": templates})

    def _handle_create_employee(self, payload):
        name = (payload or {}).get("name", "").strip()
        email = (payload or {}).get("email", "").strip().lower()
        department = (payload or {}).get("department", "").strip()
        employer_id = payload.get("employerId")
        password = (payload or {}).get("password", "Temp123")  # default password

        if not name or not email or not password:
            return self._send_json({"error": "Name, email, and password are required"}, status=400)

        con = _connect()
        cur = con.cursor()
        resolved_employer_id = _resolve_employer_id(employer_id, con)
        if resolved_employer_id is None:
            con.close()
            return self._send_json({"error": "Invalid employerId"}, status=400)

        try:
            cur.execute(
                    """
                    INSERT INTO users (name, email, hashed_password, department, employer_id, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (name, email, hash_password(password), department or None, resolved_employer_id, "employee"),
                )

            employee_id = cur.lastrowid
            con.commit()
        except sqlite3.IntegrityError as exc:
            con.close()
            return self._send_json({"error": str(exc)}, status=400)

        cur.execute(
            "SELECT id, name, email, department, employer_id, role FROM users WHERE id = ?",
            (employee_id,),
        )
        user = cur.fetchone()
        con.close()

        self._send_json(
            {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "department": user["department"],
                "employerId": user["employer_id"],
                "role": user["role"],
            },
            status=201,
        )


    def _handle_delete_employees(self, payload):
        employer_id = payload.get("employerId")
        con = _connect()
        cur = con.cursor()
        resolved_employer_id = _resolve_employer_id(employer_id, con)
        if resolved_employer_id is None:
            con.close()
            return self._send_json({"error": "Invalid employerId"}, status=400)

    # ✅ count and delete by employer_id only
        cur.execute("SELECT COUNT(1) FROM users WHERE employer_id = ?", (resolved_employer_id,))
        count = cur.fetchone()[0] or 0
        cur.execute("DELETE FROM users WHERE employer_id = ?", (resolved_employer_id,))
        con.commit()
        con.close()
        self._send_json({"deleted": count})


    def _handle_delete_employee(self, employee_id, payload):
        employer_id = payload.get("employerId")
        con = _connect()
        cur = con.cursor()
        cur.execute("SELECT employer_id FROM users WHERE id = ?", (employee_id,))
        row = cur.fetchone()
        if not row:
            con.close()
            return self._send_json({"error": "Employee not found"}, status=404)

        if employer_id is not None:
            try:
                expected_employer = int(employer_id)
            except (TypeError, ValueError):
                con.close()
                return self._send_json({"error": "Invalid employerId"}, status=400)
            if row["employer_id"] not in (None, expected_employer):
                con.close()
                return self._send_json({"error": "Employer mismatch"}, status=403)

    # ✅ delete without role filter
        cur.execute("DELETE FROM users WHERE id = ?", (employee_id,))
        con.commit()
        con.close()
        self._send_json({"deleted": 1, "id": employee_id})


    def _handle_send_metrics(self, payload):
        """Email each employee a link to their metrics page."""
        employer_id = payload.get("employerId")
        base_url = (payload.get("baseUrl") or "http://localhost:5173").rstrip("/")
        con = _connect()
        cur = con.cursor()

        resolved_employer_id = _resolve_employer_id(employer_id, con)
        if resolved_employer_id is None:
            con.close()
            return self._send_json({"error": "Invalid employerId"}, status=400)

        cur.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE employer_id = ?
            """,
            (resolved_employer_id,),
        )
        rows = cur.fetchall()
        if not rows:
            con.close()
            return self._send_json({"sent": 0, "message": "No employees found"}, status=200)

        sent = 0
        errors = []
        for row in rows:
            emp_id = row["id"]
            name = row["name"] or "Team Member"
            email = row["email"]
            if not email:
                errors.append({"id": emp_id, "error": "missing email"})
                continue
            link = f"{base_url}/employees/{emp_id}"
            subject = "Your phishing performance dashboard"
            body = f"""
            Hi {name},<br><br>
            Your latest phishing training metrics are ready. View them here:<br>
            <a href="{link}">{link}</a><br><br>
            Stay vigilant,<br>
            Security Awareness Team
            """
            try:
                success = send_email(email, subject, body)
                if success:
                    sent += 1
                else:
                    errors.append({"id": emp_id, "error": "send failed"})
            except Exception as exc:
                errors.append({"id": emp_id, "error": str(exc)})

        con.close()
        return self._send_json({"sent": sent, "errors": errors, "total": len(rows)})

    def _handle_run_simulations(self, template_ids):
        """Queue outbound phishing simulation emails for selected templates."""
        deliveries = send_department_emails(template_ids)
        summary = {"scheduled": len(deliveries), "deliveries": deliveries}
        self._send_json(summary)

    def _handle_sweep(self, threshold):
        """Mark stale simulations as ignored after the given threshold in hours."""
        try:
            hours = int(threshold)
        except (TypeError, ValueError):
            hours = 24
        ignored = mark_expired_simulations_as_ignored(hours)
        self._send_json({"ignored": ignored, "thresholdHours": hours})
        

    def _handle_tracking_event(self, token, action_param):
        """Record a click/report action from a tracking pixel or link."""
        con = _connect()
        cur = con.cursor()
        cur.execute(
            """
            SELECT id, simulation_id, user_id, action, acted_at
            FROM tracking_tokens
            WHERE token = ?
            """,
            (token,),
        )
        row = cur.fetchone()
        if not row:
            con.close()
            return self._send_json({"error": "Tracking token not found"}, status=404)

        if row["acted_at"]:
            con.close()
            return self._send_json({"status": "already-recorded"})

        cur.execute(
            "SELECT sent_at FROM simulations WHERE id = ?", (row["simulation_id"],)
        )
        sim = cur.fetchone()
        sent_at = datetime.fromisoformat(sim["sent_at"]) if sim else datetime.utcnow()
        response_time = max((datetime.utcnow() - sent_at).total_seconds(), 0.0)

        action_label = row["action"]
        action_taken = "clicked_link" if action_label == "clicked" else "reported"

        record_employee_action(
            row["simulation_id"], row["user_id"], action_taken, response_time
        )
        cur.execute(
            "UPDATE tracking_tokens SET acted_at = CURRENT_TIMESTAMP WHERE id = ?",
            (row["id"],),
        )
        con.commit()
        con.close()

        message = (
            "Thanks for reporting this simulation."
            if action_taken == "reported"
            else "This click has been recorded for training metrics."
        )
        self._set_headers(content_type="text/html")
        self.wfile.write(f"<html><body><p>{message}</p></body></html>".encode("utf-8"))


def run(server_class=HTTPServer, handler_class=SecurityAwarenessHandler, port=DEFAULT_PORT):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Security Awareness API running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()