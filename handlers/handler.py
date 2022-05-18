import abc
from markup.markup import Keyboards
from data_base.dbalchemy import DBManager


class Handler(metaclass=abc.ABCMeta):
    def __init__(self, bot):
        # получаем обьект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keybords = Keyboards()
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()

    # его задача показать что задекорированный метод должен быть обязательно переопределен в наследнике
    @abc.abstractmethod
    def handle(self):
        pass
