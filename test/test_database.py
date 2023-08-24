import sys, os; rootpath = os.path.join(os.path.dirname(__file__), ".."); sys.path.append(rootpath)
import unittest

from src.distrida.pfade import Ort, Blick
from src.distrida.ortreg import nochfrei, reserviere, Kind, Database, artvon, finDing
from json import load, dump
from sys import argv
import os
import sys
from tempfile import TemporaryDirectory
class DatabaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tempdir = TemporaryDirectory()
        self._db = Database(self._tempdir.name)
    def __del__(self):
        self._tempdir.cleanup()
    def test_load_kind_kind(self):
        thing = self._db["a"]
        self.assertIsNotNone(thing)
    def test_load_kindtree_kind(self):
        thing = self._db["ab"]
        self.assertIsNotNone(thing)
    def test_load_owningtree_kind(self):
        thing = self._db["ah"]
        self.assertIsNotNone(thing)
    def test_load_freedomcone_kind(self):
        thing = self._db["af"]
        self.assertIsNotNone(thing)
    def test_load_dispenser_kind(self):
        thing = self._db["as"]
        self.assertIsNotNone(thing)
    def test_load_non_existing(self):
        self.assertRaises(Exception, lambda: self._db["non_existing"])
    def test_free(self):
        a = self._db["a"]
        hb = self._db["h"]
        for x in a.liste():
            for y in x.liste():
                hb.beanspruche(y._orts)
        self.assertTrue(self._db.frei("#blub"))
        self.assertFalse(self._db.frei("s"))
    def test_write_text(self):
        self._db["t#est"] = "Halloho"
        self._db["t#test"] = "Hida"
    def test_setUp(self):
        db = self._db
        #regi.speicher("dump.yaml")
        print(db.ansicht())
        print(db.artvon("$"))
        print(db.artvon("$/fe"))
        Text = db["at"]
        self.assertTrue(True)
        #t = Text("hihi")
if __name__ == '__main__':
    unittest.main()
