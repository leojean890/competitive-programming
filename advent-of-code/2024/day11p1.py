from time import process_time

start_time = process_time()
starts = []

stones = [int(i) for i in input().split()]

for gen in range(25):
    print(gen)
    newStones = []
    for stone in stones:
        s = str(stone)
        if len(s) % 2 == 0:
            v = s[:len(s) // 2]
            while v[0] == "0" and len(v) > 1:
                v = v[1:]
            newStones.append(int(v))
            v = s[len(s) // 2:]
            while v[0] == "0" and len(v) > 1:
                v = v[1:]
            newStones.append(int(v))
        elif stone == 0:
            newStones.append(1)
        else:
            newStones.append(stone*2024)
    stones = newStones

print(len(newStones), process_time() - start_time)  # 220722
