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
        for (a,b) in ((1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1)):
            i,j = y+a, x+b
            while 0 <= i < H and 0 <= j < W and (i,j) not in empty:
                if (i,j) in full:
                    n_empty.add((y,x))
                    break
                i, j = i + a, j + b
            else:
                continue
            break
        else:
            n_full.add((y,x))

    for (y,x) in full:
        counter = 0
        for (a,b) in ((1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1)):
            i,j = y+a, x+b
            while 0 <= i < H and 0 <= j < W and (i,j) not in empty:
                if (i,j) in full:
                    counter += 1
                    break
                i, j = i + a, j + b

        if counter < 5:
            n_full.add((y,x))
        else:
            n_empty.add((y,x))

    if full == n_full:
        print(len(full)) # 2032
        exit()
    full = n_full
    empty = n_empty
