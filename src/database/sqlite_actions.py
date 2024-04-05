from .base import BaseCRUD, DBException
from .models import UserCRUDModel
from ..models.user_model import UserData

import sqlite3


class CRUDActions(BaseCRUD):
    db = sqlite3.connect('./src/database/db.sqlite')


    @classmethod
    def create_table(cls) -> None:
        conn = cls.db.cursor()

        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (uid int, username text);''')
            cls.db.commit()
        finally:
            conn.close()
    
    
    @classmethod 
    def check_user_in_db(cls, user: UserData) -> bool:
        try:
            cls.select_user(user)
        except DBException:
            return False 
        return True 


    @classmethod
    def add_user(cls, user: UserData) -> None:
        conn = cls.db.cursor()
        uid = user.uid
        username = user.username

        try:
            print(f'INSERT INTO users (uid, username) VALUES ({uid}, {username});')
            conn.execute(f'INSERT INTO users (uid, username) VALUES ({uid}, "{username}");')
            cls.db.commit()
        finally:
            conn.close()


    @classmethod
    def select_user(cls, user: UserData) -> UserCRUDModel:
        conn = cls.db.cursor()
        uid = user.uid
        
        try:
            conn.execute(f'SELECT uid, username FROM users WHERE uid == {uid};')
            data = conn.fetchone()
        finally:
            conn.close()
        
        try:    
            result = UserCRUDModel(uid=data[0], username=data[1])
        except:
            raise DBException('user {uid} not in database')
        else:
            return result
