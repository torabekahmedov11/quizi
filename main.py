import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import database as db

load_dotenv()

# Test qilish uchun maxsus o'zgaruvchilar (Qat'iy cheklov olib tashlandi)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

if not BOT_TOKEN or not CHANNEL_ID:
    logger.error("BOT_TOKEN yoki CHANNEL_ID topilmadi! .env yoki Render sozlamalarini tekshiring.")
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
        await bot.send_poll(
            chat_id=CHANNEL_ID,
            question=question_data['question'],
            options=question_data['options'],
            type='quiz',
            correct_option_id=question_data['correct_option_id'],
            is_anonymous=True
        )
        db.mark_as_sent(question_data['id'])
        logger.info(f"Savol muvaffaqiyatli yuborildi! ID: {question_data['id']}")
    except Exception as e:
        logger.error(f"Savol yuborishda xatolik yuz berdi: {e}")

# TEST UCHUN KOMANDA: Botga /test deb yozsangiz, darhol 1 ta savol kanalga tashlaydi
@dp.message(Command("test"))
async def test_command_handler(message: types.Message):
    await message.reply("Test ishga tushdi! Kanalga savol yuborilmoqda...")
    await send_daily_quiz()

# RENDER 'Web Service' UCHUN DUMMY SERVER (Xatolikni oldini olish uchun)
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render o'zining portini beradi, agar yo'q bo'lsa 10000 ishlatiladi
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Dummy web server port {port} da ishga tushdi")

async def main():
    db.init_db()
    stats = db.get_stats()
    logger.info(f"Baza holati: Jami: {stats['total']}, Yuborilmagan: {stats['unsent']}")
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_quiz, 'cron', hour=9, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=13, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=17, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=20, minute=0)
    scheduler.start()
    
    # Render uchun Web Serverni yoqish
    await start_dummy_server()
    
    # Botni yoqish
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
