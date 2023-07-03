rocks = set()

for i in range(179):
    line = [a.split(',') for a in input().split("->")]

    for j in range(len(line)-1):
        x, y = line[j]
        x = int(x.replace(" ",""))
        y = int(y.replace(" ",""))

        x1, y1 = line[j+1]
        x1 = int(x1.replace(" ",""))
        y1 = int(y1.replace(" ",""))

        if x == x1:
            ym = min(y, y1)
            yM = max(y, y1)
            for y2 in range(ym, yM+1):
                rocks.add((x, y2))
        else:
            xm = min(x, x1)
            xM = max(x, x1)
            for x2 in range(xm, xM+1):
                rocks.add((x2, y))



# si resultingY > 171, alors stop counter

for x in range(-500, 1000):
    rocks.add((x, 173))

counter = 0


while 1:
    counter += 1
    x = 500
    y = 0

    while 1:
        y += 1
        if (x,y) in rocks:
            x -= 1
            if (x,y) in rocks:
                x += 2
                if (x,y) in rocks:
                    if (x-1, y-1) == (500, 0):
                        print(counter)
                        exit()
                    rocks.add((x-1, y-1))
                    break


