

xR = yR = xT = yT = 0
x = [0 for j in range(10)]
y = [0 for j in range(10)]
visited = set()

while 1:
    try:
        direc, nbSteps = input().split()
        for i in range(int(nbSteps)):
            if direc == "R":
                x[0] += 1
                prev = ["R"]
                for j in range(1, 10):
                    if abs(y[j-1] - y[j]) == abs(x[j-1] - x[j]) == 2:
                        if "U" in prev:
                            y[j] -= 1
                        if "D" in prev:
                            y[j] += 1
                        if "L" in prev:
                            x[j] -= 1
                        if "R" in prev:
                            x[j] += 1
                    elif y[j-1] == y[j] - 2:
                        y[j] -= 1
                        prev = ["U"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif y[j-1] == y[j] + 2:
                        y[j] += 1
                        prev = ["D"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif x[j-1] == x[j] - 2:
                        x[j] -= 1
                        prev = ["L"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")

                    elif x[j-1] == x[j] + 2:
                        x[j] += 1
                        prev = ["R"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")

            elif direc == "L":
                x[0] -= 1
                for j in range(1, 10):
                    if abs(y[j-1] - y[j]) == abs(x[j-1] - x[j]) == 2:
                        if "U" in prev:
                            y[j] -= 1
                        if "D" in prev:
                            y[j] += 1
                        if "L" in prev:
                            x[j] -= 1
                        if "R" in prev:
                            x[j] += 1
                    elif y[j-1] == y[j] - 2:
                        y[j] -= 1
                        prev = ["U"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif y[j-1] == y[j] + 2:
                        y[j] += 1
                        prev = ["D"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif x[j-1] == x[j] - 2:
                        x[j] -= 1
                        prev = ["L"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")

                    elif x[j-1] == x[j] + 2:
                        x[j] += 1
                        prev = ["R"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")


            elif direc == "D":
                y[0] += 1
                for j in range(1, 10):
                    if abs(y[j-1] - y[j]) == abs(x[j-1] - x[j]) == 2:
                        if "U" in prev:
                            y[j] -= 1
                        if "D" in prev:
                            y[j] += 1
                        if "L" in prev:
                            x[j] -= 1
                        if "R" in prev:
                            x[j] += 1
                    elif y[j-1] == y[j] - 2:
                        y[j] -= 1
                        prev = ["U"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif y[j-1] == y[j] + 2:
                        y[j] += 1
                        prev = ["D"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif x[j-1] == x[j] - 2:
                        x[j] -= 1
                        prev = ["L"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")

                    elif x[j-1] == x[j] + 2:
                        x[j] += 1
                        prev = ["R"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")


            elif direc == "U":
                y[0] -= 1
                for j in range(1, 10):
                    if abs(y[j-1] - y[j]) == abs(x[j-1] - x[j]) == 2:
                        if "U" in prev:
                            y[j] -= 1
                        if "D" in prev:
                            y[j] += 1
                        if "L" in prev:
                            x[j] -= 1
                        if "R" in prev:
                            x[j] += 1
                    elif y[j-1] == y[j] - 2:
                        y[j] -= 1
                        prev = ["U"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif y[j-1] == y[j] + 2:
                        y[j] += 1
                        prev = ["D"]
                        if x[j-1] == x[j] + 1:
                            x[j] += 1
                            prev.append("R")
                        elif x[j-1] == x[j] - 1:
                            x[j] -= 1
                            prev.append("L")

                    elif x[j-1] == x[j] - 2:
                        x[j] -= 1
                        prev = ["L"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")

                    elif x[j-1] == x[j] + 2:
                        x[j] += 1
                        prev = ["R"]
                        if y[j-1] == y[j] + 1:
                            y[j] += 1
                            prev.append("D")
                        elif y[j-1] == y[j] - 1:
                            y[j] -= 1
                            prev.append("U")


            visited.add((x[9], y[9]))


    except Exception:
        print(len(visited))
        break

