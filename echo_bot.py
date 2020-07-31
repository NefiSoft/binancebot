import telebot
import binance_connect
from ChatInfo import Chat_info
import phrases
import keyboards
import telegram_token

bot = telebot.TeleBot(telegram_token.token)
chats = dict()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if chats.get(message.chat.id) is None:
        chats[message.chat.id] = Chat_info(message.chat.id)
    if not hasattr(chats[message.chat.id], "lang"):
        bot.send_message(message.chat.id, phrases.all["eng"].choose_lang, reply_markup=keyboards.choose_lang())
    else:
        bot.send_message(message.chat.id, phrases.all[chats[message.chat.id].lang].welcome,
                         reply_markup=keyboards.go_to_cabinet(chats[message.chat.id].lang), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    if call.message:
        chat_id = call.message.chat.id
        if call.data == "rus" or call.data == "eng":  # Choosing language
            chats[chat_id].lang = call.data
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=phrases.all[chats[chat_id].lang].welcome,
                                  reply_markup=keyboards.go_to_cabinet(chats[chat_id].lang), parse_mode="Markdown")
        elif call.data == "cabinet":  # Login
            if hasattr(chats[chat_id], "api_key") and hasattr(chats[chat_id], "api_secret"):
                show_wallets(call.message)
            else:
                loginning(chat_id, call.message.message_id)
        elif call.data == "login_key":
            chats[chat_id].login = 1
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=phrases.all[chats[chat_id].lang].login1,
                                  reply_markup=None, parse_mode="Markdown")
        elif call.data == "hide_small_price":
            chats[chat_id].hide_small = not chats[call.message.chat.id].hide_small
            show_wallets(call.message)
        elif call.data == "refresh_wallet":
            show_wallets(call.message)


def loginning(chat_id, message_id=None):
    if message_id is None:
        bot.send_message(chat_id, phrases.all[chats[chat_id].lang].need_login,
                         reply_markup=keyboards.login(chats[chat_id].lang), parse_mode="Markdown")
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=phrases.all[chats[chat_id].lang].need_login,
                              reply_markup=keyboards.login(chats[chat_id].lang), parse_mode="Markdown")


def show_coins(hide_small_price, api_key, api_secret, chat_id):
    all_coins = binance_connect.get_account_info(hide_small_price, api_key, api_secret)
    full_balance = 0.0
    for coin in all_coins:
        full_balance += float(coin['inUSDT'])
    future_message = phrases.all[chats[chat_id].lang].your_balance + " = " + str(full_balance) + "$\n\n"
    for coin in all_coins:
        future_message += "*" + coin['asset'] + "*" + ":\n   " + coin['free'] + " - " + phrases.all[
            chats[chat_id].lang] + "   █   " + coin[
                              'locked'] + " - " + phrases.all[chats[chat_id].lang].locked + "   (≈" + str(
            round(float(coin['inUSDT']), 2)) + "$) \n\n"
    return future_message


def show_wallets(call):
    chat_id = call.chat.id

    bot.edit_message_text(chat_id=call.chat.id, message_id=call.message_id,
                          text=show_coins(chats[call.chat.id].hide_small, chats[call.chat.id].api_key,
                                          chats[call.chat.id].api_secret, call.chat.id),
                          reply_markup=keyboards.wallets(chats[call.chat.id].lang,chats[call.chat.id].hide_small),
                          parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    if chats[chat_id].login == 1:
        bot.send_message(chat_id, phrases.all[chats[chat_id].lang].login2, reply_markup=None)
        chats[chat_id].api_key = message.text
        chats[chat_id].login = 2
    elif chats[chat_id].login == 2:
        chats[chat_id].login = 0
        chats[chat_id].api_secret = message.text
        if binance_connect.try_connect(chats[chat_id].api_key, chats[chat_id].api_secret) is True:
            _message = bot.send_message(chat_id, phrases.all[chats[chat_id].lang].authorised, reply_markup=None)
            show_wallets(_message)
        else:
            del chats[chat_id].api_key
            del chats[chat_id].api_secret
            bot.send_message(chat_id, phrases.all[chats[chat_id].lang].fail_authorisation,
                             reply_markup=keyboards.go_to_cabinet(chats[chat_id].lang))


if __name__ == '__main__':
    bot.polling(none_stop=True)
