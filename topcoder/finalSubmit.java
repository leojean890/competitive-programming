import java.io.*;
import java.util.*;
import java.time.Instant;
import java.security.SecureRandom;

public class Reversi {
    private static int ctrAbort = 0;
    private static int ctrRollouts = 0;
    private static int ctrNodes = 0;
    private static double TT = 9500;
    private static double T;
    private static int N;
    private static int C;
    private static int[][] grid;
    private static int[][] target;
    private static final List<int[]> DIR = new ArrayList<>();
    private static int initNbZeros;
    private static int nbBeginTiles;
    private static long startTime;
    private static long elapsed;
    private static List<int[]> iHaveNeighs = new ArrayList<>();
    private static int bestScore;
    private static List<int[]> bestMoves = new ArrayList<>();
    private static List<int[][]> bestStates = new ArrayList<>();
    private static List<List<int[]>> bestNeighs = new ArrayList<>();
    private static int currScore;
    private static List<int[]> currMoves = new ArrayList<>();
    private static List<int[][]> currStates = new ArrayList<>();
    private static List<List<int[]>> currNeighs = new ArrayList<>();
    private static Random rand = new Random(6);
    private static final double t_start = 90.0d;
    private static final double t_final = 94.0d;
    private static SecureRandom rnd;

    public static final double randomDouble(double origin, double bound) {
        if (bound <= origin) return origin;
        double r = (rnd.nextLong() >>> 11) * 0x1.0p-53;
        if (origin < bound) {
            r = r * (bound - origin) + origin;
            if (r >= bound) r = Double.longBitsToDouble(Double.doubleToLongBits(bound) - 1);
        }
        return r;
    }

    public static void main(String[] args) throws Exception {
        Scanner in = new Scanner(System.in);
        N = in.nextInt();
        startTime = System.currentTimeMillis();
        elapsed = 0L;
        C = in.nextInt();
        rnd = SecureRandom.getInstance("SHA1PRNG");
        rnd.setSeed(6);

        grid = new int[N][N];
        target = new int[N][N];

        initNbZeros = 0;
        nbBeginTiles = 0;

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                grid[r][c] = in.nextInt();
                if (grid[r][c] == 0) {
                    initNbZeros++;
                } else if (grid[r][c] > 0) {
                    nbBeginTiles++;
                }
            }
        }

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                target[r][c] = in.nextInt();
            }
        }

        int[][] DR = new int[][]{{-1, 0}, {1, 0}, {0, 1}, {0, -1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
        for (int[] direction : DR) {
            DIR.add(direction);
        }
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] == 0) {
                    for (int[] direction : DIR) {
                        int y = r + direction[0];
                        int x = c + direction[1];
                        if (y >= 0 && y < N && x >= 0 && x < N && grid[y][x] > 0) {
                            iHaveNeighs.add(new int[]{r, c});
                            break;
                        }
                    }
                }
            }
        }

        bestScore = scorer(grid);
        bestStates.add(copyGrid(grid));
        bestNeighs.add(new ArrayList<>(iHaveNeighs));
        currScore = bestScore;
        currStates.add(copyGrid(grid));
        currNeighs.add(new ArrayList<>(iHaveNeighs));

        while (elapsed < TT) {
            performRollout();
            elapsed = elapsedTimeInSeconds();
        }

        System.out.println(bestMoves.size());
        for (int[] move : bestMoves) {
            System.out.println(move[0] + " " + move[1] + " " + move[2]);
        }
        System.err.println("ctrRollouts "+ ctrRollouts);
        System.err.println("ctrNodes "+ ctrNodes);
        System.err.println("ctrAbort "+ ctrAbort);
    }

    private static void performRollout() {
        ctrRollouts += 1;
        // Select a random move index
        int index = rand.nextInt(currMoves.size() + 1);
        int[][] cgrid = copyGrid(currStates.get(index));
        List<int[]> haveNeighs = new ArrayList<>(currNeighs.get(index));
        List<int[]> moves = new ArrayList<>(currMoves.subList(0, index));
        List<int[][]> states = new ArrayList<>();
        List<List<int[]>> neighs = new ArrayList<>();

        int nbZeros = initNbZeros - index;
        boolean stopBeforeTheEndIfCannotImprove = true;

        while (nbZeros > 0 && stopBeforeTheEndIfCannotImprove && elapsed < TT) {
            ctrNodes += 1;
            if (haveNeighs.isEmpty()) {
                ctrAbort += 1;
                elapsed = elapsedTimeInSeconds();
                break;
            }
            boolean selected = false;
            int nbTrials = 0;
            Collections.shuffle(haveNeighs,rand);

            while (!selected) {

                if (nbTrials >= haveNeighs.size()) {
                    stopBeforeTheEndIfCannotImprove = false;
                    break;
                }

                int[] chosenTile = haveNeighs.get(nbTrials);
                nbTrials += 1;

                int r = chosenTile[0];
                int c = chosenTile[1];
                Collections.shuffle(DIR,rand);

                for (int[] direction : DIR) {
                    int dy = direction[0];
                    int dx = direction[1];
                    int y = r + dy;
                    int x = c + dx;

                    if (y >= 0 && y < N && x >= 0 && x < N && cgrid[y][x] > 0) {
                        int initColor = cgrid[y][x];
                        List<Integer> validMoves = new ArrayList<>();
                        while (y >= 0 && y < N && x >= 0 && x < N && cgrid[y][x] > 0) {
                            if (cgrid[y][x] != initColor && !validMoves.contains(cgrid[y][x])) {
                                validMoves.add(cgrid[y][x]);
                            }
                            y += dy;
                            x += dx;
                        }

                        if (!validMoves.isEmpty()) {
                            int chosenColor = validMoves.get(rand.nextInt(validMoves.size()));
                            moves.add(new int[]{r, c, chosenColor});
                            applyMove(cgrid, r, c, chosenColor);
                            nbZeros--;
                            selected = true;

                            // Update neighbors after move
                            haveNeighs.remove(chosenTile);
                            updateNeighbors(cgrid, haveNeighs, r, c);
                            states.add(copyGrid(cgrid));
                            neighs.add(new ArrayList<>(haveNeighs));
                            int score = scorer(cgrid);
                            elapsed = elapsedTimeInSeconds();
                            if (score > currScore) {
                                currScore = score;
                                currMoves = new ArrayList<>(moves);
                                currStates = new ArrayList<>(currStates.subList(0, index + 1));
                                currNeighs = new ArrayList<>(currNeighs.subList(0, index + 1));
                                currStates.addAll(new ArrayList<>(states));
                                currNeighs.addAll(new ArrayList<>(neighs));
                                if (score > bestScore) {
                                    bestScore = score;
                                    System.err.println(score);
                                    bestMoves = new ArrayList<>(moves);
                                }

                            } else {
                                double rr = randomDouble(0,1);

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


                                if (Math.exp((score - currScore)/T) > rr){
                                    currScore = score;
                                    currMoves = new ArrayList<>(moves);
                                    currStates = new ArrayList<>(currStates.subList(0, index + 1));
                                    currNeighs = new ArrayList<>(currNeighs.subList(0, index + 1));
                                    currStates.addAll(new ArrayList<>(states));
                                    currNeighs.addAll(new ArrayList<>(neighs));
                                }
                            }
                            break;
                        }
                    }
                }
            }
        }
    }

    private static int scorer(int[][] grid) {
        int score = 0;
        int correctColors = 0;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (grid[r][c] > 0) {
                    score++;
                    if (grid[r][c] == target[r][c]) {
                        correctColors++;
                    }
                }
            }
        }
        return score + correctColors * correctColors - nbBeginTiles;
    }

    private static int[][] copyGrid(int[][] grid) {
        int[][] newGrid = new int[N][N];
        for (int i = 0; i < N; i++) {
            newGrid[i] = Arrays.copyOf(grid[i], N);
        }
        return newGrid;
    }

    private static void applyMove(int[][] cgrid, int r, int c, int chosenColor) {
        cgrid[r][c] = chosenColor;

        for (int[] direction : DIR) {
            int dy = direction[0];
            int dx = direction[1];
            int y = r + dy;
            int x = c + dx;
            List<int[]> tilesToChange = new ArrayList<>();
            while (y >= 0 && y < N && x >= 0 && x < N && cgrid[y][x] > 0) {
                if (cgrid[y][x] == chosenColor) break;
                tilesToChange.add(new int[]{y, x});
                y += dy;
                x += dx;
            }
            if (y >= 0 && y < N && x >= 0 && x < N && cgrid[y][x] == chosenColor) {
                for (int[] tile : tilesToChange) {
                    cgrid[tile[0]][tile[1]] = chosenColor;
                }
            }
        }
    }

    private static void updateNeighbors(int[][] cgrid, List<int[]> haveNeighs, int r, int c) {
        for (int[] direction : DIR) {
            int y = r + direction[0];
            int x = c + direction[1];
            if (y >= 0 && y < N && x >= 0 && x < N && cgrid[y][x] == 0) {
                boolean alreadyInList = false;
                for (int[] neighbor : haveNeighs) {
                    if (neighbor[0] == y && neighbor[1] == x) {
                        alreadyInList = true;
                        break;
                    }
                }
                if (!alreadyInList) {
                    haveNeighs.add(new int[]{y, x});
                }
            }
        }
    }

    private static long elapsedTimeInSeconds() {
        return System.currentTimeMillis() - startTime;
    }
}
