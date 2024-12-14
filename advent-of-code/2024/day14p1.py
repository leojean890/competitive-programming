from time import process_time

start_time = process_time()
robots = []
W = 101
H = 103
N = 500
T = 100
for i in range(N):
    p,v = input().split()
    x,y = [int(u) for u in p.split("=")[1].split(",")]
    vx,vy = [int(u) for u in v.split("=")[1].split(",")]
    robots.append({"x":x,"y":y,"vx":vx,"vy":vy})

for t in range(T):
    nrobots = []
    for i in range(N):
        robot = robots[i]
        nrobots.append({"x":(robot["x"]+robot["vx"])%W,"y":(robot["y"]+robot["vy"])%H,"vx":robot["vx"],"vy":robot["vy"]})
    robots = nrobots

a = 0
b = 0
c = 0
d = 0

for i in range(N):
    robot = robots[i]
    if robot["x"] < W//2 and robot["y"] < H//2:
        a += 1
    if robot["x"] < W//2 and H//2 < robot["y"] < H:
        b += 1
    if W//2 < robot["x"] < W and H//2 < robot["y"] < H:
        c += 1
    if robot["y"] < H//2 and W//2 < robot["x"] < W:
        d += 1
print(a*b*c*d, process_time() - start_time)  # 211773366 0.04
