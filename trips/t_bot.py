import asyncio

import telebot
from telebot import types
from config import TOKEN_TBOT
from reposit import DataGet, DataLoads, UtilityFunction
from trips.reposit import month
from trips.schema import DriverDate, IdentificationAdd

bot = telebot.TeleBot(token=TOKEN_TBOT,
                      threaded=True,
                      num_threads=300)

bot.delete_webhook()


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text.lower() == "привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.chat.id, message)
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # loop = asyncio.get_event_loop()
    # taskA = loop.create_task(UtilityFunction.get_identification())
    if message.from_user.id in asyncio.run(UtilityFunction.get_identification()):
        button_fuel = types.KeyboardButton(text='Баланс топлива')
        button_cost = types.KeyboardButton(text='Сумма заездов')
        markup.add(button_fuel).row(button_cost)
        bot.send_message(message.chat.id, text=f'Привет {message.from_user.first_name} Вы зарегестрированый пользователь!',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text=f'Привет {message.from_user.first_name}, для регистрации напиши ФИО полностью (н-р: Иванов Иван Иванович)')
        bot.register_next_step_handler(message, registration)


def registration(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if message.text != "":
        loop = asyncio.get_event_loop()
        fio = message.text.strip()
        id_people = loop.create_task(UtilityFunction.id_people(fio))
        if id_people == 0:
            answer = f'Вас нет в базе'
        elif id_people == -1:
            answer = f'Неправельно ввели данные'
        else:
            id_role = loop.create_task(UtilityFunction.get_id_role())
            data_fg = DataLoads.add_identification(data=IdentificationAdd(id_tg=str(message.from_user.id),
                                                                          id_people=id_people,
                                                                          id_role=id_role))
            loop.run_until_complete(asyncio.wait([id_people, id_role, data_fg]))
            #users[id_people] = message.from_user.id
            answer = f'Успешно зарегестрировались'
        bot.send_message(message.chat.id, answer)
        button_fuel = types.KeyboardButton(text='Баланс топлива')
        button_cost = types.KeyboardButton(text='Сумма заездов')
        markup.row(button_fuel, button_cost)
        bot.send_message(message.chat.id,
                         text='Получить информацию',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Введите данные')

# def on_click(message):
#     if message.text == 'Баланс топлива':
#         fg = asyncio.run(UtilityFunction.get_count_gas(1, data=DriverDate(month_trip=10)))
#         bot.send_message(message.chat.id, f'<b>{fg[0]}</b> \n{fg[1]}\n{fg[2]}\n{fg[3]}\n{fg[4]}',
#                          parse_mode='html')


# @bot.callback_query_handler(func=lambda callback: True)
# def response(callback):
#     if callback.data == 'fuel':
#         fg = asyncio.run(UtilityFunction.get_count_gas(1, data=DriverDate(month_trip=10)))
#         bot.send_message(callback.message.chat.id, f'<b>{fg[0]}</b> \n{fg[1]}\n{fg[2]}\n{fg[3]}\n{fg[4]}', parse_mode='html')
#     elif callback.data == 'registration':
#         users = {}
#         first_message = f'Для регистрации напиши ФИО полностью (н-р: Иванов Иван Иванович)'
#         bot.send_message(callback.message.chat.id, 'Введите данные')
#         if callback.message.from_user.text != "":
#             fio = callback.message.from_user.text
#             id_people = asyncio.run(UtilityFunction.id_people(fio))
#             if id_people == 0:
#                 answer = f'Вас нет в базе'
#             elif id_people == -1:
#                 answer = f'Неправельно ввели данные'
#             else:
#                 users[id_people] = callback.message.from_user.id
#                 answer = f'Успешно зарегестрировались'
#             bot.send_message(callback.message.chat.id, answer)
#         else:
#             bot.send_message(callback.message.chat.id, 'Введите данные')
#         bot.send_message(callback.message.chat.id, f'<b>{first_message}</b>', parse_mode='html')




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



bot.infinity_polling()
