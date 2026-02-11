from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_data.config import Config, load_config

config: Config = load_config()


class IsAdminFilter(BaseFilter):
    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def __call__(self, message: Message) -> bool:  # [3]
        if str(message.from_user.id) == str(config.tg_bot.admin_chat_id):
            print('YOU ARE ADMIN', message.from_user.id)
            return True
        print('YOU ARE NOT ADMIN', message.from_user.id)
        return False

