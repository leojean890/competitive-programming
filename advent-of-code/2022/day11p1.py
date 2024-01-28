
from collections import defaultdict
turn = 0
nbActions = defaultdict(int)
operations = defaultdict(str)
monkeyStuff = defaultdict(list)
toProcess = []
throw = defaultdict(list)
divisibleCond = defaultdict(int)
current = 0
while 1:
    try:
        action = input()
        if "Monkey" in action:
            for item in toProcess:
                nItem = eval(operation.replace("old", item))#//3
                if nItem % divisibleCond[current]: # pas divisible par car reste non nul
                    monkeyStuff[throw[current][1]].append(nItem)
                else:
                    monkeyStuff[throw[current][0]].append(nItem)
            nbActions[current] += len(monkeyStuff[current])

            for item in monkeyStuff[current]:
                nItem = eval(operation.replace("old", str(item))) #// 3
                if nItem % divisibleCond[current]: # pas divisible par car reste non nul
                    monkeyStuff[throw[current][1]].append(nItem)
                else:
                    monkeyStuff[throw[current][0]].append(nItem)
            monkeyStuff[current] = []
            current = int(action[7])
        elif "Starting items" in action:
            toProcess = action.replace(" ","").split(":")[1].split(",")
            nbActions[current] += len(toProcess)
        elif "Operation" in action:
            operation = action.replace(" ","").split("=")[1]
            operations[current] = operation
        elif "Test" in action:
            divisibleCond[current] = int(action.replace(" ","").split("by")[1])
        elif "monkey" in action:
            throw[current].append(int(action.replace(" ","").split("monkey")[1]))


    except Exception as ex:
        for item in toProcess:
            nItem = eval(operation.replace("old", item)) #// 3
            if nItem % divisibleCond[current]:  # pas divisible par car reste non nul
                monkeyStuff[throw[current][1]].append(nItem)
            else:
                monkeyStuff[throw[current][0]].append(nItem)

        nbActions[current] += len(monkeyStuff[current])

        for item in monkeyStuff[current]:
            nItem = eval(operation.replace("old", str(item))) #// 3
            if nItem % divisibleCond[current]:  # pas divisible par car reste non nul
                monkeyStuff[throw[current][1]].append(nItem)
            else:
                monkeyStuff[throw[current][0]].append(nItem)
        monkeyStuff[current] = []

        current = 0
        prodDiv = 1
        for elt in divisibleCond.values():
            prodDiv *= elt
            print(prodDiv)

        for i in range(9999):
            for current in range(max(monkeyStuff.keys())+1):
                nbActions[current] += len(monkeyStuff[current])
                for item in monkeyStuff[current]:
                    nItem = eval(operations[current].replace("old", str(item))) #// 3

                    if nItem % divisibleCond[current]: # pas divisible par car reste non nul
                        monkeyStuff[throw[current][1]].append(nItem%prodDiv)
                    else:
                        monkeyStuff[throw[current][0]].append(nItem%prodDiv)
                monkeyStuff[current] = []
        print(nbActions)
        break



