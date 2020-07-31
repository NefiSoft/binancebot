class Chat_info:
    chat_id: str
    api_key: int
    api_secret: int
    lang: str
    login = 0
    hide_small = False

    def __init__(self, chat_id):
        pass

    def get_chat_id(self):
        return self.chat_id
