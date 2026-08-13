import asyncio
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import database as db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8987917712:AAE8LBRR3UwFOipRG_dvl245aw7FI_t457U")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002358747723")

# O'zbekiston vaqti va Loyihaning ilk boshlangan KUN VA VAQTI (Epoch)
TZ = ZoneInfo('Asia/Tashkent')
START_DATE = datetime(2026, 8, 12, 0, 0, 0, tzinfo=TZ)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def send_daily_quiz(message: types.Message = None):
    logger.info("Yangi savol yuborish jarayoni boshlandi...")
    question_data = db.get_unsent_question()
    
    if not question_data:
        err = "DIQQAT: Bazada yuborilmagan savollar qolmadi!"
        logger.warning(err)
        if message: await message.reply(err)
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
        if message: await message.reply(f"✅ Savol kanalingizga muvaffaqiyatli yuborildi! (ID: {question_data['id']})")
    except Exception as e:
        err_msg = f"❌ Savol yuborishda xatolik yuz berdi!\n\nXato matni: {e}\n\nEslatma: Botni kanalga admin qildingizmi va kanal ID to'g'rimi?"
        logger.error(err_msg)
        if message: await message.reply(err_msg)

@dp.message(Command("test"))
async def test_command_handler(message: types.Message):
    await message.reply(f"Test ishga tushdi! {CHANNEL_ID} kanaliga savol yuborishga harakat qilaman...")
    await send_daily_quiz(message)

@dp.channel_post(Command("test"))
async def test_channel_handler(message: types.Message):
    await send_daily_quiz(message)

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

def sync_time_based_state():
    """Vaqtga qarab qayerda qolganini (indexni) hisoblash mantiqiy qismi"""
    now = datetime.now(TZ)
    delta = now - START_DATE
    days = delta.days
    
    if days < 0:
        return
        
    count = days * 4
    if now.hour >= 9: count += 1
    if now.hour >= 13: count += 1
    if now.hour >= 17: count += 1
    if now.hour >= 20: count += 1
    
    # Topilgan o'tkazib yuborilishi kerak bo'lgan savollar sonini belgilaymiz
    if count > 0:
        db.fast_forward(count)
        logger.info(f"Sinxronizatsiya: {count} ta savol avtomatik o'tkazib yuborildi. Davom etamiz!")

async def main():
    db.init_db()
    stats = db.get_stats()
    
    if stats['total'] == 0:
        logger.info("Baza bo'sh! Render xotirasini yangilagan bo'lishi mumkin. Savollar avtomatik qayta tiklanmoqda...")
        import advanced_seed
        advanced_seed.generate_big_db()
        
        import os
        if os.path.exists('savollar.xlsx'):
            import import_excel
            import_excel.import_from_excel()
            
        # Bazani tiklagach, kalendar orqali qayerda to'xtaganligini hisoblab o'tkazib yuboramiz
        sync_time_based_state()
        stats = db.get_stats()
        
    logger.info(f"Baza holati: Jami: {stats['total']}, Yuborilmagan: {stats['unsent']}")
    
    scheduler = AsyncIOScheduler(timezone=TZ)
    scheduler.add_job(send_daily_quiz, 'cron', hour=9, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=13, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=17, minute=0)
    scheduler.add_job(send_daily_quiz, 'cron', hour=20, minute=0)
    scheduler.start()
    
    await start_dummy_server()
    
    # Muhim: Agar oldin webhook yoqilgan bo'lsa, polling ishlashi uchun uni o'chiramiz
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except:
        pass
        
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
