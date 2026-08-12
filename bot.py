import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import database as db

# .env fayldan o'zgaruvchilarni yuklash
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8987917712:AAE8LBRR3UwFOipRG_dvl245aw7FI_t457U")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002358747723")

# Loglarni sozlash (Serverda xatoliklarni kuzatish uchun muhim)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Xavfsizlik: Boshqa kanalga ulanib qolmasligi uchun qat'iy himoya
ALLOWED_CHANNEL = "-1002358747723"
if str(CHANNEL_ID) != ALLOWED_CHANNEL:
    CHANNEL_ID = ALLOWED_CHANNEL

if not BOT_TOKEN or not CHANNEL_ID:
    logger.error("BOT_TOKEN yoki CHANNEL_ID topilmadi! Iltimos .env faylini tekshiring.")
    exit(1)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def send_daily_quiz():
    """Bazadan yangi savolni olib kanalga tashlaydi"""
    logger.info("Yangi savol yuborish jarayoni boshlandi...")
    
    question_data = db.get_unsent_question()
    
    if not question_data:
        logger.warning("DIQQAT: Bazada yuborilmagan savollar qolmadi!")
        return
    
    try:
        # Telegramga viktorina yuborish
        await bot.send_poll(
            chat_id=CHANNEL_ID,
            question=question_data['question'],
            options=question_data['options'],
            type='quiz',
            correct_option_id=question_data['correct_option_id'],
            is_anonymous=True # Telegramdagi barcha quizlar asosan anonim bo'ladi
        )
        # Yuborilgandan so'ng uni belgilab qo'yish
        db.mark_as_sent(question_data['id'])
        logger.info(f"Savol muvaffaqiyatli yuborildi! ID: {question_data['id']}")
        
    except Exception as e:
        logger.error(f"Savol yuborishda xatolik yuz berdi: {e}")

async def main():
    # Bazani tekshirish
    db.init_db()
    stats = db.get_stats()
    logger.info(f"Baza holati: Jami: {stats['total']}, Yuborilmagan (Qoldiq): {stats['unsent']}")
    
    # Schedulerni sozlash (Rejalashtiruvchi)
    scheduler = AsyncIOScheduler()
    
    # Standart vaqtlar (Toshkent vaqti bilan ishlashi uchun server vaqt zonasini to'g'rilash tavsiya etiladi)
    # Yoki agar server UTC da bo'lsa, UTC ga moslab soatlarni o'zgartirishingiz mumkin.
    scheduler.add_job(send_daily_quiz, 'cron', hour=9, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=13, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=17, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=20, minute=0)
    
    scheduler.start()
    logger.info("Bot va Rejalashtiruvchi muvaffaqiyatli ishga tushdi. Bot kanalga jadval asosida savol yuboradi.")
    
    # Botni doimiy ishlab turishi uchun Polling yoqiladi
    # Agar botga admin sifatida biror komandalar qo'shsangiz, polling kerak bo'ladi.
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
