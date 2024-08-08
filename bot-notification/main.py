from telethon import TelegramClient
from config import API_HASH, API_ID, TELEGRAM_TOKEN
import asyncio
from schedule_decorator import periodic
from database import get_notes_at_time
from datetime import datetime
from loguru import logger


client = TelegramClient("notification_bot", api_hash=API_HASH, api_id=API_ID).start(bot_token=TELEGRAM_TOKEN)


async def send_notification(telegram_id: int, text: str):
    """
    Send notification to user
    :param telegram_id: id of user chat
    :param text: notification text
    """
    await client.send_message(telegram_id, f"{'{:*^30}'.format('Notification')}\n{text}")
    logger.info(f"Send notification to {telegram_id}")


@periodic(minutes=1)
async def run_notifications():
    """
    Runs a notification search every minute
    """
    notes = await get_notes_at_time(datetime.now())
    logger.debug(f"Select {len(notes)} notifications")

    for note in notes:
        telegram_id: int = note.get("telegram_id")
        note_text: str = note.get("text")
        await send_notification(telegram_id, note_text)


if __name__ == '__main__':
    logger.info("Notification service is running")
    asyncio.run(run_notifications())
