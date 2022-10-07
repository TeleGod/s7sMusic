from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from RaiChu.config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from Process.filters import other_filters2
from time import time
from Process.filters import command
from datetime import datetime
from Process.decorators import authorized_users_only

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 ** 2 * 24),
    ("hour", 60 ** 2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(other_filters2)
async def start(_, message: Message):
        await message.reply_text(
        f"""مرحبا {message.from_user.mention()}, انا {BOT_NAME}.
        
• استطيع تشغيل الموسيقي بدون تقطيع وبجوده فائقه في الجروبات والقنوات

• لا تتردد في إضافتي إلى مجموعاتك.
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [                   
                    InlineKeyboardButton(
                        "اوامر التشغيل", callback_data="cbbasic"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "طريقة استخدامي", callback_data="cbhowtouse"
                    ),
                  ],[
                    InlineKeyboardButton(
                       "SouRce TeleGod", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                    InlineKeyboardButton(
                       "جروب الدعم", url=f"https://t.me/{GROUP_SUPPORT}"
                    )
                ],[
                    InlineKeyboardButton(
                        "ضيفني لمجموعتك ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(command(["مبرمج السورس", f"صلاح", f"سحس", f"المبرمج"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/c11147b8c614b2b647428.jpg",
        caption=f"""Programmer [TeleGod](https://t.me/SR_TeleGod) 𖡼\nᴛᴏ ᴄᴏᴍᴍụɴɪᴄᴀᴛᴇ ᴛᴏɢᴇᴛʜᴇʀ 𖡼\nғᴏʟʟᴏᴡ ᴛʜᴇ ʙụᴛᴛᴏɴѕ ʟᴏᴡᴇʀ 𖡼""",
        reply_markup=InlineKeyboardMarkup(
         [
            [
                InlineKeyboardButton("DEV SALAH", url=f"https://t.me/BK_ZT"),
            ],
            [
                InlineKeyboardButton(
                    "SouRce TeleGod", url=f"https://t.me/sr_TeleGod"
                ),
            ],
            [
                InlineKeyboardButton("ضيف البوت لمجموعتك ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            ]
         ]
     )
  )
  
@Client.on_message(command(["سورس", "source", f"السورس", f"تلي جود"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/c11147b8c614b2b647428.jpg",
        caption=f"""WelCome To SouRce TeleGod Music ✨""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "DeveLoPer", url=f"https://t.me/Bk_ZT")
                ]
            ]
        ),
    )
