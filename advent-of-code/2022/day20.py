
list = []
while 1:
    try:
        list.append({"value":int(input())*811589153, "initCoord":len(list)})

    except Exception:
        break


n = len(list)
for iter in range(10):
    for i in range(n):

        for j in range(n):
            elt = list[j]
            if elt["initCoord"] == i:
                break
        value = list[j]["value"]

        elt = list[j]
        if value != 0:
            del list[j]
            list.insert((j + value) % (n-1), elt)

for v in range(len(list)):
    elt = list[v]
    if elt["value"] == 0:
        break

print(list[(v+1000)%n]["value"] + list[(v+2000)%n]["value"] + list[(v+3000)%n]["value"])
