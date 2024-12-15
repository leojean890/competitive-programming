from time import process_time

start_time = process_time()
lines = []
N = 50
deltaPerInput = {"<":(-1,0),"^":(0,-1),">":(1,0),"v":(0,1)}
for i in range(N):
    lines.append(list(input()))
    for j in range(N):
        if lines[i][j] == "@":
            y,x=i,j
            lines[i][j] = "."

input()
for j in range(20):
    for action in input():
        (dx,dy) = deltaPerInput[action]
        r,c = y+dy,x+dx
        while lines[r][c] == "O":
            r, c = r + dy, c + dx
        if lines[r][c] == ".":
            if dy == 1:
                for i in reversed(range(min(r,y)+1,max(r,y)+1)):
                    lines[i][c] = lines[i-1][c]
            elif dy == -1:
                for i in range(min(r,y),max(r,y)):
                    lines[i][c] = lines[i+1][c]
            if dx == 1:
                for i in reversed(range(min(c,x)+1,max(c,x)+1)):
                    lines[r][i] = lines[r][i-1]
            elif dx == -1:
                for i in range(min(c,x),max(c,x)):
                    lines[r][i] = lines[r][i+1]
            y, x = y+dy,x+dx

score = 0
for i in range(N):
    for j in range(N):
        if lines[i][j] == "O":
            score += 100*i+j

print(process_time() - start_time, score)  # 0.03 1349898
