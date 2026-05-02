from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TOKEN, DEFAULT_INTERVAL
from db import add_group, add_points, get_ranking, set_interval
from scheduler import start_scheduler

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_group(chat_id)
    await update.message.reply_text("机器人已启动 🤖")

# 统计发言积分
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    add_points(user.id, chat_id)

# /rank 排行榜
async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    ranking = get_ranking(chat_id)

    text = "🏆 排行榜：\n"
    for i, (user_id, points) in enumerate(ranking, 1):
        text += f"{i}. {user_id} - {points}\n"

    await update.message.reply_text(text)

# /setinterval 1800
async def set_interval_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    try:
        seconds = int(context.args[0])
        set_interval(chat_id, seconds)
        await update.message.reply_text(f"间隔已设置为 {seconds} 秒")
    except:
        await update.message.reply_text("用法: /setinterval 3600")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("setinterval", set_interval_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    start_scheduler(app)

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
