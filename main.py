import telebot
import sqlite3
import os
import threading
import time
import shutil
import requests
import json
from datetime import datetime, timedelta

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
TOKEN = '8502077315:AAFsAdWXuo_06YGCjwyAI11JbgCWH8Y3pso'  # Ваш токен

bot = telebot.TeleBot(TOKEN)

# Пароль для доступа
PASSWORD = '0918'

authorized_users = set()

# Создаем необходимые папки
os.makedirs('medicine_photos', exist_ok=True)
os.makedirs('trash_photos', exist_ok=True)
os.makedirs('notes_photos', exist_ok=True)


# ==================== НЕЙРОСЕТЕВЫЕ API ====================

class NeuralNetworkAPI:
    """Класс для работы с нейросетевыми API"""

    @staticmethod
    def get_medicine_info_kandinsky(medicine_name):
        """Получение изображения через Kandinsky API (бесплатно)"""
        try:
            # Kandinsky API (нужна регистрация)
            # Это заглушка, для реальной работы нужно получить API ключ
            api_url = "https://api-key.fusionbrain.ai/"
            # Здесь будет код для генерации изображения
            return None
        except:
            return None

    @staticmethod
    def get_medicine_info_gigachat(medicine_name):
        """Получение информации через GigaChat API"""
        try:
            # GigaChat API требует авторизации
            # Это пример структуры запроса
            url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
            headers = {
                "Authorization": "Bearer YOUR_TOKEN",  # Нужно получить токен
                "Content-Type": "application/json"
            }
            data = {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Дай подробную информацию о лекарстве {medicine_name}: описание, применение, дозировка, побочные эффекты, противопоказания. Ответ структурируй."
                    }
                ]
            }
            # response = requests.post(url, headers=headers, json=data, timeout=10)
            # return response.json()
            return None
        except:
            return None

    @staticmethod
    def get_medicine_info_deepseek(medicine_name):
        """Получение информации через DeepSeek API (бесплатно)"""
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": "Bearer sk-4cda6670c8984a3f9bd8b9e4cf7d58c9",  # Ваш ключ DeepSeek
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Дай подробную информацию о лекарстве '{medicine_name}' на русском языке. Включи: описание, показания к применению, способ применения и дозы, побочные действия, противопоказания. Ответ оформи красиво с эмодзи."
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            print(f"Отправляем запрос к DeepSeek для '{medicine_name}'...")
            response = requests.post(url, headers=headers, json=data, timeout=15)

            print(f"Статус ответа DeepSeek: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
            else:
                print(f"Ошибка DeepSeek: {response.text}")

        except Exception as e:
            print(f"Ошибка DeepSeek API: {e}")
        return None

    @staticmethod
    def get_medicine_info_openrouter(medicine_name):
        """Получение информации через OpenRouter API (бесплатные модели)"""
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer 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",
                # Ваш ключ OpenRouter
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/medicine_bot",
                "X-Title": "Medicine Bot"
            }
            data = {
                "model": "openai/gpt-3.5-turbo",  # Изменил модель на более стабильную
                "messages": [
                    {
                        "role": "user",
                        "content": f"Дай подробную информацию о лекарстве '{medicine_name}' на русском языке. Включи: описание, показания к применению, способ применения и дозы, побочные действия, противопоказания. Ответ оформи красиво с эмодзи."
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            print(f"Отправляем запрос к OpenRouter для '{medicine_name}'...")
            response = requests.post(url, headers=headers, json=data, timeout=20)

            print(f"Статус ответа OpenRouter: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    print(f"Неожиданный формат ответа: {result}")
            else:
                print(f"Текст ошибки OpenRouter: {response.text}")

        except Exception as e:
            print(f"Ошибка OpenRouter API: {e}")
        return None

    @staticmethod
    def get_medicine_info_gemini(medicine_name):
        """Получение информации через Google Gemini API (бесплатно)"""
        try:
            # Нужно получить API ключ на https://aistudio.google.com/
            api_key = "YOUR_GEMINI_API_KEY"  # Замените на ваш ключ Gemini
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

            data = {
                "contents": [{
                    "parts": [{
                        "text": f"Дай подробную информацию о лекарстве '{medicine_name}' на русском языке. Включи: описание, показания к применению, способ применения и дозы, побочные действия, противопоказания. Ответ оформи красиво с эмодзи."
                    }]
                }]
            }

            print(f"Отправляем запрос к Gemini для '{medicine_name}'...")
            response = requests.post(url, json=data, timeout=15)

            print(f"Статус ответа Gemini: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Ошибка Gemini: {response.text}")

        except Exception as e:
            print(f"Ошибка Gemini API: {e}")
        return None

    @staticmethod
    def get_medicine_info_ai21(medicine_name):
        """Получение информации через AI21 API"""
        try:
            # AI21 Labs Jurassic-2 (есть бесплатные токены)
            url = "https://api.ai21.com/studio/v1/j2-ultra/complete"
            headers = {
                "Authorization": "Bearer YOUR_AI21_KEY",
                "Content-Type": "application/json"
            }
            data = {
                "prompt": f"Дай информацию о лекарстве {medicine_name} на русском языке:",
                "maxTokens": 500,
                "temperature": 0.7
            }
            response = requests.post(url, headers=headers, json=data, timeout=10)
            return response.json()
        except:
            return None


# ==================== ЛОКАЛЬНАЯ БАЗА ЛЕКАРСТВ (ЗАПАСНОЙ ВАРИАНТ) ====================
MEDICINE_DATABASE = {
    "парацетамол": {
        "name": "Парацетамол",
        "info": "🔴 **Парацетамол** - жаропонижающее и обезболивающее средство.\n\n"
                "💊 **Применение:** Головная боль, зубная боль, температура.\n"
                "📊 **Дозировка:** Взрослым 500-1000 мг до 4 раз в день.\n"
                "⚠️ **Побочные эффекты:** Редко - аллергия, тошнота.\n"
                "🚫 **Противопоказания:** Болезни печени, алкоголизм."
    },
    "ибупрофен": {
        "name": "Ибупрофен",
        "info": "🔴 **Ибупрофен** - нестероидный противовоспалительный препарат.\n\n"
                "💊 **Применение:** Боль, воспаление, температура.\n"
                "📊 **Дозировка:** 200-400 мг 3-4 раза в день, после еды.\n"
                "⚠️ **Побочные эффекты:** Тошнота, изжога.\n"
                "🚫 **Противопоказания:** Язва желудка, беременность."
    },
    "амоксициллин": {
        "name": "Амоксициллин",
        "info": "🔴 **Амоксициллин** - антибиотик широкого спектра.\n\n"
                "💊 **Применение:** Инфекции дыхательных путей, ЛОР-органов.\n"
                "📊 **Дозировка:** Назначается врачом, обычно 500 мг 3 раза в день.\n"
                "⚠️ **Побочные эффекты:** Аллергия, диарея.\n"
                "🚫 **Противопоказания:** Аллергия на пенициллины."
    }
}


def get_medicine_from_local_db(medicine_name):
    """Поиск в локальной базе данных"""
    medicine_lower = medicine_name.lower().strip()

    # Точное совпадение
    if medicine_lower in MEDICINE_DATABASE:
        return MEDICINE_DATABASE[medicine_lower]['info']

    # Частичное совпадение
    for key, value in MEDICINE_DATABASE.items():
        if key in medicine_lower or medicine_lower in key:
            return value['info']

    return None


def get_medicine_from_neural_network(medicine_name):
    """Получение информации о лекарстве через нейросеть"""

    # Пробуем разные нейросети по очереди
    neural_networks = [
        ("OpenRouter", NeuralNetworkAPI.get_medicine_info_openrouter),
        ("DeepSeek", NeuralNetworkAPI.get_medicine_info_deepseek),
        # ("Gemini", NeuralNetworkAPI.get_medicine_info_gemini),  # Раскомментируйте когда получите ключ Gemini
    ]

    for name, func in neural_networks:
        try:
            print(f"🤔 Пробуем {name}...")
            result = func(medicine_name)
            if result:
                print(f"✅ Получили ответ от {name}")
                return result
            else:
                print(f"❌ {name} вернул пустой результат")
        except Exception as e:
            print(f"❌ Ошибка {name}: {e}")
            continue

    # Если нейросети не сработали, используем локальную базу
    print("⚠️ Нейросети не сработали, используем локальную базу")
    local_info = get_medicine_from_local_db(medicine_name)
    if local_info:
        return local_info + "\n\n🤖 Информация из локальной базы данных."

    # Если ничего не найдено
    return None


# ==================== БАЗА ДАННЫХ ====================
conn = sqlite3.connect('medicines.db', check_same_thread=False)
c = conn.cursor()

# Создаем основную таблицу для лекарств
c.execute('DROP TABLE IF EXISTS medicines')
c.execute('''CREATE TABLE medicines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    name TEXT NOT NULL,
    description TEXT,
    manufactured_date TEXT,
    expiry_date TEXT,
    photo_path TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

# Создаем таблицу для корзины
c.execute('''CREATE TABLE IF NOT EXISTS trash(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_id INTEGER,
    user_id INTEGER NOT NULL,
    username TEXT,
    deleted_by_id INTEGER,
    deleted_by_username TEXT,
    name TEXT NOT NULL,
    description TEXT,
    manufactured_date TEXT,
    expiry_date TEXT,
    photo_path TEXT,
    deleted_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

# Создаем таблицу для приватных заметок
c.execute('''CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    title TEXT NOT NULL,
    content TEXT,
    photo_path TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

# Создаем таблицу для корзины заметок
c.execute('''CREATE TABLE IF NOT EXISTS notes_trash(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_id INTEGER,
    user_id INTEGER NOT NULL,
    username TEXT,
    deleted_by_id INTEGER,
    deleted_by_username TEXT,
    title TEXT NOT NULL,
    content TEXT,
    photo_path TEXT,
    deleted_at TEXT DEFAULT CURRENT_TIMESTAMP)''')

conn.commit()

print("✅ Таблицы созданы")


# ==================== КЛАВИАТУРЫ ====================
def kb():
    """Главное меню"""
    k = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    k.row('➕ Добавить', '🔍 Поиск')
    k.row('📋 Список', '⚠️ Срок годности')
    k.row('🗑 Корзина', '👥 Мои лекарства')
    k.row('📝 Заметки', '❌ Удалить')
    k.row('🤖 Нейросеть')
    return k


def kb_with_cancel():
    """Клавиатура с кнопкой отмены"""
    k = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    k.row('❌ Отмена')
    return k


def notes_kb():
    """Клавиатура для заметок"""
    k = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    k.row('➕ Новая заметка', '📋 Мои заметки')
    k.row('🔍 Поиск заметок', '🗑 Корзина заметок')
    k.row('⬅️ Назад в меню')
    return k


def auth_kb():
    """Клавиатура авторизации"""
    k = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    k.row('🔑 Ввести пароль')
    return k


def neural_search_kb(medicine_name):
    """Клавиатура для результатов поиска через нейросеть"""
    k = telebot.types.InlineKeyboardMarkup(row_width=2)
    k.add(
        telebot.types.InlineKeyboardButton("➕ Добавить в список", callback_data=f"add_from_neural_{medicine_name}"),
        telebot.types.InlineKeyboardButton("🔄 Новый запрос", callback_data="new_neural_search")
    )
    return k


states = {}
note_states = {}


# ==================== АВТОРИЗАЦИЯ ====================
def is_authorized(user_id):
    return user_id in authorized_users


def auth_required(func):
    def wrapper(message):
        if is_authorized(message.from_user.id):
            return func(message)
        else:
            bot.send_message(message.chat.id,
                             "🔒 <b>Доступ запрещен!</b>\nВведите пароль для входа:",
                             reply_markup=auth_kb(), parse_mode='HTML')

    return wrapper


@bot.message_handler(commands=['start'])
def start(m):
    if is_authorized(m.from_user.id):
        bot.send_message(m.chat.id,
                         "👋 <b>Бот для лекарств и заметок</b>\n\n"
                         "<b>💊 РАЗДЕЛ ЛЕКАРСТВ:</b>\n"
                         "➕ Добавить - новое лекарство\n"
                         "🔍 Поиск - найти по названию\n"
                         "📋 Список - все лекарства\n"
                         "⚠️ Срок годности - проверка\n"
                         "👥 Мои лекарства - только ваши\n"
                         "❌ Удалить - удалить ЛЮБОЕ лекарство\n"
                         "🗑 Корзина - просмотреть и восстановить\n"
                         "🤖 Нейросеть - найти информацию через нейросеть\n\n"
                         "<b>📝 РАЗДЕЛ ЗАМЕТОК:</b>\n"
                         "📝 Заметки - личные заметки (видите только вы)\n\n"
                         "⚠️ ВНИМАНИЕ: удаленные лекарства можно восстановить из корзины!\n"
                         "📝 Заметки видны только вам и не удаляются другими пользователями",
                         reply_markup=kb(), parse_mode='HTML')
    else:
        bot.send_message(m.chat.id,
                         "🔒 <b>Для доступа к боту введите пароль:</b>",
                         reply_markup=auth_kb(), parse_mode='HTML')


@bot.message_handler(func=lambda m: m.text == '🔑 Ввести пароль')
def handle_password_button(m):
    if is_authorized(m.from_user.id):
        bot.send_message(m.chat.id, "✅ <b>Вы уже авторизованы!</b>", reply_markup=kb(), parse_mode='HTML')
        return
    msg = bot.send_message(m.chat.id, "Введите пароль:", reply_markup=kb_with_cancel())
    bot.register_next_step_handler(msg, check_password)


@bot.message_handler(func=lambda m: not is_authorized(m.from_user.id) and m.text != '🔑 Ввести пароль')
def handle_unauthorized(m):
    if m.text == '❌ Отмена':
        bot.send_message(m.chat.id, "❌ <b>Действие отменено</b>", reply_markup=auth_kb(), parse_mode='HTML')
        return
    if m.text.strip() == PASSWORD:
        authorized_users.add(m.from_user.id)
        bot.send_message(m.chat.id,
                         "✅ <b>Пароль верный!</b> Добро пожаловать в бот.",
                         reply_markup=kb(), parse_mode='HTML')
        start(m)
    else:
        bot.send_message(m.chat.id,
                         "❌ <b>Неверный пароль!</b> Нажмите кнопку '🔑 Ввести пароль' для повторной попытки.",
                         reply_markup=auth_kb(), parse_mode='HTML')


def check_password(m):
    if m.text == '❌ Отмена':
        bot.send_message(m.chat.id, "❌ <b>Действие отменено</b>", reply_markup=auth_kb(), parse_mode='HTML')
        return
    if m.text.strip() == PASSWORD:
        authorized_users.add(m.from_user.id)
        bot.send_message(m.chat.id,
                         "✅ <b>Пароль верный!</b> Добро пожаловать в бот.",
                         reply_markup=kb(), parse_mode='HTML')
        start(m)
    else:
        bot.send_message(m.chat.id,
                         "❌ <b>Неверный пароль!</b> Попробуйте еще раз.",
                         reply_markup=kb_with_cancel(), parse_mode='HTML')
        bot.register_next_step_handler_by_chat_id(m.chat.id, check_password)


# ==================== ПОИСК ЧЕРЕЗ НЕЙРОСЕТЬ ====================
@bot.message_handler(func=lambda m: m.text == '🤖 Нейросеть')
@auth_required
def neural_search_start(m):
    msg = bot.send_message(m.chat.id,
                           "🤖 <b>Введите название лекарства для поиска через нейросеть:</b>\n\n"
                           "Я использую искусственный интеллект, чтобы найти подробную информацию:\n"
                           "• Описание препарата\n"
                           "• Показания к применению\n"
                           "• Способ применения и дозы\n"
                           "• Побочные эффекты\n"
                           "• Противопоказания\n\n"
                           "Например: парацетамол, ибупрофен, амоксициллин",
                           reply_markup=kb_with_cancel(), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_neural_search)


def process_neural_search(m):
    if m.text == '❌ Отмена':
        bot.send_message(m.chat.id, "❌ <b>Поиск отменен</b>", reply_markup=kb(), parse_mode='HTML')
        return

    medicine_name = m.text.strip()
    if not medicine_name:
        msg = bot.send_message(m.chat.id, "❌ <b>Введите название для поиска</b>",
                               reply_markup=kb_with_cancel(), parse_mode='HTML')
        bot.register_next_step_handler(msg, process_neural_search)
        return

    # Отправляем сообщение о начале поиска
    wait_msg = bot.send_message(m.chat.id,
                                f"🤖 <b>Нейросеть ищет информацию о '{medicine_name}'...</b>\nЭто может занять несколько секунд.",
                                parse_mode='HTML')

    # Получаем информацию через нейросеть
    info = get_medicine_from_neural_network(medicine_name)

    # Удаляем сообщение о поиске
    bot.delete_message(m.chat.id, wait_msg.message_id)

    if info:
        response = f"🤖 <b>ИНФОРМАЦИЯ О ПРЕПАРАТЕ: {medicine_name.upper()}</b>\n\n{info}"
        bot.send_message(m.chat.id, response,
                         reply_markup=neural_search_kb(medicine_name),
                         parse_mode='HTML')
    else:
        response = f"❌ <b>Информация о препарате '{medicine_name}' не найдена.</b>\n\n"
        response += "Возможные причины:\n"
        response += "• Редкое или новое лекарство\n"
        response += "• Ошибка в названии\n"
        response += "• Проблемы с подключением к нейросети\n\n"
        response += "Попробуйте:\n"
        response += "• Проверить правильность написания\n"
        response += "• Использовать торговое название\n"
        response += "• Поискать позже"

        bot.send_message(m.chat.id, response,
                         reply_markup=neural_search_kb(medicine_name),
                         parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_from_neural_'))
def handle_add_from_neural(call):
    medicine_name = call.data.replace('add_from_neural_', '')

    # Инициализируем состояние для добавления
    uid = call.from_user.id
    username = call.from_user.username or call.from_user.first_name or f"id{uid}"

    states[uid] = {
        'user_id': uid,
        'username': username,
        'name': medicine_name
    }

    # Убираем клавиатуру
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    # Начинаем добавление
    msg = bot.send_message(call.message.chat.id,
                           f"📝 <b>Добавление лекарства '{medicine_name}'</b>\n\n"
                           "📝 <b>Описание</b> (или '-'):",
                           reply_markup=kb_with_cancel(), parse_mode='HTML')
    bot.register_next_step_handler(msg, lambda msg: state(msg, 'description'))


@bot.callback_query_handler(func=lambda call: call.data == 'new_neural_search')
def handle_new_neural_search(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    neural_search_start(call.message)


# ==================== РАЗДЕЛ ЗАМЕТОК ====================
@bot.message_handler(func=lambda m: m.text == '📝 Заметки')
@auth_required
def notes_menu(m):
    bot.send_message(m.chat.id,
                     "<b>📝 РАЗДЕЛ ЗАМЕТОК</b>\n\n"
                     "➕ Новая заметка - создать заметку\n"
                     "📋 Мои заметки - просмотреть все\n"
                     "🔍 Поиск заметок - найти по названию\n"
                     "🗑 Корзина заметок - восстановить удаленные\n"
                     "⬅️ Назад в меню - вернуться в главное меню",
                     reply_markup=notes_kb(), parse_mode='HTML')


# Здесь должен быть весь остальной код из вашего оригинального файла:
# - Функции для заметок (new_note, process_note_title, process_note_content, process_note_photo, show_note_card, my_notes, search_notes_start, search_notes, handle_delete_note, handle_restore_note, show_notes_trash, back_to_main)
# - Функции для лекарств (add, state, add_photo, search_s, search, lst, my_meds, exp_chk, show_trash, handle_restore, del_s, delete, card)
# - Функции уведомлений (send_daily_notifications, start_notification_thread)

# ==================== ЗАПУСК ====================
if __name__ == '__main__':
    # Удаляем вебхук перед запуском
    bot.remove_webhook()

    print("✅ Бот запущен (требуется пароль)")
    print(f"🔑 Пароль: {PASSWORD}")
    print("🗑 Корзина с кнопками восстановления")
    print("📝 Добавлены личные заметки для каждого пользователя")
    print("🤖 Добавлен поиск через НЕЙРОСЕТЬ:")
    print("   • OpenRouter API (ключ вставлен)")
    print("   • DeepSeek API (ключ вставлен)")
    print("   • Gemini API (нужен ключ)")
    print("   • Локальная база как запасной вариант")
    print("❌ Кнопка отмены добавлена во все действия")
    print("✨ Жирный шрифт в тексте сообщений")

    # Запускаем уведомления (если они есть в вашем коде)
    # start_notification_thread()

    # Запускаем бота
    bot.infinity_polling()


    #sk-4cda6670c8984a3f9bd8b9e4cf7d58c9