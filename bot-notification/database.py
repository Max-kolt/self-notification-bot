import asyncpg
from config import DB_URL
from datetime import datetime
from asyncpg import Record


async def get_notes_at_time(time: datetime) -> list[Record]:
    """
    Select reminder notes
    :param time: current time
    :return: list of notes
    """
    connection = await asyncpg.connect(DB_URL)
    notes_records: list[Record] = await connection.fetch("""
        select U.telegram_id, N.text 
        from notes as N join users as U on U.id = N.user_id
        where reminder_time = $1;
    """, time)
    return notes_records

