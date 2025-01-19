import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Функция для взаимодействия с GigaChat API
def get_gigachat_response(message: str) -> str:
    url = "YOUR_GIGACHAT_API_ENDPOINT"  # Замените на реальный URL
    headers = {
        "Authorization": "Bearer YOUR_GIGACHAT_API_KEY",  # Замените на ваш API ключ
        "Content-Type": "application/json"
    }
    data = {
        "message": message  # Структура данных может отличаться в зависимости от API
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("response", "Извините, не удалось получить ответ.")
    else:
        logger.error(f"Ошибка при обращении к GigaChat API: {response.status_code} - {response.text}")
        return "Извините, произошла ошибка при обработке вашего запроса."

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот для взаимодействия с GigaChat. Просто напишите мне сообщение!')

# Обработка текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"Получено сообщение: {user_message} от {update.message.from_user.username}")

    # Получаем ответ от GigaChat
    response = get_gigachat_response(user_message)
    
    # Отправляем ответ обратно пользователю или в группу
    update.message.reply_text(response)

# Основная функция
def main() -> None:
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Замените на ваш токен

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
