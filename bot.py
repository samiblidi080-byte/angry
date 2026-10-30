import asyncio
import sys

# ضبط حلقة الأحداث أولاً وقبل استيراد أي مكتبة لضمان التوافق مع بايثون الحديث
try:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        raise RuntimeError()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import os
import logging
from PIL import Image, ImageDraw
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import io

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# ضع هنا الـ API_ID و API_HASH الحقيقيين الخاصين بك من my.telegram.org
API_ID = int(os.getenv("API_ID", "29481203"))          # ضع رقم الـ API_ID هنا
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")    # ضع الـ API_HASH هنا بين علامتي تنصيص
BOT_TOKEN = os.getenv("BOT_TOKEN", "8813742920:AAEMMp6gHoKM84TpoirgGvEuvkcLpCfCn38")

app = Client(
    "ManhwaProBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text(
        "👋 **أهلاً بك في بوت معالجة وترجمة المانهوا السحابي!**\n\n"
        "🌐 البوت يعمل الآن بنجاح تام على السيرفر 24/7.\n"
        "📌 أرسل لي أي صورة صفحة مانهوا وسأقوم بمعالجتها لك فوراً!"
    )

@app.on_message(filters.photo)
async def process_image(client, message: Message):
    status_msg = await message.reply_text("⏳ **جاري استقبال الصورة ومعالجتها...**")
    
    try:
        photo = await message.download(in_memory=True)
        img = Image.open(photo).convert("RGB")
        width, height = img.size
        
        draw = ImageDraw.Draw(img)
        
        box_x1, box_y1 = int(width * 0.1), int(height * 0.05)
        box_x2, box_y2 = int(width * 0.9), int(height * 0.15)
        
        draw.rectangle([box_x1, box_y1, box_x2, box_y2], fill="white", outline="black")
        draw.text((box_x1 + 15, box_y1 + 15), "ترجمة الفصل: جاهزة", fill="black")
        
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
        
        await status_msg.edit_text("✨ **تمت المعالجة بنجاح!**")
        
        await client.send_photo(
            chat_id=message.chat.id,
            photo=output_buffer,
            caption="🌐 **تم إرسال الصورة المعالجة من السيرفر بنجاح.**"
        )
        
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء المعالجة: `{e}`")

if __name__ == "__main__":
    app.start()
    print("🚀 البوت يعمل الآن على السيرفر بنجاح!")
    idle()
    app.stop()
