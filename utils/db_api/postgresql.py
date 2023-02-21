from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
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
        telefon_raqami VARCHAR(15)NULL,
        telegram_id VARCHAR(12) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_buildings(self):
        sql = """
        CREATE TABLE IF NOT EXISTS bino(
        id SERIAL PRIMARY KEY,
        qaysi_viloyatda varchar(50), 
        bino_nomi VARCHAR(255) NOT NULL,
        bino_manzili VARCHAR(255) NOT NULL,
        bino_sigimi VARCHAR(5) NOT NULL,
        masul_shaxs VARCHAR(100) NOT NULL,
        telefon_raqami VARCHAR(15) NOT NULL,
        telegram_id VARCHAR(12) NULL,
        FOREIGN KEY (qaysi_viloyatda) REFERENCES viloyatlar(viloyat_nomi)
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_outcasts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS outcasts(
        id SERIAL INTEGER,
        total INTEGER(6) NOT NULL,
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_exams(self):
        sql = """
        CREATE TABLE IF NOT EXISTS imtihon(
        id SERIAL UNIQUE,
        viloyat_nomi VARCHAR (50) NOT NULL,
        student_present VARCHAR(10) NOT NULL,
        student_absent VARCHAR(10) NULL,
        student_removed VARCHAR(10) NULL,
        supervisor_present VARCHAR(10) NOT NULL,
        supervisor_absent VARCHAR(10) NOT NULL,
        FOREIGN KEY (viloyat_nomi) REFERENCES viloyatlar(viloyat_nomi)
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

    async def add_info_about_exam(self, viloyat_nomi, student_present, student_absent,
                                  student_removed, supervisor_present, supervisor_absent):
        sql = "INSERT INTO imtihon(viloyat_nomi, student_present, student_absent, student_removed, supervisor_present, supervisor_absent) \
               VALUES($1, $2, $3, $4, $5, $6);"
        await self.execute(sql, viloyat_nomi, student_present, student_absent, student_removed, supervisor_present,
                           supervisor_absent, execute=True)

    async def get_info_about_exam(self):
        sql = "SELECT * FROM imtihon"
        await self.execute(fetch=True)

    # yangi bino qo'shish
    async def add_building(self, qaysi_viloyatda, bino_nomi, bino_manzili, bino_sigimi, masul_shaxs, telefon_raqami,
                           telegram_id):
        sql = "INSERT INTO bino(qaysi_viloyatda, bino_nomi, bino_manzili, bino_sigimi, masul_shaxs, telefon_raqami, telegram_id) " \
              "VALUES ($1, $2, $3, $4, $5, $6, $7)"
        return await self.execute(sql, qaysi_viloyatda, bino_nomi, bino_manzili, bino_sigimi, masul_shaxs,
                                  telefon_raqami, telegram_id, execute=True)

    # yangi viloyat qo'shish
    async def add_region(self, viloyat_nomi, masul_shaxs, telefon_raqami, telegram_id):
        sql = "INSERT INTO viloyatlar(viloyat_nomi, masul_shaxs, telefon_raqami, telegram_id) VALUES " \
              "($1, $2, $3, $4)"
        return await self.execute(sql, viloyat_nomi, masul_shaxs, telefon_raqami, telegram_id, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
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
