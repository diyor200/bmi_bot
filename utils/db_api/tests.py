import asyncio
import pandas as pd
from utils.db_api.postgresql import Database

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


async def get_admins(db: Database):
    return list(await db.get_admin())


class Storing:
    def __init__(self):
        self.admin = []
        self.db = Database()

    async def get_admins(self, db: Database):
        self.admin = list(await db.get_admin())
        return self.admin

    def d(self):
        self.admin = await self.get_admins(self.db)
        return self.admin


print(Storing().d())


# db = Database()
# s = Storing()
# royhat = await s.get_admin(db)

async def test():
    db = Database()
    await db.create()
    await db.create_table_admins()
    #
    # print("Users jadvalini yaratamiz...")
    # # await db.drop_users()
    # await db.create_table_users()
    # print("Yaratildi")
    #
    # print("Foydalanuvchilarni qo'shamiz")
    #
    # await db.add_user("anvar", "sariqdev", 123456789)
    # await db.add_user("olim", "olim223", 12341123)
    # await db.add_user("1", "1", 131231)
    # await db.add_user("1", "1", 23324234)
    # await db.add_user("John", "JohnDoe", 4388229)
    # print("Qo'shildi")
    lists = []
    # adminlar = [5697570359, 'Diyorbek']
    # print(type(adminlar[0]))
    # users = await db.add_admin(adminlar[0], adminlar[1])
    admins = await Storing().get_admin(db)
    print(admins)
    # telegram_ids = await db.selcet_user_id()
    # for i in telegram_ids:
    #     print(i[0])
    # text = ""
    for i in await Storing().get_admin(db):
        # print(i[0])
        print(i[1])
    await db.add_admin(admin_id=1257550701, name='testdan so\'ng')
    for i in await Storing().get_admin(db):
        # print(i[0])
        print(i[1])

    # await db.add_admin()
        # id = i[0]
        # viloyat_nomi = i[1]
        # student_present = i[2]
        # student_absent = i[3]
        # student_removed = i[4]
        # supervisor_present = i[5]
        # supervisor_absent = i[6]
        # lists.append((id, viloyat_nomi, student_present, student_absent, student_removed,
        #               supervisor_present, supervisor_absent))
        # # username = users[i]
        # # telegram_id = users[i][3]
        # lists.append((table_id))
        # text += f"{i}. {users[i][0]} {users[i][1]} {users[i][2]} {users[i][3]}\n"
        # print(f"Foydalanuvchilar: {users[i][0]} {users[i][1]} {users[i][2]} {users[i][3]}\n")
        # yield text
    # user = await db.select_user(id=1)
    # print(f"Foydalanuvchi: {user}")
    # print(lists)
    # df = pd.DataFrame(lists, columns=['id', 'viloyat_nomi', 'student_keldi', 'student_kelmadi',
    #                                   'student_chetlatildi', 'nazoratchi_keldi', 'nazoratchi_kelmadi'])
    # print(df)
# asyncio.run(test())
