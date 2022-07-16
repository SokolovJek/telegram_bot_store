# ЗАПУСКАЕМЫЙ ФАЙЛ

# импортируем функцию создания обьекта бота
from telebot import TeleBot
from settings import config
# импортируем главный класс-обработчик бота
from handlers.handler_main import HandlerMain


class TelBot:
    """
    основной класс телеграмм бота(сервер), в основе которого используется
    библиотека pyTelegramBotAPI
    """

    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        """
        инициализация бота
        """

        self.token = config.TOKEN
        # иницыализируем бота на основе зарегестрированного токена
        self.bot = TeleBot(self.token)
        # иницыализируем обработчик событий
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        метод предназначен для старта обработчика событий
        """
        self.handler.handle()

    def run_bot(self):
        """
        метод запускает основные события сервера
        """
        # запуск обработчиков
        self.start()
        # служит для запуска бота(работа в режимке нон-стоп)
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()

