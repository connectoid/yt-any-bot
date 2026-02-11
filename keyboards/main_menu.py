from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)



def get_main_menu():
    button_1: KeyboardButton = KeyboardButton(text='Button 1')
    button_2: KeyboardButton = KeyboardButton(text='Button 2')
    button_3: KeyboardButton = KeyboardButton(text='Button 3')
    button_4: KeyboardButton = KeyboardButton(text='Button 4')

    main_menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1, button_2],
                                                [button_3, button_4]],
                                        resize_keyboard=True,
                                        input_field_placeholder='placeholder')
    return main_menu_keyboard
