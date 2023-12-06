
time = int("".join(input().split()[1:]))
distance = int("".join(input().split()[1:]))

nbOfWins = 0

for speed in range(1,time):
    if speed*(time-speed) > distance:
        nbOfWins += 1
print(nbOfWins) # 24655068
