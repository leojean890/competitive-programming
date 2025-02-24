import random
import sys
from collections import defaultdict
from copy import deepcopy
from time import process_time

Pos = tuple[int, int]
EMPTY = -1
DO_NOTHING = -1
STATION = 0
RAIL_HORIZONTAL = 1
RAIL_VERTICAL = 2
RAIL_LEFT_DOWN = 3
RAIL_LEFT_UP = 4
RAIL_RIGHT_UP = 5
RAIL_RIGHT_DOWN = 6
COST_STATION = 5000
COST_RAIL = 100


def distance(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Action:
    def __init__(self, type: int, pos: Pos):
        self.type = type
        self.pos = pos

    def __str__(self):
        if self.type == DO_NOTHING:
            return "-1"
        else:
            return f"{self.type} {self.pos[0]} {self.pos[1]}"


class Result:
    def __init__(self, actions: list[Action], score: int):
        self.actions = actions
        self.score = score

    def __str__(self):
        return "\n".join(map(str, self.actions))


class Field:
    def __init__(self, N: int):
        self.N = N
        self.rail = [[EMPTY] * N for _ in range(N)]

    def build(self, type: int, r: int, c: int) -> None:
        assert self.rail[r][c] != STATION
        if 1 <= type <= 6:
            assert self.rail[r][c] == EMPTY
        self.rail[r][c] = type


class Solver:
    def __init__(self, N: int, M: int, K: int, T: int, home: list[Pos], workplace: list[Pos]):
        self.N = N
        self.M = M
        self.K = K
        self.T = T
        self.home = home
        self.workplace = workplace
        self.field = Field(N)
        self.money = K
        self.actions = []

    def calc_income(self, homes, workplaces) -> int:
        income = 0
        for index in homes:
            if index in workplaces:
                income += distsPerPerson[index]
        return income

    def build_rail(self, type: int, r: int, c: int) -> None:
        self.field.build(type, r, c)
        self.money -= COST_RAIL
        self.actions.append(Action(type, (r, c)))

    def build_station(self, r: int, c: int) -> None:
        self.field.build(STATION, r, c)
        self.money -= COST_STATION
        self.actions.append(Action(STATION, (r, c)))

    def build_nothing(self) -> None:
        self.actions.append(Action(DO_NOTHING, (0, 0)))

    def findAPath(self, home, workplace):
        r0, c0 = home
        r1, c1 = workplace
        # r0 -> r1
        if r0 < r1:
            for r in range(r0 + 1, r1):
                if self.field.rail[r][c0] != EMPTY:return False
            if c0 < c1:
                if self.field.rail[r1][c0] != EMPTY:return False
            elif c0 > c1:
                if self.field.rail[r1][c0] != EMPTY:return False
        elif r0 > r1:
            for r in range(r0 - 1, r1, -1):
                if self.field.rail[r][c0] != EMPTY:return False
            if c0 < c1:
                if self.field.rail[r1][c0] != EMPTY:return False
            elif c0 > c1:
                if self.field.rail[r1][c0] != EMPTY:return False
        # c0 -> c1
        if c0 < c1:
            for c in range(c0 + 1, c1):
                if self.field.rail[r1][c] != EMPTY:return False
        elif c0 > c1:
            for c in range(c0 - 1, c1, -1):
                if self.field.rail[r1][c] != EMPTY:return False
        return True

    def solve(self) -> Result:

        bestScore = 0
        bestActions = []
        nR = 0
        neighbors = defaultdict(list)

        for person_idx in range(self.M):
            neighbors[self.home[person_idx]].append(self.workplace[person_idx])
            neighbors[self.workplace[person_idx]].append(self.home[person_idx])

        while process_time() - start_time < 2.5:
            homes = []
            workplaces = []
            nR += 1
            self.field = Field(N)
            self.money = K
            self.actions = []
            nbActions = random.randint(1,T//64)
            nbBuilds = 0
            builtWorkplaces = []
            builtHomes = []
            while nbBuilds < nbActions and len(self.actions) < T/32:
                action = random.randint(0,4)
                built = builtWorkplaces+builtHomes

                candidates = []
                r0 = None
                if not action or nbBuilds == 0:
                    rail_count = (self.money - COST_STATION * 2) // COST_RAIL

                    for person_idx in range(self.M):
                        d = distance(self.home[person_idx], self.workplace[person_idx]) - 1
                        if d <= rail_count and self.findAPath(self.home[person_idx], self.workplace[person_idx]):
                            candidates.append(person_idx)

                    if candidates:
                        person_idx = random.choice(candidates)

                        # build stations

                        # connect stations with rails
                        r0, c0 = self.home[person_idx]
                        r1, c1 = self.workplace[person_idx]

                        if (r0, c0) not in builtWorkplaces and (r0, c0) not in builtHomes:
                            self.build_station(*self.home[person_idx])
                            builtHomes.append((r0, c0))

                        if (r1, c1) not in builtWorkplaces and (r1, c1) not in builtHomes:
                            self.build_station(*self.workplace[person_idx])
                            builtWorkplaces.append((r1, c1))

                        for indexWorkplace in concernedWorkplacesPerStation[self.workplace[person_idx]]:
                            if indexWorkplace not in workplaces:
                                workplaces.append(indexWorkplace)
                        for indexHome in concernedHomesPerStation[self.home[person_idx]]:
                            if indexHome not in homes:
                                homes.append(indexHome)
                if action > 1 and nbBuilds > 0:
                    rail_count = (self.money - COST_STATION) // COST_RAIL
                    candidates = [(r1, c1) for (r1, c1) in built if any(len(neighbors[(a, b)]) > 0 for a in range(r1-2,r1+3) for b in range(c1-2,c1+3) if abs(r1-a) + abs(c1-b) <= 2)]
                    if candidates:
                        r1, c1 = random.choice(candidates)
                        possible = []
                        for a in range(r1 - 2, r1 + 3):
                            for b in range(c1-2, c1+3):
                                if abs(r1-a) + abs(c1-b) <= 2 and len(neighbors[(a, b)]) > 0:
                                    for (u,v) in neighbors[(a, b)]:
                                        possible.append((u,v))
                        r0, c0 = random.choice(possible)
                        itt1 = 0
                        departOrArrival = (r1, c1) in builtWorkplaces

                        while not (r0 < len(self.field.rail) and c0 < len(self.field.rail[r0]) and self.field.rail[r0][c0] == EMPTY):
                            itt1 += 1
                            if itt1 > 100:break
                            r0, c0 = random.choice(possible)
                        if itt1 > 100: continue

                    else:
                        departOrArrival = random.randint(0, 1)

                        if departOrArrival:
                            r1, c1 = random.choice(builtWorkplaces)
                            r0, c0 = random.choice(self.home)
                            while self.field.rail[r0][c0] != EMPTY:
                                r0, c0 = random.choice(self.home)
                        else:
                            r0, c0 = random.choice(self.workplace)
                            while self.field.rail[r0][c0] != EMPTY:
                                r0, c0 = random.choice(self.workplace)
                            r1, c1 = random.choice(builtHomes)

                    itt = 0

                    while not self.findAPath((r0, c0), (r1, c1)) or distance((r0, c0), (r1, c1)) - 1 > rail_count:
                        itt += 1
                        if itt > 100:
                            break

                        candidates = [(r1, c1) for (r1, c1) in built if any(
                            len(neighbors[(a, b)]) > 0 for a in range(r1 - 2, r1 + 3) for b in range(c1 - 2, c1 + 3) if
                            abs(r1 - a) + abs(c1 - b) <= 2)]
                        if candidates:
                            r1, c1 = random.choice(candidates)
                            possible = []
                            for a in range(r1 - 2, r1 + 3):
                                for b in range(c1 - 2, c1 + 3):
                                    if abs(r1 - a) + abs(c1 - b) <= 2 and len(neighbors[(a, b)]) > 0:
                                        for (u, v) in neighbors[(a, b)]:
                                            possible.append((u, v))
                            r0, c0 = random.choice(possible)
                            departOrArrival = (r1, c1) in builtWorkplaces
                            itt1 = 0
                            while not (
                                r0 < len(self.field.rail) and c0 < len(self.field.rail[r0]) and self.field.rail[r0][
                                c0] == EMPTY):
                                itt1 += 1
                                if itt1 > 100: break
                                r0, c0 = random.choice(possible)
                            if itt1 > 100: continue

                        else:
                            departOrArrival = random.randint(0, 1)

                            if departOrArrival:
                                r1, c1 = random.choice(builtWorkplaces)
                                r0, c0 = random.choice(self.home)
                                while self.field.rail[r0][c0] != EMPTY:
                                    r0, c0 = random.choice(self.home)
                            else:
                                r0, c0 = random.choice(self.workplace)
                                while self.field.rail[r0][c0] != EMPTY:
                                    r0, c0 = random.choice(self.workplace)
                                r1, c1 = random.choice(builtHomes)

                    if itt > 100:
                        break
                    else:
                        if self.field.rail[r0][c0] != EMPTY:continue

                        self.build_station(r0, c0)
                        if departOrArrival:
                            builtHomes.append((r0,c0))
                        else:
                            builtWorkplaces.append((r0,c0))

                        for indexWorkplace in concernedWorkplacesPerStation[(r0, c0)]:
                            if indexWorkplace not in workplaces:
                                workplaces.append(indexWorkplace)
                        for indexHome in concernedHomesPerStation[(r0, c0)]:
                            if indexHome not in homes:
                                homes.append(indexHome)

                if (r0 is None or action == 1) and nbBuilds > 0:
                    income = self.calc_income(homes, workplaces)
                    self.build_nothing()
                    self.money += income
                    continue

                # r0 -> r1
                if r0 < r1:
                    for r in range(r0 + 1, r1):
                        self.build_rail(RAIL_VERTICAL, r, c0)
                    if c0 < c1:
                        self.build_rail(RAIL_RIGHT_UP, r1, c0)
                    elif c0 > c1:
                        self.build_rail(RAIL_LEFT_UP, r1, c0)
                elif r0 > r1:
                    for r in range(r0 - 1, r1, -1):
                        self.build_rail(RAIL_VERTICAL, r, c0)
                    if c0 < c1:
                        self.build_rail(RAIL_RIGHT_DOWN, r1, c0)
                    elif c0 > c1:
                        self.build_rail(RAIL_LEFT_DOWN, r1, c0)
                # c0 -> c1
                if c0 < c1:
                    for c in range(c0 + 1, c1):
                        self.build_rail(RAIL_HORIZONTAL, r1, c)
                elif c0 > c1:
                    for c in range(c0 - 1, c1, -1):
                        self.build_rail(RAIL_HORIZONTAL, r1, c)
                income = self.calc_income(homes, workplaces)

                self.money += income
                nbBuilds += 1

            income = self.calc_income(homes, workplaces)

            while len(self.actions) < self.T:
                self.build_nothing()
                self.money += income

            if self.money > bestScore:
                bestScore = self.money
                bestActions = deepcopy(self.actions)

        print("nRollouts", nR, file=sys.stderr)
        return Result(bestActions, bestScore)


N, M, K, T = map(int, input().split())
start_time = process_time()
random.seed(1)
home = []
workplace = []
concernedWorkplacesPerStation = defaultdict(list)
concernedHomesPerStation = defaultdict(list)
distsPerPerson = defaultdict(int)
for i in range(M):
    r0, c0, r1, c1 = map(int, input().split())
    home.append((r0, c0))
    workplace.append((r1, c1))
    for dr in range(-2, 3):
        for dc in range(-2, 3):
            if abs(dr) + abs(dc) <= 2:
                concernedHomesPerStation[(r0+dr,c0+dc)].append(i)
                concernedWorkplacesPerStation[(r1+dr,c1+dc)].append(i)
                distsPerPerson[i] = distance((r0, c0), (r1, c1))

solver = Solver(N, M, K, T, home, workplace)
result = solver.solve()
print(result)
print(f"score={result.score}", file=sys.stderr)

