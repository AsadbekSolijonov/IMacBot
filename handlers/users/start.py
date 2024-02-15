from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.default_keyboards import DefaultKeyboards
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    telegram_msg = f"Assalomu aleykum, {message.from_user.full_name}!\n\n"
    telegram_msg += """Ushbu bot Macshop.uz kanaling nasiya savdo boti hisoblanadi.
    \n1. Nasiya savdo shartlari bilan tanishib chiqing 
    \n2. Kanal orqali harid qilmoqchi bo'lgan maxsulotni tanlang
    \n3. Ushbu botga summani kiritish orqali hisoblang 
    \n4. Harid qilish uchun do'konimizga tashrif buyuring
    \n\nSavol va takliflar uchun:
    \n💬Chat: @macshop_admin
    \n📞Tel: +998 (91) 797 91 13"""

    url = 'media/image/logo.png'
    with open(url, 'rb') as pic:
        await message.answer_photo(photo=pic, caption=telegram_msg)
