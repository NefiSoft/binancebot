class Phrases:
    welcome: str
    choose_lang: str
    button_cabinet: str
    button_back: str
    need_login: str
    button_login: str
    login1: str
    login2: str
    authorised: str
    fail_authorisation: str
    button_try_again: str
    button_refresh: str
    hide_small: str
    on: str
    off: str
    your_balance: str
    locked: str
    free: str


_rus = Phrases()
_rus.welcome = '''
    *Добро пожаловать!*
Благодарим вас за использование нашего бота!
/help - посмотреть команды.
Чтобы начать работу с нашим ботом, перейдите в кабинет.
    '''
_rus.choose_lang = "Choose the language:"
_rus.button_cabinet = "Перейти в кабинет"
_rus.need_login = '''
Для начала вам необходимо авторизоваться с помощью "API key" и "API secret".
Вот [инструкция](https://www.binance.com/ru/support/articles/360002502072), которая подскажет Вам, как правильно получить эти ключи.
'''
_rus.button_login = "Авторизоваться"
_rus.login1 = "Введите сначала ваш API key без пробелов и лишних символов:"
_rus.login2 = "Отлично! Теперь отправьте API secret:"
_rus.authorised = "Вы успешно авторизовались!"
_rus.fail_authorisation = "Ключ или секрет оказался неверным. Повторите попытку."
_rus.button_try_again = "🔃Повторить попытку"
_rus.button_refresh = "🔃Обновить"
_rus.button_back = "Назад"
_rus.hide_small = "Скрыть малые суммы (<0.01$)"
_rus.on = "ВКЛ"
_rus.off = "ВЫКЛ"
_rus.your_balance = "Баланс вашего кошелька"
_rus.locked = "занято"
_rus.free = "свободно"

_eng = Phrases()
_eng.welcome = "Добро пожаловать"
_eng.choose_lang = "Choose the language:"
_eng.button_cabinet = "Go to cabinet"

all = dict(rus=_rus, eng=_eng)
