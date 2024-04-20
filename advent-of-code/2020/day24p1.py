
# day24p1

from collections import defaultdict

incr = {"ne":(-1,0.5), "nw":(-1,-0.5), "se":(1,0.5), "sw":(1,-0.5), "e":(0,1), "w":(0,-1)}
black = defaultdict(bool)

for i in range(333):#20
    s = input()
    c = y = x = 0
    while c < len(s):
        chr = s[c]
        if chr in "ns":
            c += 1
            chr += s[c]
        y += incr[chr][0]
        x += incr[chr][1]
        c += 1
    black[(y,x)] = not black[(y,x)]
print(len([x for x in black.values() if x])) # 289
