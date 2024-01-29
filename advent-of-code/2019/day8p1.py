s = input()
m0 = 151
best = 0
for i in range(100):
    current = s[150*i:150*(i+1)]
    n0 = current.count("0")
    if n0 < m0:
        m0 = n0
        n1 = current.count("1")
        n2 = current.count("2")
        best = n1*n2

print(best) # 1703
