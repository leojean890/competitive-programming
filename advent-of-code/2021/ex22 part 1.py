cubes = set()

for turn in range(420):#22):
    action, line = input().split()
    x, y, z = line.split(",")
    x = x.split("=")
    y = y.split("=")
    z = z.split("=")
    print(action, x,y,z)
    x0,x1 = [int(i) for i in x[1].split("..")]
    y0,y1 = [int(i) for i in y[1].split("..")]
    z0,z1 = [int(i) for i in z[1].split("..")]
    x0 = max(min(x0, 50),-50)
    x1 = max(min(x1, 50),-50)
    y0 = max(min(y0, 50),-50)
    y1 = max(min(y1, 50),-50)
    z0 = max(min(z0, 50),-50)
    z1 = max(min(z1, 50),-50)

    if x1==x0 or y1==y0 or z1==z0:
        continue

    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            for z in range(z0, z1+1):
                if (x,y,z) in cubes:
                    if action == "off":
                        cubes.remove((x,y,z))
                else:
                    if action == "on": cubes.add((x, y, z))

    print(len(cubes)) #503864

