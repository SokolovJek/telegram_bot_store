from os import path

from sqlalchemy import create_engine  # необхадим для подключения к БД
# через этот метод мы выполняем создания сессии(через сессии ORM  взаимодействует с БД)
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base  # необхадим для подключения к БД

from settings import config
from models.product import Products


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
