import json

try:
    dbfr = json.load(open("test.json"))
except FileNotFoundError:
    dbfr = {"books": {}}

dbw = open("test.json", "w")


def selector(ls, funcs):
    for k in range(0, len(ls)):
        print(k + 1, ":", ls[k])

    c = int(input("choose")) - 1

    if c >= len(ls) or c < 0:
        print("not in range")
        selector(ls, funcs)
    else:
        funcs[c]()


def addBooks():
    name = input("name")
    pgs = input("pages")
    gen = input("genres (separated by spaces)")
    dbfr["books"].update({name: {"pages": pgs, "genres": gen.split()}})


def delBooks():
    name = input("name")
    try:
        dbfr["books"].pop(name)
    except KeyError:
        print("not found")


def upBooks():
    oname = input("name")

    try:
        tmp = dbfr["books"].get(oname)
        dbfr["books"].pop(oname)

        for i in tmp:
            new = input("Enter new " + i + " (leave blank for no change)")
            if new != "":
                tmp[i] = new
                new = ""

        nname = input("new name")
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
    dbw.write(json.dumps(dbfr))
    print("ty for using ig")
    exit()


while True:
    selector(
        ["Add Books", "Remove Books", "Update Books", "search", "List Books", "exit"],
        [addBooks, delBooks, upBooks, search, listBooks, die],
    )
