import asyncio
from RaiChu.config import BOT_USERNAME, SUDO_USERS
from Process.decorators import authorized_users_only, sudo_users_only, errors
from Process.filters import command, other_filters
from Process.main import user as USER
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["انضم", f"ادخل"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except BaseException:
        await message.reply_text(
            "• **ليس لدي إذن :**\n\n» ❌ __اضافة مستخدمين__",
        )
        return

    try:
        user = await USER.get_me()
    except BaseException:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 خطأ انتظر قليلا 🛑 \n\n**لم يتمكن البوت من اضافة المساعد الى المجموعه بسبب كثرة طلبات الانضمام إلى المساعد**"
            "\n\n**انتظر او أضف المساعد يدويًا إلى مجموعتك وحاول مرة أخرى**",
        )
        return
    await message.reply_text(
        f"**انضم المساعد الى المجموعه بنجاح**",
    )


@Client.on_message(command(["userbotleave",
                            f"غادر"]) & filters.group & ~filters.edited)
@authorized_users_only
async def leave_one(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ غادر المساعد من المجموعه بنجاح")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "❌ **لا يمكن للبوت مغادرة المجموعه انتظر قليلا واعد المحاوله**\n\n**» او قم بطرد البوت يدويا**"
        )

        return


@Client.on_message(command(["غادر الكل", f"leaveall"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 جاري مغادرة كل المجموعات !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"يغادر كل المجموعات...\n\nغادر : {left} مجموعه.\nلم يستطيع مغادرة: {failed} مجموعه."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"يغادر...\n\nغادر: {left} مجموعه.\nلم يستطيع مغادرة : {failed} مجموعه."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ غادر من : {left} مجموعه.\n❌ لم يستطيع مغادرة : {failed} مجموعه."
    )
