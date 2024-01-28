while 1:
    try:
        a = input()
        if not a.isdigit():
            l.append(current)
            current = 0
        else:
            current += int(a)
    except Exception:
        l.append(current)
        break

l.sort()
print(sum(l[-3:]))
