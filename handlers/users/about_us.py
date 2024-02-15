from loader import dp
from aiogram import types


@dp.message_handler(text=["Do'konimiz haqida"])
async def about_us(message: types.Message):
    url = 'media/docs/nasiya.docx'
    with open(url, 'rb') as doc:
        await message.answer_document(document=doc, caption="""Nasiya savdo shartlari\n\n<b>sana: 02/05/2024</b>\n\nBog'lanish uchun: \n💬Chat: @macshop_admin\n📞Tel: +998 (91) 797 91 13 \n<a href="https://t.me/macshop_uz">Telegram</a> | <a href="https://www.instagram.com/iseller.uz">Instagram</a>""")
