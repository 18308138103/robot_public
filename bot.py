import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

# 用集合存所有群（自动去重）
group_ids = set()

# 收到消息时记录群ID
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type in ["group", "supergroup"]:
        group_ids.add(chat.id)
        print("已记录群ID:", chat.id)

    await update.message.reply_text("收到 👍")

# 定时发送（给所有群）
async def send_message(context: ContextTypes.DEFAULT_TYPE):
    if not group_ids:
        print("还没有任何群ID")
        return

    for gid in group_ids:
        try:
            await context.bot.send_message(
                chat_id=gid,
                text="⏰ 每个群每小时自动发送一次"
            )
        except Exception as e:
            print(f"发送失败 {gid}:", e)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

    # ⏰ 定时任务（先用30秒测试）
    app.job_queue.run_repeating(send_message, interval=30, first=10)

    print("机器人已启动...")
    app.run_polling()

if __name__ == "__main__":
    main()
