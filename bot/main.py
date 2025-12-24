import asyncio
import logging
import os
import sys
import io
sys.dont_write_bytecode = True
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.inference import MushroomPredictor
from services.llm import get_mushroom_info

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

try:
    print("Инициализация нейросети...")
    predictor = MushroomPredictor()
except Exception as e:
    print(f" Фатальная ошибка: {e}")
    sys.exit(1)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("📸 **Кидай фото гриба!**\nЯ определю его вид и съедобность.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    status_msg = await message.answer("**Обрабатываю...**")
    
    try:
        # 1. Создаем буфер в памяти (виртуальный файл)
        buffer = io.BytesIO()
        
        # 2. Скачиваем фото прямо в буфер
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        await bot.download_file(file.file_path, destination=buffer)
        
        # Важно! Перематываем буфер в начало, чтобы PIL мог его прочитать
        buffer.seek(0)
        
        # 3. Предсказываем (передаем буфер вместо пути к файлу)
        class_name, prob = predictor.predict(buffer)
        confidence = prob * 100
        
        await status_msg.edit_text(f"🍄 Это **{class_name}** ({confidence:.1f}%)\n⏳ Генерирую описание...")
        
        # 4. LLM
        desc = await get_mushroom_info(class_name, confidence)
        
        await status_msg.edit_text(
            f"Вид: **{class_name}**\n"
            f"Точность: `{confidence:.1f}%`\n\n"
            f"{desc}"
        )

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await status_msg.edit_text("❌ Не удалось обработать фото.")

async def main():
    print("🚀 Бот запущен (Режим: In-Memory)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())