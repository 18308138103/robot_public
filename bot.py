from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import os

TOKEN = os.getenv("8315308209:AAEZdx14nEWTlEmCpr7vKjz0KNDNwcPgdgU")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("我在运行中 👍")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle_msg))

app.run_polling()