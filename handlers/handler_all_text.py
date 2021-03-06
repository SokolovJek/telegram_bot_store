from handlers.handler import Handler
from settings import config
from settings.message import MESSAGES


class HandlerAllText(Handler):
    """
    Класс обрабатывает текстовые сообщения в зависимости от нажатия кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # step необхадим для поочередном обходе заказаных продуктов при отрисовки "Заказа"(ORDER)
        self.step = 0

    def pressed_btn_settings(self, message):
        """ Нстройки """
        self.bot.send_message(message.chat.id,
                              MESSAGES['settings'],
                              parse_mode='HTML',
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_info(self, message):
        """ О магазине """
        self.bot.send_message(message.chat.id,
                              MESSAGES['trading_store'],
                              parse_mode='HTML',
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_back(self, message):
        """ Обрабатывает входящее текстовое сообщение от нажатия на кнопку 'Назад' """
        self.bot.send_message(message.chat.id,
                              'Вы вернулись назад',
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_category(self, message):
        """ Обрабатывает входящее текстовое сообщение от нажатия на кнопку ' Выбрать товар' """
        self.bot.send_message(message.chat.id,
                              'Каталог категорий товара',
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id,
                              'Сделайте свой выбор',
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_product(self, message, product):
        """ Обрабатывает входящее текстовое сообщение от нажатия на кнопку 'Категории продукта' """
        self.bot.send_message(message.chat.id,
                              f'Категория {config.KEYBOARD[product]}',
                              reply_markup=self.keybords.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id,
                              'ОК',
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие сообщения от нажатия на кнопку "Заказ(ORDER)"
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])
        # отпровляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        :param product_id: ID продукта
        :param quantity: количество его в БД
        :param message: сообщение от переданное от бота
        """
        self.bot.send_message(message.chat.id,
                              MESSAGES['order_number'].format(self.step + 1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].format(self.BD.select_single_product_name(product_id),
                                                       self.BD.select_single_product_title(product_id),
                                                       self.BD.select_single_product_price(product_id),
                                                       self.BD.select_single_product_quantity(product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(self.step, quantity))

    def handle(self):
        """
        обработчик(декоратор) сообщений
        который обрабатывает входящие текстовые сообщения от нажатия кнопок
        """
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):

            # *** меню ****

            print(message.text)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['ORDER']:
                # если в БД есть заказ
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                # если нет, шлем смс 'у вас нет заказов и рендерим меню
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keybords.category_menu())

            # обработка конкретного выбора категории

            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:

                self.pressed_btn_product(message, 'ICE_CREAM')



            else:
                print(f'my ERROR from HandlerAllText {message.text}')
