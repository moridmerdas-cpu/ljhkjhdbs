import database

async def forward(bot, message):
    database.cursor.execute("SELECT group_id FROM groups")
    groups = database.cursor.fetchall()

    for (gid,) in groups:
        try:
            await bot.forward_message(
                chat_id=gid,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except:
            pass
