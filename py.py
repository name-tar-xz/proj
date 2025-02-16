import json

try:
    dbfr = json.load(open("test.json"))
except (FileNotFoundError, json.JSONDecodeError):
    dbfr = {"books": {}}


def selector(ls, funcs):
    for k in range(0, len(ls)):
        print(k + 1, ":", ls[k])

    try:
        c = int(input("choose")) - 1
        if c >= len(ls) or c < 0:
            print("not in range")
        else:
            funcs[c]()
    except ValueError:  # also catches letters in pgs lmfao
        print("enter a no")


def dump():
    dbw = open("test.json", "w")
    dbw.write(json.dumps(dbfr))


def addBooks():
    name = input("name")
    if name not in dbfr["books"]:
        pgs = int(input("pages"))
        gen = input("genres (separated by spaces)").split()
        dbfr["books"].update({name: {"pages": pgs, "genres": gen}})
    else:
        print("book already exists")


def delBooks():
    name = input("name")
    try:
        dbfr["books"].pop(name)
    except KeyError:
        print("not found")


def upBooks():
    oname = input("name")

    try:
        tmp = dbfr["books"][oname]

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

        nname = input("new name") or oname

        dbfr["books"].pop(oname)
        dbfr["books"].update({nname: tmp})

    except KeyError:
        print("not found")


def listBooks():
    for i in dbfr["books"]:
        print(i)


def search():
    search = input("search").lower()
    k = True
    for i in dbfr["books"]:
        if search in i.lower():
            k = False
            print("found", i)
    if k:
        print("not found")


def die():
    print("ty for using ig")
    exit()


while True:
    dump()
    selector(
        ["Add Books", "Remove Books", "Update Books", "search", "List Books", "exit"],
        [addBooks, delBooks, upBooks, search, listBooks, die],
    )
