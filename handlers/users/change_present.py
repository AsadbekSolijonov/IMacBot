import logging

from aiogram import types

from data.config import ADMINS
from loader import dp
from utils.db_api.database import SalePresent


@dp.message_handler(commands=['change_present'])
async def change_present(message: types.Message):
    text = ("Foizlarni o'rzartirish bo'yicha yo'riqnoma:\n\n"
            "<b>Agar quyidagicha yozilsa:</b>\n"
            "<tg-spoiler><b>#4 35</b></tg-spoiler> - <i>4 oylik foiz 35 % ga</i> <b>O'ZGARADI.</b>\n"
            "<tg-spoiler><b>#6 35</b></tg-spoiler> - <i>6 oylik foiz 35 % ga</i> <b>O'ZGARADI.</b>\n"
            "<tg-spoiler><b>#8 35</b></tg-spoiler> - <i>8 oylik foiz 35 % ga</i> <b>O'ZGARADI.</b>\n\n")
    presents = SalePresent().select_presents()
    month_4, month_6, month_8 = (presents if presents else (0, 0, 0))
    text_now = (
        f"<pre>Hozirgi foizlar quyidagicha:\n\n"
        f"4 oylik foiz: {month_4}%\n"
        f"6 oylik foiz: {month_6}%\n"
        f"8 oylik foiz: {month_8}%</pre>")
    if str(message.chat.id) in ADMINS:
        await message.reply(text + text_now)
    else:
        await message.answer("Buni faqat adminlar ko'ra oladi!")


async def check_crud():
    data = SalePresent().select_presents()
    crud = 'update' if data else 'insert'
    return crud


async def change_month(message, month, repl=None):
    month_value = None
    try:
        month_value = float(message.text.replace(f'{repl}', '').strip())
        logging.warning(month_value)
    except Exception as e:
        await message.reply(
            f"⚠️ Foizni xato yozdingiz <tg-spoiler>{message.text}</tg-spoiler> emas.\nIltimos qaytadan harakat qiling!")
        return

    logging.warning(f"crud: {await check_crud()}")

    SalePresent().insert_one_month(month_value=month_value, month=month, crud=await check_crud())

    await message.answer(f"✅ <b>{month}</b>\n<b>{month_value}%</b> ga o'zgartirildi!\nKo'rish uchun: /change_present")


@dp.message_handler(lambda message: '#4' in message.text)
async def change_present(message: types.Message):
    await change_month(message=message, month='month_4', repl='#4')


@dp.message_handler(lambda message: '#6' in message.text)
async def change_present(message: types.Message):
    await change_month(message=message, month='month_6', repl='#6')


@dp.message_handler(lambda message: '#8' in message.text)
async def change_present(message: types.Message):
    await change_month(message=message, month='month_8', repl='#8')
