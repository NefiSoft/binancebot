from telebot import types
import phrases


def choose_lang():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text="🇷🇺Русский", callback_data="rus"),
                 types.InlineKeyboardButton(text="🇺🇸English", callback_data="eng"))
    return keyboard


def go_to_cabinet(lang):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text=phrases.all[lang].button_cabinet,
                                   callback_data="cabinet"))
    return keyboard


def login(lang):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text=phrases.all[lang].button_login,
                                   callback_data="login_key"))
    return keyboard


def wallets(lang, hide_small):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text=phrases.all[lang].button_refresh,
                                            callback_data="refresh_wallet"),
                 types.InlineKeyboardButton(text=phrases.all[lang].button_back,
                                            callback_data="back"))
    if not hide_small:
        keyboard.add(types.InlineKeyboardButton(
            text=phrases.all[lang].hide_small + " - " + phrases.all[lang].off,
            callback_data="hide_small_price"))
    else:
        keyboard.add(types.InlineKeyboardButton(
            text=phrases.all[lang].hide_small + " - " + phrases.all[lang].on,
            callback_data="hide_small_price"))
    return keyboard
