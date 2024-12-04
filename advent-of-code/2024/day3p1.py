import re
s = ""
for i in range(6):
    s += input()
req = re.findall("mul\((\d+),(\d+)\)", s)
sum = 0
for (a,b) in req:
    sum += int(a)*int(b)
print(sum) # 174561379
