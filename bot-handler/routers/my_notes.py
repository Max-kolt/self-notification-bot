from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
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
            f"Начало события: {note['date']} {note['time']}\n"
            f"{note['text']}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Удалить", callback_data=f"del_{note['id']}")]]
            )
        )


@get_notes_route.callback_query(F.data.startswith("del_"), F.data.split("_")[1].as_("note_id"))
async def delete_note(call: CallbackQuery, session: AsyncSession, note_id: str):
    try:
        await NoteService.delete_note(session, int(note_id))
    except ModuleNotFoundError:
        await call.message.edit_text('Запись уже была удалена')
        return
    await call.message.edit_text('Запись удалена')

