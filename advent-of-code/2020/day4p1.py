
keys = set()
counter = 0
cc = 0
for i in range(1159):
    l = input()
    if not l:
        for j in range(7):
            if j not in keys:
                cc += 1
                print(i)
                break
        else:
            counter += 1
        keys = set()
    for line in l.split():
        key, value = line.split(":")
        if "iyr" == key:
            keys.add(0)
        if "hgt" == key:
            keys.add(1)
        if "ecl" == key:
            keys.add(2)
        if "pid" == key:
            keys.add(3)
        if "byr" == key:
            keys.add(4)
        if "hcl" == key:
            keys.add(5)
        if "eyr" == key:
            keys.add(6)

for j in range(7):
    if j not in keys:
        break
else:
    counter += 1

print(counter, cc)
