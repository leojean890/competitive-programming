
counter = 0
pos = 50
for i in input().split(","):
    b = i.split("-")[0]
    c = i.split("-")[1]

    for a in range(int(b),int(c)+1):
        a = str(a)
        for size in range(1, len(a)//2+1):
            X = 0
            if len(a)%size == 0 and all(a[i*size:(i+1)*size] == a[0:size] for i in range(len(a)//size)):
                print(a)
                counter += int(a)
                break

print(counter) # 43952536386
