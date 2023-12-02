MAX = {"red": 12, "green": 13, "blue": 14}
total = 0

for turn in range(1,101):
    game = input().split(":")[1].split(";")
    for partie in game:
        curr = partie.split(",")
        for elt in curr:
            eltt = elt.split()
            color, amount = eltt[-1], int(eltt[-2])
            if amount > MAX[color]:
                break
        if amount > MAX[color]:
            break
    else:
        total += turn
print(total) # 2176
