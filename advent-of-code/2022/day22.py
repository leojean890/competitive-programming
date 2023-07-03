
def getNext(instruction, dir):
    if dir == 0:
        if instruction == "R":
            return 1
        if instruction == "L":
            return 3
    if dir == 1:
        if instruction == "R":
            return 2
        if instruction == "L":
            return 0
    if dir == 2:
        if instruction == "R":
            return 3
        if instruction == "L":
            return 1
    if dir == 3:
        if instruction == "R":
            return 0
        if instruction == "L":
            return 2

lines = []

while 1:

    line = input()
    if line == "":
        break
    else:
        if len(lines) > 0 and len(line) < len(lines[0]):
            line += (len(lines[0]) - len(line))*" "
        lines.append(line)


instructions = input()

print(lines)
print(instructions)

current, y, x, dir = 0, 0, lines[0].index("."), 0

while current < len(instructions):
    nxt = current
    while nxt+1 < len(instructions) and instructions[nxt+1].isdigit():
        nxt += 1

    print((y, x), dir)
    toMove = int(instructions[current:nxt+1])
    nb = 0
    if dir == 0:
        while lines[y][(x+1)%len(lines[0])] in (".", " ") and nb <= toMove:
            if lines[y][(x+1)%len(lines[0])] == ".":
                nb += 1
                x = (x + 1) %len(lines[0])
            else:
                currX = x
                while lines[y][(currX+1)%len(lines[0])] == " ":
                    currX = (currX + 1) %len(lines[0])
                if lines[y][(currX+1)%len(lines[0])] == ".":
                    x = (currX + 1) %len(lines[0])
                else:
                    break


    if dir == 1:
        while lines[(y+1)%len(lines)][x] in (".", " ") and nb <= toMove:
            if lines[(y+1)%len(lines)][x] == ".":
                nb += 1
                y = (y+1)%len(lines)
            else:
                currY = y
                while lines[(currY + 1) % len(lines)][x] == " ":
                    currY = (currY + 1) % len(lines)

                if lines[(currY + 1) % len(lines)][x] == ".":
                    y = (currY + 1) % len(lines)
                else:
                    break

    if dir == 2:
        while lines[y][(x-1)%len(lines[0])] in (".", " ") and nb <= toMove:
            if lines[y][(x-1)%len(lines[0])] == ".":
                nb += 1
                x = (x - 1) %len(lines[0])
            else:
                while lines[y][(x-1)%len(lines[0])] == " ":
                    x = (x - 1) %len(lines[0])

                currX = x
                while lines[y][(currX-1)%len(lines[0])] == " ":
                    currX = (currX - 1) %len(lines[0])
                if lines[y][(currX-1)%len(lines[0])] == ".":
                    x = (currX - 1) %len(lines[0])
                else:
                    break

    if dir == 3:
        while lines[(y-1)%len(lines)][x] in (".", " ") and nb <= toMove:
            if lines[(y-1)%len(lines)][x] == ".":
                nb += 1
                y = (y-1)%len(lines)
            else:
                currY = y
                while lines[(currY-1)%len(lines)][x] == " ":
                    currY = (currY-1)%len(lines)
                if lines[(currY - 1) % len(lines)][x] == ".":
                    y = (currY - 1) % len(lines)
                else:
                    break

    current = nxt+1
    if current < len(instructions):
        dir = getNext(instructions[current], dir)
    current += 1


print(y+1, x+1, dir)
print(1000*(y+1) + 4*(x+1) + dir)
