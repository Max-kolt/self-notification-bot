from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy import Sequence
from pydantic import BaseModel
from datetime import datetime
from loguru import logger
from datetime import datetime

from database import Note, User


class NoteSchema(BaseModel):
    id: int | None
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
            reminder_time=datetime.strptime(note_data.time+" "+note_data.date, "%H:%M %d-%m-%Y"),
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

        query = select(Note).where(Note.user_id == user_id).order_by(Note.reminder_time)
        result = await session.scalars(query)

        user_notes = [
            NoteSchema(
                id=row.id,
                telegram_id=telegram_id,
                text=row.text,
                date=datetime.strptime(str(row.reminder_time), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y"),
                time=datetime.strptime(str(row.reminder_time), "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            ).model_dump(exclude={"telegram_id"})
            for row in result
        ]

        return user_notes

    @staticmethod
    async def delete_note(session: AsyncSession, note_id: int) -> bool:
        """
        Deleting note
        :param session: database session
        :param note_id: id of note
        """
        note_to_delete = await session.scalar(select(Note).where(Note.id == note_id))
        if not note_to_delete:
            raise ModuleNotFoundError()

        await session.delete(note_to_delete)
        await session.commit()
        logger.debug(f"{note_id} note is deleted")
        return True



