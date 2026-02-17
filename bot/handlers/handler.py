import os
from dotenv import load_dotenv

from database.database import Database
from aiogram import types
from aiogram import Router, html, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from keyboards import categories_keyboard, products_keyboard, get_admin_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.schemas import Category, Product, Cart

class LotteryStates(StatesGroup):
    waiting_for_announcement = State()  
    waiting_for_prize = State() 

my_router = Router(name=__name__)
load_dotenv()
@my_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}\nв данном боте вы можете отслеживать скидки и розыгрыши!")


@my_router.message(Command("help"))
async def echo_handler(message: Message) -> None:
    try:
        await message.answer("за помощью вы можете обратиться к @Levvis22")
    except TypeError:
        await message.answer("Nice try!")

@my_router.message(Command("sales"))
async def cmd_sales(message: types.Message, db: Database):
    """Показать корневые категории"""
    categories = await db.get_root_categories()
    if not categories:
        await message.answer("Нет доступных категорий")
        return
    
    await message.answer(
        "Выберите категорию:",
        reply_markup=categories_keyboard(categories)
    )

@my_router.callback_query(lambda c: c.data.startswith("cat_"))
async def process_category(callback: types.CallbackQuery, db: Database):
    """Обработка выбора категории"""
    category_id = int(callback.data.split("_")[1])
    
    subcats = await db.get_subcategories(category_id)
    if subcats:
        await callback.message.edit_text(
            "Выберите подкатегорию:",
            reply_markup=categories_keyboard(subcats, back=True)
        )
    else:
        products = await db.get_products_by_category(category_id)
        if not products:
            await callback.answer("В этой категории нет товаров", show_alert=True)
            return
        
        await callback.message.edit_text(
            "Товары в категории:",
            reply_markup=products_keyboard(products)
        )
    
    await callback.answer()

def is_admin(user_id: int) -> bool:
    admin_id = os.getenv("ADMIN_ID")
    return admin_id and user_id == int(admin_id)

@my_router.message(Command("admin"))
async def admin_panel(message: Message):
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("🚫 У вас нет прав на выполнение данной команды")
        return
    
    await message.answer(
        "👑 Админ-панель управления лотереей\n"
        "Выберите действие:",
        reply_markup=get_admin_keyboard()
    )

@my_router.callback_query(F.data.startswith("lottery_"))
async def admin_actions(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    
    if not is_admin(user_id):
        await callback.answer("🚫 Недостаточно прав", show_alert=True)
        return
    
    action = callback.data.replace("lottery_", "")
    
    if action == "start":
        await start_lottery(callback, state)
    elif action == "stop":
        await stop_lottery(callback)
    elif action == "stats":
        await show_stats(callback)
    elif action == "pick_winner":
        await pick_winner(callback)
    
    await callback.answer()

async def start_lottery(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.edit_text(
        "✅ Лотерея успешно запущена!\n"
        "Теперь пользователи могут участвовать командой /participate"
    )
    

async def stop_lottery(callback: CallbackQuery):
    
    await callback.message.edit_text(
        "⏹ Лотерея завершена. Теперь можно выбрать победителя."
    )

async def show_stats(callback: CallbackQuery):
    participants_count = 42  
    
    await callback.message.edit_text(
        f"📊 Статистика лотереи:\n"
        f"👥 Участников: {participants_count}\n"
        f"🎁 Приз: iPhone 15 Pro\n"
        f"⏳ Осталось: 2 дня 3 часа"
    )

async def pick_winner(callback: CallbackQuery):
    winner_name = "@username"  
    winner_id = 123456789
    
    await callback.message.edit_text(
        f"🏆 Победитель выбран!\n"
        f"Поздравляем: {winner_name} (ID: {winner_id})\n\n"
        f"Напишите ему в личку для вручения приза."
    )

@my_router.message(Command("lottery"))
async def lottery_register(message: Message):
    await message.answer("поздравляем вы зарегистрированы в лотерее!")
    #добавить sqlite, с базой пользователей (никнейм и юзер), относительно него уже выводить данные

#@my_router.message(Command("promo")) если пользователь в первый раз, то выдать скидку, иначе выдать ошибку

