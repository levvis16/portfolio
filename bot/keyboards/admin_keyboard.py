from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для админа с действиями над лотереей"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="🎲 Начать лотерею",
        callback_data="lottery_start"
    ))
    builder.add(InlineKeyboardButton(
        text="⏹ Завершить лотерею",
        callback_data="lottery_stop"
    ))
    builder.add(InlineKeyboardButton(
        text="📊 Статистика",
        callback_data="lottery_stats"
    ))
    builder.add(InlineKeyboardButton(
        text="🏆 Выбрать победителя",
        callback_data="lottery_pick_winner"
    ))
    builder.add(InlineKeyboardButton(
        text="📢 Сделать объявление",
        callback_data="lottery_announce"
    ))
    
    builder.adjust(2)
    
    return builder.as_markup()