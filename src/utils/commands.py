from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


async def set_commands(bot: Bot, admins_ids: list[int]):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/cancel", description="Отменить действие"),
        BotCommand(command="/about", description="Информация о боте"),
        BotCommand(command="/help", description="Команды бота"),
    ]
    admin_commands = [
        BotCommand(command="/admin", description="Панель администратора"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    for admin in admins_ids:
        await bot.set_my_commands(
            commands + admin_commands, BotCommandScopeChat(chat_id=admin)
        )
