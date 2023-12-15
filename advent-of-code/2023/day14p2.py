
N = 100
lines = []

for i in range(N):
    lines.append(list(input()))

visited = {}
total_nb_turns = 4000000000

for turn in range(total_nb_turns):
    if turn % 4 == 0:
        for i in range(1, N):
            for j in range(N):
                if lines[i][j] == "O":
                    current = i
                    while current-1 >= 0 and lines[current-1][j] == ".":
                        current -= 1
                    lines[i][j] = "."
                    lines[current][j] = "O"

    if turn % 4 == 1:
        for j in range(1, N):
            for i in range(N):
                if lines[i][j] == "O":
                    current = j
                    while current-1 >= 0 and lines[i][current-1] == ".":
                        current -= 1
                    lines[i][j] = "."
                    lines[i][current] = "O"

    if turn % 4 == 2:
        for i in reversed(range(N-1)):
            for j in range(N):
                if lines[i][j] == "O":
                    current = i
                    while current+1 < N and lines[current+1][j] == ".":
                        current += 1
                    lines[i][j] = "."
                    lines[current][j] = "O"

    if turn % 4 == 3:
        for j in reversed(range(N-1)):
            for i in range(N):
                if lines[i][j] == "O":
                    current = j
                    while current+1 < N and lines[i][current+1] == ".":
                        current += 1
                    lines[i][j] = "."
                    lines[i][current] = "O"


    hash = tuple(tuple(l) for l in lines)
    if hash in visited:
        gap = turn - visited[hash]

        for trn in range(visited[hash], turn):
            if (total_nb_turns - 1 - trn) % gap == 0:
                for lines, found in visited.items():
                    if found == trn:
                        total = 0
                        for i in range(N):
                            print(lines[i])
                            total += lines[i].count("O") * (N - i)

                        print(total)  # 104533
                        exit()

    else:
        visited[hash] = turn


