l = list(input().split())
print(list(sorted([(l.count(a),a) for a in l]))[-1][1])
