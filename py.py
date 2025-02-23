import json
from time import time
from hashlib import blake2b

curUser = ""
inside = False

try:
	db = json.load(open("db.json"))
except FileNotFoundError:
	db = {"books": {}, "users": {"root": {"admin": True, "password": blake2b(b"root").hexdigest()}}}


def selector(ls, funcs, key=""):
	for k in range(0, len(ls)):
		print(k, ":", ls[k])

	try:
		c = int(input("Choose one of the above: "))
		if c >= len(ls) or c < 0:
			print("Entered number not in range")
		else:
			try:
				funcs[c](key)
			except TypeError:
				funcs[c]()
	except ValueError:
		print("Enter a valid number")


def dump():
	dbw = open("db.json", "w")
	dbw.write(json.dumps(db))


def addKey(key):
	global curUser
	name = input("Input name: ")
	dc = {}
	if name not in db[key] and name != "":
		if key == "books":
			pgs = int(input("Input no of pages: "))
			stock = int(input("Input stock: "))
			gen = input("Input genres (separated by spaces): ").split()
			author = input("Input author: ")
			dc = {"author": author, "pages": pgs, "genres": gen, "stock": stock, "borrowed": 0}
		elif key == "users":
			passwd = blake2b(input("Enter your password: ").encode()).hexdigest()
			dc = {"password": passwd, "admin": False, "borrowed": {}}
			if curUser == "":
				curUser = name

		db[key].update({name: dc})
	else:
		print(key, "already exists")


def delKey(key):
	name = input("Input name to delete: ")
	try:
		db[key].pop(name)
	except KeyError:
		print(name, "not found in", key)


def upKey(key):
	global curUser
	oname = ""
	tmp = {}
	try:
		if key == "books":
			oname = input(f"Enter {key} to modify: ")
			nname = input("Enter new name (blank for no change): ") or oname
			tmp = db[key][oname]
			for i in tmp:
				new = input(f"Enter new {i} (blank for no change): ")
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
				oname = input(f"Enter {key} to modify: ")
				admin = input("Make user admin (y/n): ")
			else:
				oname = curUser

			nname = input("Enter new username (blank for no change): ") or oname
			curUser = nname

			tmp = db[key][oname]
			try:
				tmp["admin"] = (admin.lower() == "yes" or "y") and True or False
			except UnboundLocalError:
				pass

			for i in tmp:
				if i != "admin":
					new = input(f"Enter new {i} (leave blank for no change): ")
					if new != "":
						if i == "password":
							tmp[i] = blake2b(new.encode()).hexdigest()
						else:
							tmp[i] = new
						new = ""

		db[key].pop(oname)
		db[key].update({nname: tmp})
		dump()

	except KeyError:
		print(oname, "not found in", key)


def listKeys(key):
	for i in db[key]:
		print(i)


def search(key):
	search = input("Enter search term: ").lower()
	k = True
	for i in db[key]:
		if search in i.lower():
			k = False
			print("Found:", i)
	if k:
		print(search, "not found")


def borrow():
	name = input("Book to borrow: ")
	if name in db["books"] and db["books"][name]["stock"]:
		db["books"][name].update({"borrowed": db["books"][name]["borrowed"] + 1})
		db["books"][name].update({"stock": db["books"][name]["stock"] - 1})
		db["users"][curUser]["borrowed"].update({name: int(time())})
	else:
		print(name, "is not borrowable")


def ret():
	name = input("Book to return: ")
	if name in db["users"][curUser]["borrowed"] and db["books"][name]["borrowed"]:
		t = int(time()) - db["users"][curUser]["borrowed"][name]
		due = 7 * 24 * 60 * 60  # 1 week
		if t > due:
			print(f"Please pay late fine of {500 * (t // due)}")

		db["books"][name].update({"borrowed": db["books"][name]["borrowed"] - 1})
		db["books"][name].update({"stock": db["books"][name]["stock"] + 1})
		db["users"][curUser]["borrowed"].pop(name)
	else:
		print(name, "has not been borrowed")


def outside():
	global inside
	inside = False


def login():
	name = input("Username: ")
	passwd = blake2b(input("Password: ").encode()).hexdigest()
	if name in db["users"] and passwd == db["users"][name]["password"]:
		global curUser
		curUser = name
	else:
		print("Failed to login")


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
	print("Thank you for using")
	exit()


users()

while True:
	dump()
	selector(["Exit", "Books", "Users"], [die, books, users])
