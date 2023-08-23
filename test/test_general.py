import sys, os; rootpath = os.path.join(os.path.dirname(__file__), ".."); sys.path.append(rootpath)
import unittest

from src.distrida.pfade import Ort, Blick
from src.distrida.ortreg import nochfrei, reserviere, Kind, Database, artvon, finDing
from json import load, dump
from sys import argv
import os
import sys
class GeneralTest(unittest.TestCase):
    def test_setUp(self):
        regi = Database()
        a = regi["a"]
        hb = regi["h"]
        regi["t#est"] = "Halloho"
        regi["t#test"] = "Hida"
        for x in a.liste():
            for y in x.liste():
                hb.beanspruche(y._orts)
        #regi.speicher("dump.yaml")
        print(regi.ansicht())
        self.assertTrue(regi.frei("#blub"))
        self.assertFalse(regi.frei("s"))
        print(regi.artvon("$"))
        print(regi.artvon("$/fe"))
        Text = regi["at"]
        self.assertTrue(True)
        #t = Text("hihi")"""
if __name__ == '__main__':
    unittest.main()
