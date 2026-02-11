from aiogram import Bot
from aiogram.types import BotCommand


# Функция для настройки кнопки Menu бота

commands = {
      '/first_command': 'First Command',
      '/second_command': 'Second Command',
      '/third_command': 'Third Command',
}

async def set_commands_menu(bot: Bot, commands=commands):
      await bot.delete_my_commands()
      main_menu_commands = [BotCommand(
                              command=command,
                              description=description
                        ) for command,
                              description in commands.items()]
      await bot.set_my_commands(main_menu_commands)