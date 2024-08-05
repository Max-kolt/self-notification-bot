from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import asyncio
from loguru import logger

from routers import all_routers
from config import TELEGRAM_TOKEN, DB_URL
from middlewares import DbSessionMiddleware
from database import Base


logger.add('app_logger.log', rotation="500 MB", compression="gz", level="DEBUG", diagnose=False, backtrace=False)


async def main():
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    engine = create_async_engine(DB_URL)

    # Create all tables in database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # Set bot commands for all private chats
    await bot.set_my_commands([
        BotCommand(command="addnote", description="Добавить заметку"),
        BotCommand(command="mynotes", description="Посмотреть заметки")
    ], scope=BotCommandScopeAllPrivateChats())

    dp = Dispatcher()
    # Register handlers
    dp.include_routers(*all_routers)
    # Add database session per endpoint
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    logger.info("Bot is running")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
