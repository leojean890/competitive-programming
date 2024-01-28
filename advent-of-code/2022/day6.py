a = input()
i = 0
print(a[i:i + 4])
print(set(a[i:i + 4]))

while len(set(a[i:i+14])) < 14:
    print(a[i:i+4], set(a[i:i+4]))
    i += 1
print(i+14)
