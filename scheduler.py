from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import database

def check_expire(bot):
    database.cursor.execute(
        "SELECT user_id, expire_date FROM users WHERE status='approved'"
    )
    for user_id, expire in database.cursor.fetchall():
        if expire and datetime.fromisoformat(expire) < datetime.now():
            database.cursor.execute(
                "UPDATE users SET status='expired' WHERE user_id=?",
                (user_id,)
            )
            bot.send_message(user_id, "⛔ اشتراک شما منقضی شد")
    database.conn.commit()

def start(bot):
    s = BackgroundScheduler()
    s.add_job(check_expire, "interval", hours=1, args=[bot])
    s.start()
