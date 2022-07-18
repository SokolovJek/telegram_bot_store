from os import path

from sqlalchemy import create_engine  # необхадим для подключения к БД
# через этот метод мы выполняем создания сессии(через сессии ORM  взаимодействует с БД)
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base  # необхадим для подключения к БД

from settings import config
from models.product import Products
from models.order import Order
from datetime import datetime
from settings import utility


class Singleton(type):
    """
    Патерн Singleton предоставляет мехонизм создания одного и только одного обьекта
    класса, и предоставления к нему глобальную точку доступа.
    Необхадима глобальная переменная  соединения и нужно постоянно проверять есть ли
    подключение к БД. Блогодаря Singleton создается соединение, если оно еще
    не было установленно, либо возвращается готовая ссылка.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        """
        в данном случае метокласс контролтрует чтоб для подчененного
        класса DBManager всегда создавался один и тотже обьект.
        """
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сессии и подключение к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()  # создаем обьект сессии
        if not path.isfile(config.DATABASE):
            # если отсутствует файл, то по декларативному подходу работы в SQLAlchemy
            # вызываем создание БД в ее исходном состоянии
            Base.metadata.create_all(self.engine)

    def select_all_products_category(self, category):
        """
        Возвращает все товары выбранной категории
        """
        result = self._session.query(Products).filter_by(
            category_id=category).all()
        self.close()
        return result

    def close(self):
        """закрываем сессию"""
        self._session.close()

    def _add_orders(self, quantity, product_id, user_id):
        """
        Метод создания и заполнения заказа. Проверяем наличие id товара
        в заказах если есть то обновляем количество товара в заказе, если нет то
        создаем новый заказ
        """
        # получаем список всех product_id
        all_id_product = self.select_all_product_id()
        # если список не пуст(есть данные), обновляем таблицу заказа.
        # Проверка совершался ли ранее такой заказ!
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)
            # необхадимо изменить количество товаара на складе
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
            # если данных нет, то создаем новый обьект заказа.
        else:
            print("data my data =======", type(quantity), type(product_id), type(user_id), end="\n")
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id(self):
        """Метод необхадим для вывода всех id продуктов в заказах"""
        result = self._session.query(Order.product_id).all()
        print('dbalchemy -> def select_all_product_id ===== ', result)
        self.close()
        # конвертируем результат в список([1,3,5,4])
        return utility._convert(result)

    def select_order_quantity(self, product_id):
        """
        Возвращает количество товара в заказе
        """
        result = self._session.query(Order.quantity).filter_by(product_id=product_id).one()
        self.close()
        return result.quantity

    def update_order_value(self, product_id, name, value):
        """
        Обновляет данные указанной позиции заказа
        в соответствии с номером товара - rownum(product_id)
        """
        self._session.query(Order).filter_by(product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_quantity(self, rownum):
        """
        Возвращает количество товара на складе
        в соответствии с номером товара - rownum(product_id)
        Этот номер определяется при выборе товара в интерфейсе
        :param rownum: product_id
        :return: количество товара
        """
        result = self._session.query(Products.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def update_product_value(self, rownum, name, value):
        """
        Обновляем количество товара на складе в соответствии с номером товара - rownum(product_id)
        :param rownum: product_id
        :param name: column_name
        :param value: quantity value
        """
        self._session.query(Products).filter_by(id=rownum).update({name: value})
        self._session.commit()
        self.close()

    # функции для состовления сообжения(MESSAGES) о заказе(product_order)

    def select_single_product_name(self, rownum):
        """
        Метод возвращает название товара
        :param rownum: id_product
        :return: название товара
        """
        result = self._session.query(Products.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_title(self, rownum):
        """
        Метод возвращает торговую марку товара
        :param rownum: id_product
        :return: возвращает торговую марку
        """
        result = self._session.query(Products.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        """
        Метод возвращает цену товара
        :param rownum: id_product
        :return: название товара
        """
        result = self._session.query(Products.price).filter_by(id=rownum).one()
        self.close()
        return result.price

    # работа с заказом

    def count_rows_order(self):
        """
        Метод который возвращает количество заказов в БД
        """
        result = self._session.query(Order).count()
        self.close()
        return result
