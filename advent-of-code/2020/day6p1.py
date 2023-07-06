
keys = set()
counter = 0
for i in range(2176):
    l = input()
    if not l:
        counter += len(keys)
        keys = set()
    keys |= set(l)

counter += len(keys)
print(counter) # 6530
