from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from states import AddNote
from services import NoteService, NoteSchema


add_notes_router = Router(name="Add notes")


@add_notes_router.message(Command("addnote"))
async def start_new_note(message: Message, state: FSMContext):
    """
    Handle /addnote command
    :param message: Telegram message
    :param state: Context
    """
    await state.clear()
    await state.set_state(AddNote.text)
    await state.update_data(telegram_id=message.from_user.id)
    await message.answer("Какое событие вы хотите записать?")


@add_notes_router.message(AddNote.text, F.text.as_("text"))
async def process_text(message: Message, state: FSMContext, text: str):
    """
    Handle notes text
    :param message: Telegram message
    :param state: Context during add new note
    :param text: Result note text
    """
    await state.update_data(text=text)
    await state.set_state(AddNote.date)

    await message.answer(f"Теперь укажите дату события.")


@add_notes_router.message(
    AddNote.date,
    F.text.regexp(r"(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[1,2])-(19|20)\d{2}"),  # Simple date validation
    F.text.as_("date")
)
async def process_date(message: Message, state: FSMContext, date: str):
    """
    Handle VALID format of date
    :param message: Telegram message
    :param state: Context during add new note
    :param date: Result date of reminder
    """
    await state.update_data(date=date)
    await state.set_state(AddNote.time)

    await message.answer("Укажите время события, за 10 минут до начала пришлем уведомление.")


@add_notes_router.message(
    AddNote.time,
    F.text.regexp(r"^[0-2][0-9]:[0-5][0-9]$"),  # Simple time validation
    F.text.as_('time')
)
async def process_time(message: Message, state: FSMContext, session: AsyncSession, time: str):
    """
    Handle VALID format of time
    :param message: Telegram message
    :param state: Context during add new note
    :param session: Database session
    :param time: Result time of reminder
    """
    await state.update_data(time=time)
    new_note = NoteSchema(id=None, **(await state.get_data()))
    # Saving note
    saved_note = await NoteService.create_new_note(session, new_note)

    await message.answer(f"Запись сохранена 📝\n{saved_note.reminder_time}\n{saved_note.text}")

    await state.clear()
    logger.info(f"User {message.from_user.username} create new note")


@add_notes_router.message(AddNote.date)
async def invalid_date(message: Message):
    """
    Handle INVALID date format
    :param message: Telegram message
    """
    await message.answer("Неверный формат даты.\nНеобходимо ввести дату похоже на пример: 21-11-2024")


@add_notes_router.message(AddNote.time)
async def invalid_date(message: Message):
    """
    Handle INVALID time format
    :param message: Telegram message
    """
    await message.answer("Неверный формат времени.\nНеобходимо ввести время похоже на пример: 19:49")
