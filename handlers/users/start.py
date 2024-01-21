from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.default_keyboards import DefaultKeyboards
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    telegram_msg = f"Salom, {message.from_user.full_name}!\n\n"
    telegram_msg += (f"Bu bot orqali sotib olmoqchi bo'lgan "
                     f"tavaringizni boshlang'ich va muddatli "
                     f"narxlarini aniq bilib olishingiz mumkin.")

    await message.answer(text=telegram_msg, reply_markup=DefaultKeyboards().detail_pay)
