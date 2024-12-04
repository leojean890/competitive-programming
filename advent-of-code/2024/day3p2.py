import re

s = ""
for i in range(6):
    s += input()

s2 = ""
trigger = True
for i in range(len(s)):
    if s[i:i+7] == "don't()":
        trigger = False

    if s[i:i+4] == "do()":
        trigger = True

    if trigger:
        s2 += s[i]

req = re.findall("mul\((\d+),(\d+)\)", s2)
sum = 0
for (a,b) in req:
    sum += int(a)*int(b)
print(sum) # 106921067
