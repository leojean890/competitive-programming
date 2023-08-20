
from time import process_time
from typing import List
import sys

class Pos:
    def __init__(self, y: int, x: int, index: int, dist: int):
        self.y = y
        self.x = x
        self.index = index
        self.dist = dist

class Judge:
    def set_temperature(self, temperature: List[List[int]]) -> None:
        for row in temperature:
            print(" ".join(map(str, row)))
        sys.stdout.flush()

    def measure(self, i: int, y: int, x: int) -> int:
        print(f"{i} {y} {x}", flush=True)
        v = int(input())

        if v == -1:
            print(f"something went wrong. i={i} y={y} x={x}", file=sys.stderr)
            sys.exit(1)
        return v

    def answer(self, estimate: List[int]) -> None:
        print("-1 -1 -1")
        for e in estimate:
            print(e)
        sys.stdout.flush()


class Solver:

    def __init__(self, L: int, N: int, S: int, landing_pos: List[Pos], time):
        self.L = L
        self.N = N
        self.S = S
        self.landing_pos = landing_pos
        self.judge = Judge()
        self.start_time = time
        self.best = (0,0)

    def solve(self) -> None:
        temperature = self._create_temperature()
        self.judge.set_temperature(temperature)
        estimate = self._predict(temperature)
        self.judge.answer(estimate)

    def _create_temperature(self) -> List[List[int]]:
        temperature = [[0] * self.L for _ in range(self.L)]
        STEP, STEP1, STEP2, STEP3 = 150, 500, 800, 1000
        self.best = (0,0)
        bestD = sys.maxsize
        for i in range(self.L):
            for j in range(self.L):
                d = 0
                for k, pos in enumerate(self.landing_pos):
                    d += abs(i-pos.y) + abs(j-pos.x)
                if d < bestD:
                    bestD = d
                    self.best = (i,j)
        if self.S < 30:
            temperature[self.best[0]][self.best[1]] = int(STEP)
        elif self.S < 100:
            temperature[self.best[0]][self.best[1]] = int(STEP1)
        elif self.S < 200:
            temperature[self.best[0]][self.best[1]] = int(STEP2)
        else:
            temperature[self.best[0]][self.best[1]] = int(STEP3)
        return temperature

    def _predict(self, temperature: List[List[int]]) -> List[int]:
        out = [-1] * self.N
        estimate = {}
        for i_in in range(self.N):
            estimate[i_in] = 0

        total = 0
        iters = 0
        while total == 0:
            total += self.N
            iters += 1
            for i_in in range(self.N):
                best = -sys.maxsize
                bestV = 0
                for j_in in range(self.N):
                    if j_in not in out:
                        
                        measured_value = self.judge.measure(i_in, self.best[0]-self.landing_pos[j_in].y, self.best[1]-self.landing_pos[j_in].x)
                        
                        if measured_value > best:
                            best = measured_value
                            bestV = j_in
                            if measured_value == 1000 or measured_value > 4*self.S:
                                break
                            
                out[i_in] = bestV

        return out

    def getNbIter(self):
        return min(self.S*280, 10001)

    def any0(self, temperature):
        for i in range(self.L):
            for j in range(self.L):
                if temperature[i][j] == 0:
                    return True
        return False

def dist(y, x, landing_pos, N, L):
    dy = y - landing_pos[0].y
    dx = x - landing_pos[0].x
    if dx < 0: dx=-dx
    if dy < 0: dy=-dy
    if 2 * dx >= N: dx=L-dx
    if 2 * dy >= N: dy=L-dy
    return dx * dx + dy * dy


def main():
    L, N, S = [int(v) for v in input().split(" ")]
    start_time = process_time()
    landing_pos = []
    for i in range(N):
        y, x = (int(v) for v in input().split(" "))
        if not landing_pos:
            landing_pos.append(Pos(y, x, i, 0))
        else:
            landing_pos.append(Pos(y, x, i, dist(y, x, landing_pos, N, L)))

    solver = Solver(L, N, S, landing_pos, start_time)
    solver.solve()


if __name__ == "__main__":
    main()
