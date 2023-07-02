import sys
import time
from collections import defaultdict, deque

# 0 pbm actuel : je delaisse parfois des piles d'étages successifs, notamment haut et bas
# mieux répartir (search bfs mc ou hongrois)
# permet aussi de mieux gérer le fait que plusieurs ascenseurs arrivent au même endroit
# et prennent de manière opti le nb de personnes (genre chacun a 2 places donc on en récup 4)

# 1 enlever une pondération si un ascenseur se rapproche des autres (-= abs(futurePosAsc1, asc2) )
# en moyenne (ça les forcera à s'éloigner les uns des autres)

# 1 enlever une pondération si un ascenseur se rapproche d'un objectif qui est plus proche d'un autre ascenseur
# surtout si c aussi celui de l'autre

# 2 bien cibler les directions (un ascenseur => même dir ?) => waiting[floor][direction] => dur sans simu

# 3 attendre au milieu des zones vides qd on a pas de mecs qui attendent => rare je suppose

# déjà tuné => il est plus important de déposer que d'en prendre
# 4 => mais on peut supposer que plusieurs ascenseurs vont en prendre
# il faut simuler au global

# 4 bien cibler les cas où on sette : objectives[i] = None
# ça m'a l'air pas mal car on l'annule qd on l'atteint et on peut aussi le moduler

# attention, si on maintient une liste d'objectifs mais qu'un truc plus intéressant se présente
# il faut être prêt à changer => DONE

F = int(input())
start_time = time.process_time()
L = int(input())
P = float(input())

lifts = {}
waiting = defaultdict(dict)
objectives = {}

for floor in range(F):
  waiting[floor]["global"] = 0
  waiting[floor]["D"] = 0
  waiting[floor]["U"] = 0

for i in range(L):
  objectives[i] = None
  lifts[i] = {"floor": int(input())-1, "open": False, "passengers": defaultdict(int), "nbPass": 0}

for turn in range(1,1001):
  #print("turn", turn, file=sys.stderr)
  newPeople = int(input())
  for i in range(newPeople):
    temp = input().split(" ")
    floor = int(temp[0])-1
    direction = temp[1][0]
    waiting[floor][direction] += 1
    waiting[floor]["global"] += 1

  for i in range(L):
    lift = lifts[i]
    floor = lift["floor"]
    if floor == objectives[i]:
      objectives[i] = None

    if lift["open"]:
      nbGoingDown = lift["passengers"][floor]

      lifts[i]["nbPass"] -= nbGoingDown
      lifts[i]["passengers"][floor] = 0

  enteredPeople=int(input())
  for i in range(enteredPeople):
    temp = input().split(" ")
    lift = int(temp[0])
    targetFloor = int(temp[1])-1
    lifts[lift]["passengers"][targetFloor] += 1
    lifts[lift]["nbPass"] += 1
    floor = lifts[lift]["floor"]

    direction = "D"

    if targetFloor > floor:
      direction = "U"

    waiting[floor]["global"] -= 1
    waiting[floor][direction] -= 1

  elapsedTime = int(input())

  # simu : depth par depth on a un branching par asc (up, down, (open sauf si c en heuristique)) (et close est en heuristic))
  # pour une depth on a donc 2**L ou 3**L combinaisons
  # donc entre 2 et 32 ou entre 3 et 243 combinaisons
  # si on se limite à up/down en simu et le reste en heuristique, on peut avoir un branching de 32 au max
  # évaluer à depth 3 c déjà 32768 states au max (en 10ms)
  # adapter la depth max au branching (à L) ou plutôt iterative deepening
  # eventuellement beamer voir MC (pas sûr pour hc ga sa)
  # l'eval sera une combinaison
  # du nb de personnes qui attendent au niveau des étages voisins
  # du nb de personnes qu'on a récup
  # du nb de personnes qu'on a déposées
  # de la distance entre ascenseurs
  # a la fin retourner la premiere action du chemin gagnant
  # le state est (lifts, waiting, objectives) ou plutot (lifts, waiting)

  def bfs(lifts, waiting, maxDepth):

    q = deque()
    q.appendleft((0, 0, lifts, waiting, 0, 0, {}))
    bestScore = -sys.maxsize
    best = None

    while q:
      if time.process_time() - start_time > turn*0.0075 and maxDepth > 1:
        #print("a",maxDepth, file=sys.stderr)
        return

      (depth, currLift, lifts, waiting, nbRecup, nbPut, first) = q.pop()

      if depth == maxDepth:
        #print("b",maxDepth, file=sys.stderr)

        score = 1000000*(nbRecup + nbPut) - 10*sum([waiting[floor]["global"] for floor in range(F)])
        bsts = defaultdict(int)

        for i in range(L):
          lift = lifts[i]
          floor = lift["floor"]
          M = 0
          bst = 0
          for j in range(i+1, L):
            lift2 = lifts[j]
            score += 10*abs(floor - lift2["floor"]) #distance entre ascenseurs
          for cfloor in range(F):
            # j'enleve du score si bcp attendent loin de mon asc le plus proche (ou de mes ascs au global)
            score -= waiting[cfloor]["global"]*abs(floor - cfloor)
            if cfloor in lift["passengers"]:
              d = F*lift["passengers"][cfloor] + (F-abs(cfloor - floor))# + waiting[cfloor]["global"]
              score -= 100 * lift["passengers"][bst] * abs(bst - floor)
              if d > M:
                M = d
                bst = cfloor
          score -= 100000 * lift["passengers"][bst] * abs(bst - floor)
          totalNbSpots = 4
          nbTakenSpots = lift["nbPass"]

          nbNewSpots = waiting[bst]["global"]
          nbWhoWillGoDown = lift["passengers"][bst]
          nbSpotsAvailableInLift = totalNbSpots+nbWhoWillGoDown-nbTakenSpots-nbNewSpots
          score += (F+1-abs(bst-floor))*(nbSpotsAvailableInLift + 2*nbNewSpots + 10*nbWhoWillGoDown)

          bsts[i] = bst
            # a garder ?
        for cfloor in range(F):
          closestDist = F
          for i in range(L):
            lift = lifts[i]
            floor = lift["floor"]
            d = abs(floor-cfloor)
            if d < closestDist:
              closestDist = d
          score -= 500*waiting[cfloor]["global"] * closestDist


        #print(first, score, file=sys.stderr)
        if score > bestScore:
          bestScore = score
          best = (first, bsts)
        continue
      #(depth, currLift, lifts, waiting, nbRecup, nbPut, first)
      nextLift = (currLift+1)%L
      nextDepth = depth if nextLift else depth+1
      nextLifts = {}
      nFirst = first
      #lifts[i] = {"floor": int(input()) - 1, "open": False, "passengers": defaultdict(int), "nbPass": 0}
      for (a, b) in lifts.items():
        nextLifts[a] = {"floor": b["floor"], "open": b["open"], "passengers": b["passengers"].copy(), "nbPass": b["nbPass"]}
      lift = nextLifts[currLift]
      #waiting[floor]["global"]
      nextWaiting = defaultdict(dict)
      for (a, b) in waiting.items():
        nextWaiting[a]["global"] = b["global"]
        nextWaiting[a]["D"] = b["D"]
        nextWaiting[a]["U"] = b["U"]

      if lift["open"]:
        nextLifts[currLift]["open"] = False
        if depth == 0:#not nFirst:
          nFirst[currLift] = "close"
        q.appendleft((nextDepth, nextLift, nextLifts, nextWaiting, nbRecup, nbPut, nFirst))
      else:
        floor = lift["floor"]
        nbGoingDown = lift["passengers"][floor]
        totalNbSpots = 4
        nbTakenSpots = lift["nbPass"]

        nbNewSpots = waiting[floor]["global"]
        nbWhoWillGoDown = lift["passengers"][floor]
        nbSpotsAvailableInLift = totalNbSpots + nbWhoWillGoDown - nbTakenSpots - nbNewSpots

        if nbGoingDown > 0 or (waiting[floor]["global"] > 0 and nbSpotsAvailableInLift >= 0):

          #nbSpotsAvailableInLift = totalNbSpots+nbWhoWillGoDown-nbTakenSpots-nbNewSpots
          howManyCanGoUp = totalNbSpots+nbWhoWillGoDown-nbTakenSpots
          realNbNewSpots = min(howManyCanGoUp, nbNewSpots)
          nextLifts[currLift]["open"] = True
          if depth == 0:  # not nFirst:
            nFirst[currLift] = "open"
          nextWaiting[floor]["global"] -= realNbNewSpots
          nextLifts[currLift]["passengers"][floor] -= realNbNewSpots
          coeffPatience = 0.5
          nbRecup += realNbNewSpots * coeffPatience**depth
          #nbRecup += (100/(depth+1))*realNbNewSpots
          #nbPut += (100/(depth+1))*nbWhoWillGoDown
          nbPut += nbWhoWillGoDown * coeffPatience**depth
          # gerer nextWaiting[floor]["D"] nextWaiting[floor]["U"] avec le vrai ordre (file) et proba etages du bon cote
          # ainsi, realimenter pour tout k lift["passengers"][k]
          q.appendleft((nextDepth, nextLift, nextLifts, nextWaiting, nbRecup, nbPut, nFirst))
        else:

          modified = False

          if floor > 0:
            nextLifts[currLift]["floor"] -= 1
            modified = True

            if depth == 0:  # not nFirst:
              nFirst[currLift] = "down"
            q.appendleft((nextDepth, nextLift, nextLifts, nextWaiting, nbRecup, nbPut, nFirst))

          if floor < F-1:
            if modified:
              nextLifts = {}
              for (a, b) in lifts.items():
                nextLifts[a] = {"floor": b["floor"], "open": b["open"], "passengers": b["passengers"].copy(),
                              "nbPass": b["nbPass"]}
              if depth == 0:  # not nFirst:
                nFirst = first.copy()
            if depth == 0:
              nFirst[currLift] = "up"
            nextLifts[currLift]["floor"] += 1


            q.appendleft((nextDepth, nextLift, nextLifts, nextWaiting, nbRecup, nbPut, nFirst))

      # tuner eval
    #print("c",maxDepth, file=sys.stderr)

    return best


  mres = None
  bbsts = None
  for maxDepth in range(1, 9):
    res = bfs(lifts, waiting, maxDepth)
    if res:
      mres, bbsts = res
    else:
      break

  for i in range(L):
    decision = mres[i]
    if decision == "open":
      print("open")
      #print("open", file=sys.stderr)
      lifts[i]["open"] = True
      floor = lifts[i]["floor"]
      for j in range(L):
        if floor == objectives[j]:
          placeRestante = 4 - lifts[i]["nbPass"]
          getAll = placeRestante >= waiting[floor]["global"]
          # on invalide les autres que si j'ai tout récup
          if getAll or floor == j:
            objectives[j] = None
    elif decision == "close":
      print("close")
      #print("close", file=sys.stderr)
      lifts[i]["open"] = False
    elif decision == "up":
      #print("up", file=sys.stderr)
      print("up")
      lifts[i]["floor"] += 1
      objectives[i] = bbsts[i]
    else: # down
      lifts[i]["floor"] -= 1
      #print("down", file=sys.stderr)
      print("down")
      objectives[i] = bbsts[i]

  sys.stdout.flush()
