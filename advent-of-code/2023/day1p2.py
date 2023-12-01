

s = 0
convert = {"zero":"0","one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9"}
for i in range(1000):
    line = input()
    digits = []
    for j in range(len(line)):
        for nb in ("zero","one", "two", "three", "four", "five", "six", "seven", "eight", "nine"):
            value = line[j:j + len(nb)]
            if value == nb:
                digits.append(convert[value])
                break
        if line[j].isdigit():
            digits.append(line[j])
    print(digits)
    s += int(digits[0]+digits[-1])
print(s) # 53592

