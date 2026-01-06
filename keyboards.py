from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def approve_keyboard(user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ تایید", callback_data=f"approve:{user_id}"),
            InlineKeyboardButton("❌ رد", callback_data=f"reject:{user_id}")
        ]
    ])

def owner_panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 کاربران", callback_data="users")],
        [InlineKeyboardButton("📢 تبلیغات", callback_data="ads")],
        [InlineKeyboardButton("🔗 اسپانسر", callback_data="sponsors")]
    ])

def user_panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ افزودن کانال", callback_data="add_channel")],
        [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")],
        [InlineKeyboardButton("📩 ارتباط با مالک", callback_data="contact")]
    ])
