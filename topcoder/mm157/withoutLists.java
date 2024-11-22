import java.util.*;
import java.io.*;
import java.security.SecureRandom;
import java.util.stream.IntStream;

public class RollingBalls {
    private static final List<String> DIR = List.of("D","U","R","L");
    private static final int[][] DIRS = new int[][]{
        new int[]{1, 0},
        new int[]{-1, 0},
        new int[]{0, 1},
        new int[]{0, -1}
    };
    private static final Map<String, int[]> DIRECTIONS = Map.of(
        "D", new int[]{1, 0},
        "U", new int[]{-1, 0},
        "R", new int[]{0, 1},
        "L", new int[]{0, -1}
    );

    private static final double t_start = 1d;
    private static final double t_final = 0.0001d;
    private static double T;

    public static void main(String[] args) throws Exception {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random(1);

        int N = scanner.nextInt();
        double startTime = System.currentTimeMillis();
        int C = scanner.nextInt();
        int K = scanner.nextInt();
        int PARAM = 40*(K+1);

        int[][] grid = new int[N][N];
        int[][] target = new int[N][N];

        int nRollouts = 0;
        int nNodes = 0;

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                grid[r][c] = scanner.nextInt();
            }
        }

        double initialPenalty = 0;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                target[r][c] = scanner.nextInt();
                if (grid[r][c] > 0) {
                    if (target[r][c] == 0) {
                        initialPenalty += N;
                    } else if (target[r][c] != grid[r][c]) {
                        initialPenalty += N / 2.0;
                    }
                }
            }
        }

        double bestScore = initialPenalty;
        System.err.println(initialPenalty);

        List<String> bestMoves = new ArrayList<>();
        List<SaState> bestStates = new ArrayList<>();
        List<String> bestBlocks = new ArrayList<>();


            while ((System.currentTimeMillis()- startTime) < 2000) {
                //nRollouts++;
                List<String> moves = new ArrayList<>();
                List<SaState> currStates = new ArrayList<>();
                int[][] currentGrid = new int[N][N];
                List<int[]> freeCells = new ArrayList<>();
                List<int[]> balls = new ArrayList<>();
                List<int[]> orderedBalls = new ArrayList<>();

                for (int r = 0; r < N; r++) {
                    System.arraycopy(grid[r], 0, currentGrid[r], 0, N);
                    for (int c = 0; c < N; c++) {
                        if (grid[r][c] == 0 && target[r][c] == 0) {
                            freeCells.add(new int[]{r, c});
                        } else if (grid[r][c] > 0) {
                            orderedBalls.add(new int[]{r, c});
                            if (target[r][c] != grid[r][c])
                                balls.add(new int[]{r, c});
                        }
                    }
                }

                Collections.shuffle(balls,random);

                double score = initialPenalty;

                for (int nMove = 0; nMove < N * N; nMove++) {
                    if (balls.isEmpty()) break;
                    if ((System.currentTimeMillis()- startTime) > 2500) break;

                    int[] move = new int[]{};
                    boolean found = false;

                    for (int[] selectedBall : balls) {
                        for (String dir : DIRECTIONS.keySet()) {
                            int dy = DIRECTIONS.get(dir)[0];
                            int dx = DIRECTIONS.get(dir)[1];
                            int a = selectedBall[0] + dy;
                            int b = selectedBall[1] + dx;
                            if (a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0) {
                                int y = selectedBall[0];
                                int x = selectedBall[1];

                                while (a + dy >= 0 && a + dy < N && b + dx >= 0 && b + dx < N && currentGrid[a + dy][b + dx] == 0) {
                                    a += dy;
                                    b += dx;
                                }

                                if (target[a][b] == currentGrid[y][x]) {
                                    move = new int[]{a, b, dy, dx, y, x};
                                    found = true;
                                }
                            }
                            if (found)break;
                        }
                        if (found)break;
                    }
                    if (!found) {

                        List<int[]> availableBalls = new ArrayList<>(balls);
                        int[] selectedBall = availableBalls.get(random.nextInt(availableBalls.size()));
                        List<int[]> validMoves = new ArrayList<>();

                        for (String dir : DIRECTIONS.keySet()) {
                            int dy = DIRECTIONS.get(dir)[0];
                            int dx = DIRECTIONS.get(dir)[1];
                            int a = selectedBall[0] + dy;
                            int b = selectedBall[1] + dx;
                            if (a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0) {
                                validMoves.add(new int[]{a, b, dy, dx});
                            }
                        }

                        while (validMoves.isEmpty() && !availableBalls.isEmpty()) {
                            availableBalls.remove(selectedBall);
                            if (availableBalls.isEmpty()) break;

                            selectedBall = availableBalls.get(random.nextInt(availableBalls.size()));
                            validMoves.clear();

                            for (String dir : DIRECTIONS.keySet()) {
                                int dy = DIRECTIONS.get(dir)[0];
                                int dx = DIRECTIONS.get(dir)[1];
                                int a = selectedBall[0] + dy;
                                int b = selectedBall[1] + dx;
                                if (a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0) {
                                    validMoves.add(new int[]{a, b, dy, dx});
                                }
                            }
                        }

                        if (availableBalls.isEmpty()) break;

                        move = validMoves.get(random.nextInt(validMoves.size()));

                        int a = move[0];
                        int b = move[1];
                        int dy = move[2];
                        int dx = move[3];

                        int y = selectedBall[0];
                        int x = selectedBall[1];

                        while (a + dy >= 0 && a + dy < N && b + dx >= 0 && b + dx < N && currentGrid[a + dy][b + dx] == 0) {
                            a += dy;
                            b += dx;
                        }

                        move = new int[]{a, b, dy, dx, y, x};

                    }

                    //nNodes++;
                    int a = move[0];
                    int b = move[1];
                    int dy = move[2];
                    int dx = move[3];
                    int y = move[4];
                    int x = move[5];
                    int[] uu = new int[]{y, x};

                    currentGrid[a][b] = currentGrid[y][x];
                    currentGrid[y][x] = 0;
                    balls.removeIf(ball -> Arrays.equals(ball, uu));
                    if (target[a][b] != currentGrid[a][b]) {
                        balls.add(new int[]{a, b});
                    }

                    int index = IntStream.range(0, orderedBalls.size())
                        .boxed().filter(ii -> Arrays.equals(orderedBalls.get(ii), uu))
                        .findFirst().orElse(0);

                    orderedBalls.set(index, new int[]{a, b});

                    moves.add(y + " " + x + " " + dirForMove(dy, dx));
                    currStates.add(new SaState(index, dir1ForMove(dy, dx)));

                    if (target[y][x] == 0) {
                        if (target[a][b] == currentGrid[a][b]) {
                            score -= N;
                        } else if (target[a][b] > 0) {
                            score -= N / 2.0;
                        }
                    } else if (target[y][x] != currentGrid[a][b]) {
                        if (target[a][b] == currentGrid[a][b]) {
                            score -= N / 2.0;
                        } else if (target[a][b] == 0) {
                            score += N / 2.0;
                        }
                    } else {
                        if (target[a][b] == 0) {
                            score += N;
                        } else if (target[a][b] != currentGrid[a][b]) {
                            score += N / 2.0;
                        }
                    }

                    score += 1;

                    if (score < bestScore) {
                        //System.err.println(score);
                        bestStates = new ArrayList<>(currStates);
                        bestScore = score;
                    }
                }
            }


            int bmovesSize = 0;
            int[] bMoves = new int[N*N*N];
            List<SaState> currStates = new ArrayList<>(bestStates);
            double currScore = bestScore;
            var elapsed = System.currentTimeMillis() - startTime;

            while (elapsed < 9000) {
                nRollouts++;

                int[] moves = new int[N*N*N];
                List<SaState> states = new ArrayList<>(currStates);
                int[][] currentGrid = new int[N][N];
                double score = initialPenalty;
                int actionType = random.nextInt(3);
                int[] balls = new int[N*N];
                int currMove = -1;//numéro dans la liste des moves
                int toMove = 0;//numéro de la balle a bouger
                int direc = 0;
                int ballsSize = 0;
                int movesSize = 0;

                for (int r = 0; r < N; r++) {
                    System.arraycopy(grid[r], 0, currentGrid[r], 0, N);
                    for (int c = 0; c < N; c++) {
                        if (grid[r][c] == 0 && target[r][c] == 0) {
                        } else if (grid[r][c] > 0) {
                            balls[ballsSize] = N*r+c;
                            ballsSize += 1;
                        }
                    }
                }

                if (actionType == 1) { // modif
                     currMove = random.nextInt(states.size());
                     toMove = random.nextInt(ballsSize);
                     direc = random.nextInt(4);

                } else if (actionType == 2) { // add
                     currMove = random.nextInt(states.size()+1);
                     toMove = random.nextInt(ballsSize);
                     direc = random.nextInt(4);

                } else { // deletion (actionType == 0)
                     currMove = random.nextInt(states.size()-1);
                     states.remove(currMove);
                }

                int i = 0;
                int L = states.size();

                while (i < L) {
                    nNodes++;

                    if (i == currMove && actionType > 0) {
                        int ball = balls[toMove];
                        int y = ball/N;
                        int x = ball%N;
                        int dy = DIRS[direc][0];
                        int dx = DIRS[direc][1];
                        if (actionType == 1) {
                            states.set(i, new SaState(toMove,direc));
                        } else {
                            states.add(i, new SaState(toMove,direc));
                            L += 1;
                        }
                    }

                    SaState state = states.get(i);
                    int dir = state.direction;
                    int dy = DIRS[dir][0];
                    int dx = DIRS[dir][1];

                    int id = state.index;
                    int ball = balls[id];
                    int y = ball/N;
                    int x = ball%N;

                    int a = y + dy;
                    int b = x + dx;
                    if(!(a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0)) {
                        i += 1;
                        if (i == currMove && L == i) {

                            dy = DIRS[direc][0];
                            dx = DIRS[direc][1];
                            states.add(new SaState(toMove,direc));
                            L += 1;
                        }
                        continue;
                    }
                    while (a + dy >= 0 && a + dy < N && b + dx >= 0 && b + dx < N && currentGrid[a + dy][b + dx] == 0) {
                        a += dy;
                        b += dx;
                    }

                    moves[movesSize] = N*N*y+N*x+dir;
                    movesSize += 1;

                    currentGrid[a][b] = currentGrid[y][x];
                    currentGrid[y][x] = 0;

                    balls[id] = N*a+b;

                    if (target[y][x] == 0) {
                        if (target[a][b] == currentGrid[a][b]) {
                            score -= N;
                        } else if (target[a][b] > 0) {
                            score -= N / 2.0;
                        }
                    } else if (target[y][x] != currentGrid[a][b]) {
                        if (target[a][b] == currentGrid[a][b]) {
                            score -= N / 2.0;
                        } else if (target[a][b] == 0) {
                            score += N / 2.0;
                        }
                    } else {
                        if (target[a][b] == 0) {
                            score += N;
                        } else if (target[a][b] != currentGrid[a][b]) {
                            score += N / 2.0;
                        }
                    }

                    score += 1;
                    i += 1;
                    if (i == currMove && L == i) {
                        ball = balls[toMove];
                        y = ball/N;
                        x = ball%N;
                        dy = DIRS[direc][0];
                        dx = DIRS[direc][1];
                        states.add(new SaState(toMove,direc));
                        L += 1;
                    }
                }

                if (score < currScore) {
                    currStates = states;
                    currScore = score;

                    if (score < bestScore) {
                        //System.err.println(score);
                        bmovesSize = movesSize;
                        for (int k = 0 ; k < movesSize ; k++) {
                            bMoves[k] = moves[k];
                        }

                        bestStates = new ArrayList<>(states);
                        bestScore = score;
                    }
                } else {
                    double rr = random.nextDouble(0,1);

                    if (elapsed < 1000)
                        T = t_start*Math.pow(t_final/t_start, elapsed/1000);
                    else if (elapsed < 2000)
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 1000)/1000);
                    else if (elapsed < 3000)
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 2000)/1000);
                    else if (elapsed < 4000)
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 3000)/1000);
                    else if (elapsed < 5000)
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 4000)/1000);
                    else if (elapsed < 6000)
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 5000)/1000);
                    else if (elapsed < 7000)
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 6000)/1000);
                    else if (elapsed < 8000)
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 7000)/1000);
                    else
                        T = t_start*Math.pow(t_final/t_start, (elapsed - 8000)/1000);


                    if (Math.exp((currScore - score)/T) > rr){
                        currScore = score;
                        currStates = states;
                    }
                }

                elapsed = System.currentTimeMillis() - startTime;
            }

            bestMoves = new ArrayList<>();
            bestScore = currScore;

            int[][] currentGrid = new int[N][N];

            for (int r = 0; r < N; r++) {
                System.arraycopy(grid[r], 0, currentGrid[r], 0, N);
            }

            for (int i = 0; i < bestBlocks.size(); i++) {
                String block = bestBlocks.get(i);
                String[] m = block.split(" ");
                int y = Integer.parseInt(m[0]);
                int x = Integer.parseInt(m[1]);
                currentGrid[y][x] = -1;
            }
            System.err.println("score avant avant "+bestScore);

            for (int i = 0 ; i < bmovesSize ; i++) {
                int move = bMoves[i];
                int y = move/(N*N);
                int temp = move%(N*N);
                int x = temp/N;
                int dir = temp%N;
                int dy = DIRS[dir][0];
                int dx = DIRS[dir][1];
                int a = y + dy;
                int b = x + dx;

                if(!(a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0)) {
                    bestScore -= 1;
                    continue;
                }
                while (a + dy >= 0 && a + dy < N && b + dx >= 0 && b + dx < N && currentGrid[a + dy][b + dx] == 0) {
                    a += dy;
                    b += dx;
                }

                currentGrid[a][b] = currentGrid[y][x];
                currentGrid[y][x] = 0;
                bestMoves.add(y + " " + x + " " + DIR.get(dir));

            }


        elapsed = System.currentTimeMillis()- startTime;
        System.err.println("score avant"+bestScore);

        while (elapsed < 9700) {

            //nRollouts++;
            currentGrid = new int[N][N];
            List<int[]> balls = new ArrayList<>();
            double score = initialPenalty + K * bestBlocks.size();
            List<String> moves = new ArrayList<>();

            for (int r = 0; r < N; r++) {
                System.arraycopy(grid[r], 0, currentGrid[r], 0, N);
                for (int c = 0; c < N; c++) {
                    if (grid[r][c] == 0 && target[r][c] == 0) {
                    } else if (grid[r][c] > 0 && target[r][c] != grid[r][c]) {
                        balls.add(new int[]{r, c});
                    }
                }
            }

            for (int i = 0; i < bestBlocks.size(); i++) {
                String block = bestBlocks.get(i);
                String[] m = block.split(" ");
                int y = Integer.parseInt(m[0]);
                int x = Integer.parseInt(m[1]);
                currentGrid[y][x] = -1;
            }

            for (int i = 0 ; i < bestMoves.size() ; i++) {
                String move = bestMoves.get(i);
                moves.add(move);
                String[] m = move.split(" ");
                int y = Integer.parseInt(m[0]);
                int x = Integer.parseInt(m[1]);
                String dir = m[2];
                int dy = DIRECTIONS.get(dir)[0];
                int dx = DIRECTIONS.get(dir)[1];
                int a = y + dy;
                int b = x + dx;
                if(!(a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0)) {
                    continue;
                }
                while (a + dy >= 0 && a + dy < N && b + dx >= 0 && b + dx < N && currentGrid[a + dy][b + dx] == 0) {
                    a += dy;
                    b += dx;
                }

                currentGrid[a][b] = currentGrid[y][x];
                currentGrid[y][x] = 0;
                balls.removeIf(ball -> Arrays.equals(ball, new int[]{y, x}));
                if (target[a][b] != currentGrid[a][b]) {
                    balls.add(new int[]{a, b});
                }

                if (target[y][x] == 0) {
                    if (target[a][b] == currentGrid[a][b]) {
                        score -= N;
                    } else if (target[a][b] > 0) {
                        score -= N / 2.0;
                    }
                } else if (target[y][x] != currentGrid[a][b]) {
                    if (target[a][b] == currentGrid[a][b]) {
                        score -= N / 2.0;
                    } else if (target[a][b] == 0) {
                        score += N / 2.0;
                    }
                } else {
                    if (target[a][b] == 0) {
                        score += N;
                    } else if (target[a][b] != currentGrid[a][b]) {
                        score += N / 2.0;
                    }
                }

                score += 1;

            }

            boolean any = true;

            while (any) {
                any = false;

                Collections.shuffle(balls, random);

                for (int[] selectedBall : balls) {
                    for (String dir : DIRECTIONS.keySet()) {
                        int dy = DIRECTIONS.get(dir)[0];
                        int dx = DIRECTIONS.get(dir)[1];
                        int a = selectedBall[0] + dy;
                        int b = selectedBall[1] + dx;
                        if (a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0) {
                            int y = selectedBall[0];
                            int x = selectedBall[1];

                            while (a + dy >= 0 && a + dy < N && b + dx >= 0 && b + dx < N && currentGrid[a + dy][b + dx] == 0) {
                                a += dy;
                                b += dx;
                            }

                            if (target[a][b] == currentGrid[y][x]) {
                                any = true;

                                currentGrid[a][b] = currentGrid[y][x];
                                currentGrid[y][x] = 0;

                                balls.removeIf(ball -> Arrays.equals(ball, new int[]{y, x}));

                                if (target[a][b] != currentGrid[a][b]) {
                                    balls.add(new int[]{a, b});
                                }

                                moves.add(y + " " + x + " " + dirForMove(dy, dx));

                                if (target[y][x] == 0) {
                                    if (target[a][b] == currentGrid[a][b]) {
                                        score -= N;
                                    } else if (target[a][b] > 0) {
                                        score -= N / 2.0;
                                    }
                                } else if (target[y][x] != currentGrid[a][b]) {
                                    if (target[a][b] == currentGrid[a][b]) {
                                        score -= N / 2.0;
                                    } else if (target[a][b] == 0) {
                                        score += N / 2.0;
                                    }
                                } else {
                                    if (target[a][b] == 0) {
                                        score += N;
                                    } else if (target[a][b] != currentGrid[a][b]) {
                                        score += N / 2.0;
                                    }
                                }

                                score += 1;

                                if (score < bestScore) {
                                    //System.err.println(score);
                                    bestMoves = new ArrayList<>(moves);
                                    bestScore = score;
                                }
                                break;

                            }

                        }

                    }
                    if(any)break;

                }

                if(!any) {

                    for (int[] selectedBall : balls) {
                        int y = selectedBall[0];
                        int x = selectedBall[1];
                        if (target[y][x] == 0) {
                            for (String dir : DIRECTIONS.keySet()) {
                                int dy = DIRECTIONS.get(dir)[0];
                                int dx = DIRECTIONS.get(dir)[1];
                                int a = selectedBall[0] + dy;
                                int b = selectedBall[1] + dx;
                                if (a >= 0 && a < N && b >= 0 && b < N && currentGrid[a][b] == 0) {

                                    while (a + dy >= 0 && a + dy < N && b + dx >= 0 && b + dx < N && currentGrid[a + dy][b + dx] == 0) {
                                        a += dy;
                                        b += dx;
                                    }

                                    if (target[a][b] > 0) {
                                        any = true;

                                        currentGrid[a][b] = currentGrid[y][x];
                                        currentGrid[y][x] = 0;

                                        balls.removeIf(ball -> Arrays.equals(ball, new int[]{y, x}));

                                        if (target[a][b] != currentGrid[a][b]) {
                                            balls.add(new int[]{a, b});
                                        }

                                        moves.add(y + " " + x + " " + dirForMove(dy, dx));

                                        if (target[y][x] == 0) {
                                            if (target[a][b] == currentGrid[a][b]) {
                                                score -= N;
                                            } else if (target[a][b] > 0) {
                                                score -= N / 2.0;
                                            }
                                        } else if (target[y][x] != currentGrid[a][b]) {
                                            if (target[a][b] == currentGrid[a][b]) {
                                                score -= N / 2.0;
                                            } else if (target[a][b] == 0) {
                                                score += N / 2.0;
                                            }
                                        } else {
                                            if (target[a][b] == 0) {
                                                score += N;
                                            } else if (target[a][b] != currentGrid[a][b]) {
                                                score += N / 2.0;
                                            }
                                        }

                                        score += 1;

                                        if (score < bestScore) {
                                            //System.err.println(score);
                                            bestMoves = new ArrayList<>(moves);
                                            bestScore = score;
                                        }
                                        break;
                                    }
                                }
                            }
                            if(any)break;
                        }
                    }
                }
            }

            elapsed = System.currentTimeMillis() - startTime;
        }

        System.err.println("score final"+bestScore);

        System.out.println(bestBlocks.size() + bestMoves.size());
        System.err.println("nRollouts " + nRollouts);
        System.err.println("nNodes " + nNodes);

        for (String block : bestBlocks) System.out.println(block);
        for (String move : bestMoves) System.out.println(move);
    }

    private static String dirForMove(int dy, int dx) {
        if (dy == 1 && dx == 0) return "D";
        if (dy == -1 && dx == 0) return "U";
        if (dy == 0 && dx == 1) return "R";
        return "L";
    }

    private static int dir1ForMove(int dy, int dx) {
        if (dy == 1 && dx == 0) return 0;
        if (dy == -1 && dx == 0) return 1;
        if (dy == 0 && dx == 1) return 2;
        return 3;
    }

    private static List<String> formatBlocks(List<int[]> blocks) {
        List<String> formattedBlocks = new ArrayList<>();
        for (int[] block : blocks) {
            formattedBlocks.add(block[0] + " " + block[1] + " B");
        }
        return formattedBlocks;
    }

    public static class SaState {
        int index;
        int direction;

        public SaState(int index, int direction) {
            this.index = index;
            this.direction = direction;
        }
    }

    public static class State implements Comparable<State>{
        int[][] grid;
        Double score;
        List<int[]> balls;
        List<String> moves;
        List<int[]> blocks;

        public State(int[][] grid, List<int[]> balls, List<String> moves, Double score, List<int[]> blocks) {
            this.grid = grid;
            this.score = score;
            this.balls = balls;
            this.moves = moves;
            this.blocks = blocks;
        }

        @Override
        public int compareTo(State o){
            return -this.score.compareTo(o.score);
        }
    }
}
