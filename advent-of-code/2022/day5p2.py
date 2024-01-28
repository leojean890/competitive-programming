

v = True
stacks = []
lines = []
pos = {}

while 1:
    try:
        a = input()
        if len(a) == 0:
            v = False
            for i in range(1, 10):
                pos[i] = lines[-1].index(str(i))
                stacks.append([lines[x][pos[i]] for x in range(8) if lines[x][pos[i]] != " "])
        elif v:
            lines.append(a)
        else:
            move, frm, to = [int(i) for i in a.replace("move", "").replace("from", "").replace("to", "").split("  ")]
            frm -= 1
            to -= 1
            b = stacks[frm][:move]
            for x in reversed(b):
                stacks[to].insert(0, x)
            del stacks[frm][:move]
    except Exception as ex:
        break

print("".join([stack[0] for stack in stacks]))
