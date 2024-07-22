from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

helper = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    input_field_placeholder='Чем я могу вам помочь?',
    keyboard=[
        [KeyboardButton(text='Как подключить умный домофон?')],
        [KeyboardButton(text='Расскажи, что умеет умный домофон')],
        [KeyboardButton(text='У меня не работает...')],
        [KeyboardButton(text='Где можно купить новый ключ?')],
        [KeyboardButton(text='Кто такая Сию?'), KeyboardButton(text='О компании')],
    ]
)

cancel = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    keyboard=[
        [KeyboardButton(text='Отмена')],
    ]
)


### Как подключить домофон
inl_connection = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Давай!', callback_data='report')]
    ]
)

inl_inter = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да, установлен', callback_data='yes_we_have')],
        [InlineKeyboardButton(text='Нет, не установлен', callback_data='no_we_havent')],
        [InlineKeyboardButton(text='Частный дом', callback_data='house')],
    ]
)

inl_connection_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Напишите мне на What's App", callback_data='whats')],
        [InlineKeyboardButton(text='Позвоните мне', callback_data='mobile')],
    ]
)


### Расскажи, что умеет умный домофон
inl_about = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да, есть', callback_data='ihave')]
    ]
)

inl_letsgo = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Здорово! Как удобно! Идем дальше', callback_data='gonext')]
    ]
)

inl_without = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='ОТКРЫВАЕМ ДВЕРЬ БЕЗ КЛЮЧА!', callback_data='without_key')]
    ]
)

### Развлетвление по ключам
inl_keys =  InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Что такое онлайн ключ?', callback_data='online_key')],
        [InlineKeyboardButton(text='Что такое временный доступ?', callback_data='time_key')]
    ]
)

### First choose
inl_keys_ex = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='А ключ есть?', callback_data='keys_ex')]
    ]
)

inl_how_work = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='А как вообще работает домофон?', callback_data='how_work')]
    ]
)

inl_what_if = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Удобно!', callback_data='good')],
        [InlineKeyboardButton(text='Что если сломается?', callback_data='good')],
    ]
)

inl_how_much = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Сколько стоит домофон?', callback_data='how_much')]
    ]
)

inl_find_money = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Узнать цены', url='https://inter.kg/')]
    ]
)

### Где можно купить новый ключ?
inl_where_ibuy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Мы', url='https://inter.kg/navigation')]
    ]
)

### О компании
inl_about_us = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Переходи на наш сайт', url='https://inter.kg/navigation')],
        [InlineKeyboardButton(text='Следи за новостями в Инстаграм', url='https://www.instagram.com/intercom.kg/?')],
        [InlineKeyboardButton(text='Пиши нам на What\'s App', url='https://wa.me/996504556604?')]
    ]
)

### У меня не работает...
not_work = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    input_field_placeholder='Сожалею(',
    keyboard=[
        [KeyboardButton(text='У меня не работает распознавание')],
        [KeyboardButton(text='Не получается войти в приложение')],
        [KeyboardButton(text='Не работают камеры')],
        [KeyboardButton(text='Приложение не работает')],
        [KeyboardButton(text='Другое')], 
        [KeyboardButton(text='Назад')],
    ]
)

inl_im_read = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Я ознакомился(-ась)', callback_data='im_read')]
    ]
)

inl_im_understood = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Понял(-а), хорошо', callback_data='report_w')]
    ]
)

inl_dnot_work = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Я ознакомился(-ась)', callback_data='im_read_app')]
    ]
)

inl_app_dnot = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Я ознакомился(-ась)', callback_data='im_app_dnot')]
    ]
)

inl_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Начнем!', callback_data='report_w')]
    ]
)