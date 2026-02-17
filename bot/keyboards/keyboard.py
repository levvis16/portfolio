from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.schemas import Category, Product

def categories_keyboard(categories: list[Category], back: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(
            text=cat.name,
            callback_data=f"cat_{cat.id}"
        )
    if back:
        builder.button(text="◀ Назад", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()

def products_keyboard(products: list[Product]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for prod in products:
        builder.button(
            text=f"{prod.name} - {prod.price} руб.",
            callback_data=f"prod_{prod.id}"
        )
    builder.button(text="◀ К категориям", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()