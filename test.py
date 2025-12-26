import os
import time
from openai import OpenAI, NotFoundError, AuthenticationError
from dotenv import load_dotenv

# Загружаем ключ
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ ОШИБКА: Нет ключа OPENROUTER_API_KEY в файле .env")
    exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Список бесплатных моделей для проверки
MODELS_TO_TEST = [
    "meta-llama/llama-3.1-8b-instruct:free",       # Llama 3.1 (Обычно топ)
    "google/gemini-2.0-flash-lite-preview-02-05:free", # Google (Быстрый, но в РФ недоступен😒)
    "mistralai/mistral-7b-instruct:free",          # Mistral (Европейская классика)
    "microsoft/phi-3-mini-128k-instruct:free",     # Microsoft (Маленькая, но удалая)
    "qwen/qwen-2-7b-instruct:free",                # Qwen (Китай, топ за свои деньги)
    "deepseek/deepseek-r1:free",                   # DeepSeek (Проверим, жив ли)
    "huggingfaceh4/zephyr-7b-beta:free"            # Zephyr
]

print(f"🔑 Ключ: {api_key[:10]}... (скрыт)")
print(f"📡 Начинаем проверку {len(MODELS_TO_TEST)} моделей...\n")
print("-" * 60)
print(f"{'МОДЕЛЬ':<50} | {'СТАТУС':<10}")
print("-" * 60)

working_models = []

for model in MODELS_TO_TEST:
    try:
        # Пытаемся отправить короткий запрос
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            extra_headers={"HTTP-Referer": "https://test.com", "X-Title": "Test"},
            timeout=10 # Ждем не больше 10 секунд
        )
        
        # Если дошли сюда - успех
        print(f"{model:<50} | ✅ ОК")
        working_models.append(model)
        
    except NotFoundError:
        print(f"{model:<50} | ❌ 404 (Нет)")
    except AuthenticationError:
        print(f"{model:<50} | ❌ Ошибка ключа")
        break # Если ключ неверный, дальше нет смысла
    except Exception as e:
        # Сокращаем текст ошибки, если он длинный
        err_msg = str(e).split(' - ')[0][:20]
        print(f"{model:<50} | ⚠️ Ошибка ({err_msg})")
    
    # Пауза, чтобы не спамить запросами (Rate Limit)
    time.sleep(1)

print("-" * 60)
if working_models:
    print("\n🎉 РЕКОМЕНДУЮ вставить в .env одну из этих:")
    for m in working_models:
        print(f"LLM_MODEL={m}")
else:
    print("\n💀 Ни одна модель не ответила. Проверь баланс/ключ или попробуй позже.")