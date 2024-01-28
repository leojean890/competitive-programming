total = 0
for i in range(100):
    n = int(input())
    while n > 0:
        n = n//3-2
        if n > 0:
            total += n

print(total) # 5243207
