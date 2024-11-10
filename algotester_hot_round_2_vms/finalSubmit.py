import sys
from collections import defaultdict

INF = 1000 * 1000 * 1000 + 7


class VMType:
    def __init__(self, cpu, mem, price, turn):
        self.cpu = cpu
        self.mem = mem
        self.price = price
        self.turn = turn


vm_types = []
existing_vms = {}
cpuAndMemPerContainer = {}


def find_vm_type(cpu, mem):
    best_price = None
    ind = -1
    for i in range(m):
        if vm_types[i].cpu >= cpu and vm_types[i].mem >= mem:
            k = 1
            while vm_types[i].cpu > k * cpu:
                mmmCpu = vm_types[i].cpu - k * cpu
                k += 1
            mmmCpu = min(mmmCpu, k * cpu - vm_types[i].cpu)

            k = 1
            while vm_types[i].mem > k * mem:
                mMem= vm_types[i].mem - k * mem
                k += 1
            mMem = min(mMem, k * mem - vm_types[i].mem)

            if j < t / 1000:
                candidate = mMem + 0.01 * factorPrice * vm_types[i].price + factorCpu * mmmCpu - 0.1 * factorPrice * stats1[i]
            else:
                candidate = mMem + 0.1 * factorPrice * vm_types[i].price + factorCpu * mmmCpu - 0.01 * factorPrice * stats1[i]

            if best_price is None or candidate < best_price:
                best_price = candidate
                ind = i
    return ind


def find_vmS(cpu, mem):
    mm = -sys.maxsize
    for i, vm in existing_vms.items():
        if vm.cpu >= cpu and vm.mem >= mem:
            candidate = 0.06 * factorDSMem * min(j - vm.turn, d) - factorCpu * (vm.cpu - cpu) - (vm.mem - mem)
            if candidate > mm:
                mm = candidate

    if mm == -sys.maxsize:
        mm = None
        for i in range(m):
            if vm_types[i].cpu >= cpu and vm_types[i].mem >= mem:
                k = 1
                while vm_types[i].cpu > k * cpu:
                    mmmCpu = vm_types[i].cpu - k * cpu
                    k += 1
                mmmCpu = min(mmmCpu, k * cpu - vm_types[i].cpu)

                k = 1
                while vm_types[i].mem > k * mem:
                    mMem = vm_types[i].mem - k * mem
                    k += 1
                mMem = min(mMem, k * mem - vm_types[i].mem)

                if j < t / 1000:
                    candidate = 0.1 * factorPrice * stats1[i] - (mMem + 0.01 * factorPrice * vm_types[i].price + factorCpu * mmmCpu)
                else:
                    candidate = 0.01 * factorPrice * stats1[i] - (mMem + 0.1 * factorPrice * vm_types[i].price + factorCpu * mmmCpu)

                if mm is None or candidate > mm:  # vm_types[i].price < best_price:
                    mm = candidate

        mm /= (factorDSMem * factorCpu * factorPrice * 10000)

    return mm


def find_vm(cpu, mem):
    mm = -sys.maxsize
    best = None
    for i, vm in existing_vms.items():
        if vm.cpu >= cpu and vm.mem >= mem:
            candidate = 0.06 * factorDSMem * min(j - vm.turn, d) - factorCpu * (vm.cpu - cpu) - (vm.mem - mem)
            if candidate > mm:
                mm = candidate
                best = i
    return best


m, d = map(int, input().split())

avgMem = 0
factorCpu = 1
factorPrice = 1
for _ in range(m):
    cpu, mem, price = map(int, input().split())
    vm_types.append(VMType(cpu, mem, price, 0))
    avgMem += mem
    factorCpu *= mem
    factorPrice *= mem
    factorCpu /= cpu
    factorPrice /= price
factorCpu /= m
factorPrice /= m
avgMem /= m
factorDSMem = avgMem / d

vms_to_shutdown = []
containers_to_allocate = defaultdict(list)
containers_per_vm = defaultdict(list)
vm_per_container = {}

t = int(input().strip())

stats1 = {}
statsMoreMemory = {}
statsMoreCpu = {}
statsLessPrice = {}
for i in range(m):
    stats1[i] = (factorCpu * vm_types[i].cpu + vm_types[i].mem) / (factorPrice * vm_types[i].price)  # **2
    statsMoreMemory[i] = vm_types[i].mem
    statsMoreCpu[i] = vm_types[i].cpu
    statsLessPrice[i] = vm_types[i].price

stats = list({a: b for a, b in sorted(stats1.items(), key=lambda x: x[1], reverse=True)}.keys())
statsMoreMemory = list({a: b for a, b in sorted(statsMoreMemory.items(), key=lambda x: x[1], reverse=True)}.keys())
statsMoreCpu = list({a: b for a, b in sorted(statsMoreCpu.items(), key=lambda x: x[1], reverse=True)}.keys())
statsLessPrice = list({a: b for a, b in sorted(statsLessPrice.items(), key=lambda x: x[1])}.keys())
FF = 4
FF2 = 4
FF3 = 6
j = -1
while True:
    j += 1
    if j >= t:
        break

    line = input().split()
    v = False

    e = int(line[0])
    if e == -1:
        break  # return  # :(

    cnt = 1
    if e == 0:
        cnt = int(line[1])

    containers_to_shutdown = []
    vms_to_create = []
    toBeProcessed = {1: [], 2: []}

    for ccc in range(e):
        line = input().split()
        type_id = int(line[0])

        if type_id == 1:
            id, cpu, mem = map(int, line[1:])
            cpuAndMemPerContainer[id] = VMType(cpu, mem, 0, 0)
            toBeProcessed[1].append((find_vmS(cpu, mem), cpu, mem, id))

        elif type_id == 2:
            id = int(line[1])
            toBeProcessed[2].append(id)

    for (score, cpu, mem, id) in sorted(toBeProcessed[1], key=lambda x: x[0] + x[1] + x[2]):

        vm_id = find_vm(cpu, mem)

        if vm_id is None:
            vm_index = find_vm_type(cpu, mem)
            existing_vms[id] = VMType(vm_types[vm_index].cpu - cpu, vm_types[vm_index].mem - mem, price, j)
            vm_per_container[id] = id
            vms_to_create.append((id, vm_index))
            containers_to_allocate[j + d].append((id, id))
            containers_per_vm[id].append(id)
        else:
            existing_vms[vm_id].cpu -= cpu
            existing_vms[vm_id].mem -= mem
            containers_to_allocate[j + max(0, d - j + existing_vms[vm_id].turn)].append((id, vm_id))
            containers_per_vm[vm_id].append(id)
            vm_per_container[id] = vm_id

    for id in toBeProcessed[2]:
        vm_id = vm_per_container[id]
        containers_per_vm[vm_id].remove(id)
        info = cpuAndMemPerContainer[id]
        existing_vms[vm_id].cpu += info.cpu
        existing_vms[vm_id].mem += info.mem
        if not containers_per_vm[vm_id]:
            containers_to_shutdown.append(vm_id)
            del existing_vms[vm_id]
        del vm_per_container[id]

    if j == 0:

        if cnt <= 0:

            for i in range(max(FF3, d // FF - len(vms_to_create))):
                k = stats[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[100000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((100000 + k, k))

            for i in range(max(0, d // FF2 - len(vms_to_create))):

                k = statsMoreMemory[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[200000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((200000 + k, k))

                k = statsMoreCpu[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[300000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((300000 + k, k))

                k = statsLessPrice[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[400000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((400000 + k, k))

        else:
            v = True

    elif j > t / 160:
        for vm_id in list(existing_vms.keys()):
            if not containers_per_vm[vm_id]:

                containers_to_shutdown.append(vm_id)
                del existing_vms[vm_id]
    j -= 1

    for vvv in range(cnt):
        j += 1

        remainingTurns = cnt - vvv

        if v and remainingTurns <= d:

            v = False

            for i in range(max(FF3, d // FF - len(vms_to_create))):
                k = stats[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[100000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((100000 + k, k))

            for i in range(max(0, d // FF2 - len(vms_to_create))):

                k = statsMoreMemory[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[200000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((200000 + k, k))

                k = statsMoreCpu[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[300000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((300000 + k, k))

                k = statsLessPrice[i % len(stats)]
                if all([uu + k not in existing_vms for uu in (0, 100000, 200000, 300000, 400000)]):
                    existing_vms[400000 + k] = VMType(vm_types[k].cpu, vm_types[k].mem, vm_types[k].price, j)
                    vms_to_create.append((400000 + k, k))

        if j in containers_to_allocate:
            print(len(vms_to_create) + len(vms_to_shutdown) + len(containers_to_allocate[j]), flush=False)
        else:
            print(len(vms_to_create) + len(vms_to_shutdown), flush=False)

        for id, vm_index in vms_to_create:
            print(f"1 {id} {vm_index + 1}", flush=False)

        for id in vms_to_shutdown:
            print(f"2 {id}", flush=False)

        if j in containers_to_allocate:
            for id, vm_index in containers_to_allocate[j]:
                print(f"3 {id} {vm_index}", flush=False)

        vms_to_shutdown = containers_to_shutdown.copy()
        containers_to_shutdown.clear()
        vms_to_create.clear()

    sys.stdout.flush()

e = int(input().strip())





