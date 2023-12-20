change = False
total = 0
rules = {}


def validate(rule):
    if "<" in rule[0]:
        var, val = rule[0].split("<")
        return rule[1] if d[var] < int(val) else None
    if ">" in rule[0]:
        var, val = rule[0].split(">")
        return rule[1] if d[var] > int(val) else None
    return rule


for i in range(17):
    line = input()
    if not change:
        if not line:
            change = True
        else:
            inp, out = line.split("{")
            out = out[:-1].split(",")
            rule = []
            for data in out:
                if ":" in data:
                    a,b = data.split(":")
                    rule.append((a,b))
                else:
                    rule.append(data)

            rules[inp] = rule

    else:
        datas = line[1:-1].split(",")

        d = {}

        for data in datas:
            a,b = data.split("=")
            d[a] = int(b)

        current = "in"

        while current not in "AR":#("A","R")
            for rule in rules[current]:
                test = validate(rule)
                if test:
                    current = test
                    break

        if current == "A":
            total += sum(d.values())

print(total) # 353046
