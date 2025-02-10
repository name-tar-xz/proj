import json

# Find a less dum way to do this
# EVERYTHING BREAKS WITH NEWLINE IN JSON KILL ME
db = open("test.json", "r+")
dbfr = json.load(db)
db.seek(0)  # does smth evryth brokey wo it


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
    book = {"name": name}
    dbfr["books"].append(book)
    json.dump(dbfr, db)


selector(["Add Books"], [addBooks])
