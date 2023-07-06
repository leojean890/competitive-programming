
keys = set()
counter = 0
cc = 0

def validateHgt(value):
    if value[-2:] == "cm" and len(value) == 5 and value[:3].isdigit() and 150 <= int(value[:3]) <= 193:
        return True
    if value[-2:] == "in" and len(value) == 4 and value[:2].isdigit() and 59 <= int(value[:2]) <= 76:
        return True

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
        if "iyr" == key and value.isdigit() and 2010 <= int(value) <= 2020:
            keys.add(0)
        if "hgt" == key and len(value) in (4,5) and validateHgt(value):
            keys.add(1)
        if "ecl" == key and value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
            keys.add(2)
        if "pid" == key and len(value) == 9 and all([i.isdigit() for i in value]):
            keys.add(3)
        if "byr" == key and value.isdigit() and 1920 <= int(value) <= 2002:
            keys.add(4)
        if "hcl" == key and len(value) == 7 and value[0] == "#" and all([i.isdigit() or i in "abcdef" for i in value[1:]]):
            keys.add(5)
        if "eyr" == key and value.isdigit() and 2020 <= int(value) <= 2030:
            keys.add(6)

for j in range(7):
    if j not in keys:
        break
else:
    counter += 1

print(counter, cc)#254 184
