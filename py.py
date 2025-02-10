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
    for i in dbfr["books"]:
        if i == name:
            dbfr["books"].pop(name)
            break

    print("not found")


selector(["Add Books", "Remove Books"], [addBooks, delBooks])
dbw.write(json.dumps(dbfr))
