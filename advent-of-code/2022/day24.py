from collections import deque

lines = []
blizzards = set()
blizzardsPos = set()
walls = set()
i = 0
while 1:
    try:
        line = input()
        lines.append(line)
        for j in range(len(line)):
            if (line[j] in "<>^v"):
                blizzards.add((i, j, line[j]))
                blizzardsPos.add((i, j))
            elif line[j] == "#":
                walls.add((i, j))

        i += 1

    except Exception as ex:
        break

print(blizzards)
start = (0,1)
end = (len(lines)-1,len(line)-2)

print(start, end)

step = 0
q = deque()
q.appendleft((start,0))
visited = set()
currentDepth = -1
while q:
    (y,x), depth = q.pop()

    if (y,x) == end and step in (0,2):
        print(depth)
        if step == 2:
            exit()
        step = 1
        q = deque()
        q.appendleft((end, depth))
        visited = set()
        currentDepth = depth
        (y, x), depth = q.pop()

    if (y,x) == start and step == 1:
        print(depth)
        step = 2
        q = deque()
        q.appendleft((start, depth))
        visited = set()
        currentDepth = depth
        (y, x), depth = q.pop()

    if depth > currentDepth:
        nblizzards = set()
        blizzardsPos = set()
        for (i,j,dir) in blizzards:
            if dir == "<":
                if (i, j-1) not in walls:
                    nblizzards.add((i,j-1,dir))
                    blizzardsPos.add((i, j-1))
                else:
                    nblizzards.add((i,len(line)-2,dir))
                    blizzardsPos.add((i, len(line)-2))
            elif dir == ">":
                if (i, j+1) not in walls:
                    nblizzards.add((i,j+1,dir))
                    blizzardsPos.add((i,j+1))
                else:
                    nblizzards.add((i,1,dir))
                    blizzardsPos.add((i,1))
            elif dir == "^":
                if (i-1, j) not in walls:
                    nblizzards.add((i-1,j,dir))
                    blizzardsPos.add((i-1,j))
                else:
                    nblizzards.add((len(lines)-2, j, dir))
                    blizzardsPos.add((len(lines)-2, j))
            elif dir == "v":
                if (i+1, j) not in walls:
                    nblizzards.add((i+1,j,dir))
                    blizzardsPos.add((i+1,j))
                else:
                    nblizzards.add((1,j,dir))
                    blizzardsPos.add((1,j))
        blizzards = nblizzards

        currentDepth = depth

    for (a,b) in ((y+1,x),(y-1,x),(y,x+1),(y,x-1),(y,x)):
        if (a,b) not in blizzardsPos and (a,b) not in walls and (step == 1 or a > -1) and (step != 1 or a < len(lines)) and (a,b,depth+1) not in visited:
            q.appendleft(((a,b), depth+1))
            visited.add((a,b,depth+1))
