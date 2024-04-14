from abc import ABC, abstractclassmethod


class DBException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'DBException: {self.message}'


class BaseCRUD(ABC):
    @abstractclassmethod
    def create_table(self):
        ...
        
    @abstractclassmethod
    def check_user_in_db(self):
        ...
    
    @abstractclassmethod
    def add_user(self):
        ...
    
    @abstractclassmethod
    def select_user(self):
        ...
    
    @abstractclassmethod
    def get_all_users(self):
        ...
