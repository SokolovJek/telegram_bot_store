from handlers.handler_com import HandlerCommands
from handlers.handler_all_text import HandlerAllText


class HandlerMain:
    """
    класс компановщик, здесь происходит инициализация
    и запуск основных обработчиков событий нашего бота
    """

    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot
        # здесь будет инициализация обработчиков
        self.handler_commands = HandlerCommands(self.bot)  # обрабатывает /start
        self.handlerP_all_text = HandlerAllText(self.bot)  # обрабатывает настроки, инфо, <<

    def handle(self):
        # здесь запуск обработчиков
        self.handler_commands.handle()
        self.handlerP_all_text.handle()
