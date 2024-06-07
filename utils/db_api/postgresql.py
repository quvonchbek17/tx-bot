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

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item[0]} = '{item[1]}'" for item in parameters.items()
        ])
        return sql
    
    async def add_user(self, chat_id):
        sql = f"""
        INSERT INTO botusers (chat_id) VALUES ({chat_id});
        """
        return await self.execute(sql, fetchrow=True)
    
    async def select_all_users(self):
        sql = "SELECT * FROM botusers"
        return await self.execute(sql, fetch=True)
    
    async def select_user(self, **kwargs):
        sql = "SELECT * FROM botusers WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_user_ids(self):
        sql = "SELECT chat_id FROM botusers;"
        return await self.execute(sql, fetch=True)
    
    async def select_user_attribute(self, chat_id, target):
        sql = f"SELECT {target} from botusers WHERE chat_id={chat_id};"
        return await self.execute(sql, fetchval=True)
    
    async def select_language(self, chat_id):
        sql = f"SELECT language from botusers WHERE chat_id='{chat_id}';"
        return await self.execute(sql, fetchval=True)
    
    async def count_users(self):
        sql = "SELECT COUNT(*) FROM botusers"
        return await self.execute(sql, fetchval=True)

    async def update_language(self, chat_id, language):
        sql = f"""
        UPDATE botusers SET language='{language}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)

    async def update_user_full_name(self, chat_id, fullname):
        sql = f"""
        UPDATE botusers SET fullname='{fullname}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)

    async def update_user_phone(self, chat_id, phone):
        sql = f"""
        UPDATE botusers SET phone='{phone}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    async def update_username(self, chat_id, username):
        sql = f"""
        UPDATE botusers SET username='{username}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    async def update_user_group_id(self, chat_id, group_id):
        if group_id is None:
            sql = f"""
            UPDATE botusers SET group_id=NULL WHERE chat_id={chat_id};
            """
        else:
            sql = f"""
            UPDATE botusers SET group_id='{group_id}' WHERE chat_id={chat_id};
            """
        return await self.execute(sql, execute=True)
    
    async def delete_user(self, chat_id):
        sql = f"""
        DELETE FROM botusers WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    # select commands
    async def select_all_universities(self):
        sql = "SELECT * FROM universities"
        return await self.execute(sql, fetch=True)
    
    async def select_university(self, **kwargs):
        sql = "SELECT * FROM universities WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_faculties(self, **kwargs):
        sql = "SELECT * FROM faculties WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_directions(self, **kwargs):
        sql = "SELECT * FROM directions WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_groups(self, **kwargs):
        sql = "SELECT * FROM groups WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_schedules(self, **kwargs):
        sql = "SELECT * FROM schedules WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_courses(self):
        sql = "SELECT * FROM courses"
        return await self.execute(sql, fetch=True)
    
    async def select_course(self, **kwargs):
        sql = "SELECT * FROM courses WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    # commands for botadmins
    async def select_all_botadmins(self):
        sql = "SELECT * FROM botadmins;"
        return await self.execute(sql, fetch=True)
    
    async def select_admin_ids(self):
        sql = "SELECT chat_id FROM botadmins;"
        return await self.execute(sql, fetch=True)
    
    async def select_botadmin(self, **kwargs):
        sql = "SELECT * FROM botadmins WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_admin_lang(self, chat_id):
        sql = f"SELECT language from botadmins WHERE chat_id='{chat_id}';"
        return await self.execute(sql, fetchval=True)
    
    async def add_botadmin(self, chat_id):
        sql = f"""
        INSERT INTO botadmins (chat_id) VALUES ({chat_id});
        """
        return await self.execute(sql, execute=True)
    
    async def count_botadmins(self):
        sql = "SELECT COUNT(*) FROM botadmins"
        return await self.execute(sql, fetchval=True)
    
    async def delete_botadmin(self, chat_id):
        sql = f"""
        DELETE FROM botadmins WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    async def update_botadmin_language(self, chat_id, language):
        sql = f"""
        UPDATE botadmins SET language='{language}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    async def update_botadmin_full_name(self, chat_id, full_name):
        sql = f"""
        UPDATE botadmins SET fullname='{full_name}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    async def update_botadmin_phone(self, chat_id, phone):
        sql = f"""
        UPDATE botadmins SET phone='{phone}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    async def update_botadmin_username(self, chat_id, username):
        sql = f"""
        UPDATE botadmins SET username='{username}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    async def update_botadmin_group_id(self, chat_id, faculty_id):
        sql = f"""
        UPDATE botadmins SET faculty_id='{faculty_id}' WHERE chat_id={chat_id};
        """
        return await self.execute(sql, execute=True)
    
    # fakultetdan keyin kursni tanlasa keladigan yo'nalishlar uchun so'rov
    async def select_directions_signup(self, faculty_id):
        sql = f"""select name from directions where faculty_id = '{faculty_id}';"""
        return await self.execute(sql, fetch=True)
    # async def select_directions_signup(self, course_id, faculty_id):
    #     sql = f"""
    #     select DISTINCT d.direction_id, d.direction_name from directions d
    #     inner join
    #     mix m on m.direction_id = d.direction_id
    #     where m.course_id = '{course_id}' and d.faculty_id = '{faculty_id}';
    #     """
    #     return await self.execute(sql, fetch=True)
    
    
    # yo'nalishni tanlab ta'lim shkalini tanlagandan keladigan guruhlar uchun so'rov
    async def select_groups_signup(self, faculty_id, course_id, direction_id, education_id):
        sql = f"""
        select id, created_at, updated_at, name from groups 
        where faculty_id = '{faculty_id}' and course_id = '{course_id}' and 
        direction_id = '{direction_id}' and education_id = '{education_id}';
        """
        return await self.execute(sql, fetch=True)
    
    async def select_group_id(self, name, faculty_id, direction_id, course_id, education_id):
        sql = f"""
        select id from groups 
        where name = '{name}' and faculty_id = '{faculty_id}' and direction_id = '{direction_id}' 
        and course_id = '{course_id}' and education_id = '{education_id}';
        """
        return await self.execute(sql, fetch=True)
    
    async def select_all_education(self):
        sql = """
        SELECT * FROM education
        """
        return await self.execute(sql, fetch=True)
    
    async def select_education(self, **kwargs):
        sql = "SELECT * FROM educations WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)
    
    async def select_mix(self, **kwargs):
        sql = "SELECT * FROM mix WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetch=True)

    # schedules jadvaliga aloqador so'rovlar
    async def select_time(self, day):
        sql = f"""SELECT t.id, t.name 
        FROM schedules AS s 
        LEFT JOIN times AS t ON s.time_id = t.id WHERE s.day = '{day}';
        """
        return await self.execute(sql, fetch=True)
    
    async def select_science(self, lesson_id):
        sql = f"""SELECT sc.name 
        FROM schedules AS s 
        LEFT JOIN sciences AS sc ON s.science_id = sc.id WHERE s.id = '{lesson_id}';
        """
        return await self.execute(sql, fetch=True)
    
    async def select_teacher(self, lesson_id):
        sql = f"""SELECT t.name 
        FROM schedules AS s 
        LEFT JOIN teachers AS t ON s.teacher_id = t.id WHERE s.id = '{lesson_id}';
        """
        return await self.execute(sql, fetch=True)
    
    async def select_room(self, lesson_id):
        sql = f"""SELECT r.name 
        FROM schedules AS s 
        LEFT JOIN rooms AS r ON s.room_id = r.id WHERE s.id = '{lesson_id}';
        """
        return await self.execute(sql, fetch=True)
    
    async def select_start_time(self, lesson_id):
        sql = f"""SELECT t.name 
        FROM schedules AS s 
        LEFT JOIN times AS t ON s.time_id = t.id WHERE s.id = '{lesson_id}';
        """
        return await self.execute(sql, fetch=True)