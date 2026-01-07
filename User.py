
class User:
    def __init__(self):
        self.__dialog = []

    def add_message(self,obj):
        self.__dialog.append(obj)
        if self.__dialog.__len__() > 15:
            self.__dialog.pop(0)

    def get_dialog(self):
        return self.__dialog










