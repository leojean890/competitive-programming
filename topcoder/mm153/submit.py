import random
import sys
from collections import deque, defaultdict
from copy import deepcopy
from time import process_time

N = int(input())
start_time = process_time()
H = int(input())
P = int(input())
RD = float(input())
CD = float(input())

FACTOR = 350

if CD > 1-1/(7*N):
  if RD > 1 - 1 / (7 * N):
    threshold = N / 2
  elif RD > 1 - 1 / (6 * N):
    threshold = 2*N / 3
  elif RD > 1 - 1 / (5 * N):
    threshold = 3*N/4
  elif RD > 1 - 1 / (4 * N):
    threshold = N
  elif RD > 1 - 1 / (3 * N):
    threshold = 4*N/3
  elif RD > 1 - 1 / (2 * N):
    threshold = 3 * N / 2
  else:
    threshold = 2*N
elif CD > 1-1/(6*N):
  if RD > 1 - 1 / (7 * N):
    threshold = N / 5
  elif RD > 1 - 1 / (6 * N):
    threshold = N / 4
  elif RD > 1 - 1 / (5 * N):
    threshold = N / 3
  elif RD > 1 - 1 / (4 * N):
    threshold = N/2
  elif RD > 1 - 1 / (3 * N):
    threshold = 2*N / 3
  elif RD > 1 - 1 / (2 * N):
    threshold = 3*N/4
  else:
    threshold = N
elif CD > 1-1/(5*N):
  if RD > 1 - 1 / (7 * N):
    threshold = N / 6
  elif RD > 1 - 1 / (6 * N):
    threshold = N / 5
  elif RD > 1 - 1 / (5 * N):
    threshold = N / 4
  elif RD > 1 - 1 / (4 * N):
    threshold = N / 3
  elif RD > 1 - 1 / (3 * N):
    threshold = N / 2
  elif RD > 1 - 1 / (2 * N):
    threshold = 2*N / 3
  else:
    threshold = 3*N/4
elif CD > 1-1/(4*N):
  if RD > 1 - 1 / (7 * N):
    threshold = N / 7
  elif RD > 1 - 1 / (6 * N):
    threshold = N / 6
  elif RD > 1 - 1 / (5 * N):
    threshold = N / 5
  elif RD > 1 - 1 / (4 * N):
    threshold = N / 4
  elif RD > 1 - 1 / (3 * N):
    threshold = N / 3
  elif RD > 1 - 1 / (2 * N):
    threshold = N / 2
  else:
    threshold = 2*N / 3
elif CD > 1-1/(3*N):
  if RD > 1 - 1 / (7 * N):
    threshold = N / 8
  elif RD > 1 - 1 / (6 * N):
    threshold = N / 7
  elif RD > 1 - 1 / (5 * N):
    threshold = N / 6
  elif RD > 1 - 1 / (4 * N):
    threshold = N / 5
  elif RD > 1 - 1 / (3 * N):
    threshold = N / 4
  elif RD > 1 - 1 / (2 * N):
    threshold = N / 3
  else:
    threshold = N / 2
elif CD > 1-1/(2*N):
  if RD > 1 - 1 / (7 * N):
    threshold = N / 9
  elif RD > 1 - 1 / (6 * N):
    threshold = N / 8
  elif RD > 1 - 1 / (5 * N):
    threshold = N / 7
  elif RD > 1 - 1 / (4 * N):
    threshold = N / 6
  elif RD > 1 - 1 / (3 * N):
    threshold = N / 5
  elif RD > 1 - 1 / (2 * N):
    threshold = N / 4
  else:
    threshold = N / 3
else:
  if RD > 1 - 1 / (7 * N):
    threshold = N / 11
  elif RD > 1 - 1 / (6 * N):
    threshold = N / 10
  elif RD > 1 - 1 / (5 * N):
    threshold = N / 9
  elif RD > 1 - 1 / (4 * N):
    threshold = N / 8
  elif RD > 1 - 1 / (3 * N):
    threshold = N / 7
  elif RD > 1 - 1 / (2 * N):
    threshold = N / 6
  else:
    threshold = N / 5

# si cd est grand, on augmente le threshold
# si rd est grand, on diminue le threshold

huttes = set()
trees = set()
grid = [['x' for x in range(N)] for y in range(N)]
for r in range(N):
  for c in range(N):
    grid[r][c] = (input())[0]
    if grid[r][c]=='^':
      huttes.add((r,c))
    if grid[r][c] == '#':
      trees.add((r, c))

mushrooms = {}
init_mushrooms = {}
values = [[0 for x in range(N)] for y in range(N)]
for r in range(N):
  for c in range(N):
    values[r][c] = float(input())
    if values[r][c] > 0:
      mushrooms[(r,c)] = values[r][c]
      init_mushrooms[(r,c)] = values[r][c]

people = [0] * P
init_people = [0] * P
hasChampis = []
init_hasChampis = []
counterCh = []
init_counterCh = []
for i in range(P):
  line = input().split(" ")
  r=int(line[0])
  c=int(line[1])
  people[i]=(r,c)
  init_people[i]=(r,c)
  hasChampis.append([])
  init_hasChampis.append([])
  counterCh.append(0)
  init_counterCh.append(0)

reservations = defaultdict(set)
init_reservations = defaultdict(set)
for (r,c) in mushrooms:
  #distancesByPlayer = {}
  closestPlayer = 0
  closestD = sys.maxsize
  for i in range(P):
    (y,x) = people[i]
    #distancesByPlayer[i] = abs(y-r) + abs(x-c)
    d = abs(y-r) + abs(x-c)
    if d < closestD:
      closestD = d
      closestPlayer = i
  reservations[closestPlayer].add((r,c))
  init_reservations[closestPlayer].add((r,c))
allDists = defaultdict(dict)
allPaths = defaultdict(dict)
interestingCoords = list(huttes) + people
for elt in mushrooms:
  interestingCoords.append(elt)


for (y1,x1) in interestingCoords:
    q = deque()

    q.appendleft((y1, x1, "", 0))
    visited = {(y1, x1)}
    while q:
      (y, x, path, depth) = q.pop()
      allDists[(y1,x1)][(y,x)] = depth
      allPaths[(y1,x1)][(y,x)] = path

      for (a, b, d) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
        if 0 <= a < N and 0 <= b < N and (a, b) not in visited and (a, b) not in trees:
          visited.add((a, b))
          q.appendleft((a, b, path+d, depth + 1))

dirs=['L','U','R','D']
dr=[0,-1,0,1]
dc=[-1,0,1,0]

currentPath = defaultdict(str)
moves = []
ccc = 0
gscore = 0
turn = -1

begin = process_time()
while ccc < P:
  turn += 1

  if turn > 0:
    toDelete = set()
    for (r,c) in mushrooms:
      mushrooms[(r, c)] *= RD
      if mushrooms[(r, c)] < 1:
        toDelete.add((r,c))

    for (r,c) in toDelete:
      del mushrooms[(r, c)]

    for i in range(P):
      counterCh[i] *= CD
      for j in range(len(hasChampis[i])):
        hasChampis[i][j] *= CD

  ccc = 0
  targets = {}
  for i in range(P):
    (y, x) = people[i]
    if people[i] in huttes:
      gscore += counterCh[i]
      hasChampis[i] = []
      counterCh[i] = 0

    if people[i] in mushrooms:
      moves.append("C")
      counterCh[i] += mushrooms[people[i]]
      hasChampis[i].append(mushrooms[people[i]])
      del mushrooms[people[i]]

    elif currentPath[i]:
      moves.append(currentPath[i][0])
      currentPath[i] = currentPath[i][1:]
      if moves[-1] == "D":
        people[i] = (y+1, x)
      elif moves[-1] == "U":
        people[i] = (y-1, x)
      elif moves[-1] == "L":
        people[i] = (y, x-1)
      else:
        people[i] = (y, x+1)
    elif mushrooms:
      scores = {}
      for ((a, b), val) in mushrooms.items():
        if not reservations[i] or (a,b) in reservations[i]:
          dist = allDists[(y, x)][(a, b)]
          score = 15*dist + 15*len(hasChampis[i]) - threshold*val/110

          if (a,b) in targets:
            score += 40

            if dist >= targets[(a,b)]:
              continue

          if counterCh[i] >= threshold*FACTOR:
            score += 60
          for j in range(P):
            if j != i:
              score -= abs(people[j][0]-a)+abs(people[j][1]-b)
          scores[(a,b)] = score

      for (a, b) in huttes:
        if len(hasChampis[i]) > 0:
          dist = allDists[(y, x)][(a, b)]
          score = 15 * dist - 15 * len(hasChampis[i])

          if counterCh[i] < threshold*FACTOR:
            score += 60
          for j in range(P):
            if j != i:
              score -= abs(people[j][0] - a) + abs(people[j][1] - b)
        scores[(a,b)] = score

      toGo, score = list(sorted(scores.items(), key=lambda h:h[1]))[0]
      if toGo in mushrooms:
        if toGo in reservations[i]:
          reservations[i].remove(toGo)
        else:
          for k in reservations:
            if toGo in reservations[k]:
              reservations[k].remove(toGo)
        targets[toGo] = allDists[(y, x)][toGo]
      path = allPaths[(y, x)][toGo]

      moves.append(path[0] if path else "C")
      currentPath[i] = path[1:]
      if moves[-1] == "D":
        people[i] = (y+1, x)
      elif moves[-1] == "U":
        people[i] = (y-1, x)
      elif moves[-1] == "L":
        people[i] = (y, x-1)
      elif moves[-1] == "R":
        people[i] = (y, x+1)

    else:
      if people[i] in huttes:
        moves.append("S")
        gscore += counterCh[i]
        hasChampis[i] = []
        counterCh[i] = 0
        ccc += 1
      else:
        (y, x) = people[i]
        q = deque()
        q.appendleft((y, x, None, 0))
        visited = {(y, x)}
        while q:
          (y, x, first, depth) = q.pop()
          if (y, x) in huttes:
            (y, x, d) = first
            people[i] = (y, x)
            moves.append(d)
            break
          for (a, b, d) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
            if 0 <= a < N and 0 <= b < N and (a, b) not in visited and (a, b) not in trees:
              visited.add((a, b))
              q.appendleft((a, b, first if first else (a, b, d), depth + 1))

C = 35
D = 60

end = process_time()
delta = end - begin
print("delta", delta, file=sys.stderr)

ctr = 0
while end - start_time + 3 * delta < 4:
  ctr += 1

  for (A, B, A1, B1) in ((20, 10, 15, 5), (20, 5, 15, 10), (15, 10, 15, 10)):

    currentPath = defaultdict(str)
    nmoves = []
    ccc = 0
    ngscore = 0
    turn = -1
    mushrooms = init_mushrooms.copy()
    people = init_people.copy()
    counterCh = init_counterCh.copy()
    hasChampis = deepcopy(init_hasChampis)
    if ctr %5 == 0:
      reservations = defaultdict(set)

      for i in range(P):
        reservations[i] = init_reservations[i].copy()
    while ccc < P:
      turn += 1

      if turn > 0:
        toDelete = set()
        for (r, c) in mushrooms:
          mushrooms[(r, c)] *= RD
          if mushrooms[(r, c)] < 1:
            toDelete.add((r, c))

        for (r, c) in toDelete:
          del mushrooms[(r, c)]

        for i in range(P):
          counterCh[i] *= CD
          for j in range(len(hasChampis[i])):
            hasChampis[i][j] *= CD

      ccc = 0
      targets = {}
      for i in range(P):
        (y, x) = people[i]
        if people[i] in huttes:
          ngscore += counterCh[i]
          hasChampis[i] = []
          counterCh[i] = 0

        if people[i] in mushrooms:
          nmoves.append("C")
          counterCh[i] += mushrooms[people[i]]
          hasChampis[i].append(mushrooms[people[i]])
          del mushrooms[people[i]]

        elif currentPath[i]:
          nmoves.append(currentPath[i][0])
          currentPath[i] = currentPath[i][1:]
          if nmoves[-1] == "D":
            people[i] = (y + 1, x)
          elif nmoves[-1] == "U":
            people[i] = (y - 1, x)
          elif nmoves[-1] == "L":
            people[i] = (y, x - 1)
          else:
            people[i] = (y, x + 1)
        elif mushrooms:
          scores = {}
          for ((a, b), val) in mushrooms.items():
            if ctr %5 > 0 or not reservations[i] or (a, b) in reservations[i]:

              dist = allDists[(y, x)][(a, b)]
              score = A * dist + B * len(hasChampis[i]) - threshold*val/110

              if (a, b) in targets:
                score += D

                if dist >= targets[(a, b)]:
                  continue

              if counterCh[i] >= threshold*FACTOR:
                score += C
              for j in range(P):
                if j != i:
                  score -= abs(people[j][0] - a) + abs(people[j][1] - b)
              scores[(a, b)] = score

          for (a, b) in huttes:
            if len(hasChampis[i]) > 0:
              dist = allDists[(y, x)][(a, b)]
              score = A1 * dist - B1 * len(hasChampis[i])

              if counterCh[i] < threshold*FACTOR:
                score += C
              for j in range(P):
                if j != i:
                  score -= abs(people[j][0] - a) + abs(people[j][1] - b)
            scores[(a, b)] = score

          sortedScores = list(sorted(scores.items(), key=lambda h: h[1]))

          nn = len(sortedScores)

          for k in range(nn):
            if random.randint(0, 4) or k == nn - 1:
              toGo, score = sortedScores[k]
              break
          if toGo in mushrooms:
            if ctr % 5 == 0:
              if toGo in reservations[i]:
                reservations[i].remove(toGo)
              else:
                for k in reservations:
                  if toGo in reservations[k]:
                    reservations[k].remove(toGo)
            targets[toGo] = allDists[(y, x)][toGo]
          path = allPaths[(y, x)][toGo]

          nmoves.append(path[0] if path else "C")
          currentPath[i] = path[1:]
          if nmoves[-1] == "D":
            people[i] = (y + 1, x)
          elif nmoves[-1] == "U":
            people[i] = (y - 1, x)
          elif nmoves[-1] == "L":
            people[i] = (y, x - 1)
          elif nmoves[-1] == "R":
            people[i] = (y, x + 1)

        else:
          if people[i] in huttes:
            nmoves.append("S")
            ngscore += counterCh[i]
            hasChampis[i] = []
            counterCh[i] = 0
            ccc += 1
          else:
            (y, x) = people[i]
            q = deque()
            q.appendleft((y, x, None, 0))
            visited = {(y, x)}
            while q:
              (y, x, first, depth) = q.pop()
              if (y, x) in huttes:
                (y, x, d) = first
                people[i] = (y, x)
                nmoves.append(d)
                break
              for (a, b, d) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
                if 0 <= a < N and 0 <= b < N and (a, b) not in visited and (a, b) not in trees:
                  visited.add((a, b))
                  q.appendleft((a, b, first if first else (a, b, d), depth + 1))

    if ngscore > gscore:
      moves = nmoves
      gscore = ngscore

    curr = process_time()
    if curr - end > delta:
      delta = curr - end
    end = curr


ctr = 0
while end - start_time + delta < 7:
  ctr += 1
  currentPath = defaultdict(str)
  nmoves = []
  ccc = 0
  ngscore = 0
  turn = -1
  mushrooms = init_mushrooms.copy()
  people = init_people.copy()
  counterCh = init_counterCh.copy()
  hasChampis = deepcopy(init_hasChampis)
  if ctr % 5 == 0:

    reservations = defaultdict(set)

    for i in range(P):
      reservations[i] = init_reservations[i].copy()
  while ccc < P:
    turn += 1
    if turn > 0:
      toDelete = set()
      for (r, c) in mushrooms:
        mushrooms[(r, c)] *= RD
        if mushrooms[(r, c)] < 1:
          toDelete.add((r, c))

      for (r, c) in toDelete:
        del mushrooms[(r, c)]

      for i in range(P):
        counterCh[i] *= CD
        for j in range(len(hasChampis[i])):
          hasChampis[i][j] *= CD

    ccc = 0
    targets = {}
    for i in range(P):
      (y, x) = people[i]
      if people[i] in huttes:
        ngscore += counterCh[i]
        hasChampis[i] = []
        counterCh[i] = 0

      if people[i] in mushrooms:
        nmoves.append("C")
        counterCh[i] += mushrooms[people[i]]
        hasChampis[i].append(mushrooms[people[i]])
        del mushrooms[people[i]]

      elif currentPath[i]:
        nmoves.append(currentPath[i][0])
        currentPath[i] = currentPath[i][1:]
        if nmoves[-1] == "D":
          people[i] = (y + 1, x)
        elif nmoves[-1] == "U":
          people[i] = (y - 1, x)
        elif nmoves[-1] == "L":
          people[i] = (y, x - 1)
        else:
          people[i] = (y, x + 1)
      elif mushrooms:
        scores = {}

        for ((a, b), val) in mushrooms.items():
          if ctr % 5 > 0 or not reservations[i] or (a, b) in reservations[i]:

            dist = allDists[(y, x)][(a, b)]
            score = 15 * dist + 15 * len(hasChampis[i]) - threshold * val / 110

            if (a, b) in targets:
              score += 40

              if dist >= targets[(a, b)]:
                continue

            if counterCh[i] >= threshold*FACTOR:
              score += 60
            for j in range(P):
              if j != i:
                score -= abs(people[j][0] - a) + abs(people[j][1] - b)
            scores[(a, b)] = score

        for (a, b) in huttes:
          if len(hasChampis[i]) > 0:
            dist = allDists[(y, x)][(a, b)]
            score = 15 * dist - 15 * len(hasChampis[i])

            if counterCh[i] < threshold*FACTOR:
              score += 60
            for j in range(P):
              if j != i:
                score -= abs(people[j][0] - a) + abs(people[j][1] - b)
          scores[(a, b)] = score

        sortedScores = list(sorted(scores.items(), key=lambda h: h[1]))

        nn = len(sortedScores)

        for k in range(nn):
            if random.randint(0, 2) or k == nn-1:
              toGo, score = sortedScores[k]
              break
        if toGo in mushrooms:
          if toGo in reservations[i]:
            reservations[i].remove(toGo)
          else:
            for k in reservations:
              if toGo in reservations[k]:
                reservations[k].remove(toGo)
          targets[toGo] = allDists[(y, x)][toGo]
        path = allPaths[(y, x)][toGo]

        nmoves.append(path[0] if path else "C")
        currentPath[i] = path[1:]
        if nmoves[-1] == "D":
          people[i] = (y + 1, x)
        elif nmoves[-1] == "U":
          people[i] = (y - 1, x)
        elif nmoves[-1] == "L":
          people[i] = (y, x - 1)
        elif nmoves[-1] == "R":
          people[i] = (y, x + 1)

      else:
        if people[i] in huttes:
          nmoves.append("S")
          ngscore += counterCh[i]
          hasChampis[i] = []
          counterCh[i] = 0
          ccc += 1
        else:
          (y, x) = people[i]
          q = deque()
          q.appendleft((y, x, None, 0))
          visited = {(y, x)}
          while q:
            (y, x, first, depth) = q.pop()
            if (y, x) in huttes:
              (y, x, d) = first
              people[i] = (y, x)
              nmoves.append(d)
              break
            for (a, b, d) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
              if 0 <= a < N and 0 <= b < N and (a, b) not in visited and (a, b) not in trees:
                visited.add((a, b))
                q.appendleft((a, b, first if first else (a, b, d), depth + 1))

  if ngscore > gscore:
    moves = nmoves
    gscore = ngscore

  curr = process_time()
  if curr-end > delta:
    delta = curr-end
  end = curr

ctr = 0
while end - start_time + delta < 9.5:
  ctr += 1
  currentPath = defaultdict(str)
  nmoves = []
  ccc = 0
  ngscore = 0
  turn = -1
  mushrooms = init_mushrooms.copy()
  people = init_people.copy()
  counterCh = init_counterCh.copy()
  hasChampis = deepcopy(init_hasChampis)
  if ctr%5 == 0:
    reservations = defaultdict(set)

    for i in range(P):
      reservations[i] = init_reservations[i].copy()
  while ccc < P:
    turn += 1
    if turn > 0:
      toDelete = set()
      for (r, c) in mushrooms:
        mushrooms[(r, c)] *= RD
        if mushrooms[(r, c)] < 1:
          toDelete.add((r, c))

      for (r, c) in toDelete:
        del mushrooms[(r, c)]

      for i in range(P):
        counterCh[i] *= CD
        for j in range(len(hasChampis[i])):
          hasChampis[i][j] *= CD

    ccc = 0
    targets = {}
    for i in range(P):
      (y, x) = people[i]
      if people[i] in huttes:
        ngscore += counterCh[i]
        hasChampis[i] = []
        counterCh[i] = 0

      if people[i] in mushrooms:
        nmoves.append("C")
        counterCh[i] += mushrooms[people[i]]
        hasChampis[i].append(mushrooms[people[i]])
        del mushrooms[people[i]]

      elif currentPath[i]:
        nmoves.append(currentPath[i][0])
        currentPath[i] = currentPath[i][1:]
        if nmoves[-1] == "D":
          people[i] = (y + 1, x)
        elif nmoves[-1] == "U":
          people[i] = (y - 1, x)
        elif nmoves[-1] == "L":
          people[i] = (y, x - 1)
        else:
          people[i] = (y, x + 1)
      elif mushrooms:
        A = random.randint(10, 25)
        B = random.randint(max(1, A - 15), A)
        A1 = random.randint(max(1, A - 10), A + 5)
        B1 = random.randint(max(1, A1 - 15), A1)
        WWW = random.randint(60, 160)
        FCTR = random.randint(200, 450)

        scores = {}
        for ((a, b), val) in mushrooms.items():
          if ctr % 5 > 0 or not reservations[i] or (a, b) in reservations[i]:

            dist = allDists[(y, x)][(a, b)]
            score = A * dist + B * len(hasChampis[i]) - threshold * val / WWW

            if (a, b) in targets:
              score += D

              if dist >= targets[(a, b)]:
                continue

            if counterCh[i] >= threshold*FCTR:
              score += C
            for j in range(P):
              if j != i:
                score -= abs(people[j][0] - a) + abs(people[j][1] - b)
            scores[(a, b)] = score

        for (a, b) in huttes:
          if len(hasChampis[i]) > 0:
            dist = allDists[(y, x)][(a, b)]
            score = A1 * dist - B1 * len(hasChampis[i])

            if counterCh[i] < threshold*FCTR:
              score += C
            for j in range(P):
              if j != i:
                score -= abs(people[j][0] - a) + abs(people[j][1] - b)
          scores[(a, b)] = score

        toGo, score = min(scores.items(), key=lambda h: h[1])
        if toGo in mushrooms:
          if ctr % 5 == 0:
            if toGo in reservations[i]:
              reservations[i].remove(toGo)
            else:
              for k in reservations:
                if toGo in reservations[k]:
                  reservations[k].remove(toGo)
          targets[toGo] = allDists[(y, x)][toGo]
        path = allPaths[(y, x)][toGo]

        nmoves.append(path[0] if path else "C")
        currentPath[i] = path[1:]
        if nmoves[-1] == "D":
          people[i] = (y + 1, x)
        elif nmoves[-1] == "U":
          people[i] = (y - 1, x)
        elif nmoves[-1] == "L":
          people[i] = (y, x - 1)
        elif nmoves[-1] == "R":
          people[i] = (y, x + 1)

      else:
        if people[i] in huttes:
          nmoves.append("S")
          ngscore += counterCh[i]
          hasChampis[i] = []
          counterCh[i] = 0
          ccc += 1
        else:
          (y, x) = people[i]
          q = deque()
          q.appendleft((y, x, None, 0))
          visited = {(y, x)}
          while q:
            (y, x, first, depth) = q.pop()
            if (y, x) in huttes:
              (y, x, d) = first
              people[i] = (y, x)
              nmoves.append(d)
              break
            for (a, b, d) in ((y + 1, x, "D"), (y - 1, x, "U"), (y, x + 1, "R"), (y, x - 1, "L")):
              if 0 <= a < N and 0 <= b < N and (a, b) not in visited and (a, b) not in trees:
                visited.add((a, b))
                q.appendleft((a, b, first if first else (a, b, d), depth + 1))

  if ngscore > gscore:
    moves = nmoves
    gscore = ngscore

  curr = process_time()
  if curr - end > delta:
    delta = curr - end
  end = curr

ctr = 0
print(len(moves)//P)
for move in moves:
  ctr += 1
  print(move)

print(gscore, file=sys.stderr)
sys.stdout.flush()
