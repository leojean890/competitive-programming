line = [int(i) for i in input().split(",")]
line[1:3] = [12,2]
current = 0
convertMap = {1:"+",2:"*"}

while line[current] != 99:
    codeModif, leftOperandIndex, rightOperandIndex, outputIndex = line[current:current+4]
    line[outputIndex] = eval(str(line[leftOperandIndex]) + convertMap[codeModif] + str(line[rightOperandIndex]))
    current += 4

print(line[0]) # 3409710
