import asyncio

import telebot
from telebot import types
from config import TOKEN_TBOT
from reposit import DataGet, UtilityFunction
from trips.reposit import month
from trips.schema import DriverDate

bot = telebot.TeleBot(token=TOKEN_TBOT,
                      threaded=True,
                      num_threads=300)

bot.delete_webhook()


@bot.message_handler(commands=['Регистрация'])
def registration(message):
    users = {}
    first_message = f'Для регистрации напиши ФИО полностью (н-р: Иванов Иван Иванович)'
    fio = 'Спешилов Николай Юрьевич'
    id_people = asyncio.run(UtilityFunction.id_people(fio))
    if id_people == 0:
        answer = f'Вас нет в базе'
    elif id_people == -1:
        answer = f'Неправельно ввели данные'
    else:
        users[id_people] = message.from_user.id
        answer = f'Успешно зарегестрировались'
    bot.send_message(message.from_user.id, first_message)
    bot.send_message(message.from_user.id, answer)
    # bot.send_message(message.chat.id, str(users))

# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# @bot.message_handler(commands=['start'])
# def start_bot(message):
#     if message.from_user.first_name == 'Николай':
#         nikname = 'Николай Спешилов'
#     else:
#         nikname = f'{message.from_user.first_name} {message.from_user.last_name}'
#     first_mess = f"<b>{nikname}</b>, привет!\nХочешь расскажу немного о нашей компании?"
#     markup = types.InlineKeyboardMarkup()
#     button_yes = types.InlineKeyboardButton(text = 'Да', callback_data='yes')
#     markup.add(button_yes)
#     bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call:True)
# def response(function_call):
#     if function_call.message:
#         if function_call.data == "yes":
#             fg = asyncio.run(UtilityFunction.get_count_gas(1, data=DriverDate(month_trip=10)))
#             print(fg)
#             second_mess = f'<b>{fg[0]}<b>, <br>{fg[1]}, <br>{fg[2]}, <br>{fg[3]}, <br>{fg[4]}'
#             markup = types.InlineKeyboardMarkup()
#             markup.add(types.InlineKeyboardButton("Перейти на сайт", url="https://127.0.0.1:8000/driver/balance/1?month_trip=10"))
#             bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
#             bot.answer_callback_query(function_call.id)


#bot.polling(none_stop=True, interval=0)


bot.infinity_polling()
