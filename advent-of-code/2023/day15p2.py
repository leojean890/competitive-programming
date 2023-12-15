boxes = []
for i in range(256):
    boxes.append({})
for seq in input().split(","):
    current = 0
    strr = ""
    for char in seq:
        if char in ("-","="):
            break
        strr += char
        current += ord(char)
        current = (current*17)%256
    if "-" in seq:
        if strr in boxes[current]:
            del boxes[current][strr]
    else:
        value = int(seq.split("=")[1])
        boxes[current][strr] = value

    total = 0

    for i in range(len(boxes)):
        j = 1
        for value in boxes[i].values():
            total += (i+1)*j*value
            j += 1

print(total) # 294474

