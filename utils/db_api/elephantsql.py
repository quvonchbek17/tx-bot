import os

import urllib.parse as up
import psycopg2

from data import config

class Database:
	
    def __init__(self):
        self.pool = None

    async def connention(self):
        return psycopg2.connect(
            host = config.DB_HOST,
            database=config.DB_NAME,
            user = config.DB_USER,
            password = config.DB_PASS
        )
        
    async def execute(self, command, fetchall: bool = False, fetchone: bool = False, execute: bool = False):
        connection = await self.connention()
        cursor = connection.cursor()
        cursor.execute(command)
        if fetchall:
            result = cursor.fetchall()
        elif fetchone:
            result = cursor.fetchone()
        elif execute:
            result = "Successfully executed"
        connection.commit()
        cursor.close()
        connection.close()
        return result
        
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql+';', tuple(parameters.values())
    
    # commands for botusers
    async def add_user(self, user_chat_id):
        sql = f"""
        INSERT INTO botusers (user_chat_id) VALUES($1);
        """
        return await self.execute(sql, user_chat_id, execute=True)
 
    async def select_all_users(self):
        sql = "SELECT * FROM botusers;"
        return await self.execute(sql, fetchall=True)
    
    async def select_user(self, **kwargs):
        sql = "SELECT * FROM botusers WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def count_users(self):
        sql = "SELECT COUNT(*) FROM botusers;"
        return await self.execute(sql, fetchone=True)
    
    async def update_language(self, user_chat_id, language):
        sql = f"""
        UPDATE botusers SET user_language=$1 WHERE user_chat_id=$2;
        """
        return await self.execute(sql, user_chat_id, language, execute=True)
    
    async def update_user_full_name(self, user_chat_id, user_full_name):
        sql = f"""
        UPDATE botusers SET user_full_name=$1 WHERE user_chat_id=$2;
        """
        return await self.execute(sql, user_chat_id, user_full_name, execute=True)
    
    async def update_user_phone_number(self, user_chat_id, phone_number):
        sql = f"""
        UPDATE botusers SET user_phone_number=$1 WHERE user_chat_id=$2;
        """
        return await self.execute(sql, execute=True)
    
    async def update_username(self, user_chat_id, username):
        sql = f"""
        UPDATE botusers SET username=$1 WHERE user_chat_id=$2;
        """
        return await self.execute(sql, execute=True)
    
    async def update_user_group_id(self, user_chat_id, group_id):
        if group_id is None:
            sql = f"""
            UPDATE botusers SET user_group_id=NULL WHERE user_chat_id=$1;
            """
            return await self.execute(sql, user_chat_id, execute=True)
        else:
            sql = f"""
            UPDATE botusers SET user_group_id=$1 WHERE user_chat_id=$2;
            """
            return await self.execute(sql, user_chat_id, group_id, execute=True)
    
    async def delete_user(self, user_chat_id):
        sql = f"""
        DELETE FROM botusers WHERE user_chat_id=$1;
        """
        return await self.execute(sql, user_chat_id, execute=True)
    
    # select commands
    
    async def select_all_universities(self):
        sql = "SELECT * FROM universities;"
        return await self.execute(sql, fetchall=True)
    
    async def select_university(self, **kwargs):
        sql = "SELECT * FROM universities WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def select_faculties(self, **kwargs):
        sql = "SELECT * FROM faculties WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def select_directions(self, **kwargs):
        sql = "SELECT * FROM directions WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def select_groups(self, **kwargs):
        sql = "SELECT * FROM groups WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def select_schedules(self, **kwargs):
        sql = "SELECT * FROM schedules WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def select_courses(self):
        sql = "SELECT * FROM courses;"
        return await self.execute(sql, fetchall=True)
    
    async def select_course(self, **kwargs):
        sql = "SELECT * FROM courses WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    # commands for botadmins
    async def select_all_botadmins(self):
        sql = "SELECT * FROM botadmins;"
        return await self.execute(sql, fetchall=True)
    
    async def select_botadmin(self, **kwargs):
        sql = "SELECT * FROM botadmins WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def add_botadmin(self, admin_chat_id):
        sql = f"""
        INSERT INTO botadmins (admin_chat_id) VALUES ($1);
        """
        return await self.execute(sql, admin_chat_id, execute=True)
    
    async def count_botadmins(self):
        sql = "SELECT COUNT(*) FROM botadmins;"
        return await self.execute(sql, fetchone=True)
    
    async def delete_botadmin(self, admin_chat_id):
        sql = f"""
        DELETE FROM botadmins WHERE admin_chat_id=$1;
        """
        return await self.execute(sql, admin_chat_id, execute=True)
    
    async def update_botadmin_language(self, admin_chat_id, language):
        sql = f"""
        UPDATE botadmins SET admin_language=$1 WHERE admin_chat_id=$2;
        """
        return await self.execute(sql, admin_chat_id, language, execute=True)
    
    async def update_botadmin_full_name(self, admin_chat_id, admin_full_name):
        sql = f"""
        UPDATE botadmins SET admin_full_name=$1 WHERE admin_chat_id=$2;
        """
        return await self.execute(sql, admin_chat_id, admin_full_name, execute=True)
    
    async def update_botadmin_phone_number(self, admin_chat_id, phone_number):
        sql = f"""
        UPDATE botadmins SET admin_phone_number=$1 WHERE admin_chat_id=$2;
        """
        return await self.execute(sql, admin_chat_id, phone_number, execute=True)
    
    async def update_botadmin_username(self, admin_chat_id, username):
        sql = f"""
        UPDATE botadmins SET admin_username=$1 WHERE admin_chat_id=$2;
        """
        return await self.execute(sql, admin_chat_id, username, execute=True)
    
    async def update_botadmin_group_id(self, admin_chat_id, faculty_id):
        sql = f"""
        UPDATE botadmins SET admin_faculty_id=$1 WHERE admin_chat_id=$2;
        """
        return await self.execute(sql, admin_chat_id, faculty_id, execute=True)
    
    # fakultetdan keyin kursni tanlasa keladigan yo'nalishlar uchun so'rov
    async def select_direcrions_signup(self, course_id, faculty_id):
        sql = f"""
        select DISTINCT d.direction_id, d.direction_name from directions d
        inner join
        mix m on m.direction_id = d.direction_id
        where m.course_id = $1 and d.faculty_id = $2;
        """
        return await self.execute(sql, course_id, faculty_id, fetchall=True)
    
    # yo'nalishni tanlab ta'lim shkalini tanlagandan keladigan guruhlar uchun so'rov
    async def select_groups_signup(self, course_id, direction_id, education_id):
        sql = f"""
        select g.group_id, g.group_name from groups g
        inner join
        mix m on m.group_id = g.group_id
        where m.course_id = $1 and m.direction_id = $2 and
        education_id = $3;
        """
        return await self.execute(sql, course_id, direction_id, education_id, fetchall=True)
    
    async def select_all_education(self):
        sql = """
        SELECT * FROM education;
        """
        return await self.execute(sql, fetchall=True)
    
    async def select_education(self, **kwargs):
        sql = "SELECT * FROM education WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)
    
    async def select_mix(self, **kwargs):
        sql = "SELECT * FROM mix WHERE "
        sql = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, fetchall=True)