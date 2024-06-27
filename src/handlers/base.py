from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from database.repo import Request
from keyboards import StartKb

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message, request: Request, state: FSMContext):
    await state.clear()
    await request.users.get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    kb = StartKb.get_kb(message)
    await message.answer(f"Добро пожаловать, {message.from_user.first_name}!", reply_markup=kb)


@router.message(Command("help"))
async def about(message: Message):
    await message.answer("О проекте")


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply("Не выполнялись никакие действия.")
        return
    await state.clear()
    await message.reply("Все действия отменены", reply_markup=ReplyKeyboardRemove())



