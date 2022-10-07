from pyrogram import Client, errors
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from youtubesearchpython import VideosSearch
from pyrogram.types import (
  CallbackQuery,
  InlineKeyboardButton,
  InlineKeyboardMarkup,
  Message,
)

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

def audio_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="• القائمة", callback_data=f'cbmenu | {user_id}'),
      InlineKeyboardButton(text="• الازرار", switch_inline_query_current_chat=""),
    ],
    [
      InlineKeyboardButton(text="• اغلاق", callback_data=f'cls'),
    ],
  ]
  return buttons

def stream_markup(user_id, dlurl):
  buttons = [
    [
      InlineKeyboardButton(text="II", callback_data=f'قفل | {user_id}'),
      InlineKeyboardButton(text="▷", callback_data=f'استئناف | {user_id}'),
      InlineKeyboardButton(text="‣‣I", callback_data=f'تخطي | {user_id}'),
      InlineKeyboardButton(text="▢", callback_data=f'ايقاف | {user_id}')
    ],
    [
      InlineKeyboardButton(text="• القائمة •", switch_inline_query_current_chat=""),
      InlineKeyboardButton(text="• يوتيوب •", url=f"{dlurl}")
    ],
    [
      InlineKeyboardButton(text="اغلاق", callback_data=f'cls'),
    ],
  ]
  return buttons

def menu_markup(user_id):
  buttons = [
     [InlineKeyboardButton(text="II", callback_data=f'ايقاف | {user_id}'),
      InlineKeyboardButton(text="▷", callback_data=f'استئناف | {user_id}')],
     [InlineKeyboardButton(text="‣‣I", callback_data=f'تخطي | {user_id}'),
      InlineKeyboardButton(text="▢", callback_data=f'ايقاف | {user_id}')
    ],
     [InlineKeyboardButton(text="🔇", callback_data=f'تم كتم | {user_id}'),
      InlineKeyboardButton(text="SouRce TeleGod", url=f"https://t.me/sr_telegod"),
      InlineKeyboardButton(text="🔊", callback_data=f'تم الغاء كتم | {user_id}')],
  ]
  return buttons

def song_download_markup(videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text="⬇️ موسيقي",
                callback_data=f"gets audio|{videoid}",
            ),
            InlineKeyboardButton(
                text="⬇️ فيديو",
                callback_data=f"gets video|{videoid}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="رجــوع",
                callback_data="cbhome",
            )
        ],
    ]
    return buttons

close_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "• اغلاق •", callback_data="cls"
      )
    ]
  ]
)


back_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "• رجوع •", callback_data="cbmenu"
      )
    ]
  ]
)
