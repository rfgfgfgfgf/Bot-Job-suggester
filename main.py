import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

def get_samples(interest_area):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT suggestion, description FROM career_paths WHERE interest_area = ?", (interest_area,))
    results = cursor.fetchall()
    conn.close()
    return results

# код для создание одной команды старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(" Искусство", callback_data='art')],
        [InlineKeyboardButton(" Технологии", callback_data='techbology')],
        [InlineKeyboardButton(" Путешествия", callback_data='travel')],
        [InlineKeyboardButton(" Финансы", callback_data='finances')],
        [InlineKeyboardButton(" Маркетинг", callback_data='marketing')],
        [InlineKeyboardButton(" Спорт", callback_data='sport')],
        [InlineKeyboardButton(" Гейминг", callback_data='gaming')],
        [InlineKeyboardButton(" Медиа/социальные сети", callback_data=' media')],
        [InlineKeyboardButton(" Письмо", callback_data='writing')],
        [InlineKeyboardButton(" Закон", callback_data='law')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Что тебе интересно?", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    interest = query.data
    suggestions = get_samples(interest)

    if suggestions:
        response = "\n\n".join([f" *{s[0]}*\n_{s[1]}_" for s in suggestions])
        await query.edit_message_text(text=response, parse_mode='Markdown')
    else:
        await query.edit_message_text(text="Пока нет рекомендаций для этой области. Попробуй позже!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, выбери интерес через кнопки ниже или введи /start для начала.")


def main():
    app = ApplicationBuilder().token("").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()