
counter = 0
pos = 50
for i in input().split(","):
    b = i.split("-")[0]
    c = i.split("-")[1]

    for a in range(int(b),int(c)+1):
        a = str(a)

        if len(a)%2==0 and a[:len(a)//2] == a[(len(a)+1)//2:]:
            print(a)
            counter += int(a)

print(counter) # 43952536386
