import aiosqlite


class Repo:
    def __init__(self, db_file="db.db"):
        self.db_file = db_file

    async def create_table(self):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    open BOOLEAN,
                    photo TEXT,
                    screenshot TEXT,
                    text TEXT,
                    payment TEXT,
                    payment_com TEXT
                )
            ''')
            await db.commit()

    async def add_record(self, user_id, open_, photo=None, screenshot=None, text=None, payment=None, payment_com=None):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.cursor()
            await cursor.execute('''
                INSERT INTO records (user_id, open, photo, screenshot, text, payment, payment_com)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, open_, photo, screenshot, text, payment, payment_com))
            await db.commit()
            # Получите ID вставленной записи
            record_id = cursor.lastrowid

            # Затем, если нужно, выполните SELECT для получения данных вставленной записи
            await cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
            inserted_record = await cursor.fetchone()

            return inserted_record

    async def add_screen(self, value, id: int):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''
                UPDATE records
                SET screenshot=?
                WHERE id=?
            ''', (value, id))
            await db.commit()

    async def add_text(self, value, id: int):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''
                UPDATE records
                SET text=?
                WHERE id=?
            ''', (value, id))
            await db.commit()

    async def get_record(self, record_id):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute('''
                SELECT * FROM records WHERE id=?
            ''', (record_id,))
            return await cursor.fetchone()

    async def get_all_records(self, open_: bool, id):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute('''
                SELECT * FROM records WHERE open=? AND user_id=?
            ''', (open_, id))
            return await cursor.fetchall()

    async def check(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute('''
                SELECT COUNT(*) FROM records WHERE user_id=? AND open=1
            ''', (user_id,))
            count = await cursor.fetchone()
            print(count)
            return count[0] != 4

    async def set_all_records_close(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                """
                UPDATE records
                SET open=0
                WHERE open=1 AND user_id=?
                """,
                (user_id,)  # Предоставьте значение для заполнителя
            )
            await db.commit()

    async def add_record_screen(self, user_id, open_, photo=None, screenshot=None, text=None, payment=None, payment_com=None):
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.cursor()
            await cursor.execute('''
                INSERT INTO records (user_id, open, photo, screenshot, text, payment, payment_com)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, open_, photo, screenshot, text, payment, payment_com))
            await db.commit()
            # Получите ID вставленной записи
            record_id = cursor.lastrowid

            # Затем, если нужно, выполните SELECT для получения данных вставленной записи
            await cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
            inserted_record = await cursor.fetchone()

            return inserted_record