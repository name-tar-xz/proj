import json

try:
	dbfr = json.load(open("db.json"))
except (FileNotFoundError, json.JSONDecodeError):
	dbfr = {"books": {}, "users": {}}


def selector(ls, funcs, key=""):
	for k in range(0, len(ls)):
		print(k + 1, ":", ls[k])

	try:
		c = int(input("choose")) - 1
		if c >= len(ls) or c < 0:
			print("not in range")
		else:
			if key == "":
				funcs[c]()
			else:
				funcs[c](key)
	except ValueError:  # also catches letters in pgs lmfao
		print("enter a no")


def dump():
	dbw = open("db.json", "w")
	dbw.write(json.dumps(dbfr))


def addKey(key):
	name = input("name")
	if name not in dbfr[key]:
		if key == "books":
			pgs = int(input("pages"))
			gen = input("genres (separated by spaces)").split()
			dc = {"pages": pgs, "genres": gen}
		elif key == "users":
			dc = {}
		else:
			dc = {}

		dbfr[key].update({name: dc})
	else:
		print(f"{key} already exists")


def delKey(key):
	name = input("name")
	try:
		dbfr[key].pop(name)
	except KeyError:
		print(f"{name} not found in {key}")


def upKey(key):
	oname = input("name")

	try:
		tmp = dbfr[key][oname]

		if key == "books":
			for i in tmp:
				new = input(f"Enter new {i} (leave blank for no change)")
				if new != "":
					if i == "genres":
						tmp[i] = new.split()
					elif i == "pages":
						tmp[i] = int(new)
					else:
						tmp[i] = new
					new = ""
		elif key == "users":
			pass

		nname = input("new name") or oname

		dbfr[key].pop(oname)
		dbfr[key].update({nname: tmp})

	except KeyError:
		print(f"{oname} not found in {key}")


def listKeys(key):
	for i in dbfr[key]:
		print(i)


def search(key):
	search = input("search").lower()
	k = True
	for i in dbfr[key]:
		if search in i.lower():
			k = False
			print("found", i)
	if k:
		print("not found")


def books():
	selector(
		["Add Books", "Remove Books", "Update Books", "Search Books", "List Books"],
		[addKey, delKey, upKey, search, listKeys],
		"books",
	)


def users():
	selector(
		["Add Users", "Remove Users", "Update Users", "Search Users", "List Users"],
		[addKey, delKey, upKey, search, listKeys],
		"users",
	)


def die():
	print("ty for using ig")
	exit()


while True:
	dump()
	selector(["Books", "Users", "Exit"], [books, users, die])
