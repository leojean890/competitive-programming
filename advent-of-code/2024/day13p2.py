from collections import defaultdict
from time import process_time

"""
a * x1 + b * y1 = z1 
a * x2 + b * x2 = z2
"""


def solve_system(x1, x2, y1, y2, z1, z2):
    det_A = x1 * y2 - x2 * y1
    if det_A == 0:
        return 0

    det_A_a = z1 * y2 - z2 * y1
    det_A_b = x1 * z2 - x2 * z1

    if det_A_a % det_A != 0 or det_A_b % det_A != 0:
        return 0

    a = det_A_a // det_A
    b = det_A_b // det_A

    return 3*a+b

start_time = process_time()
elts = defaultdict(list)
N = 1279

for j in range(N):
    s = input()
    if j%4 < 2:
        elts[j//4].append([int(a[-2:]) for a in s.split(":")[1].split(",")])
    elif j%4 == 2:
        elts[j//4].append([10000000000000+int(a.split("=")[1]) for a in s.split(":")[1].split(",")])

score = 0

for index, elt in elts.items():
    score += solve_system(elt[0][0], elt[0][1], elt[1][0], elt[1][1], elt[2][0], elt[2][1])

print(score, process_time() - start_time)  # 73458657399094 0.015
