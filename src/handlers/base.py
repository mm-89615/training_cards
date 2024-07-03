from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import settings
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
        last_name=message.from_user.last_name,
    )
    kb = StartKb.get_kb(message)
    await message.answer(
        f"Добро пожаловать, {message.from_user.first_name}!", reply_markup=kb
    )


@router.message(Command("help"))
async def about(message: Message):
    text = (
        "Доступные команды бота:\n"
        "/start - Начать работу с ботом\n"
        "/about - Информация о боте\n"
        "/cancel - Отменить действие\n"
        "/help - Команды бота\n"
        "/words - Управление словами\n"
        "/add_word - Добавить новое слово в ваш словарь\n"
        "/find - Поиск слова в вашем словаре\n"
    )

    if message.from_user.id in settings.bot.admin_ids:
        text += (
            "\nКоманды администратора:\n"
            "/admin - Панель администратора\n"
            "!add_word - Добавить новое слово в общий словарь\n"
            "!find - Найти слово в общем словаре\n"
        )

    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


@router.message(Command("about"))
async def about(message: Message):
    text = (
        "Этот бот создан для запоминания английских слов. \n"
        "Вы можете учить слова из общего словаря или добавить свои. \n\n"
        "Обучение происходит по методике, основанной на кривой забывания Эббингауза.\n"
        "Новое слово заучивается путем частого повторения, "
        "затем повторяется через определенный промежуток времени.\n\n"
        "Первое повторение - через 30 минут.\n"
        "Второе повторение - через 1 день.\n"
        "Третье повторение - через 1 неделю.\n"
        "Четвертое повторение - через 2 недели.\n"
        "Пятое повторение и больше - через 2 месяца.\n\n"
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply("Не выполнялись никакие действия.")
        return
    await state.clear()
    await message.reply("Все действия отменены", reply_markup=ReplyKeyboardRemove())
