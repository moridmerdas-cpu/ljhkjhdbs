from datetime import datetime
import database

def is_active(user_id):
    database.cursor.execute(
        "SELECT expire_date FROM users WHERE user_id=? AND status='approved'",
        (user_id,)
    )
    row = database.cursor.fetchone()
    if not row or not row[0]:
        return False
    return datetime.fromisoformat(row[0]) > datetime.now()
