from collections import deque
from time import process_time
import sys

sys.setrecursionlimit(100000)

def dynamicProgramming():
  global scores, nbErrSurRects
  q = deque()
  q.appendleft((0,0,(0,0)))
  seen = set()
  while q:
    (h, w, (dy, dx)) = q.pop()

    rr = max(0, yl-h)
    cc = max(0, xl-w)

    RR = min(ylimit+1, H-h)
    CC = min(xlimit+1, W-w)

    for r in range(rr, RR):
      for c in range(cc, CC):
        if dy:
          nbErrSurRects[(r,c,r+h,c+w,col)] = nbErrSurRects[(r,c,r+h-1,c+w,col)] + nbErrSurRects[(r+h,c,r+h,c+w,col)]
          if nbErrSurRects[(r,c,r+h,c+w,col)] > 0:
            scores[(r,c,r+h,c+w,col)] = ((h + 1) * (w + 1)) ** 0.5 / nbErrSurRects[(r,c,r+h,c+w,col)]
          elif (r, c, r + h, c + w, col) in scores:
            scores[(r, c, r + h, c + w, col)] = 100000000
        elif dx:
          nbErrSurRects[(r,c,r+h,c+w,col)] = nbErrSurRects[(r,c,r+h,c+w-1,col)] + nbErrSurRects[(r,c+w,r+h,c+w,col)]
          if nbErrSurRects[(r, c, r + h, c + w, col)] > 0:
            scores[(r, c, r + h, c + w, col)] = ((h + 1) * (w + 1)) ** 0.5 / nbErrSurRects[(r, c, r + h, c + w, col)]
          elif (r, c, r + h, c + w, col) in scores:
            scores[(r, c, r + h, c + w, col)] = 100000000
        else:
          if init[r][c] == target[r][c] and col != target[r][c]:
            nbErrSurRects[(r,c,r,c,col)] = -1
            scores[(r,c,r,c,col)] = 100000000
          elif init[r][c] != target[r][c] and col == target[r][c]:
            nbErrSurRects[(r,c,r,c,col)] = 1
            scores[(r,c,r,c,col)] = 1
          else:
            nbErrSurRects[(r,c,r,c,col)] = 0
            scores[(r,c,r,c,col)] = 100000000

    if h < H-1 and (h+1, w) not in seen:
      q.appendleft((h+1, w, (1,0)))
      seen.add((h+1, w))
    if w < W-1 and (h, w+1) not in seen:
      q.appendleft((h, w+1, (0,1)))
      seen.add((h, w+1))


def noOverlap(r,c,r2,c2,selected):
  for (a,b,a2,b2) in selected:
    for (y,x) in ((r,c),(r2,c),(r2,c2),(r,c2)):
      if a <= y <= a2 and b <= x <= b2:
        return False
  return True


def getAvailableCols(r,c,r2,c2):
  if W*H < 250:
    return range(1,C+1)

  availableCols = set()

  if W*H < 400:
    if target[r][c] == target[r2][c2] and init[r][c] != target[r][c] and init[r2][c2] != target[r][c]:
      availableCols.add(target[r2][c2])
    if target[r][c2] == target[r2][c] and init[r][c2] != target[r2][c] and init[r2][c] != target[r2][c]:
      availableCols.add(target[r2][c])
    if target[r][c] == target[r2][c] and init[r][c] != target[r][c] and init[r2][c] != target[r][c]:
      availableCols.add(target[r][c])
    if target[r][c2] == target[r][c] and init[r][c2] != target[r][c] and init[r][c] != target[r][c]:
      availableCols.add(target[r][c])

  else:
    if target[r][c] == target[r2][c2] == target[r][c2] == target[r2][c] and init[r][c] != target[r][c] and init[r2][c2] != target[r][c] and init[r][c2] != target[r][c] and init[r2][c] != target[r][c]:
      availableCols.add(target[r2][c2])

  return availableCols


H = int(input())
start_time = process_time()
W = int(input())
C = int(input())
print(W*H, file=sys.stderr)

T = 10

if W*H > 600:
  T = 9
if W*H > 1000:
  T = 8
if W*H > 1400:
  T = 7
if W*H > 1800:
  T = 6
if W*H > 2200:
  T = 5

target = [[-1 for x in range(W)] for y in range(H)]
init = [[-1 for x in range(W)] for y in range(H)]
for r in range(H):
  for c in range(W):
    target[r][c] = int(input())     

seuil = 0
moves = []
ctr = 0

xl = 0
yl = 0
xlimit = W - 1
ylimit = H - 1
scores = {}
nbErrSurRects = {}

while init != target:
  ctr += 1

  condDp = ((W * H < 1000 and C < 4) or (W * H < 700 and C < 6)) and process_time() - start_time < T
  if condDp:
    seuil = W * H // 5
    if W * H < 1000:
      seuil = 2
    for col in range(1,C+1):
      dynamicProgramming()
  else:
    scores = {}
    for r in range(H):
      for c in range(W):
        if process_time() - start_time < T:
          seuil = 0
          for r2 in range(r,H):
            c_time = process_time()
            if c_time - start_time > T:
              break
            for c2 in range(c,W):
              for col in getAvailableCols(r, c, r2, c2):
                nbErrSurCeRect = 0
                for i in range(r, r2 + 1):
                  for j in range(c, c2 + 1):
                    if init[i][j] == target[i][j] and col != target[i][j]:
                      nbErrSurCeRect -= 1
                    elif init[i][j] != target[i][j] and col == target[i][j]:
                      nbErrSurCeRect += 1
                if nbErrSurCeRect > 0:
                  scores[(r, c, r2, c2, col)] = ((r2 - r + 1) * (c2 - c + 1)) ** 0.5 / nbErrSurCeRect

        else:
          seuil = W * H // 5
          if W * H < 1000:
            seuil = 2
          pts = []
          for r2 in range(r,H):
            pts.append((r2, c))
          for c2 in range(c,W):
            pts.append((r,c2))
          for (r2,c2) in pts:
              c_time = process_time()
              if c_time - start_time > 9.8:
                break
              for col in getAvailableCols(r,c,r2,c2):
                nbErrSurCeRect = 0
                for i in range(r, r2 + 1):
                  for j in range(c, c2 + 1):
                    if init[i][j] == target[i][j] and col != target[i][j]:
                      nbErrSurCeRect -= 1
                    elif init[i][j] != target[i][j] and col == target[i][j]:
                      nbErrSurCeRect += 1
                if nbErrSurCeRect > 0:
                  scores[(r, c, r2, c2, col)] = ((r2 - r + 1) * (c2 - c + 1)) ** 0.5 / nbErrSurCeRect

        if c_time - start_time > 9.8:
          break
      if c_time - start_time > 9.8:
        break

  selected = set()
  itr = 0
  xlimit = 0
  ylimit = 0
  yl = H
  xl = W
  for ((r,c,r2,c2,col), score) in sorted(scores.items(), key=lambda x:x[1]):
    itr += 1

    if score < 100000000 and noOverlap(r,c,r2,c2,selected):
      v = True
      if not condDp and c_time - start_time > T:
        if r == r2:
          if r-1 >= 0 and all(init[r-1][j] == col for j in range(c, c2+1)) and (r-1,c,r-1,c2,col) in moves:
            v = False
            ind = moves.index((r-1,c,r-1,c2,col))
            moves[ind] = (r-1,c,r,c2,col)
            selected.add((r-1, c, r, c2))
            xl = min(c, xl)
            yl = min(r-1, yl)
            xlimit = max(c2, xlimit)
            ylimit = max(r2, ylimit)

          elif r+1 < H and all(init[r+1][j] == col for j in range(c, c2+1)) and (r+1,c,r+1,c2,col) in moves:
            v = False
            ind = moves.index((r+1,c,r+1,c2,col))
            moves[ind] = (r,c,r+1,c2,col)
            selected.add((r, c, r+1, c2))
            xl = min(c, xl)
            yl = min(r, yl)
            xlimit = max(c2, xlimit)
            ylimit = max(r2+1, ylimit)

        elif c == c2:
          if c-1 >= 0 and all(init[j][c-1] == col for j in range(r, r2+1)) and (r, c-1, r2, c-1, col) in moves:
            v = False
            ind = moves.index((r, c-1, r2, c-1, col))
            moves[ind] = (r, c-1, r2, c, col)
            selected.add((r, c-1, r2, c))
            xl = min(c-1, xl)
            yl = min(r, yl)
            xlimit = max(c2, xlimit)
            ylimit = max(r2, ylimit)

          elif c+1 < W and all(init[j][c+1] == col for j in range(r, r2+1)) and (r, c+1, r2, c+1, col) in moves:
            v = False
            ind = moves.index((r, c+1, r2, c+1, col))
            moves[ind] = (r, c, r2, c+1, col)
            selected.add((r, c, r2, c+1))
            xl = min(c, xl)
            yl = min(r, yl)
            xlimit = max(c2+1, xlimit)
            ylimit = max(r2, ylimit)

      if v:
        moves.append((r,c,r2,c2,col))
        selected.add((r,c,r2,c2))
        xlimit = max(c2, xlimit)
        ylimit = max(r2, ylimit)
        xl = min(c, xl)
        yl = min(r, yl)
      for i in range(r, r2 + 1):
        for j in range(c, c2 + 1):
          init[i][j] = col

    if score >= 100000000 or itr > seuil:
      break

  c_time = process_time()
  if c_time - start_time > 9.8:
    break
  if xlimit == 0:
    xlimit = W - 1
  if ylimit == 0:
    ylimit = H-1
  if xl == W:
    xl = 0
  if yl == H:
    yl = 0

for r in range(H):
  for c in range(W):
    if init[r][c] != target[r][c]:
      moves.append((r,c,r,c,target[r][c]))

print(ctr, file=sys.stderr)
print(len(moves))

for move in moves:
  print(*move)

sys.stdout.flush()
