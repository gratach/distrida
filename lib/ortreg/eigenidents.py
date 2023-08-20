def eigenidents(reg):
	pubks = reg["a#gpg#pub"]
	privs = reg["a#gpg#priv"]
	r = {}
	for idio, idi in reg["ai"].items():
		binich = True
		keys = []
		for x in idi["inh"]["log"]:
			if x["typ"] == "pluskenn":
				gpg = pubks.get(x["inh"]["kenn"])
				if gpg:
					priv = privs.get(gpg["inh"]["privort"])
					if not priv:
						binich = False
						break
					keys.append(priv["inh"]["key"])
		if binich and keys != []:
			r[idio] = keys
	return r
