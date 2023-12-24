
pos = []
speeds = []
N = 300
m = 200000000000000
M = 400000000000000

for i in range(N):
    p, s = input().split("@")
    pos.append([int(j) for j in p.split(",")])
    speeds.append([int(j) for j in s.split(",")])

# trouver d1, d2 tq
# x1 + d1*u1 = x2 + d2*u2
# y1 + d1*v1 = y2 + d2*v2
# d1 = (d2*u2+x2-x1)/u1
# y1 + v1*(d2*u2+x2-x1)/u1 = y2 + d2*v2
# d2*(v1*u2/u1 - v2) = y2 - y1 - v1*(x2-x1)/u1
# d2 = (y2 - y1 - v1*(x2-x1)/u1)/(v1*u2/u1 - v2)

# xCroisement = x2 + d2*u2
# yCroisement = y2 + d2*v2

# on ne veut pas les croisements qui ont lieu dans le passé, donc
# if d2 >= 0 and d1 >= 0 and  m <= xCroisement <= M and m <= yCroisement <= M:counter += 1

counter = 0

for i in range(N-1):
    x1, y1, z1 = pos[i]
    u1, v1, w1 = speeds[i]
    for j in range(i+1,N):
        x2, y2, z2 = pos[j]
        u2, v2, w2 = speeds[j]
        if v1 * u2 / u1 != v2 and v2 * u1 / u2 != v1:
            d2 = (y2 - y1 - v1 * (x2 - x1) / u1) / (v1 * u2 / u1 - v2)
            d1 = (y1 - y2 - v2 * (x1 - x2) / u2) / (v2 * u1 / u2 - v1)
            xCroisement = x2 + d2*u2
            yCroisement = y2 + d2*v2
            if d2 >= 0 and d1 >= 0 and m <= xCroisement <= M and m <= yCroisement <= M:
                counter += 1
print(counter) # 13892
