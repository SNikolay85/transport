import telebot
from telebot import types
from config import TOKEN_TBOT

bot = telebot.TeleBot(token=TOKEN_TBOT,
                      threaded=True,
                      num_threads=300)


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(commands=['start'])
def start_bot(message):
    if message.from_user.first_name == 'Николай':
        nikname = 'Николай Спешилов'
    else:
        nikname = f'{message.from_user.first_name} {message.from_user.last_name}'
    first_mess = f"<b>{nikname}</b>, привет!\nХочешь расскажу немного о нашей компании?"
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text = 'Да', callback_data='yes')
    markup.add(button_yes)
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:
        if function_call.data == "yes":
            second_mess = "Мы облачная платформа для разработчиков и бизнеса. Более детально можешь ознакомиться с нами на нашем сайте!"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Перейти на сайт", url="https://timeweb.cloud/"))
            bot.send_message(function_call.message.chat.id, second_mess, reply_markup=markup)
            bot.answer_callback_query(function_call.id)


#bot.polling(none_stop=True, interval=0)


bot.infinity_polling()
