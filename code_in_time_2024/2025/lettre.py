
import sys

i = 0
m = 0
for line in sys.stdin:
    if i > 0:
        tokens = line.split(";")
        v = sum([int(j) for j in tokens[2:]])
        if v > m:
            m = v
            best = tokens[1]
            print(m,best) # 6900 2024-07-09
            # 5013;2024-07-09;BXD-KC4;336
            # 413;E52;BXD-KC4;NTA
            # 152;NTA;Rodep Hautoire
    i += 1



