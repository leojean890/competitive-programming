from functools import cmp_to_key


def compare(l1, l2):
    if isinstance(l1, list) and not isinstance(l2, list):
        out = compare(l1, [l2])
        if out != 0:
            return out

    if isinstance(l2, list) and not isinstance(l1, list):
        out = compare([l1], l2)
        if out != 0:
            return out

    if len(l1) > len(l2):
        for j in range(len(l2)):
            if isinstance(l1[j], list) and not isinstance(l2[j], list):

                out = compare(l1[j], [l2[j]])
                if out != 0:
                    return out
                else:
                    continue
            if isinstance(l2[j], list) and not isinstance(l1[j], list):
                out = compare([l1[j]], l2[j])

                if out != 0:
                    return out
                else:
                    continue
            if isinstance(l2[j], list) and isinstance(l1[j], list):
                out = compare(l1[j], l2[j])

                if out != 0:
                    return out
                else:
                    continue
            if l2[j] > l1[j]:
                return -1
            if l2[j] < l1[j]:
                return 1

        return 1

    if len(l1) < len(l2):
        for j in range(len(l1)):
            if isinstance(l1[j], list) and not isinstance(l2[j], list):

                out = compare(l1[j], [l2[j]])
                if out != 0:
                    return out
                else:
                    continue
            if isinstance(l2[j], list) and not isinstance(l1[j], list):
                out = compare([l1[j]], l2[j])
                if out != 0:
                    return out
                else:
                    continue

            if isinstance(l2[j], list) and isinstance(l1[j], list):
                out = compare(l1[j], l2[j])
                #print(out)
                if out != 0:
                    return out
                else:
                    continue

            if l2[j] > l1[j]:
                return -1
            if l2[j] < l1[j]:
                return 1

        return -1


    if len(l1) == len(l2):
        for j in range(len(l1)):
            if isinstance(l1[j], list) and not isinstance(l2[j], list):

                out = compare(l1[j], [l2[j]])
                if out != 0:
                    return out
                else:
                    continue
            if isinstance(l2[j], list) and not isinstance(l1[j], list):
                out = compare([l1[j]], l2[j])
                if out != 0:
                    return out
                else:
                    continue
            if isinstance(l2[j], list) and isinstance(l1[j], list):
                out = compare(l1[j], l2[j])

                if out != 0:
                    return out
                else:
                    continue
            if l2[j] > l1[j]:
                return -1
            if l2[j] < l1[j]:
                return 1

        return 0


r1 = [[2]]
r2 = [[6]]
allLists = [r1, r2]
score = 0
for i in range(1,151):#9
    l1 = eval(input())
    l2 = eval(input())
    allLists.append(l1)
    allLists.append(l2)
    if i != 150:
        input()


allLists = list(sorted(allLists, key=cmp_to_key(compare)))  
print(allLists)
print((allLists.index(r1)+1)*(allLists.index(r2)+1))#20304
