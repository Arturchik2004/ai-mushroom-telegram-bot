import os
import logging
from openai import AsyncOpenAI # <--- БЕРЕМ АСИНХРОННЫЙ КЛИЕНТ
from dotenv import load_dotenv

load_dotenv()

# Настраиваем АСИНХРОННЫЙ клиент
# Это критически важно: теперь бот не будет зависать, ожидая ответа
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Дефолтная модель (Llama 3.1 - стабильная и бесплатная)
DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
MODEL_NAME = os.getenv("LLM_MODEL", DEFAULT_MODEL)

def load_prompt(filename="prompt.txt"):
    """
    Загружает системный промпт из файла рядом со скриптом.
    """
    try:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"⚠️ Ошибка чтения файла {filename}: {e}. Использую стандартный промпт.")
        return "Ты — миколог. Опиши гриб и скажи, съедобен ли он."

SYSTEM_PROMPT = load_prompt()

async def get_mushroom_info(mushroom_name: str, confidence: float) -> str:
    """
    Генерирует описание гриба через LLM OpenRouter (Асинхронно).
    """
    user_prompt = (
        f"Нейросеть распознала на фото гриб: **{mushroom_name}**.\n"
        f"Уверенность распознавания: {confidence:.1f}%.\n"
        "Дай справку по этому грибу."
    )

    # Пишем в консоль, чтобы ты видел, что процесс идет
    print(f"📡 Отправляю запрос к LLM ({MODEL_NAME}) для гриба {mushroom_name}...")

    try:
        # ВАЖНО: Используем await!
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            extra_headers={
                "HTTP-Referer": "https://github.com/MushroomBot",
                "X-Title": "Mushroom Telegram Bot",
            },
            timeout=20.0 # Если нейронка тупит больше 20 сек, отменяем
        )
        
        print("✅ Ответ от LLM получен!")
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Ошибка LLM: {e}")
        return (
            "**Связь с лесом прервана🥲...**\n"
            "Не могу получить описание от нейросети (таймаут или ошибка). "
            f"Но мой классификатор уверен, что это **{mushroom_name}**. Проверь в гугле!"
        )