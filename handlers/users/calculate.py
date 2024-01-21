import asyncio
import logging
import time

from aiogram.dispatcher import FSMContext

from handlers.users.calculate_class import Calculate
from keyboards.default.default_keyboards import DefaultKeyboards
from loader import dp, bot
from aiogram import types

from states.calculate_state import CalculateState
from utils.db_api.database import Users


@dp.message_handler(text=["Muddatli to'lov"])
async def calculate(message: types.Message):
    telegram_msg = "Olmoqchi bo'lgan tavaringizni to'liq narxini kiriting.\nMasalan$: 1000"
    await message.reply(telegram_msg)
    await CalculateState.calculation.set()


async def calculate_dry(message, total, first_pay=None):
    await message.answer(text=f"Marxamat!", reply_markup=DefaultKeyboards().pay_first_pay_btns)
    # mac
    mac = Calculate(price=total, pro_type='mac')
    await mac.send_msg(message=message, first_pay=first_pay)

    # iphone
    iphone = Calculate(price=total, pro_type='iphone')
    await iphone.send_msg(message=message, first_pay=first_pay, mac_iphone='Iphone')


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=CalculateState.calculation)
async def calculate_2(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # total price
    try:
        total = int(message.text)
        try:
            await Users().insert_price(chat_id=chat_id, price=total, crud='insert')
        except Exception as e:
            await Users().insert_price(chat_id=chat_id, price=total, crud='update')

    except Exception as e:
        message = await message.answer(f"To'lovni miqdori <tg-spoiler>{message.text}</tg-spoiler> emas!")
        return await calculate(message)

    await calculate_dry(message=message, total=total)

    await state.finish()


@dp.message_handler(text=["Muddatli to'lov", "Birinchi to'lovni o'zgartirish"])
async def change_first_pay(message: types.Message):
    msg = message.text
    if msg == "Muddatli to'lov":
        return await calculate(message)
    else:
        await message.answer("Birinchi to'lov summasini kiriting:")
        await CalculateState.first_pay.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=CalculateState.first_pay)
async def calculate_first_pay(message: types, state: FSMContext):
    chat_id = message.chat.id
    try:
        first_pay = int(message.text)
    except Exception as e:
        message = await message.answer(f"To'lovni miqdori <tg-spoiler>{message.text}</tg-spoiler> emas!")
        return await change_first_pay(message)
    total = await Users().select_price(chat_id=chat_id)

    await calculate_dry(message=message, total=total, first_pay=first_pay)

    await state.finish()


@dp.message_handler(text=["Qayta ko'rish"])
async def see_again(message: types.Message):
    chat_id = message.chat.id
    total = await Users().select_price(chat_id=chat_id)
    await calculate_dry(message, total=total)
