from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import get_groups
import random

scheduler = AsyncIOScheduler()

MESSAGES = [
    "今天也要加油 💪",
    "开始摸鱼！！ 😏",
    "喝水了吗？🥤",
    "起来活动一下 🏃",
]

def start_scheduler(app):

    async def send_message(chat_id):
        msg = random.choice(MESSAGES)
        await app.bot.send_message(chat_id=chat_id, text=msg)

    async def job():
        groups = get_groups()
        for chat_id, _ in groups:
            await send_message(chat_id)

    scheduler.add_job(job, "interval", seconds=3600)
    scheduler.start()
