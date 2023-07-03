
d = {}
while 1:
    try:
        a, b = input().split(": ")
        d[a] = int(b) if b.isdigit() else b

    except Exception:
        break

print(d["humn"])
print(d["root"])
d["humn"] = "xxxxx"
d["root"] = d["root"].replace("+", "-")
dd = d.copy()


for i in range(3006709229900, 3006730099830):# 3006709232464 dicho
    d = dd.copy()
    d["humn"] = i
    while type(d["root"]) == str:#enlever les casts
        for a,b in d.copy().items():
            if str == type(b):
                if " * " in b:
                    temp1, temp2 = b.split(" * ")
                    if type(d[temp1]) == int == type(d[temp2]):
                        d[a] = int(d[temp1]) * int(d[temp2])
                if " / " in b:
                    temp1, temp2 = b.split(" / ")
                    if type(d[temp1]) == int == type(d[temp2]):
                        d[a] = int(d[temp1]) // int(d[temp2])
                if " + " in b:
                    temp1, temp2 = b.split(" + ")
                    if type(d[temp1]) == int == type(d[temp2]):
                        d[a] = int(d[temp1]) + int(d[temp2])
                    #else:
                    #    print(a, d[temp1], d[temp2])
                if " - " in b:
                    temp1, temp2 = b.split(" - ")
                    if type(d[temp1]) == int == type(d[temp2]):
                        d[a] = int(d[temp1]) - int(d[temp2])
    print(i, d["root"])

    if d["root"] == 0:
        break


print(d["root"])
