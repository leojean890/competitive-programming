total = 0
for seq in input().split(","):
    current = 0
    for char in seq:
        current += ord(char)
        current = (current*17)%256
    total += current
print(total) # 511343
