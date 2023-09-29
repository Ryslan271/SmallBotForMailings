from Token import bot

from AdditionalMethods.ButtonFactory import creating_buttons

from AdditionalMethods.CommunicationMethods import withdraw_all_user_ids, delete_user_id,\
    get_messages, set_user_ids, set_message, text_set_users_ids,\
    text_delete_users_id, select_message, text_sending_message, text_set_message

from models.DatabaseStructure import UserIDs, Messages
from models import db_session

db_session.global_init('Storage.db')


# region Начальное сообщение
def welcome(message):
    sti = open('assets/hi.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = creating_buttons()

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для "
                     "для обучения и ты можешь его научить новым ответам на твои слова :D\n"
                     "<b>Прошу без мата</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


# endregion


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')

    match req[0]:
        case 'StartNewsletter':
            select_message(call.message)
        case 'GetAllUsers':
            withdraw_all_user_ids(call.message)
        case 'ChangeRecipientList':
            set_user_ids(call.message)
        case 'DeleteRecipient':
            delete_user_id(call.message)
        case 'MailingMessage':
            get_messages(call.message)
        case 'ChangeMailingMessage':
            set_message(call.message)
        case 'DeleteMailingMessage':
            pass


@bot.message_handler(content_types=['text'])
def text_reader(message):
    match str(message.text)[0]:
        case "+":
            text_set_users_ids(message)
        case "-":
            text_delete_users_id(message)
        case "!":
            text_set_message(message)
        case "@":
            text_sending_message(int(message.text[1:].split(' ')[0]), int(message.text[1:].split(' ')[1]), message)


bot.polling(none_stop=True)
