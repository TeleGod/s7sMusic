from Process.main import bot
from pyrogram import filters


@bot.on_message(filters.command('id'))
def ids(_, message):
    reply = message.reply_to_message
    if reply:
        message.reply_text(
            f"**معلومات الايدي**: `{message.from_user.id}`\n**{reply.from_user.first_name}'s ايديك**: `{reply.from_user.id}`\n**ايدي المحادثه**: `{message.chat.id}`"
        )
    else:
        message.reply(
            f"**ايديك**: `{message.from_user.id}`\n**ايدي المحادثه**: `{message.chat.id}`"
        )
