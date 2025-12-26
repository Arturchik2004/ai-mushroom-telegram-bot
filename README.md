# Mushroom AI Classifier Bot
## **Индивидуальный проект по дисциплине ТИПиС**

> **Студент:** Марганов А. Г.

> **Группа:** 3392


# 📂 Структура проекта   



 [ai-mushroom-telegram-bot](https://github.com/Arturchik2004/ai-mushroom-telegram-bot)    
├──  [bot](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/tree/main/bot) - *Логика Telegram бота*   
│   └──  [main.py](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/bot/main.py) - *Точка входа*  
├──  [model](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/tree/main/model) - *Папка с моделью и её работой*      
│   ├──  [inference.py](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/model/inference.py) - *Блок кода для работы с обученной моделью*  
│   ├──  [mushroom_model.pth](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/model/mushroom_model.pth) - *Обученная модель*  
│   └──  [config.json](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/model/config.json) - *Список классов*  
├──  [services](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/tree/main/services) - *Папка для работы с LLM*   
│   ├──  [llm.py](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/services/llm.py) - *Инициализация LLM*  
│   └──  [prompt.txt](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/services/prompt.txt) - *Промпт*  
├──  [notebooks](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/tree/main/notebooks)  
│   └──  [train_model.ipynb](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/notebooks/train_model.ipynb) - *Блокнот с обучением*  
├──  [requirements.txt](https://github.com/Arturchik2004/ai-mushroom-telegram-bot/blob/main/requirements.txt)  
└──  .env  - *здесь хранятся ключи от Openrouter, токен бота и наименование используемой LLM* 
-------------------

# Описание проекта
*Телеграм-бот для распознавания родов грибов по фотографии. Использует гибридный подход: сверточная нейросеть (EfficientNet) определяет визуальный класс, а языковая модель (LLM) генерирует подробное описание, рецепты и предупреждения.*


# Датасет
Для обучения использовался открытый набор данных с платформы Kaggle:  
[Mushroom Classification - Common Genus Images](https://www.kaggle.com/datasets/maysee/mushrooms-classification-common-genuss-images)

**Описание дата сета**

Он содержит 9 папок с изображениями распространенных родов грибов Северной Европы. Каждая папка содержит от 300 до 1500 отобранных изображений грибов разных родов. Где каждый отдельный класс - это название папки.


# Функционал

### Распознавание
Классификация 9 основных родов грибов ("Шампиньон", "Мухомор", "Белый гриб", "Паутинник", "Энтолома", "Гигроцибе", "Груздь", "Сыроежка", "Масленок")

### Интеллект
- **Компьютерное зрение:** Определяет вид гриба и уверенность в %.
- **LLM:** Пишет описание (съедобность, где растет, как готовить).


# Установка и запуск

### 1. Клонируйте репозиторий
```
git clone https://github.com/Arturchik2004/ai-mushroom-telegram-bot.git
cd ai-mushroom-telegram-bot
```
### 2. Создайте виртуальное окружение

```
python -m venv venv
venv\Scripts\activate
```
### 3. Установка библиотек
```
pip install -r requirements.txt
```

### 4. Настройте .env и запустите бота 
 - **.env**   
```
BOT_TOKEN=токен_бота
OPENROUTER_API_KEY=ключ_от_openrouter
LLM_MODEL=mistralai/mistral-7b-instruct:free
```
- **Запуск**   
```
python bot/main.py
```



