from telethon import TelegramClient

from config import API_HASH, API_ID, TELEGRAM_TOKEN
import asyncio
from schedule_decorator import periodic
from database import get_notes_at_time
from datetime import datetime, timedelta
from loguru import logger


async def send_notification(telegram_id: int, text: str, reminder_time: datetime):
    """
    Send notification to user
    :param telegram_id: id of user chat
    :param text: notification text
    :param reminder_time: time to start event
    """

    client = TelegramClient("notification_bot", api_hash=API_HASH, api_id=API_ID)
    await client.start(bot_token=TELEGRAM_TOKEN)
    await client.send_message(telegram_id, f"{'{:~^29}'.format('Событие')}\n{reminder_time}\n<b>{text}</b>", parse_mode="HTML")
    await client.disconnect()
    logger.info(f"Send notification to {telegram_id}")


@periodic(minutes=1)
async def run_notifications():
    """
    Runs a notification search
    """
    time_now = datetime.now()
    notes = await get_notes_at_time(
        datetime(
            year=time_now.year, month=time_now.month, day=time_now.day, hour=time_now.hour, minute=time_now.minute
        ) + timedelta(minutes=10)
    )
    logger.debug(f"Select {len(notes)} notifications")

    for note in notes:
        telegram_id: int = note.get("telegram_id")
        note_text: str = note.get("text")
        note_reminder_time: datetime = note.get("reminder_time")
        await send_notification(telegram_id, note_text, note_reminder_time)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        logger.info("Notification service is running")
        loop.create_task(run_notifications())
        loop.run_forever()
    finally:
        logger.info('Shutting down')
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.stop()
        loop.close()


