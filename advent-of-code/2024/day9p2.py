from time import process_time

start_time = process_time()
line = [int(i) for i in input()]
N = len(line)
memory = []
for i in range(N):
    memory.append((-1 if i%2 else i//2,line[i]))

i = N-1
while i > 0:
    (index,size) = memory[i]
    if index > -1:
        for j in range(i):
            (index2, size2) = memory[j]
            if index2 == -1 and size2 >= size:
                memory[j] = (index,size)
                memory[i] = (-1,size)
                if size2 > size:
                    memory.insert(j+1, (-1,size2-size))
                break
    i -= 1
mem = []
for (value,size) in memory:
    for i in range(size):
        mem.append(value)

counter = 0
for k in range(len(mem)):
    if mem[k] > -1:
        counter += k * mem[k]
print(counter, process_time() - start_time)  # 6413328569890 20.0
