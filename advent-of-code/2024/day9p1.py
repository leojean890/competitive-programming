from time import process_time

start_time = process_time()
line = [int(i) for i in input()]
N = len(line)
memory = []
for i in range(N):
    size = line[i]
    for j in range(size):
        memory.append(-1 if i%2 else i//2)

currentIndex = 0
M = len(memory)
for i in reversed(range(M)):
    if memory[i] > -1:
        while memory[currentIndex] > -1:
            currentIndex += 1
            if currentIndex >= i:
                counter = 0
                for k in range(M):
                    if memory[k] == -1:break
                    counter += k*memory[k]
                print(counter, "".join([str(h) for h in memory]), process_time() - start_time)  # 6378826667552
                exit()

        memory[currentIndex] = memory[i]
        memory[i] = -1
