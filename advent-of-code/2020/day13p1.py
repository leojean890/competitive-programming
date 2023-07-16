timestamp = int(input())

print(reduce(lambda x, y: x*y, list(sorted([(elt-timestamp%elt,elt) for elt in [int(i) for i in input().split(",") if i != "x"]]))[0]))
