from loader import dp
from aiogram import types


@dp.message_handler(text=["Do'konimiz haqida"])
async def about_us(message: types.Message):
    telegram_msg = """Bizning do'kon Malika S56 do'kon bo'lib.\n\nBiz bu do'konda <b>Iphone</b> va <b>MacBook</b> sotamiz! Murojat uchun tel raqam: +998911779116
    """
    await message.answer(telegram_msg)
