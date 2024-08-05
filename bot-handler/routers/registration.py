from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import bot_command_scope_type
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from services import RegistrationService, UserSchema
from states import Registration


registration_router = Router(name='Registration')


@registration_router.message(CommandStart())
async def start_registration(message: Message, state: FSMContext, session: AsyncSession):
    """
    Handle /start command
    :param message:
    :param state: Catching other contexts to clean them up
    :param session: Database connection
    """
    await state.clear()
    user_id = message.from_user.id
    # Check user registration
    is_registered = await RegistrationService.verify(session, user_id)

    if not is_registered:
        await state.set_state(Registration.name)
        await state.update_data(telegram_id=user_id)
        await message.answer(
            "Добро пожаловать в страну заметок 🗺\n"
            "Перед тем как начать работу нам нужно познакомиться ✍️\n"
            "Как Вас зовут?"
        )
        logger.info(f"New user {message.from_user.username} start registration")
        return

    await message.answer(
        "Добро пожаловать в страну заметок 🗺\n"
        "Попробуйте создать заметку:\n"
        "/addnote \n\n"
        "Или просмотреть уже созданные заметки:\n"
        "/mynotes"
    )


@registration_router.message(Registration.name, F.text.as_("name"))
async def process_name(message: Message, state: FSMContext, name: str):
    """
    Handle username during registration process
    :param message: Telegram message
    :param state: Registration context
    :param name: Result username
    """
    # Save username
    await state.update_data(name=name)
    await state.set_state(Registration.email)
    await message.answer(f"Приятно прознакомиться, {name}!\nОстался всего один пунк. Напиши свою почту ✉️")


@registration_router.message(
    Registration.email,
    F.text.regexp(r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"),  # Simple regex for email validation
    F.text.as_('email')
)
async def process_email(message: Message, state: FSMContext, session: AsyncSession, email: str):
    """
    Handle VALID email during registration process
    :param message: telegram message
    :param state: Registration context
    :param session: Database session
    :param email: filter result of email validation
    """
    await state.update_data(email=email)

    user_data = await state.get_data()
    new_user = UserSchema(telegram_id=int(user_data['telegram_id']), name=user_data['name'], email=user_data['email'])
    # Register new user
    await RegistrationService.registration(session, new_user)
    await message.answer(
        "Добро пожаловать в страну заметок 🗺\n"
        "Попробуйте создать заметку:\n"
        "/addnote \n\n"
        "Или просмотреть уже созданные заметки:\n"
        "/mynotes"
    )
    await state.clear()
    logger.info(f"User {message.from_user.username} successfully registered")


@registration_router.message(Registration.email)
async def invalid_email(message: Message):
    """
    Handle INVALID email during registration process
    :param message: Telegram message
    """
    await message.answer(
        "Неверный формат почты.\nНеобходимо ввести почту в формате: name@mail.com"
    )
