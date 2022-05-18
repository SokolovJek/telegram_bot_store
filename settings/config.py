import os
from emoji import emojize

with open('keys.txt', 'r', encoding='utf-8') as fp:
    key = fp.read().rstrip()

TOKEN = key
NAME_DB = 'products.db'
VERSION = '0.0.1'
AUTHOR = 'Sokolov Evgeniy'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_DB)

COUNT = 0

KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize(':wrench: Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфобрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize(':fast_reverse_button:'),
    '>>': emojize(':fast-forward_button:'),
    'BACK_STEP': emojize(':play_button:'),
    'NEXT_STEP': emojize(':reverse_button:'),
    'ORDER': emojize(':check_mark_button: Заказ'),
    'X': emojize(':cross_mark_button:'),
    'DOWN': emojize(':down_arrow:'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize(':up_arrow:'),
    'APPLY': emojize(':check_box_with_check: Оформить заказ'),
    'COPY': emojize(':copyright:')
}

CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3
}

COMMANDS = {
    'START': 'start',
    'HELP': 'help'
}


