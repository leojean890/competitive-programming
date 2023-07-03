
tgt, area, x, y = input().split()
print(tgt, area, x, y)

x0, x1 = [int(i.replace(",","")) for i in x.split("=")[1].split("..")]
y0, y1 = [int(i) for i in y.split("=")[1].split("..")]
MY = 0

ix = []# list(range(10))
for dx in range(11,500):
    #if True:#x0 <= dx*(dx+1)//2 <= x1: => signifie que ça finit dedans
    if dx <= x1 and x0 <= dx*(dx+1)//2:# le dernier arrive dans l'intervalle, et le premier ne dépasse pas la fin
        ix.append(dx)

counter = 0
for dx in ix:
    #for dy in range(-500,500): # trouver un elagage ici aussi basé sur y0, y1, mais on peut lancer plus haut et ça redesc
    for dy in range(-500,500):
        my = 0
        inTarget = False
        x, y = 0, 0
        cdx, cdy = dx, dy
        #for it in range(200):
        while x <= x1 and y >= y0:
            x += cdx
            y += cdy
            #if (dx, dy) == (4, 38):
            #    print(x,y)
            if x0 <= x <= x1 and y0 <= y <= y1:
                inTarget = True
            if y > my:
                my = y
            if cdx > 0:
                cdx = max(cdx-1, 0)
            else:
                cdx = min(cdx + 1, 0)
            cdy -= 1
        if inTarget:# and my > MY:
            #MY = my
            #print(dx, dy, MY) 4278
            counter += 1
            print(counter) #1994
