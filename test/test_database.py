import sys, os; rootpath = os.path.join(os.path.dirname(__file__), ".."); sys.path.append(rootpath)
import unittest

from src.distrida.address_system import Ort, Blick
from src.distrida.ortreg import nochfrei, reserviere, Kind, Database, artvon, finDing
from json import load, dump
from sys import argv
import os
import sys
from tempfile import TemporaryDirectory
class AlwaysPassingTest(unittest.TestCase):
    def test_passing(self):
        self.assertTrue(True)
class DatabaseTest(unittest.TestCase):
    def test_load_kind_kind(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            thing = db[Ort("a")]
            self.assertIsNotNone(thing)
    def test_load_kindtree_kind(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            thing = db[Ort("ab")]
            self.assertIsNotNone(thing)
    def test_load_owningtree_kind(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            thing = db[Ort("ah")]
            self.assertIsNotNone(thing)
    def test_load_freedomcone_kind(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            thing = db[Ort("af")]
            self.assertIsNotNone(thing)
    def test_load_dispenser_kind(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            thing = db[Ort("as")]
            self.assertIsNotNone(thing)
    def test_load_non_existing(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            self.assertRaises(Exception, lambda: db["non_existing"])
    def test_free(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            a = db["a"]
            hb = db["h"]
            for x in a.liste():
                for y in x.liste():
                    hb.beanspruche(y._orts)
            self.assertTrue(db.frei("#blub"))
            self.assertFalse(db.frei("s"))
    def test_write_text(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            db["t#est"] = "Halloho"
            db["t#test"] = "Hida"
    def test_setUp(self):
        with TemporaryDirectory() as tempdir:
            db = Database(tempdir)
            #regi.speicher("dump.yaml")
            print(db.ansicht())
            print(db.artvon("$"))
            print(db.artvon("$/fe"))
            Text = db["at"]
            self.assertTrue(True)
            #t = Text("hihi")
if __name__ == '__main__':
    unittest.main()
