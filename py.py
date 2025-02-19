import json

try:
	db = json.load(open("db.json"))
except (FileNotFoundError, json.JSONDecodeError):
	db = {"books": {}, "users": {"root": {"admin": True}}}


def selector(ls, funcs, key=""):
	for k in range(0, len(ls)):
		print(k, ":", ls[k])

	try:
		c = int(input("choose"))
		if c >= len(ls) or c < 0:
			print("not in range")
		else:
			try:
				funcs[c](key)
			except TypeError:  # errors as control flow are bad but wtv
				funcs[c]()
	except ValueError:  # also catches letters in pgs lmfao
		print("enter a no")


def dump():
	dbw = open("db.json", "w")
	dbw.write(json.dumps(db))


def addKey(key):
	global curUser
	name = input("name")
	dc = {}
	if name not in db[key] and name != "":
		if key == "books":
			pgs = int(input("pages"))
			gen = input("genres (separated by spaces)").split()
			dc = {"pages": pgs, "genres": gen, "borrowed": False}
		elif key == "users":
			dc = {"admin": False, "borrowed": []}
			if curUser == "":
				curUser = name

		db[key].update({name: dc})
	else:
		print(f"{key} already exists")


def delKey(key):
	name = input("name")
	try:
		db[key].pop(name)
	except KeyError:
		print(f"{name} not found in {key}")


def upKey(key):
	global curUser
	oname = ""
	tmp = {}
	try:
		if key == "books":
			oname = input("name")
			tmp = db[key][oname]
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
			if db[key][curUser]["admin"]:
				oname = input("name")
			else:
				oname = curUser

		nname = input("new name") or oname

		db[key].pop(oname)
		db[key].update({nname: tmp})

	except KeyError:
		print(f"{oname} not found in {key}")


def listKeys(key):
	for i in db[key]:
		print(i)


def search(key):
	search = input("search").lower()
	k = True
	for i in db[key]:
		if search in i.lower():
			k = False
			print("found", i)
	if k:
		print("not found")


def borrow():
	name = input("name")
	if name in db["books"] and not db["books"][name]["borrowed"]:
		db["books"][name].update({"borrowed": True})
		db["users"][curUser]["borrowed"].append(name)
	else:
		print(f"{name} not borrowable")


def ret():
	name = input("name")
	if name in db["users"][curUser]["borrowed"] and db["books"][name]["borrowed"]:
		db["books"][name].update({"borrowed": False})
		db["users"][curUser]["borrowed"].remove(name)
	else:
		print(f"{name} not borrowed")


curUser = ""
inside = False


def outside():
	global inside
	inside = False


def login():
	name = input("name")
	if name in db["users"]:
		global curUser
		curUser = name


def logout():
	global curUser
	curUser = ""


def books():
	global inside
	inside = True

	destr = ["Back", "Search Books", "List Books"]
	defunc = [outside, search, listKeys]

	while inside:
		if curUser != "" and db["users"][curUser]["admin"]:
			selector(destr + ["Add Books", "Remove Books", "Update Books"], defunc + [addKey, delKey, upKey], "books")
		elif curUser != "":
			selector(destr + ["Borrow Books", "Return Books"], defunc + [borrow, ret], "books")
		else:
			selector(destr, defunc, "books")


def users():
	global inside
	inside = True

	destr = ["Back", "Sign Up Users"]
	defunc = [outside, addKey]

	while inside:
		if curUser == "":
			selector(destr + ["Login"], defunc + [login], "users")
			outside()
		elif curUser != "" and db["users"][curUser]["admin"]:
			selector(destr + ["Remove Users", "Update Users", "Search Users", "Log Out"], defunc + [delKey, upKey, search, logout], "users")
		else:
			selector(["Update Info", "Log Out"], [upKey, logout], "users")


def die():
	print("ty for using ig")
	exit()


while True:
	dump()
	selector(["Exit", "Books", "Users"], [die, books, users])
