from time import process_time

start_time = process_time()
robots = []
W = 101
H = 103
N = 500
T = 20000
for i in range(N):
    p,v = input().split()
    x,y = [int(u) for u in p.split("=")[1].split(",")]
    vx,vy = [int(u) for u in v.split("=")[1].split(",")]
    robots.append({"x":x,"y":y,"vx":vx,"vy":vy})

for t in range(T):
    nrobots = []
    nbXEntre40et60 = 0
    neighbors = 0
    centre = 50

    positions = set()

    for i in range(N):
        robot = robots[i]
        nrobots.append({"x":(robot["x"]+robot["vx"])%W,"y":(robot["y"]+robot["vy"])%H,"vx":robot["vx"],"vy":robot["vy"]})
        positions.add((nrobots[-1]["x"],nrobots[-1]["y"]))
        if centre-12 < nrobots[-1]["x"] < centre+12:
            nbXEntre40et60 += 1
        if (nrobots[-1]["x"]-1,nrobots[-1]["y"]) in positions:
            neighbors += 1
        if (nrobots[-1]["x"]+1,nrobots[-1]["y"]) in positions:
            neighbors += 1
        if (nrobots[-1]["x"],nrobots[-1]["y"]-1) in positions:
            neighbors += 1
        if (nrobots[-1]["x"],nrobots[-1]["y"]+1) in positions:
            neighbors += 1

    robots = nrobots

    if nbXEntre40et60 > 250 and neighbors > 300:
        print(t,nbXEntre40et60, neighbors) # 7343 300 527
        lines = []
        for r in range(H):
            line = []
            for c in range(W):
                line.append(".")
            lines.append(line)
        for i in range(N):
            robot = robots[i]
            lines[robot["y"]][robot["x"]] = "X"
        for r in range(H):
            print("".join(lines[r]))

        for r in range(5):
            print()

print(process_time() - start_time)
