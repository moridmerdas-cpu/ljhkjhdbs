from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
from datetime import datetime, timedelta

import database, keyboards, checks, forwarder, scheduler
from config import *

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# ───── START ─────
async def start_cmd(update: Update, context):
    user_id = update.effective_user.id

    database.cursor.execute(
        "SELECT status FROM users WHERE user_id=?", (user_id,)
    )
    user = database.cursor.fetchone()

    if not user:
        database.cursor.execute(
            "INSERT INTO users VALUES (?, 'pending', NULL, NULL)",
            (user_id,)
        )
        database.conn.commit()

        await context.bot.send_message(
            OWNER_ID,
            f"درخواست جدید:\n{user_id}",
            reply_markup=keyboards.approve_keyboard(user_id)
        )
        await update.message.reply_text("⏳ منتظر تایید مالک باشید")
        return

    if user[0] != "approved":
        await update.message.reply_text("⛔ دسترسی ندارید")
        return

    await update.message.reply_text(
        "✅ پنل شما فعال است",
        reply_markup=keyboards.user_panel()
    )

# ───── APPROVE / REJECT ─────
async def approve_cb(update: Update, context):
    q = update.callback_query
    action, uid = q.data.split(":")
    uid = int(uid)

    if action == "approve":
        expire = (datetime.now() + timedelta(days=DEFAULT_SUB_DAYS)).isoformat()
        database.cursor.execute(
            "UPDATE users SET status='approved', expire_date=? WHERE user_id=?",
            (expire, uid)
        )
        await context.bot.send_message(uid, "✅ تایید شدید")
    else:
        database.cursor.execute(
            "UPDATE users SET status='rejected' WHERE user_id=?",
            (uid,)
        )
        await context.bot.send_message(uid, "❌ رد شدید")

    database.conn.commit()
    await q.answer("انجام شد")

# ───── CHANNEL POSTS ─────
async def channel_post(update: Update, context):
    await forwarder.forward(context.bot, update.channel_post)

# ───── WEBHOOK ─────
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ───── HANDLERS ─────
application.add_handler(CommandHandler("start", start_cmd))
application.add_handler(CallbackQueryHandler(approve_cb))
application.add_handler(MessageHandler(filters.ChatType.CHANNEL, channel_post))

# ───── RUN ─────
if __name__ == "__main__":
    scheduler.start(application.bot)
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )
