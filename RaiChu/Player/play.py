import io
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty
import os
import random
import re
import youtube_dl
import youtube_dl
import aiofiles
import aiohttp
from RaiChu.converter import convert
import ffmpeg
import requests
from Process.fonts import CHAT_TITLE
from PIL import Image, ImageDraw, ImageFont
from RaiChu.config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2, IMG_5
from Process.filters import command, other_filters
from Process.queues import QUEUE, add_to_queue
from Process.main import call_py, aman as user
from Process.utils import bash
from Process.main import bot as Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch
from Process.design.thumbnail import play_thumb, queue_thumb
from RaiChu.inline import stream_markup, audio_markup

def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []

    
@Client.on_message(command(["play", f"تشغيل"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    buttons = audio_markup(user_id)
    if m.sender_chat:
        return await m.reply_text("أنت مشرف __مجهول__ !\n\n» عد إلى حساب المستخدم من حقوق المشرف..")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"Error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 لاستخدامي ، أحتاج إلى أن أكون ** مسؤول ** مع الأذونات ** التالية**:\n\n» ❌ __حذف الرسائل__\n» ❌__إضافة مستخدمين__\n» ❌ __إدارة دردشة الفيديو__\n\nيتم تحديث البيانات ** تلقائيًا بعد ترقيتك ****"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "الصلاحيه مفقوده :" + "\n\n» ❌ __إدارة دردشة الفيديو__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "الصلاحيه مفقوده :" + "\n\n» ❌ __حذف الرسائل__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("الصلاحيه مفقوده :" + "\n\n» ❌ __أضف مستخدمين__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **محظور من الجروب** {m.chat.title}\n\n» **تأكد من تقييد الحساب المساعد واعد المحاوله.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **فشل في الانضمام**\n\n**reason**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **فشل في الانضمام**\n\n**reason**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 *جاري تنزيل الملف الصوتي...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else: 
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار »** `{pos}`\n\n🏷 **الاسم :** [{songname}]({link}) | `موسيقي`\n💭 **المحادثه :** `{chat_id}`\n🎧 **طلب الكائن دا:** {m.from_user.mention()}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            else:
             try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"🏷 **الاسم :** [{songname}]({link})\n💭 **المحادثه :** `{chat_id}`\n💡 **الحاله :** `مشغل`\n🎧 **طلب الكائن دا:** {requester}\n📹 **اسم العمليه:** `موسيقي`",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 error:\n\n» {e}")
        
    else:
        if len(m.command) < 2:
         await m.reply_photo(
                     photo=f"{IMG_5}",
                    caption="**رد على ملف صوتي او ارسل اسم للبحث عنه**",
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("• جروب الدعم", url=f"https://t.me/te_God"),
                            InlineKeyboardButton("• اغلاق", callback_data="cls")
                        ]
                    ]
                )
            )
        else:
            suhu = await m.reply_text(
        f"**جاري التنزيل**\n\n100% ▓▓▓▓▓▓▓▓▓▓▓▓ 00%"
    )
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("• **لم يتم العثور على نتائج.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                videoid = search[4]
                dlurl = f"https://www.youtubepp.com/watch?v={videoid}"
                info = f"https://t.me/te_god"
                keyboard = stream_markup(user_id, dlurl)
                playimg = await play_thumb(videoid)
                queueimg = await queue_thumb(videoid)
                await suhu.edit(
                            f"**جاري التنزيل**\n\n**الاسم**: {title[:22]}\n\n100% ▓▓▓▓▓▓▓▓▓▓▓▓0%\n\n**وقت الاستغراق**: 00:00 ثانيه\n\n**تحويل الصوت[FFmpeg Process]**"
                        )
                format = "bestaudio"
                abhi, ytlink = await ytdl(format, url)
                if abhi == 0:
                    await suhu.edit(f"• تم اكتشاف مشكله\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=queueimg,
                            caption=f"⏳ تمت الإضافة إلى قائمة الانتظار في {pos}\n\n👤طلب الكائن دا :{requester}\nمزيد من المعلومات : [اضغط هنا]({info})",
                            reply_markup=InlineKeyboardMarkup(keyboard),
                        )
                    else:
                        try:
                            await suhu.edit(
                            f"**تم التحميل**\n\n**الاسم**: {title[:22]}\n\n0% ████████████100%\n\n**الوقت المستغرق**: 00:00 ثانيه\n\n**تحويل الصوت [FFmpeg Process]**"
                        )
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=playimg,
                                caption=f"📡 تم تشغيل ملف صوتي بنجاح 💡\n\n👤طلب الكائن دا:{requester}\nمزيد من المعلومات : [اضغط هنا]({info})",
                                reply_markup=InlineKeyboardMarkup(keyboard),
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"حدث خطأ : `{ep}`")
