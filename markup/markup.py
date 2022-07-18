# KeyboardButton - модуль обеспечивает формирование разметки интерфейса,
# ReplyKeyboardMarkup - реализует настраиваемую клавиатуру
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Кдасс предназначен для создания разметки интерфейса бота
    и отрисовки ее.

     Здесь создается красота :) !
    """

    def __init__(self):
        """
        инициализирует менеджер для работы с БД
        """
        self.markup = None
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        """
        создает и возвращает кнопку по входным параметрам
        """
        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Создает разметку кнопок в основном меню
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')
        # расположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        return self.markup

    def info_menu(self):
        """
         Создает разметку кноапок в меню 'О магазине'
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        """
        Создает разметку кноапок в меню 'Настройки'
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def orders_menu(self, step, quantity):
        """
        Создает разметку кнопок в заказе товара("Заказ") и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X', step, quantity)
        itm_btn_2 = self.set_btn('DOWN', step, quantity)
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn_4 = self.set_btn('UP', step, quantity)

        itm_btn_5 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity)
        itm_btn_7 = self.set_btn('BACK_STEP', step, quantity)

        itm_btn_8 = self.set_btn('APPLY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)

        # расположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        self.markup.row(itm_btn_9, itm_btn_8)

        return self.markup

    @staticmethod
    def remove_menu():
        """
        Удаляет стартовое меню
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Создает разметку кнопок в меню 'Настройки'
        """
        self.markup = ReplyKeyboardMarkup(True, row_width=1)
        itm_btn_1 = self.set_btn('SEMIPRODUCT')
        itm_btn_2 = self.set_btn('GROCERY')
        itm_btn_3 = self.set_btn('ICE_CREAM')
        itm_btn_4 = self.set_btn('<<')
        itm_btn_5 = self.set_btn('ORDER')
        self.markup.add(itm_btn_1)
        self.markup.add(itm_btn_2)
        self.markup.add(itm_btn_3)
        self.markup.row(itm_btn_4, itm_btn_5)
        return self.markup

    def set_select_category(self, id_category):
        """
        Создает разметку инлайн-кнопок в зависимости
        от выбранной категории и возвращает собраную(финальную) in_line разметкку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в инлайн-кнопки название из БД
        for item in self.BD.select_all_products_category(id_category):
            self.markup.add(self.set_inline_btn(item))
        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Cоздаем и возвращаем инлайн-кнопку по входным параметрам
        :param name: обьект Продукта
        :return: возвращает in_line кнопку(с данными о продукте-вывод названия кнопки)
         с callback_data которая отрабатывает при нажАтии
         и передает ID продукта для дальнейшего добавления его в заказ
        """
        # callback_data срабатывает при нажатии на in_line кнопку(при нажатии, получаем ID),
        # а после обрабатываем(в ORDER)
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))
