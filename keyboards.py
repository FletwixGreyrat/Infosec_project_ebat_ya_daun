from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def startKb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("OSINT🖥️"))
    kb.insert(KeyboardButton("Антивирус🦠"))
    kb.add(KeyboardButton("Шифровщик/дешифровщик📄"))
    return kb


def otmenaOsint():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отмена🚫", callback_data="break"))
    return kb


def otmenaAntivirus():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отмена🚫", callback_data="break"))
    return kb


def otmenaKrypto():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Отмена🚫", callback_data="break"))
    return kb


def codeOrDecode():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Шифрование", callback_data="code:coding"))
    kb.add(InlineKeyboardButton(text="Дешифрование", callback_data="code:decode"))
    return kb