import asyncio

from .settings import PATH_DB
from datetime import datetime
import os, sqlite3 as sql
from typing import Any, List

exists_table = False

def create_con(path):
    if not os.path.exists(path):
        open(path, 'x').close()
    return sql.connect(path, detect_types=sql.PARSE_DECLTYPES|sql.PARSE_COLNAMES)

class DB:
    def __init__(self, path=PATH_DB) -> None:
        self.con = create_con(path)
        global exists_table
        if not exists_table:
            exists_table = True
            self.create_table()
        

    def excute(self, req: str, params: List[Any]=None) -> sql.Cursor:
        cur = self.con.cursor()
        if params:
            cur.execute(req, params)
        else:
            cur.execute(req)
        self.con.commit()
        res = list(cur)
        cur.close()
        return res

    def create_table(self):
        req = (
            'CREATE TABLE IF NOT EXISTS Diary('
            'chat_id INTEGER, '
            'dat TIMESTAMP, '
            'msg TEXT,'
            'id INTEGER PRIMARY KEY AUTOINCREMENT'
            ');'
        )
        self.excute(req)

class Diary:
    DB = DB()
    
    def __init__(self, chat_id: int=None, date: datetime=None, message: str=None, id: int=None) -> None:
        self.chat_id, self.date, self.message, self.id = chat_id, date, message, id

    # @property
    def get_fields(self):
        return self.chat_id, self.date, self.message

    def save(self):
        req = (
            'INSERT INTO Diary'
            '(chat_id, dat, msg) '
            'VALUES (?, ?, ?);'
        )
        fields = self.get_fields()
        return self.DB.excute(req, fields)
    
    @classmethod
    def all(cls, limit=None, expr: str=None) -> list:
        req = f'''SELECT * FROM Diary 
            GROUP BY dat
            {f'WHERE {expr}' if expr else ''}
            {f'LIMIT ?;' if limit else ';'}
            '''
        func = cls.DB.excute
        responce = func(req, (limit,)) if limit else func(req)
        return [cls(*args) for args in responce]
    
    def delete(self):
        req = '''DELETE FROM Diary WHERE id = ?;'''
        return self.DB.excute(req, (self.id,))

    def __repr__(self):
        return f'<Diary: id={self.id} >'



class Poll:
    poll = False

    def will_poll(self):
        return self.poll
    
    async def start(self):
        self.poll = True
        x = 1
        while self.will_poll():
            x += 1
            print(f'hello {x=}')
            await asyncio.sleep(1)
    
    async def stop(self):
        self.poll = True
