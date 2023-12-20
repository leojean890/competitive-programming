def validate(rule, dUnapplyCond, dApplyCond):
    if "<" in rule[0]:
        var, val = rule[0].split("<")
        val = int(val)
        a, b = dUnapplyCond[var]

        if val > b:
            dUnapplyCond[var] = (-1,-1)
            return rule[1], dUnapplyCond, dApplyCond

        if a <= val <= b:
            dApplyCond[var] = (a,val-1)
            dUnapplyCond[var] = (val,b)
            return rule[1], dUnapplyCond, dApplyCond

        dApplyCond[var] = (-1, -1)
        return rule[1], dUnapplyCond, dApplyCond

    if ">" in rule[0]:
        var, val = rule[0].split(">")
        val = int(val)
        a, b = dUnapplyCond[var]

        if val > b:
            dApplyCond[var] = (-1,-1)
            return rule[1], dUnapplyCond, dApplyCond

        if a <= val <= b:
            dUnapplyCond[var] = (a,val)
            dApplyCond[var] = (val+1,b)
            return rule[1], dUnapplyCond, dApplyCond

        dUnapplyCond[var] = (-1, -1)
        return rule[1], dUnapplyCond, dApplyCond

    return rule, dUnapplyCond, dApplyCond


def dfs(d,current):
    if current == "A":
        res = 1
        for (m,M) in d.values():
            if m != -1:
                res *= (M-m+1)
        return res

    if current == "R":
        return 0

    M = 0
    for rule in rules[current]:
        dApplyCond = {}
        for k, v in d.items():
            dApplyCond[k] = v
        dUnapplyCond = {}
        for k, v in d.items():
            dUnapplyCond[k] = v
        ncurrent, dUnapplyCond, dApplyCond = validate(rule, dUnapplyCond, dApplyCond)
        M += dfs(dApplyCond, ncurrent)
        d = dUnapplyCond

    return M


change = False
rules = {}

for i in range(707):
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

print(dfs({"s":(1,4000),"m":(1,4000),"a":(1,4000),"x":(1,4000)},"in")) # 125355665599537

