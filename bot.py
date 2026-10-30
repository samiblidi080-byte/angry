import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image

# 1. إعداد السجلات (Logging) لمتابعة حالة البوت بدقة
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 2. بيانات الاتصال والمعلومات الخاصة بك
API_ID = 30392142
API_HASH = "b4990613e615ca3cd05404b65a3e3f55"
BOT_TOKEN = "8813742920:AAEMMp6gHoKM84TpoirgGvEuvkcLpCfCn38"

# تهيئة عميل البوت
app = Client(
    "manhwa_translator_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """رسالة الترحيب عند بدء البوت"""
    user_name = message.from_user.first_name if message.from_user else "صديقي"
    welcome_text = (
        f"أهلاً بك يا {user_name} في بوت ترجمة المانها والمانهوا! 🎨📖\n\n"
        "أرسل لي أي صورة لفصل مانهوا (صورة عادية)، وسأقوم بمعالجتها واستقبالها فوراً."
    )
    await message.reply_text(welcome_text)
    logger.info(f"تم استقبال أمر البدء من المستخدم: {message.from_user.id if message.from_user else 'unknown'}")

@app.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    """معالجة الصور المرسلة من المستخدم"""
    processing_msg = await message.reply_text("⏳ جاري تحميل وتنزيل الصورة للمعالجة...")
    
    try:
        # تحميل الصورة المرسلة إلى مجلد مؤقت
        photo_path = await message.download()
        logger.info(f"تم تحميل الصورة بنجاح إلى المسار: {photo_path}")
        
        # فتح الصورة باستخدام مكتبة Pillow للتحقق منها وتعديلها إن أمكن
        with Image.open(photo_path) as img:
            width, height = img.size
            logger.info(- f"أبعاد الصورة: {width}x{height}")

        # هنا يمكنك إضافة كود الترجمة ومعالجة النصوص لاحقاً
        await processing_msg.edit_text(
            "✅ تم استقبال الصورة وتحميلها بنجاح على السيرفر!\n"
            f"📐 الأبعاد: {width}x{height} بكسل.\n\n"
            "🔄 (جاري ربط محرك الترجمة الذكي...)"
        )
        
        # تنظيف الملف المؤقت بعد الانتهاء
        if os.path.exists(photo_path):
            os.remove(photo_path)
            
    except Exception as e:
        logger.error(f"حدث خطأ أثناء معالجة الصورة: {e}")
        await processing_msg.edit_text(f"❌ حدث خطأ أثناء معالجة الصورة: {str(e)}")

if __name__ == "__main__":
    logger.info("🚀 جاري إقلاع وتشغيل البوت...")
    app.run()
