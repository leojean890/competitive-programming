from collections import deque, defaultdict

UNKNOWN = 0
FLIP_FLOP = 1
CONJUNCTION = 2
BROADCAST = 3

LOW = 0
HIGH = 1

counters = defaultdict(int)
modules = defaultdict(int) # si pas rempli, le type sera UNKNOWN et il ne se passera rien
sons = {}
state = {}

for i in range(58):
    parent, lsons = input().split(" -> ")

    if parent == "broadcaster":
        modules[parent] = BROADCAST
        sons[parent] = lsons.split(", ")
    elif parent[0] == "%":
        parent_ = parent[1:]
        modules[parent_] = FLIP_FLOP
        state[parent_] = HIGH
        sons[parent_] = lsons.split(", ")
    elif parent[0] == "&":
        parent_ = parent[1:]
        modules[parent_] = CONJUNCTION
        state[parent_] = {}
        sons[parent_] = lsons.split(", ")

for parent in sons:
    for son in sons[parent]:
        if modules[son] == CONJUNCTION:
            state[son][parent] = LOW

for turn in range(1000):
    counters[LOW] += 1
    actions = deque()
    for son in sons["broadcaster"]:
        actions.appendleft((son, LOW))
        counters[LOW] += 1

    while actions:
        parent, pulse = actions.pop()
        if modules[parent] == FLIP_FLOP and pulse == LOW:
            toSend = state[parent]
            for son in sons[parent]:
                actions.appendleft((son, toSend))
                counters[toSend] += 1
                if modules[son] == CONJUNCTION:
                    state[son][parent] = toSend
            state[parent] = HIGH if toSend == LOW else LOW 

        if modules[parent] == CONJUNCTION:
            toSend = LOW if all(state[parent][gp] == HIGH for gp in state[parent]) else HIGH
            for son in sons[parent]:
                actions.appendleft((son, toSend))
                counters[toSend] += 1
                if modules[son] == CONJUNCTION:
                    state[son][parent] = toSend

print(counters[0]*counters[1]) # 791120136
