s = input()
m0 = 151
found = list(s[0:150])
for i in range(1,100):
    for j in range(150):
        if found[j] == "2":
            found[j] = s[150*i+j]

for i in range(6):
    for j in range(25):
        print(found[25*i+j], end=" ")
    print()
    print() # HCGFE
