import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
GROUP_ID = -1003745769770  # 你的群ID

# 普通消息处理（可留可删）
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("chat_id:", update.effective_chat.id)
    await update.message.reply_text("收到 👍")

# 定时发送函数
async def send_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=GROUP_ID,
        text="⏰ 我是panda pan的机器人儿，每小时自动发送一次消息"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # 监听消息
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

    # ⏰ 每3600秒（1小时）执行一次
    app.job_queue.run_repeating(
        send_message,
        interval=300,
        first=10         # 启动后10秒先发一次（方便测试）
    )

    print("机器人已启动...")
    app.run_polling()

if __name__ == "__main__":
    main()
