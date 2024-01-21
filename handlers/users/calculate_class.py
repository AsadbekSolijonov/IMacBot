import asyncio

from utils.db_api.database import SalePresent


class Calculate:
    def __init__(self, price, *ignore, pro_type='mac'):
        self.total = price
        self.pro_type = pro_type
        if self.pro_type == 'mac':
            self.sale_present = 0.5
        elif self.pro_type == 'iphone':
            self.sale_present = 0.4

    def pro_type_price(self, first_pay=None):
        pay = first_pay if first_pay else self.total * self.sale_present
        presents = SalePresent().select_presents()
        presents = [present / 100 for present in presents]
        month_4, month_6, month_8 = presents if presents else 0

        mod = self.total - pay

        month_4 = mod / 4 + mod * month_4 / 4
        month_6 = mod / 6 + mod * month_6 / 6
        month_8 = mod / 8 + mod * month_8 / 8
        amounts = [pay, month_4, month_6, month_8]
        return amounts

    async def send_msg(self, message, first_pay=None, *ignore, mac_iphone='MacBook'):
        slp = 0.1
        amounts = self.pro_type_price(first_pay=first_pay) if first_pay else self.pro_type_price()
        message = await message.answer(
            f'<b>{mac_iphone}</b> - $ {self.total:,.0f}\n\n1. Birinchi to`lov: ${amounts[0]:,.0f}')
        await asyncio.sleep(slp)

        await message.edit_text(
            f'<b>{mac_iphone}</b> - $ {self.total:,.0f}\n\n1. Birinchi to`lov: ${amounts[0]:,.0f}\n2. 4 oy ga: ${amounts[1]:,.0f}')
        await asyncio.sleep(slp)

        await message.edit_text(
            f'<b>{mac_iphone}</b> - $ {self.total:,.0f}\n\n1. Birinchi to`lov: ${amounts[0]:,.0f}\n2. 4 oy ga: ${amounts[1]:,.0f}\n3. 6 oy ga: ${amounts[2]:,.0f}')
        await asyncio.sleep(slp)

        summary = f'<pre><b>{mac_iphone}</b> - $ {self.total:,.0f}\n\n1. Birinchi to`lov: ${amounts[0]:,.0f}\n2. 4 oy ga: ${amounts[1]:,.0f}\n3. 6 oy ga: ${amounts[2]:,.0f}\n4. 8 oy ga: ${amounts[3]:,.0f}</pre>'

        if first_pay:
            if mac_iphone == 'MacBook' and first_pay >= self.total * 0.5:
                await message.edit_text(summary)
            elif mac_iphone == 'MacBook' and first_pay < self.total * 0.5:
                summary = f'<pre><b>{mac_iphone}</b> - $ {self.total:,.0f}\n\nBoshlang`ich to`lov 50% dan kam bo`lmasligi kerak.</pre>'
                await message.edit_text(summary)
            elif mac_iphone == 'Iphone' and first_pay >= self.total * 0.4:
                await message.edit_text(summary)
            elif mac_iphone == 'Iphone' and first_pay < self.total * 0.4:
                summary = f'<pre><b>{mac_iphone}</b> - $ {self.total:,.0f}\n\nBoshlang`ich to`lov 40% dan kam bo`lmasligi kerak.</pre>'
                await message.edit_text(summary)
        else:
            await message.edit_text(summary)
