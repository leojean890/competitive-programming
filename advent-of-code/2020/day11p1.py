empty = set()
full = set()

W = 91#10
H = 94#10

for i in range(H):
    line = input()
    for j in range(W):
        if line[j] == "L":
            empty.add((i,j))

while 1:
    n_empty = set()
    n_full = set()

    for (y,x) in empty:
        for (a,b) in ((y+1,x),(y-1,x),(y+1,x+1),(y+1,x-1),(y-1,x+1),(y-1,x-1),(y,x+1),(y,x-1)):
            if (a,b) in full:
                n_empty.add((y,x))
                break
        else:
            n_full.add((y,x))

    for (y,x) in full:
        counter = 0
        for (a,b) in ((y+1,x),(y-1,x),(y+1,x+1),(y+1,x-1),(y-1,x+1),(y-1,x-1),(y,x+1),(y,x-1)):
            if (a,b) in full:
                counter += 1

        if counter < 4:
            n_full.add((y,x))
        else:
            n_empty.add((y,x))

    if full == n_full:
        print(len(full)) # 2222
        exit()
    full = n_full
    empty = n_empty
