from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from services import NoteService

get_notes_route = Router(name="Get notes")


@get_notes_route.message(Command("mynotes"))
async def get_notes(message: Message, state: FSMContext, session: AsyncSession):
    """
    Hndle /mynotes command
    :param message: Telegram message
    :param state: Catching other contexts to clean them up
    :param session: Database session
    """
    await state.clear()
    user_notes = await NoteService.get_user_notes(session, message.from_user.id)
    for note in user_notes:
        await message.answer(
            f"Время напоминаия: {note['date']} {note['time']}\n"
            f"{note['text']}",
            # reply_markup=
        )




