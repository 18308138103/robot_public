import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 从 Railway 环境变量读取 TOKEN
TOKEN = os.getenv("TOKEN")

# 处理消息的函数
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 打印 chat_id（你要的功能）
    print("chat_id:", update.effective_chat.id)

    # 回复一条消息（方便你确认机器人在工作）
    await update.message.reply_text("收到 👍")

def main():
    # 创建应用
    app = ApplicationBuilder().token(TOKEN).build()

    # 添加消息处理器（监听所有文本消息）
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

    # 启动机器人
    print("机器人已启动...")
    app.run_polling()

if __name__ == "__main__":
    main()
