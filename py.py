import json
import time
import hashlib

curUser = ""
inside = False

try:
	db = json.load(open("db.json"))
except FileNotFoundError:
	db = {"books": {}, "users": {"root": {"admin": True, "password": hashlib.md5(b"root").hexdigest()}}}


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
			stock = int(input("stock"))
			gen = input("genres (separated by spaces)").split()
			author = input("author")
			dc = {"author": author, "pages": pgs, "genres": gen, "stock": stock, "borrowed": 0}
		elif key == "users":
			passwd = hashlib.md5(input("password").encode()).hexdigest()
			dc = {"password": passwd, "admin": False, "borrowed": {}}
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
			nname = input("new name") or oname
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
			global curUser
			if db[key][curUser]["admin"]:
				oname = input("name")
				admin = input("admin")
			else:
				oname = curUser

			nname = input("new name") or oname
			curUser = nname

			tmp = db[key][oname]
			try:
				tmp["admin"] = (admin.lower() == "yes" or "y") and True or False
			except UnboundLocalError:
				pass

			for i in tmp:
				if i != "admin":
					new = input(f"Enter new {i} (leave blank for no change)")
					if new != "":
						if i == "password":
							tmp[i] = hashlib.md5(new.encode()).hexdigest()
						else:
							tmp[i] = new
						new = ""

		db[key].pop(oname)
		db[key].update({nname: tmp})
		dump()

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
	if name in db["books"] and db["books"][name]["stock"]:
		db["books"][name].update({"borrowed": db["books"][name]["borrowed"] + 1})
		db["books"][name].update({"stock": db["books"][name]["stock"] - 1})
		db["users"][curUser]["borrowed"].update({name: int(time.time())})
	else:
		print(f"{name} not borrowable")


def ret():
	name = input("name")
	if name in db["users"][curUser]["borrowed"] and db["books"][name]["borrowed"]:
		t = int(time.time()) - db["users"][curUser]["borrowed"][name]
		due = 7 * 24 * 60 * 60  # 1 week
		if t > due:
			print(f"Please pay late fine of {500 * (t // due)}")

		db["books"][name].update({"borrowed": db["books"][name]["borrowed"] - 1})
		db["books"][name].update({"stock": db["books"][name]["stock"] + 1})
		db["users"][curUser]["borrowed"].pop(name)
	else:
		print(f"{name} not borrowed")


def outside():
	global inside
	inside = False


def login():
	name = input("name")
	passwd = hashlib.md5(input("passwd").encode()).hexdigest()
	if name in db["users"] and passwd == db["users"][name]["password"]:
		global curUser
		curUser = name
	else:
		print("failed")


def logout():
	global curUser
	curUser = ""


def books():
	dump()
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
	dump()
	global inside
	inside = True

	destr = ["Back", "Sign Up Users"]
	defunc = [outside, addKey]

	while inside:
		if curUser == "":
			selector(["Continue Logged Out", "Sign Up", "Login"], [outside, addKey, login], "users")
			outside()
		elif curUser != "" and db["users"][curUser]["admin"]:
			selector(destr + ["Remove Users", "Update Users", "Search Users", "Log Out"], defunc + [delKey, upKey, search, logout], "users")
		else:
			selector(destr + ["Update Info", "Log Out"], defunc + [upKey, logout], "users")


def die():
	print("ty for using ig")
	exit()


users()

while True:
	dump()
	selector(["Exit", "Books", "Users"], [die, books, users])
