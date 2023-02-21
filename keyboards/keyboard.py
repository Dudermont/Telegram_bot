from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


buttons: dict[str, str] = {'but_1': 'Кнопка 1',
                           'but_2': 'Кнопка 2',
                           'but_3': 'Кнопка 3',
                           'but_4': 'Кнопка 4',
                           'but_5': 'Кнопка 5',
                           'but_6': 'Кнопка 6',
                           'but_7': 'Кнопка 7'}


def create_inline_kb(row_width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=row_width)
    if args:
        [inline_kb.insert(InlineKeyboardButton(
                                               text=buttons[button],
                                               callback_data=button)) for button in args]
    if kwargs:
        [inline_kb.insert(InlineKeyboardButton(
                                               text=text,
                                               callback_data=button)) for button, text in kwargs.items()]
    return inline_kb


keyboard_1 = create_inline_kb(2,
                              spending='Внести трату',
                              expense='Потрачено всего',
                              category='Категория трат',
                              during='Траты за период'
                              )
keyboard_2 = create_inline_kb(2,
                              help='Помощь',
                              spending='Внести трату',
                              expense='Потрачено всего',
                              category='Категория трат',
                              during='Траты за период')

spend_during_keyboard = create_inline_kb(3,
                                         day='День',
                                         month='Месяц',
                                         year='Год',
                                         period='Задать период')
cancel_keyboard = create_inline_kb(1,
                                   cancel='Отменить ввод')

month_keyboard = create_inline_kb(4,
                                  january='Январь',
                                  february='Февраль',
                                  march='Март',
                                  april='Апрель',
                                  may='Май',
                                  june='Июнь',
                                  july='Июль',
                                  august='Август',
                                  september='Сентябрь',
                                  october='Октябрь',
                                  november='Ноябрь',
                                  december='Декабрь')

month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
         'september', 'october', 'november', 'december']
month2 = ['Январь', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
         'september', 'october', 'november', 'december']
month3 = {'january': 'Январь',
          'february': 'Февраль',
          'march': 'Март',
          'april': 'Апрель',
          'may': 'Май',
          'june': 'Июнь',
          'july': 'Июль',
          'august': 'Август',
          'september': 'Сентябрь',
          'october': 'Октябрь',
          'november': 'Ноябрь',
          'december': 'Декабрь'}
month4 = {'Январь': 1,
          'Февраль': 2,
          'Март': 3,
          'Апрель': 4,
          'Май': 5,
          'Июнь': 6,
          'Июль': 7,
          'Август': 8,
          'Сентябрь': 9,
          'Октябрь': 10,
          'Ноябрь': 11,
          'Декабрь': 12}
