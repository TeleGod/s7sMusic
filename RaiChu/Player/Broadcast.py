import asyncio

from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant

from Process.main import bot as Ufo
from RaiChu.config import SUDO_USERS

@Client.on_message(filters.command(["اذاعه"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("`بدأ الاذاعه...`")
        if not message.reply_to_message:
            await wtf.edit("الرجاء الرد على رسالة لبدء الاذاعه !")
            return
        lmao = message.reply_to_message.text
        async for dialog in Ufo.iter_dialogs():
            try:
                await Ufo.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`الاذاعه...` \n\n**تم الارسال الى :** `{sent}` مجموعه \n**لم يرسل الى :** {failed} مجموعه")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"`انتهت الاذاعه` \n\n**تم ارساله الي :** `{sent}` مجموعه \n**لم يتم ارساله الى :** {failed} مجموعه")
