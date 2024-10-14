from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
from config import BOT_CONFIG
from bdpsql import db_connection, create_table
import logging
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data='1')],
        [InlineKeyboardButton("Кнопка 2", callback_data='2')],
        [InlineKeyboardButton("Кнопка 3", callback_data='3')],
        [InlineKeyboardButton("Кнопка 4", callback_data='4'), InlineKeyboardButton("Кнопка 5", callback_data='5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Оберіть дію:', reply_markup=reply_markup)

async def myGen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

# Функція для створення нагадування
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.debug(f"Received update: {update}")
    logging.debug(f"Received context: {context}") 
    # if len(context.args) < 2:
    #     await update.message.reply_text("Використайте формат: /remind <текст> <час (YYYY-MM-DD HH:MM:SS)>")
    #     return
    
    # reminder_text = " ".join(context.args[:-1])
    # reminder_time = context.args[-1]  # Потрібно вказати формат дати

    # # Конвертуємо час у формат datetime
    # try:
    #     reminder_time = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")
    # except ValueError:
    #     await update.message.reply_text("Неправильний формат часу. Використайте формат: YYYY-MM-DD HH:MM:SS")
    #     return

    # conn = db_connection()
    # cursor = conn.cursor()
    # cursor.execute('INSERT INTO reminders (user_id, reminder_text, reminder_time) VALUES (%s, %s, %s)',
    #                (update.effective_user.id, reminder_text, reminder_time))
    # conn.commit()
    # conn.close()

    # await update.message.reply_text(f"Нагадування встановлено: {reminder_text} о {reminder_time}")

# Функція для перегляду нагадувань
async def view_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT reminder_text, reminder_time FROM reminders WHERE user_id = %s', (update.effective_user.id,))
    reminders = cursor.fetchall()
    conn.close()

    if not reminders:
        await update.message.reply_text("У вас немає нагадувань.")
        return
    
    response = "Ваші нагадування:\n"
    for reminder in reminders:
        response += f"- {reminder[0]} о {reminder[1]}\n"
    
    await update.message.reply_text(response)

# Функція для обробки текстових повідомлень
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Помилка {context.error}')

def startBot() -> None:
    create_table()  # Створюємо таблицю при запуску бота

    token = BOT_CONFIG["telegramApiToken"] # Вставте свій токен

    # Створюємо об’єкт Application
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gen", myGen))
    application.add_handler(CommandHandler("remind", set_reminder))  # Додаємо команду для встановлення нагадування
    application.add_handler(CommandHandler("view", view_reminders))    # Додаємо команду для перегляду нагадувань
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    application.run_polling()

startBot()
