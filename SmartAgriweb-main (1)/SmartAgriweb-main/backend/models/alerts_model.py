from database.db import query_db, execute_db
from datetime import datetime

class AlertModel:

    @staticmethod
    def get_active(limit=10):
        rows = query_db(
            "SELECT * FROM alerts WHERE resolved=0 ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return [dict(r) for r in rows]

    @staticmethod
    def get_all(limit=20):
        rows = query_db(
            "SELECT * FROM alerts ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return [dict(r) for r in rows]

    @staticmethod
    def create(alert_type, title, message):
        return execute_db(
            "INSERT INTO alerts (type, title, message) VALUES (?,?,?)",
            (alert_type, title, message)
        )

    @staticmethod
    def resolve(alert_id):
        execute_db("UPDATE alerts SET resolved=1 WHERE id=?", (alert_id,))

    @staticmethod
    def count_active():
        row = query_db("SELECT COUNT(*) as cnt FROM alerts WHERE resolved=0", one=True)
        return row["cnt"] if row else 0

    @staticmethod
    def format_for_frontend(rows):
        result = []
        for r in rows:
            ts = r.get("created_at", "")
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                time_str = dt.strftime("%I:%M %p")
            except Exception:
                time_str = ts
            result.append({
                "type":    r["type"],
                "title":   r["title"],
                "message": r["message"],
                "time":    time_str,
            })
        return result
