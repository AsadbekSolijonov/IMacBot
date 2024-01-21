import logging
import sqlite3


class Database:
    def __init__(self):
        try:
            url_db = '/Users/asadbeksolijonov/Bots/imac/database.db'
            self.connection = sqlite3.connect(url_db)
            self.cursor = self.connection.cursor()
        except Exception as e:
            logging.warning("Ma'lumotlar ba'zasiga ulanishda xatolik yuz beradi!")


class Users(Database):
    def __init__(self):
        super().__init__()
        self.create_table()

    def create_table(self):
        with self.connection:
            sql = """
            CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY NOT NULL,
            price REAL)
            """
            self.cursor.execute(sql)

    async def insert_price(self, chat_id, price, *ignore, crud='insert'):
        with self.connection:
            if crud == 'insert':
                sql = """
                INSERT INTO users (chat_id, price) VALUES (:chat_id, :price)
                """
            elif crud == 'update':
                sql = """
                UPDATE users SET price = :price WHERE chat_id = :chat_id
                """
            params = {'chat_id': chat_id, 'price': price}
            self.cursor.execute(sql, params)

    async def select_price(self, chat_id):
        sql = """
        SELECT price FROM users WHERE chat_id = :chat_id
        """
        params = {'chat_id': chat_id}
        datas = self.cursor.execute(sql, params).fetchone()
        return datas[0] if datas else None


class SalePresent(Database):
    def __init__(self):
        super().__init__()
        self.create_table()

    def create_table(self):
        with self.connection:
            sql = """
            CREATE TABLE IF NOT EXISTS sale_present (
            chat_id INTEGER PRIMARY KEY NOT NULL,
            month_4 REAL,
            month_6 REAL,
            month_8 REAL)
            """
            self.cursor.execute(sql)

    def insert_one_month(self, month_value, month=None, *ignore, crud='insert'):
        with self.connection:
            if crud == 'insert':
                sql = f"""INSERT INTO sale_present (chat_id, '{month}')
                VALUES (:chat_id, :month_value);
                """
            elif crud == 'update':
                sql = f"""UPDATE sale_present SET '{month}'=:month_value WHERE chat_id = :chat_id;
                """
            params = {"chat_id": 1, "month_value": month_value}
            self.cursor.execute(sql, params)

    def select_presents(self):
        sql = """
        SELECT month_4, month_6, month_8 FROM sale_present
        """
        data = self.cursor.execute(sql).fetchone()
        return data if data else None


if __name__ == '__main__':
    Database()
    Users()
    sp = SalePresent()
    sp.insert_one_month(month_value=42, month='month_4', crud='update')
