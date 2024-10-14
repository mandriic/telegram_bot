from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
from config import BOT_CONFIG
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data='1')],
        [InlineKeyboardButton("Кнопка 2", callback_data='2')],
        [InlineKeyboardButton("Кнопка 3", callback_data='3')],
        [InlineKeyboardButton("Кнопка 4", callback_data='4'), InlineKeyboardButton("Кнопка 5", callback_data='5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Оберіть дію:', reply_markup=reply_markup)

    
async def myGen(update: Update, context) -> None:
    await update.message.reply_text(update.message.text)

# Функція для обробки текстових повідомлень
async def echo(update: Update, context) -> None:
    await update.message.reply_text(update.message.text)

async def error(update: Update, context) -> None:
    print(f'Помилка {context.error}')

def main() -> None:

    token = BOT_CONFIG["telegramApiKey"]

    # Створюємо об’єкт Application (заміняє Updater)
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gen", myGen))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
