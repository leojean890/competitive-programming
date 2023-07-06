
keys = set()
counter = 0
justChanged = True
for i in range(2176):
    l = input()
    if not l:
        counter += len(keys)
        justChanged = True
        keys = set()
    else:
        if justChanged:
            justChanged = False
            keys = set(l)
        else:
            keys &= set(l)

counter += len(keys)
print(counter) # 6530 3323
