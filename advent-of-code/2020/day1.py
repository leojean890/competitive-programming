items = []

for i in range(200):
    items.append(int(input()))

"""for i in range(199):
    for j in range(i+1,200):
        if items[i]+items[j] == 2020:
            print(items[i]*items[j])#355875
            exit()"""

for i in range(198):
    for j in range(i+1,199):
        for k in range(j+1,200):
            if items[i]+items[j]+items[k] == 2020:
                print(items[i]*items[j]*items[k])#140379120
                exit()
