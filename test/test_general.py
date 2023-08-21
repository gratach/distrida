#!/usr/bin/env python3
#reserviere: art [wunschpfad] -> reservierter_pfad

import unittest

from src.distrida.pfade import Ort, Blick
from src.distrida.ortreg import nochfrei, reserviere, Art, Register, artvon, finDing
from json import load, dump
from sys import argv
import os
import sys
class GeneralTest(unittest.TestCase):
    def test_setUp(self):
        self.registerjsonpath = os.path.join(os.path.dirname(__file__), "..", "register.json")
        regi = Register(self.registerjsonpath)
        a = regi["a"]
        hb = regi["h"]
        regi["t#est"] = "Halloho"
        regi["t#test"] = "Hida"
        for x in a.liste():
            for y in x.liste():
                hb.beanspruche(y._orts)
        regi.speicher("dump.json")
        print(regi.ansicht())
        print(regi.frei("#blub"))
        print(regi.frei("s"))
        print(regi.artvon("$"))
        print(regi.artvon("$/fe"))
        Text = regi["at"]
        self.assertTrue(True)
        #t = Text("hihi")"""
if __name__ == '__main__':
    unittest.main()
