from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        db_url = config.DATABASE_URL
        self.pool = await asyncpg.create_pool(
            db_url
            # user=config.DB_USER,
            # password=config.DB_PASS,
            # host=config.DB_HOST,
            # database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_regions(self):
        sql = """
        CREATE TABLE IF NOT EXISTS viloyatlar(
        id SERIAL PRIMARY KEY,
        viloyat_nomi VARCHAR(50) UNIQUE NOT NULL,
        masul_shaxs VARCHAR(100) NULL,
        telefon_raqami VARCHAR(15)NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_buildings(self):
        sql = """
        CREATE TABLE IF NOT EXISTS bino(
        id SERIAL PRIMARY KEY,
        qaysi_viloyatda integer not null, 
        bino_nomi VARCHAR(255) NOT NULL UNIQUE,
        bino_manzili VARCHAR(255) NOT NULL,
        bino_sigimi integer NOT NULL,
        masul_shaxs VARCHAR(100) NOT NULL,
        telefon_raqami VARCHAR(15) NOT NULL,
        telegram_id VARCHAR(12) NULL,
        FOREIGN KEY (qaysi_viloyatda) REFERENCES viloyatlar(id)
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_outcasts(self):
        sql = """
        create table IF NOT EXISTS outcasts(
        id serial primary key,
        viloyat_id integer not null,
        bino_id integer not null,
        ismi varchar(255) not null,
        sababi varchar(500),
        vaqti timestamp not null,
        FOREIGN KEY (viloyat_id) REFERENCES viloyatlar(id),
        FOREIGN KEY (bino_id) REFERENCES bino(id)
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_exams(self):
        sql = """
        CREATE TABLE IF NOT EXISTS imtihon(
        id SERIAL UNIQUE,
        viloyat_id integer NOT NULL,
        bino_id integer NOT NULL UNIQUE,
        student_present integer NOT NULL,
        student_absent integer NULL,
        student_removed integer NULL,
        supervisor_present integer NOT NULL,
        supervisor_absent integer NOT NULL,
        FOREIGN KEY (viloyat_id) REFERENCES viloyatlar(id),
        FOREIGN KEY (bino_id) REFERENCES bino(id)
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # chetlatilganlar jadvaliga ma'lumot qo'shish
    async def add_info_outcasts(self, viloyat_id, bino_id, ism, sabab):
        sql = """
        INSERT INTO outcasts (viloyat_id, bino_id, ismi, sababi, vaqti) 
        VALUES ($1, $2, $3, $4, date_trunc('minute', NOW() AT TIME ZONE 'Asia/Tashkent'))
        """
        return await self.execute(sql, viloyat_id, bino_id, ism, sabab, execute=True)

    # Barcha chetlatilgan talabalarni viloyatva binoga qarab olish
    async def get_all_outcasts_by_building(self, viloyat_id, bino_id):
        sql = """select * from outcasts where
                viloyat_id=$1 and bino_id=$2 order by ismi"""
        return await self.execute(sql, viloyat_id, bino_id, fetch=True)

    # Chetlatilgan talabani id siga qarab olish
    async def get_outcast_reason(self, vil_id, bino_id, id):
        sql = """select sababi from outcasts where
                    viloyat_id=$1 and bino_id=$2 and id=$3"""
        return await self.execute(sql, vil_id, bino_id, id, fetchrow=True)

    # Chetlatilgan talabani sababini o'zgartirish
    async def edit_outcast_reason(self, vid, bid, id, reason):
        sql = """update outcasts set sababi=$1 where
                 viloyat_id=$2 and bino_id=$3 and id=$4"""
        return await self.execute(sql, reason, vid, bid, id)

    # chetlatilgan talabalarni viloyatga qarab olish
    async def get_info_outcasts_by_region(self, viloyat_id):
        sql = """
        select bino.bino_nomi as bino_nomi, ismi, sababi, vaqti from outcasts
        join bino on bino.qaysi_viloyatda = outcasts.viloyat_id
        where outcasts.viloyat_id=$1 order by bino.bino_nomi asc
        """
        return await self.execute(sql, viloyat_id, fetch=True)

    # chetlatilgan talabalar ma'lumotini viloyat va binoga qarab olish
    async def get_info_outcasts_by_region_building(self, viloyat_id, bino_id):
        sql = """
        select viloyatlar.viloyat_nomi, bino.bino_nomi, outcasts.ismi, outcasts.sababi, outcasts.vaqti
        from outcasts join viloyatlar on viloyatlar.id = outcasts.viloyat_id
        join bino on bino.id = outcasts.bino_id
        where viloyat_id = $1 and bino_id=$2
        """
        return await self.execute(sql, viloyat_id, bino_id, fetch=True)

    async def get_info_outcasts_by_region_building_count(self, viloyat_id, bino_id):
        sql = "select count(id) from outcasts where viloyat_id=$1 and bino_id=$2"
        return await self.execute(sql, viloyat_id, bino_id, fetchrow=True)


    # imtihon natijalarini olish
    async def add_info_about_exam(self, viloyat_nomi, bino_nomi, student_present, student_absent,
                                  supervisor_present, supervisor_absent):
        # sql = "INSERT INTO imtihon(viloyat_id, bino_id, student_present, student_absent, student_removed, supervisor_present, supervisor_absent) \
        #        VALUES($1, $2, $3, $4, $5, $6);"
        sql = """
        insert into imtihon(viloyat_id, bino_id, student_present, student_absent, student_removed, supervisor_present, supervisor_absent)
        values ($1, $2, $3, $4, (select count(id) from outcasts), $5, $6)                                   
        on conflict (bino_id) do update
        set student_present = Excluded.student_present,
        student_absent = excluded.student_absent,
        supervisor_present = Excluded.supervisor_present,
        supervisor_absent = excluded.supervisor_absent;
        """
        return await self.execute(sql, viloyat_nomi, bino_nomi, student_present, student_absent,
                                  supervisor_present,
                                  supervisor_absent, execute=True)

    async def get_info_about_exam(self, viloyat_id, bino_id):
        sql = """
        SELECT viloyatlar.viloyat_nomi, bino.bino_nomi, imtihon.student_present, imtihon.student_absent, imtihon.student_removed,
        imtihon.supervisor_present, imtihon.supervisor_absent
        FROM imtihon
        JOIN bino ON bino.id = imtihon.bino_id
        JOIN viloyatlar ON viloyatlar.id = imtihon.id AND viloyatlar.id = bino.qaysi_viloyatda 
        where viloyatlar.id = $1 and bino.id = $2;
        """ 
        return await self.execute(sql, viloyat_id, bino_id, fetchrow=True)

    async def get_info_about_exam_by_region(self, viloyat_id):
        sql = """
        select (select viloyat_nomi from viloyatlar where viloyatlar.id=$1) as viloyat_nomi, sum(student_present) as keldi, sum(student_absent) as kelmadi,
        sum(student_removed) as chetlatildi, sum(supervisor_present) as s_keldi, sum(supervisor_absent) as s_kelmadi
        from imtihon where viloyat_id = $1
        """
        return await self.execute(sql, viloyat_id, fetchrow=True)

    # Bino nomini viloyatlarga qarab oladi
    async def get_bino_nomi_by_region(self, viloyat_nomi):
        sql = "select bino.bino_nomi from bino " \
              "join viloyatlar on viloyatlar.id = bino.qaysi_viloyatda where viloyatlar.viloyat_nomi=$1"
        return await self.execute(sql, viloyat_nomi, fetch=True)

    # yangi bino qo'shish
    async def add_building(self, qaysi_viloyatda, bino_nomi, bino_manzili, bino_sigimi, masul_shaxs, telefon_raqami):
        sql = "INSERT INTO bino(qaysi_viloyatda, bino_nomi, bino_manzili, bino_sigimi, masul_shaxs, telefon_raqami) " \
              "VALUES ($1, $2, $3, $4, $5, $6)"
        return await self.execute(sql, qaysi_viloyatda, bino_nomi, bino_manzili, bino_sigimi, masul_shaxs,
                                  telefon_raqami, execute=True)

    # bino nomlarini olish
    async def get_bino_nomi(self):
        sql = "SELECT bino_nomi FROM bino"
        return await self.execute(sql, fetch=True)

    # yangi viloyat qo'shish
    async def add_region_name(self, viloyat_nomi, masul_shaxs, telefon_raqami):
        sql = "INSERT INTO viloyatlar(viloyat_nomi, masul_shaxs, telefon_raqami) VALUES " \
              "($1, $2, $3)"
        return await self.execute(sql, viloyat_nomi, masul_shaxs, telefon_raqami, execute=True)

    # viloyatlarni olish
    async def get_viloyatlar_nomi(self):
        sql = "select viloyat_nomi from viloyatlar"
        return await self.execute(sql, fetch=True)

    # viloyat idisini olish
    async def get_region_id(self, viloyat_nomi):
        sql = "select id from viloyatlar where viloyat_nomi= $1"
        return await self.execute(sql, viloyat_nomi, fetchrow=True)

    # Bino idisini olish
    async def get_building_id(self, bino_nomi):
        sql = "select id from bino where bino_nomi= $1"
        return await self.execute(sql, bino_nomi, fetchrow=True)

    # yangi admin qo'shish
    async def add_admin(self, admin_id: int, name: str):
        sql = "INSERT INTO admins(admin_id, admin_name) VALUES ($1, $2)"
        return await self.execute(sql, admin_id, name, execute=True)

    # adminlar ro'yhatini olish
    async def get_admin(self):
        sql = "SELECT * FROM admins"
        return await self.execute(sql, fetch=True)

    # yangi foydalanuvchi qo'shish
    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user_id(self):
        sql = "SELECT telegram_id FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
