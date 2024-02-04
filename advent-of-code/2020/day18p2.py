total = 0


def dfs(line):
    score = 0
    currOp = "+"
    i = 0
    while i < len(line):
        chr = line[i]
        if chr in "+*":
            currOp = chr
            i += 1
        elif chr.isdigit():
            score = eval(str(score)+currOp+chr)
            i += 1
        elif chr == "(":
            ctr = 1
            j = i+1
            while ctr > 0:
                if line[j] == "(":
                    ctr += 1
                if line[j] == ")":
                    ctr -= 1
                j += 1
            score = eval(str(score)+currOp+str(dfs(line[i+1:j-1])))
            i = j
        else:
            i+=1
    return score

total = 0

for it in range(372):
    line = list(input())
    print(line)

    i = 0
    while i < len(line):
        if line[i] == "+":
            if line[i-2] != ")":
                line.insert(i-2,"(")
            else:
                ctr = -1
                j = i - 3
                while ctr < 0:
                    if line[j] == "(":
                        ctr += 1
                    if line[j] == ")":
                        ctr -= 1
                    j -= 1

                line.insert(j+1, "(")
                # ici on remonte tout le bloc puis insert au debut
            i += 1

            if line[i + 2] != "(":
                line.insert(i + 3, ")")
            else:
                ctr = 1
                j = i + 3
                while ctr > 0:
                    if line[j] == "(":
                        ctr += 1
                    if line[j] == ")":
                        ctr -= 1
                    j += 1
                line.insert(j, ")")
                # ici on compte tout le bloc puis insert à la fin
        i += 1

    score = dfs(line)
    total += score

print(total) # 275011754427339
