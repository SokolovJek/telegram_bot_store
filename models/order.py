from sqlalchemy import Column, Integer, ForeignKey, DateTime
from data_base.dbcore import Base
from sqlalchemy.orm import relationship, backref
from models.product import Products


class Order(Base):
    """
    Класс модель для описания таблици 'Заказ'
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)
    # для каскадного удаления данных из таблици
    category = relationship(Products,
                            backref=backref('orders',
                                            uselist=True,
                                            cascade='delete, all'
                                            ))

    def __str__(self):
        return f'{self.quantity}  {self.date}'
