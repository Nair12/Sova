import enum


class AiMode(enum.Enum):
    DIALOG = 1
    VOICE = 2
    LISTEN = 3




class User:
    def __init__(self):
        self.__dialog = []
        self.__mode = AiMode.DIALOG
        self.__notify_enabled = True

    def add_message(self,obj):
        self.__dialog.append(obj)
        if self.__dialog.__len__() > 15:
            self.__dialog.pop(0)

    def get_dialog(self):
        return self.__dialog

    def get_mode(self):
        return self.__mode

    def set_mode(self,mode:AiMode):
        self.__mode = mode

    def get_notify_status(self):
        return self.__notify_enabled

    def set_notify_enabled(self,notify_enabled:bool):
        self.__notify_enabled = notify_enabled











