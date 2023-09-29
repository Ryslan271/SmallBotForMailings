from telebot import types


def creating_buttons():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton("Начать\nрассылку", callback_data="StartNewsletter"))
    markup.add(types.InlineKeyboardButton("Вывести\nвсех получателей", callback_data="GetAllUsers"))
    markup.add(types.InlineKeyboardButton("Изменить\nсписок получателей", callback_data="ChangeRecipientList"))
    markup.add(types.InlineKeyboardButton("Удалить\nполучателя", callback_data="DeleteRecipient"))
    markup.add(types.InlineKeyboardButton("Сообщение\nдля рассылки", callback_data="MailingMessage"))
    markup.add(types.InlineKeyboardButton("Изменить\nсообщение для рассылки", callback_data="ChangeMailingMessage"))
    markup.add(types.InlineKeyboardButton("Удалить\nсообщение для рассыки", callback_data="DeleteMailingMessage"))

    return markup
