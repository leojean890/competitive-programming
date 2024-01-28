from collections import defaultdict
parents = {}
currentParent = None
sums = defaultdict(int)
children = defaultdict(list)
visited = set()

while 1:
    try:
        a = input().split()
        if "cd" == a[1]:#dir ftqs ['dir', 'ftqs']
            if ".." == a[2]:
                currentParent = parents[currentParent]
            else:
                if currentParent:
                    currentParent = "/".join([currentParent, a[-1]])
                else:
                    currentParent = a[-1]
        elif a[0].isdigit():
            if (a[0], a[1]) not in visited:
                sums[currentParent] += int(a[0])
                visited.add((a[0], a[1]))
                current = currentParent
                while current != "/":
                    current = parents[current]
                    sums[current] += int(a[0])
                    
        elif a[0] == "dir":
            parents["/".join([currentParent, a[-1]])] = currentParent
            children[currentParent].append("/".join([currentParent, a[-1]]))
    except Exception as ex:
            total = 0
            for x, y in sums.items():
                if y <= 100000:
                    total += y
            print(total)
            exit()

