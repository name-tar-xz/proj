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
    dbfr["books"].update({name: {}})


def delBooks():
    name = input("name")
    try:
        dbfr["books"].pop(name)
    except KeyError:
        print("not found")


ctrl = 0


def die():
    global ctrl
    ctrl = 1


while ctrl == 0:
    selector(["Add Books", "Remove Books", "exit"], [addBooks, delBooks, die])

dbw.write(json.dumps(dbfr))
