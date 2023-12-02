from collections import defaultdict

MAX = {"red": 12, "green": 13, "blue": 14}
total = 0

for turn in range(1,101):
    game = input().split(":")[1].split(";")
    m = defaultdict(int)
    for partie in game:
        curr = partie.split(",")
        for elt in curr:
            eltt = elt.split()
            color, amount = eltt[-1], int(eltt[-2])
            m[color] = max(m[color], amount)
    total += m["red"] * m["green"] * m["blue"]
print(total) #63700
