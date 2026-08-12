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

# Avtomatik tushib ketishi uchun ehtiyot shart qilib yana hardcode qo'shildi
BOT_TOKEN = os.getenv("BOT_TOKEN", "8987917712:AAE8LBRR3UwFOipRG_dvl245aw7FI_t457U")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002358747723")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def send_daily_quiz():
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

# Agar shaxsiy xabarda (lichkada) /test deb yozsa:
@dp.message(Command("test"))
async def test_command_handler(message: types.Message):
    await message.reply(f"Test ishga tushdi! {CHANNEL_ID} kanaliga savol yuborilmoqda...")
    await send_daily_quiz()

# Agar kanal ichida /test deb yozsa (kanal xabarlarini ushlash):
@dp.channel_post(Command("test"))
async def test_channel_handler(message: types.Message):
    await send_daily_quiz()

async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Dummy web server port {port} da ishga tushdi")

async def main():
    db.init_db()
    
    # MUHIM: Render keshni tozalaganda bazani o'chirib yuboradi (bepul tarifda).
    # Shuning uchun agar baza bo'sh bo'lsa, uni kod ishga tushganda o'zi to'ldirib oladi!
    stats = db.get_stats()
    if stats['total'] == 0:
        logger.info("Baza bo'sh! Render xotirasini yangilagan bo'lishi mumkin. Savollar avtomatik qayta tiklanmoqda...")
        import advanced_seed
        advanced_seed.generate_big_db()
        stats = db.get_stats()
        
    logger.info(f"Baza holati: Jami: {stats['total']}, Yuborilmagan: {stats['unsent']}")
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_quiz, 'cron', hour=9, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=13, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=17, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=20, minute=0)
    scheduler.start()
    
    await start_dummy_server()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
