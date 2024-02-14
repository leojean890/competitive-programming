import math
import random
import sys
from collections import defaultdict
from time import process_time
T = int(input())
start_time = process_time()
S = int(input())
C = int(input())
N = int(input())
P = float(input())

sys.setrecursionlimit(1000000000)
probaToGetNxN = {}


def dfsAmongChosen(depth, chosen, current):
    solutions = set()
    if depth == len(chosen):
        for rotation in range(N):
            nchosen = tuple()
            for elt in current:
                nchosen += ((elt+rotation)%N,)
            solutions.add(nchosen)

        return solutions
    solutions |= dfsAmongChosen(depth+1, chosen, current)
    solutions |= dfsAmongChosen(depth+1, chosen, current+(chosen[depth],))

    return solutions


def getStats(chosen):
    chsn = dfsAmongChosen(0, chosen, tuple())
    ctr = 0
    
    for elt in chsn:
      l = len(elt)
      if l > 0:
        ctr += probaToGetEachTypColorPieceCombPerAmountOfColoured[l] 

    return ctr


def dfs(depth, chosen):
    if depth == N:
      if len(chosen) < N-1:
        probaToGetNxN[chosen] = getStats(chosen)
      return

    dfs(depth+1, chosen)
    dfs(depth+1, chosen+(depth,))


THRESHOLD = 0.01

targets = [[0 for x in range(N)] for y in range(T)]  
targetCounts = [0] * T

sources = [[0 for x in range(N)] for y in range(S)]  
for i in range(S):
  s = input()
  for k in range(N):
    sources[i][k] = int(s[k])

countersPerSource = defaultdict(int)
colorPerSource = {}
for source in range(S):
  for i in range(N):
    if sources[source][i] > 0:
      colorPerSource[source] = sources[source][i]
      countersPerSource[sources[source][i]] += 1

countersPerTarget = defaultdict(int)
colorPerTarget = {}
for target in range(T):
  colors1 = defaultdict(int)
  ctr = 0
  for i in range(N):
    if targets[target][i] > 0:
      colorPerTarget[target] = targets[target][i]
      colors1[targets[target][i]] += 1
      ctr += 1

  if len(colors1) > 1 and target in colorPerTarget:
    del colorPerTarget[target]
  else:
    countersPerTarget[targets[target][i]] += ctr

stats = defaultdict(int)
found = 0
while process_time() - start_time < 7:
  counter = sum([1 if random.uniform(0,1) < P else 0 for i in range(N)])
  if 0 < counter < N:
    stats[counter] += 1
    found += 1

for a,b in stats.items():
  stats[a] /= found

probaToGetEachTypColorPieceCombPerAmountOfColoured = {}
for i in range(N-1):
  nIparmiN = math.factorial(N) / (math.factorial(N - i) * math.factorial(i))
  probaToGetEachTypColorPieceCombPerAmountOfColoured[i] = stats[i] / (C * nIparmiN)

dfs(0, tuple())
numMoves = 1000
moves = 0

while moves < numMoves:

  scores = {}

  for source in range(S):
    for rotate in range(N):
      src = sources[source][rotate:] + sources[source][:rotate]
      for target in range(T):
        if all(targets[target][i] == 0 for i in range(N) if src[i] > 0):

          score = abs(rotate-N/2)
          colors = defaultdict(int)
          colors1 = defaultdict(int)
          ccc = 0
          aaa = 0
          notIncluded = tuple()
          for i in range(N):
            if targets[target][i] > 0:
              colors[targets[target][i]] += 1
              colors1[targets[target][i]] += 1
              score += 1
              ccc += 1
              aaa += 1
            else:
              notIncluded += (i,)
            if src[i] > 0:
              colors[src[i]] += 1
              score += 1
              ccc += 1
          if notIncluded in probaToGetNxN:
            probaThatANextSourceCorrespondsToCurrentUnfilledSpotsAmongCurrentTarget = probaToGetNxN[notIncluded]

          if len(colors) == 1:
            score += 1000*ccc
          elif len(colors1) == 1:
            if (notIncluded in probaToGetNxN and probaThatANextSourceCorrespondsToCurrentUnfilledSpotsAmongCurrentTarget > THRESHOLD) and (len(targets) < 3 and C < 5):
              break
            else:
              score -= 1000*aaa
          if len(colors) > 1:
            if target in colorPerTarget and colorPerTarget[target] in countersPerTarget:
              score += N*countersPerTarget[colorPerTarget[target]]

          scores[(source, rotate, target)] = score

  if scores:
    source, rotate, target = list({a:b for a,b in sorted(scores.items(), key=lambda x:x[1])}.keys())[-1]

    if rotate == 0:
      print(source, target)
      for i in range(N):
        if sources[source][i] > 0:
          targets[target][i] = sources[source][i]
      if all(targets[target][i] > 0 for i in range(N)):
        targets[target] = [0 for x in range(N)]
      s = input()
      for k in range(N):
        sources[source][k]=int(s[k])
    elif rotate > N/2:
      print(source, "L")
      sources[source] = sources[source][-1:] + sources[source][:-1]

    else:
      print(source, "R")
      sources[source] = sources[source][1:] + sources[source][:1]

  else:
    print(str(source)+" D")
    sources[source] = [0 for x in range(N)]
    s = input()
    for k in range(N):
      sources[source][k] = int(s[k])

  sys.stdout.flush()

  moves+=1
  elapsedTime=int(input())

print("-1")
print(process_time() - start_time, file=sys.stderr)
sys.stdout.flush()  
