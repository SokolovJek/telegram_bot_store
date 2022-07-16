# KeyboardButton - модуль обеспечивает формирование разметки интерфейса,
# ReplyKeyboardMarkup - реализует настраиваемую клавиатуру
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    """Кдасс предназначен для создания и разметки интерфейса бота"""

    def __init__(self):
        """инициализирует менеджер для работы с БД"""
        self.markup = None
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        """создает и возвращает кнопку по входным параметрам"""
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
        от выбранной категории и возвращает разметкку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в инлайн-кнопки название из БД
        for item in self.BD.select_all_products_category(id_category):
            self.markup.add(self.set_inline_btn(item))
        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """Cоздаем и возвращаем инлайн-кнопку по входным параметрам"""
        return InlineKeyboardButton(str(name),  # вывод названия кнопки
                                    # перенаправляем в другую функцию ID товара,
                                    # она будет добавлять выбранный товар в заказ
                                    # т.е. тоесть при нажатии, получаем ID
                                    callback_data=str(name.id))
