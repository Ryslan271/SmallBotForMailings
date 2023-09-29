import telebot

from Token import bot

from models import db_session
from models.DatabaseStructure import UserIDs, Messages

from AdditionalMethods.ButtonFactory import creating_buttons


# region Вывод всех получателей списком
def withdraw_all_user_ids(message):
    session = db_session.create_session()

    user_all = session.query(UserIDs).all()

    if not quantity_check_users_ids(message):
        return

    list_user = ""

    for user in user_all:
        if user.senderId == message.chat.id:
            list_user += str(user.id) + " - " + user.ListIds + "//"

    markup = creating_buttons()

    bot.send_message(message.chat.id,
                     "Вот список получателей:\n" +
                     "\n".join(list_user.split("//")),
                     parse_mode='html', reply_markup=markup)
# endregion


# region Информация о изменении списка получателей
def set_user_ids(message):
    markup = creating_buttons()
    bot.send_message(message.chat.id,
                     'Теперь напиши Ники пользователей в одном сообщении,'
                     ' начни свое сообщение с символа, пример: "+(тут ники пользователей)",'
                     ' между словами ставь простотые пробелы, но после + не ставь пробел пожалуйста, я пойму"',
                     parse_mode='html', reply_markup=markup)
# endregion


# region Информация для удаления получателя
def delete_user_id(message):
    markup = creating_buttons()

    session = db_session.create_session()

    if not quantity_check_users_ids(message):
        return

    bot.send_message(message.chat.id,
                     'Для удаления выберите из списка пользователей кого хотели бы удалить, символом -,'
                     'Пример: -(Ник пользователя)',
                     parse_mode='html', reply_markup=markup)
# endregion


# region Вывод сообщений рассылки
def get_messages(message):
    markup = creating_buttons()

    session = db_session.create_session()

    new_messages = session.query(Messages).all()

    if not quantity_check_message(message):
        return

    mes_text = ""

    for mes in new_messages:
        if mes.senderId == message.chat.id:
            mes_text += str(mes.id) + " - " + mes.text + "//"

    bot.send_message(message.chat.id,
                     "Вот сообщение для получателей:\n" +
                     "\n".join(mes_text.split('//')),
                     parse_mode='html', reply_markup=markup)
# endregion


# region Информация о изменении сообщений для отправки получателям
def set_message(message):
    markup = creating_buttons()
    bot.send_message(message.chat.id,
                     "Для измения списка нужно отправить символ '!', без пробела после, "
                     "пример: '!Добрый день, напоминая, сегодня собрание'", reply_markup=markup)
# endregion


# region информация о отправке сообщений
def select_message(message):
    markup = creating_buttons()
    bot.send_message(message.chat.id,
                     "Для отправки сообщения пользователю напишите так:"
                     "@(Номер ника пользователя, он выводится перед ником при команде 'Вывести всех получателей') и"
                     " через пробел (номер сообщения, он выводится перед ником при команде 'Сообщение для рассылки')",
                     reply_markup=markup)
# endregion


def text_set_users_ids(message):
    session = db_session.create_session()

    user_all = session.query(UserIDs).all()

    markup = creating_buttons()

    for user in user_all:
        if user.ListIds == str(message.text)[1:]:
            bot.send_message(message.chat.id,
                             'Такой пользователь уже есть в списке,'
                             ' прошу проверить командой "Вывести всех получателей"',
                             parse_mode='html', reply_markup=markup)
            return

    new_users_id = UserIDs(
        senderId=message.chat.id,
        ListIds=str(message.text)[1:].strip()
    )
    session.add(new_users_id)
    session.commit()

    bot.send_message(message.chat.id,
                     'Новые пользователи добавлены',
                     parse_mode='html', reply_markup=markup)


def text_delete_users_id(message):
    session = db_session.create_session()
    user_all = session.query(UserIDs).all()

    if not quantity_check_users_ids(message):
        return

    if message.text[1:].strip() not in [user.ListIds for user in user_all]:
        markup = creating_buttons()
        bot.send_message(message.chat.id,
                         "Прошу проверить ник, такого пользователя нет", reply_markup=markup)
        return

    user_all = session.query(UserIDs).all()

    current_user = [user.id for user in user_all if user.ListIds == message.text[1:].strip()][0]

    session.delete(session.query(UserIDs).get(current_user))
    session.commit()

    bot.send_message(message.chat.id,
                     'Получатель удален из списка',
                     parse_mode='html')

    if quantity_check_users_ids(message):
        session = db_session.create_session()
        user_all = session.query(UserIDs).all()
        markup = creating_buttons()
        bot.send_message(message.chat.id,
                         "Вот новый список получателей:\n" +
                         "\n".join([user.ListIds for user in user_all]),
                         parse_mode='html', reply_markup=markup)


def text_sending_message(id_recipient, id_message, message):

    if not quantity_check_message(message) or not quantity_check_users_ids(message):
        return

    session = db_session.create_session()
    user_current_message = session.query(Messages).get(id_message)
    user_current_recipient = session.query(UserIDs).get(id_recipient)

    bot.send_message(chat_id=user_current_recipient.ListIds, text=user_current_message.text)

    markup = creating_buttons()

    bot.send_message(message.chat.id,
                     'Сообщение отправлено',
                     parse_mode='html', reply_markup=markup)


def text_set_message(message):
    session = db_session.create_session()

    new_messages = Messages(
        senderId=message.chat.id,
        text=message.text[1:]
    )
    session.add(new_messages)
    session.commit()

    markup = creating_buttons()

    bot.send_message(message.chat.id,
                     'Новые сообщение добавлено',
                     parse_mode='html', reply_markup=markup)


def quantity_check_users_ids(message):
    session = db_session.create_session()
    user_all = session.query(UserIDs).all()

    list_user = 0

    for user_id in user_all:
        if user_id.senderId == message.chat.id:
            list_user += 1

    if list_user <= 0:
        markup = creating_buttons()
        bot.send_message(message.chat.id,
                         "Список пустой)\n"
                         "Можете добавить получателей командой 'Изменить список получателей'", reply_markup=markup)
        return False

    return True


def quantity_check_message(message):
    session = db_session.create_session()
    user_all = session.query(Messages).all()

    list_user = 0

    for user_id in user_all:
        if user_id.senderId == message.chat.id:
            list_user += 1

    if list_user <= 0:
        markup = creating_buttons()
        bot.send_message(message.chat.id,
                         "Список пустой)\n"
                         "Можете добавить сообщение командой 'Изменить сообщение для рассылки'", reply_markup=markup)
        return False

    return True
