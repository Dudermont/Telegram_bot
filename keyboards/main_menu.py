from aiogram import Dispatcher, types


async def set_mein_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/start', description='Приветствие'),
        types.BotCommand(command='/help', description='Помощь'),
        types.BotCommand(command='/cancel', description='Отменить ввод данных')
    ]
    await dp.bot.set_my_commands(main_menu_commands)
