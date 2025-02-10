import json

# Find a less dum way to do this
# EVERYTHING BREAKS WITH NEWLINE IN JSON KILL ME
dbr = open("test.json", "r")
dbfr = json.load(dbr)
dbw = open("test.json", "w")


def selector(ls: list[str], funcs: list):
    if len(funcs) != len(ls):
        print("BOOM BOOM")

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
    dbfr["books"].update({name: {"pages": pgs}})


def delBooks():
    name = input("name")
    try:
        dbfr["books"].pop(name)
    except KeyError:
        print("not found")


def upBooks():
    oname = input("name")
    tmp = dbfr["books"].get(oname)

    try:
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


def search():
    search = input("search")
    k = True
    for i in dbfr["books"]:
        if search in i:
            k = False
            print("found", i)
    if k:
        print("not found")


ctrl = 0


def die():
    global ctrl
    ctrl = 1


while ctrl == 0:
    selector(
        ["Add Books", "Remove Books", "Update Books", "search", "exit"],
        [addBooks, delBooks, upBooks, search, die],
    )

dbw.write(json.dumps(dbfr))
