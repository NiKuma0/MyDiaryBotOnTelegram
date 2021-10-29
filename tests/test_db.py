import unittest, os, datetime as dt
from app import db

DIR = os.path.dirname(os.path.abspath(__file__))

class TestBD(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = db.DB(os.path.join(DIR, 'db.test'))
        cls.db.create_table()
    
    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(os.path.join(DIR, 'db.test'))

    def setUp(self) -> None:
        self.diary = db.Diary
        self.diary.DB = self.db
        obj = self.diary(1, dt.datetime.now(), 'test')
        obj.save()

    def test_getall(self):
        req = self.diary.all()
        self.assertEqual(len(req), 1)

    def test_delete(self):
        self.diary.all()[0].delete()
        print('deleted')
        self.assertEqual(len(self.diary.all()), 0)
