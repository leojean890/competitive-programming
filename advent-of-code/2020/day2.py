counter = 0
for i in range(1000):
    rule, pwd = input().split(": ")
    interval, letter = rule.split()
    a, b = map(int,interval.split("-"))
    if letter in (pwd[a-1], pwd[b-1]) and pwd[a-1] != pwd[b-1]:# a <= pwd.count(letter) <= b:
        counter += 1
print(counter)
