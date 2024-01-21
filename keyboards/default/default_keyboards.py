import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class DefaultKeyboards:

    @property
    def detail_pay(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        detail = KeyboardButton("Do'konimiz haqida")
        pay = KeyboardButton("Muddatli to'lov")
        keyboard.add(detail, pay)
        return keyboard

    @property
    def pay_first_pay_btns(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        first_pay = KeyboardButton("Birinchi to'lovni o'zgartirish")
        pay = KeyboardButton("Muddatli to'lov")
        see_again = KeyboardButton("Qayta ko'rish")
        keyboard.add(pay, first_pay, see_again)
        return keyboard

