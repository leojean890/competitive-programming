iline = [int(i) for i in input().split(",")]
convertMap = {1:"+",2:"*"}

for noun in range(100):
    for verb in range(100):
        line = iline.copy()
        line[1:3] = [noun, verb]
        current = 0

        while line[current] != 99:
            codeModif, leftOperandIndex, rightOperandIndex, outputIndex = line[current:current+4]
            line[outputIndex] = eval(str(line[leftOperandIndex]) + convertMap[codeModif] + str(line[rightOperandIndex]))
            current += 4
        if line[0] == 19690720:
            print(100*noun+verb) # 7912
            exit()
