from handlers.handler_com import HandlerCommands
from handlers.handler_all_text import HandlerAllText
from handlers.handler_inline_query import HandlerInlineQuery


class HandlerMain:
    """
    класс компановщик, здесь происходит инициализация
    и запуск основных обработчиков событий нашего бота
    """

    def __init__(self, bot):
        # получаем нашего бота
        self.bot = bot

        # здесь будет инициализация обработчиков

        # обрабатывает /start
        self.handler_commands = HandlerCommands(self.bot)

        # обрабатывает настроки, инфо, <<
        self.handlerP_all_text = HandlerAllText(self.bot)

        # обрабатывае inline_query(нажатие на продукт для его заказа)
        self.handler_inline_query = HandlerInlineQuery(self.bot)

    def handle(self):
        # здесь запуск обработчиков
        self.handler_commands.handle()
        self.handlerP_all_text.handle()
        self.handler_inline_query.handle()
