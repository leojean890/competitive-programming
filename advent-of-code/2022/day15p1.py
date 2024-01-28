
possible = set()
beacons = set()
while 1:
    try:
        action = input().split("=")
        xS = int(action[1].split(",")[0])
        yS = int(action[2].split(":")[0])
        xB = int(action[3].split(",")[0])
        yB = int(action[4])
        beacons.add((xB, yB))
        closestDistToSensor = abs(xS-xB) + abs(yS-yB)
        coveredArea = "a"
        for i in range(4000001):
            for j in range(4000001):
                if abs(xS-i) + abs(yS-j) <= closestDistToSensor:
                    possible.add((i,j))


    except Exception as ex:
        for i in possible.copy():
            if (i, 2000000) in beacons:
                possible.remove(i)
        print(len(possible))#4237111
        break


















"""possible = set()
beacons = set()
while 1:
    try:
        action = input().split("=")
        print(action)
        xS = int(action[1].split(",")[0])
        print(xS)
        yS = int(action[2].split(":")[0])
        print(yS)
        xB = int(action[3].split(",")[0])
        print(xB)
        yB = int(action[4])
        print(yB)
        beacons.add((xB, yB))
        closestDistToSensor = abs(xS-xB) + abs(yS-yB)
        print(xS, yS, xB, yB, closestDistToSensor)
        print(xS, yS, xB, yB, closestDistToSensor)
        coveredArea = "a"
        for i in range(-5000000,10000000):
            if abs(xS-i) + abs(yS-2000000) <= closestDistToSensor:
                possible.add(i)


    except Exception as ex:
        print(beacons)
        print(len(possible))#4237111 4886370
        print(possible)#4237111
        for i in possible.copy():
            if (i, 2000000) in beacons:
                possible.remove(i)
        print(ex)
        print(len(possible))#4237111
        break"""

