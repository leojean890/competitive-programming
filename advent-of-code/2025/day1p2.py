
counter = 0
pos = 50
for i in range(4333):
    ss = input()
    sense = ss[0]
    nb = int(ss[1:])

    oldpos = pos
    pos = (pos+nb if sense == "R" else pos -nb)%100

    counter += abs((oldpos + nb if sense == "R" else oldpos - nb) // 100)

    # en m'arretant en 0, j'ajoute ceux qui manquent et j'en enleve un systmatiquement pour avoir +1 tjr (ça ne fait qu'un passage en 0 en 2 moves)

    if oldpos == 0 and sense == "R":
        counter += 1

    if pos == 0 and sense == "L":
        counter += 1

    if oldpos == 0:
        counter -= 1

    # left vers 0 => +0
    # left depuis 0 => +1

    # right vers 0 => +1
    # right depuis 0 => +0

print(counter) # 6498
