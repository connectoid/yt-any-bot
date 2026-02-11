import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.commands_menu import set_commands_menu

logger = logging.getLogger(__name__)
storage = MemoryStorage()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        filename = "botlog.log",
        filemode='a',
        format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
        )
    logger.info('Starting bot')
    
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    print()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands_menu(bot)
    await dp.start_polling(bot)
    print('Bot started')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')