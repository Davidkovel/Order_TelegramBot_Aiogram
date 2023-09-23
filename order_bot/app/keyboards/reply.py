from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Меню")
    ]
], resize_keyboard=True)


main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Создать накладную')
    ]
], resize_keyboard=True)

admin_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Создать накладную'),
        KeyboardButton(text='Открытые накладные'),
        KeyboardButton(text='Закрытые накладные')
    ]
], resize_keyboard=True)

order_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Накладная с товаром')
    ],
    [
        KeyboardButton(text='Квитанция об оплате')
        
    ],
    [
        KeyboardButton(text='ТТН новой почты')
    ],
    [
        KeyboardButton(text='Скрин оприходованной накладной\nпосле получения на почте')
    ],
], resize_keyboard=True) 