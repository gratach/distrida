#!/usr/bin/env python3
#reserviere: art [wunschpfad] -> reservierter_pfad


from lib.pfade import Ort, Blick
from lib.ortreg import nochfrei, reserviere, Art, Register, artvon, finDing
from json import load, dump
from sys import argv
import os
import sys
def lade():
	with open("register.json", "r+") as f:
		j = load(f)
		print(reserviere(Ort.vonString(argv[1]), j))
		#f.seek(0)
		#dump(jr, f)
def test():
	regi = Register("register.json")
	a = Art(regi)
	t = regi["at"]("ttest", "Hallo, das ist ein Test")
	#print(t)
	for x in a.liste():
		print(x)
		for y in x.liste():
			print("	" + str(y))
	print(argv[1], "gehoert", regi.find("h").besitzer(argv[1]))
def meldeAlle():
	registerjsonpath = os.path.join(os.path.dirname(__file__), "register.json")
	regi = Register(registerjsonpath)
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
	#t = Text("hihi")
meldeAlle()
