p1 bugged
N = 1347

allBricks = []
for i in range(N):
    brick = input().split("~")

    a = [int(i) for i in brick[0].split(",")]
    b = [int(i) for i in brick[1].split(",")]

    #print(a,b)
    allBricks.append((a,b))


#allBricks = list(sorted(allBricks, key=lambda x:(min(x[0][2],x[1][2]),max(x[0][2],x[1][2]))))
allBricks = list(sorted(allBricks, key=lambda x: (x[0][2],x[1][2])))
print(allBricks)

for i in range(1,N):
    print(i)
    (a,b) = allBricks[i]
    vv = False
    while a[2] > 1 and b[2] > 1 and not vv:
        x,y = ([a[0], a[1], a[2]-1],[b[0], b[1], b[2]-1])
        vv = False
        for u in range(a[0],b[0]+1):
            for v in range(a[1],b[1]+1):
                for j in reversed(range(i)):
                    (c,d) = allBricks[j]
                    for u1 in range(c[0], d[0] + 1):
                        for v1 in range(c[1], d[1] + 1):
                            if (u1,v1,d[2]) == (u,v,a[2]-1):
                                vv = True  #trouvé au moins un elt dont le bloc le plus haut est juste en dessous des blocs du courant donc jpx pas desc
                        if vv:break
                    if vv:break
                if vv:break
            if vv:break
        if not vv:
            (a,b) = (x,y)
    allBricks[i] = (a,b)

print(allBricks)

# une fois que j'ai fait tomber les briques au maximum,
# simuler le fait de remove des briques
# si rien ne tombe, compteur += 1

counter = 0

for i in range(1,N-1):
    (a,b) = allBricks[i]
    print(i)
    # on remove la brique i, on teste toutes les briques de z plus grand pour voir si elles tombent
    # en gros si on a un des éléments de (a,b) juste en dessous elle va tomber => faux car peut ê retenu par autre chose
    # parcourir tous les précédents pour voir si qqc la retient
    for j in range(i+1, N):
        vv = False
        (c,d) = allBricks[j]
        for u1 in range(c[0], d[0] + 1):
            for v1 in range(c[1], d[1] + 1):
                for k in range(j):
                    if k != i:
                        (x, y) = allBricks[k]
                        for u2 in range(x[0], y[0] + 1):
                            for v2 in range(x[1], y[1] + 1):
                                if (u1,v1,c[2]-1) == (u2,v2,y[2]):# signifie que (x,y) retient (c,d)
                                    vv = True # la brique j est retenue par k
                            if vv:break
                    if vv:break
                if vv:break
            if vv:break
        if not vv:break # la brique j n'a rien pour la retenir
    else:
        #pas de break => else => toutes les briques sont retenues => on peut supprimer la brique i => counter += 1
        counter += 1
        #print(a,b)

print(counter+1) #459 too low => 471 RE
