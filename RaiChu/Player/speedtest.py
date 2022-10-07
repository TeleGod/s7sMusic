import os
import wget
import speedtest

from PIL import Image
from pyrogram.types import Message
from pyrogram import filters, Client

from Process.main import bot as app
from RaiChu.config import SUDO_USERS as SUDOERS

@app.on_message(filters.command("speedtest") & ~filters.edited)
async def run_speedtest(_, message):
    userid = message.from_user.id
    m = await message.reply_text("__جاري حساب سرعة البوت__...")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("🔥 __سرعة التنزيل__")
        test.download()
        m = await m.edit("🔥 __سرعة الرفع__")
        test.upload()
        test.results.share()
    except speedtest.ShareResultsConnectFailure:
        pass
    except Exception as e:
        await m.edit_text(e)
        return
    result = test.results.dict()
    m = await m.edit_text("💠 سرعة البوت")
    if result["share"]:
        path = wget.download(result["share"])
        try:
            img = Image.open(path)
            c = img.crop((17, 11, 727, 389))
            c.save(path)
        except BaseException:
            pass
    output = f"""💡 **نتيجة اختبار السرعة**
    
<u>**عميل :**</u>

**مزود خدمة الإنترنت :** {result['client']['isp']}
**دولة :** {result['client']['country']}
  
<u>**معلومات السيرفر :**</u>

**الاسم :** {result['server']['name']}
**الدوله :** {result['server']['country']}, {result['server']['cc']}
**كفيل :** {result['server']['sponsor']}
**وقت الإستجابة :** {result['server']['latency']}  

⚡ **البينج :** {result['ping']}"""
    if result["share"]:
        msg = await app.send_photo(
            chat_id=message.chat.id, photo=path, caption=output
        )
        os.remove(path)
    else:
        msg = await app.send_message(
            chat_id=message.chat.id, text=output
        )
    await m.delete()
