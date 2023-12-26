
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


occurencesParInverseurParent = defaultdict(list)

for turn in range(1, 10000):
    actions = deque()
    for son in sons["broadcaster"]:
        actions.appendleft((son, LOW))

    while actions:
        parent, pulse = actions.pop()
        if modules[parent] == FLIP_FLOP and pulse == LOW:
            toSend = state[parent]
            for son in sons[parent]:
                actions.appendleft((son, toSend))
                if modules[son] == CONJUNCTION:
                    state[son][parent] = toSend
            state[parent] = HIGH if toSend == LOW else LOW

        if modules[parent] == CONJUNCTION:
            toSend = LOW if all(state[parent][gp] == HIGH for gp in state[parent]) else HIGH
            if toSend == HIGH:
                if parent in ("sb", "nd", "ds", "hf"):
                    occurencesParInverseurParent[parent].append(turn) 
                    # ppcm des 4 cycles des entrées du dernier inverseur 
                    # 4 entrées associées hardcodées, mais on peut les détecter automatiquement dans les inputs pour rendre le code plus générique si les inputs de tlm ont cette spécificité
            for son in sons[parent]:
                actions.appendleft((son, toSend))
                if modules[son] == CONJUNCTION:
                    state[son][parent] = toSend

def ppcm(a,b):
    p=a*b
    while(a!=b):
        if (a<b): b-=a
        else: a-=b
    return p/a

res = 1
for l in occurencesParInverseurParent.values():
    res = ppcm(res, l[1]-l[0])

print(res) # 215252378794009


