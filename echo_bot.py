import telebot
import binance_connect
# import phrases
import keyboards
import telegram_token
import sql_connect
from time import sleep
import json

class v:
    chat_id = "chat_id"
    api_key = "api_key"
    api_secret = "api_secret"
    login = "login"
    lang = "lang"
    hide_small = "hide_small"


bot = telebot.TeleBot(telegram_token.token)
chat_info = {'chat_id': 0, 'lang': '', 'api_key': '', 'api_secret': '', 'login': 0, 'hide_small': False}
chats = dict(chat_info)
with open("phrases.json", "r", encoding='utf-8') as file:
    phrases = json.load(file)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = str(message.chat.id)
    if chats.get(chat_id) is None:
        chats[chat_id] = chat_info
        chats[chat_id][v.chat_id] = message.chat.id
    if chats[chat_id]["lang"] == "":
        bot.send_message(message.chat.id, phrases["choose_lang"], reply_markup=keyboards.choose_lang())
    else:
        bot.send_message(message.chat.id, phrases[chats[chat_id][v.lang]]["welcome"],
                         reply_markup=keyboards.go_to_cabinet(chats[chat_id][v.lang]), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    if call.message:
        chat_id = str(call.message.chat.id)
        if call.data == "rus" or call.data == "eng":  # Choosing language
            chats[chat_id][v.lang] = call.data
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=phrases[chats[chat_id][v.lang]]["welcome"],
                                  reply_markup=keyboards.go_to_cabinet(chats[chat_id][v.lang]), parse_mode="Markdown")
        elif call.data == "cabinet":  # Login
            if chats[chat_id]["api_key"] != "" and chats[chat_id]["api_secret"] != "":
                show_wallets(call.message)
            else:
                loginning(chat_id, call.message.message_id)
        elif call.data == "login_key":
            chats[chat_id][v.login] = 1
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=phrases[chats[chat_id][v.lang]]["login1"],
                                  reply_markup=None, parse_mode="Markdown")
        elif call.data == "hide_small_price":
            chats[chat_id][v.hide_small] = not chats[chat_id][v.hide_small]
            show_wallets(call.message)
        elif call.data == "refresh_wallet":
            show_wallets(call.message)


def loginning(chat_id, message_id=None):
    if message_id is None:
        bot.send_message(chat_id, phrases[chats[chat_id][v.lang]]["need_login"],
                         reply_markup=keyboards.login(chats[chat_id][v.lang]), parse_mode="Markdown")
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=phrases[chats[chat_id][v.lang]]["need_login"],
                              reply_markup=keyboards.login(chats[chat_id][v.lang]), parse_mode="Markdown")


def show_coins(hide_small_price, api_key, api_secret, chat_id):
    all_coins = binance_connect.get_account_info(hide_small_price, api_key, api_secret)
    full_balance = 0.0
    for coin in all_coins:
        full_balance += float(coin['inUSDT'])
    future_message = phrases[chats[chat_id][v.lang]]["your_balance"] + " = " + str(full_balance) + "$\n\n"
    for coin in all_coins:
        future_message += "*" + coin['asset'] + "*" + ":\n   " + coin['free'] + " - " + phrases[
            chats[chat_id][v.lang]]["free"] + "   █   " + coin['locked'] + " - " + phrases[
                              chats[chat_id][v.lang]]["locked"] + "   (≈" + \
                          str(round(coin['inUSDT'], 2)) + "$) \n\n"
    return future_message


def show_wallets(call):
    chat_id = call.chat.id

    bot.edit_message_text(chat_id=call.chat.id, message_id=call.message_id,
                          text=show_coins(chats[str(call.chat.id)][v.hide_small], chats[str(call.chat.id)][v.api_key],
                                          chats[str(call.chat.id)][v.api_secret], str(call.chat.id)),
                          reply_markup=keyboards.wallets(chats[str(call.chat.id)][v.lang],
                                                         chats[str(call.chat.id)][v.hide_small]),
                          parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = str(message.chat.id)
    if chats[chat_id][v.login] == 1:
        bot.send_message(chat_id, phrases[chats[chat_id][v.lang]]["login2"], reply_markup=None)
        chats[chat_id][v.api_key] = message.text
        chats[chat_id][v.login] = 2
    elif chats[chat_id][v.login] == 2:
        chats[chat_id][v.login] = 0
        chats[chat_id][v.api_secret] = message.text
        try_binance = binance_connect.try_connect(chats[chat_id][v.api_key], chats[chat_id][v.api_secret])
        if try_binance is True:
            sql_connect.save_json(chats)
            _message = bot.send_message(chat_id, phrases[chats[chat_id][v.lang]]["authorised"], reply_markup=None)
            show_wallets(_message)
        else:
            del chats[chat_id][v.api_key]
            del chats[chat_id][v.api_secret]
            bot.send_message(chat_id, phrases[chats[chat_id][v.lang]]["fail_authorisation"],
                             reply_markup=keyboards.go_to_cabinet(chats[chat_id][v.lang]))


if __name__ == '__main__':
    can_connect = sql_connect.try_connect()
    if can_connect:
        chats = sql_connect.get_json()

    bot.polling(none_stop=True)
    while True:
        sql_connect.save_json(chats)
        sleep(60)