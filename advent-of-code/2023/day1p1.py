s = 0

for i in range(1000):
    line = input()
    digits = []
    for j in line:
        if j.isdigit():
            digits.append(j)
    s += int(digits[0]+digits[-1])
print(s) # 55621
