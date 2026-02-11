from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_resolutions_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=button,
        callback_data=f'{button}') for button in buttons],
        width=1)
    kb_builder.adjust(3)
    return kb_builder.as_markup()

def create_count_keyboard(*buttons: str, width) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=button,
        callback_data=f'{button}') for button in buttons],
        width=width)
    kb_builder.adjust(3)
    return kb_builder.as_markup()

def create_tariffs_keyboard(buttons: list, lang: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=f'{MESSAGE[lang]["TARIFF_WORD"]} {button.name}, {button.gpt_amount} {MESSAGE[lang]["PROMPTS_WORD"]}, {button.price} {MESSAGE[lang]["CURRENCY_WORD"]}',
        callback_data=f'tariff {button.id}') for button in buttons],
        width=1)
    return kb_builder.as_markup() 
