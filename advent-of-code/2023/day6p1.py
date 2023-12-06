
times = [int(i) for i in input().split()[1:]]
distances = [int(i) for i in input().split()[1:]]

total = 1
for i in range(len(times)):
    time = times[i]
    bestDistance = distances[i]
    nbOfWins = 0

    for speed in range(1,time):
        if speed*(time-speed) > bestDistance:
            nbOfWins += 1
    total *= nbOfWins
print(total) #3317888
