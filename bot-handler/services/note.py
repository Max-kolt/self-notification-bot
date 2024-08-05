from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import Sequence
from pydantic import BaseModel
from datetime import datetime
from loguru import logger
from datetime import datetime

from database import Note, User
from exceptions import Unregistered


class NoteSchema(BaseModel):
    telegram_id: int
    text: str
    date: str
    time: str


class NoteService:

    @staticmethod
    async def create_new_note(session: AsyncSession, note_data: NoteSchema) -> Note:
        """
        Create new note for current user
        :param session: Databaase session
        :param note_data: Note inforamtion
        :return: NoteSchema
        """

        user_id = await session.scalar(select(User.id).where(User.telegram_id == note_data.telegram_id))
        # if not user_id:
        #     raise Unregistered(telegram_id=note_data.telegram_id)

        new_note = Note(
            text=note_data.text,
            reminder_time=datetime.strptime(note_data.time+" "+note_data.date, "%H:%M %d/%m/%Y"),
            user_id=user_id
        )
        session.add(new_note)
        await session.commit()
        return new_note

    @staticmethod
    async def get_user_notes(session: AsyncSession, telegram_id: int) -> list[dict]:
        """
        Fetch notes for current user
        :param session: Database session
        :param telegram_id: Telegram user id
        :return: list of Notes
        """
        user_id: int = await session.scalar(select(User.id).where(User.telegram_id == telegram_id))

        query = select(Note).where(Note.user_id == user_id)
        result = await session.scalars(query)

        user_notes = [
            NoteSchema(
                telegram_id=telegram_id,
                text=row.text,
                date=datetime.strptime(str(row.reminder_time), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y"),
                time=datetime.strptime(str(row.reminder_time), "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            ).model_dump(exclude={"telegram_id"})
            for row in result
        ]

        return user_notes

