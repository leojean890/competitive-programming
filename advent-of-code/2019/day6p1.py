fathers = {}
for i in range(1069):
    a,b = input().split(")")
    fathers[b] = a

total = 0

for elt in fathers:
    counter = 0
    while elt in fathers:
        elt = fathers[elt]
        counter += 1
    total += counter
print(total) # 162439
