import random
import sys
import math
from json import loads, dumps, dump
from copy import copy
from copy import deepcopy
import collections
from time import process_time
import numpy
import numpy.random

s = ""
while 1:
    try:
        s += input()
    except Exception:
        break

start_time = process_time()

currentIndex = -1

loaded = loads(s)
integers = numpy.random.randint(360, size=90000000)

print(loaded["hero"])
print(loaded["start_x"])
print(loaded["start_y"])
width = loaded["width"]
print(width)
height = loaded["height"]
print(height)
print(loaded["num_turns"])
print(loaded["monsters"])
nbMonsters = len(loaded["monsters"])
monstersIndexes = list(range(nbMonsters))
bestScore = 0
bestActions = {}
while process_time() - start_time < 240:

    allMonsters = {}
    for i in range(nbMonsters):
        allMonsters[i] = loaded["monsters"][i]["hp"]
    y,x,nTurns,level,xp = loaded["start_y"],loaded["start_x"],loaded["num_turns"],0,0
    actions = []
    features = []
    score = 0
    init_nTurns = nTurns
    currLevelXp = 1000+50*level*(level+1)

    d = sorted(monstersIndexes, key=lambda i: (init_nTurns-nTurns)*loaded["monsters"][i]["gold"] + nTurns*loaded["monsters"][i]["exp"] - init_nTurns*loaded["monsters"][i]["hp"] - (1+init_nTurns*10*math.dist((loaded["monsters"][i]["y"],loaded["monsters"][i]["x"]),(y,x))))

    kys = list(d)
    probs = []
    ss = 0.0
    for i in range(len(kys) - 7):
        probs.append(0.00005)
        ss += 0.00005
    probs.append(0.05)
    ss += 0.05
    probs.append(0.07)
    ss += 0.07
    probs.append(0.08)
    ss += 0.08
    probs.append(0.1)
    ss += 0.1
    probs.append(0.15)
    ss += 0.15
    probs.append(0.2)
    ss += 0.2
    probs.append(1.0 - ss)
    currentMonster = numpy.random.choice(kys, p=probs)

    while nTurns > 0:

        power = math.floor(loaded["hero"]["base_power"] * (1 + level * loaded["hero"]["level_power_coeff"] / 100))
        speed = math.floor(loaded["hero"]["base_speed"] * (1 + level * loaded["hero"]["level_speed_coeff"] / 100))
        h_range = math.floor(loaded["hero"]["base_range"] * (1 + level * loaded["hero"]["level_range_coeff"] / 100))

        for monster, hp in allMonsters.copy().items():
            if nTurns == 0:
                break
            yz = loaded["monsters"][monster]["y"]
            xz = loaded["monsters"][monster]["x"]

            distance = math.dist((yz,xz), (y,x))

            if distance <= h_range:
                while hp > 0 and nTurns > 0:
                    nTurns -= 1
                    actions.append({"type": "attack", "target_id": monster})
                    features.append((level, speed, power, h_range, xp, currLevelXp))

                    hp -= power

                if hp <= 0:
                    score += loaded["monsters"][monster]["gold"]
                    xp += loaded["monsters"][monster]["exp"]
                    del allMonsters[monster]
                    if monster == currentMonster:
                            d = sorted(allMonsters, key=lambda i: (init_nTurns-nTurns)*loaded["monsters"][i]["gold"] + nTurns*loaded["monsters"][i]["exp"] - init_nTurns*loaded["monsters"][i]["hp"] - (1+init_nTurns*10*math.dist((loaded["monsters"][i]["y"],loaded["monsters"][i]["x"]),(y,x))))
                            kys = list(d)
                            probs = []
                            ss = 0.0
                            if len(kys) >= 7:
                                for i in range(len(kys) - 7):
                                    probs.append(0.00005)
                                    ss += 0.00005
                                probs.append(0.05)
                                ss += 0.05
                                probs.append(0.07)
                                ss += 0.07
                                probs.append(0.08)
                                ss += 0.08
                                probs.append(0.1)
                                ss += 0.1
                                probs.append(0.15)
                                ss += 0.15
                                probs.append(0.2)
                                ss += 0.2
                                probs.append(1.0 - ss)
                            elif len(kys) == 6:
                                probs.append(0.07)
                                ss += 0.07
                                probs.append(0.08)
                                ss += 0.08
                                probs.append(0.1)
                                ss += 0.1
                                probs.append(0.15)
                                ss += 0.15
                                probs.append(0.2)
                                ss += 0.2
                                probs.append(1.0 - ss)
                            elif len(kys) == 5:
                                probs.append(0.08)
                                ss += 0.08
                                probs.append(0.1)
                                ss += 0.1
                                probs.append(0.15)
                                ss += 0.15
                                probs.append(0.2)
                                ss += 0.2
                                probs.append(1.0 - ss)
                            elif len(kys) == 4:
                                probs.append(0.1)
                                ss += 0.1
                                probs.append(0.15)
                                ss += 0.15
                                probs.append(0.2)
                                ss += 0.2
                                probs.append(1.0 - ss)
                            elif len(kys) == 3:
                                probs.append(0.15)
                                ss += 0.15
                                probs.append(0.2)
                                ss += 0.2
                                probs.append(1.0 - ss)
                            elif len(kys) == 2:
                                probs.append(0.2)
                                ss += 0.2
                                probs.append(1.0 - ss)
                            else:
                                probs.append(1.0)

                            currentMonster = numpy.random.choice(kys, p=probs)

                    while xp >= currLevelXp:
                        xp -= currLevelXp
                        level += 1
                        currLevelXp = 1000 + 50 * level * (level + 1)
                        power = math.floor(
                            loaded["hero"]["base_power"] * (1 + level * loaded["hero"]["level_power_coeff"] / 100))
                        speed = math.floor(
                            loaded["hero"]["base_speed"] * (1 + level * loaded["hero"]["level_speed_coeff"] / 100))
                        h_range = math.floor(
                            loaded["hero"]["base_range"] * (1 + level * loaded["hero"]["level_range_coeff"] / 100))

        if nTurns > 0:
            nTurns -= 1
            while True:
                currentIndex += 1
                gotoMonster = integers[currentIndex] % 9
                if gotoMonster:
                    yz = loaded["monsters"][currentMonster]["y"]
                    xz = loaded["monsters"][currentMonster]["x"]

                    distance = math.dist((yz,xz), (y,x))

                    if distance <= speed:
                        y = yz
                        x = xz
                    else:
                        y += int((yz - y) * speed / distance)
                        x += int((xz - x) * speed / distance)
                    break

                else:
                    currentIndex += 1
                    dd = min(speed,100)
                    distance = (integers[currentIndex] % (speed//dd) + 1) * dd
                    currentIndex += 1
                    a = integers[currentIndex] * math.pi / 180  # entre 0 et 350
                    # dy = angle*dx
                    # dxdx + dydy = dist*dist
                    # dxdx +a*a*dx*dx = dist*dist
                    sqrt = math.sqrt(distance * distance / (1 + a * a))
                    dx = int(sqrt)
                    dy = int(a * dx)
                    if x+dx > width:
                        continue
                    if x+dx < 0:
                        continue
                    if y+dy > height:
                        continue
                    if y+dy < 0:
                        continue
                    x += dx
                    y += dy
                    break

            actions.append({"type": "move", "target_x": x, "target_y": y})

    if score > bestScore:
        bestScore = score
        bestActions = {"moves": actions}
        bestFeatures = {"features": features}
        print(bestActions, file=sys.stdout, flush=True)
        print(bestFeatures, file=sys.stdout, flush=True)
        print(bestScore, file=sys.stdout, flush=True)





