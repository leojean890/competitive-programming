import java.security.SecureRandom;
import java.io.*;
import java.util.*;

public class Arrows {
    private static final double t_start = 90;
    private static final double t_final = 99;
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

    public static void main(String[] args)  throws Exception {
        Scanner scanner = new Scanner(System.in);
        long startTime = System.nanoTime();
        rnd = SecureRandom.getInstance("SHA1PRNG");
        rnd.setSeed(0);

        int N = scanner.nextInt();
        int[][] arrows = new int[N][N];
        int[][] mults = new int[N][N];
        boolean[][] is5 = new boolean[N][N];
        boolean[][] is3 = new boolean[N][N];
        boolean[][] is2 = new boolean[N][N];
        ArrayList<int[]> starting = new ArrayList<>();

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                arrows[r][c] = scanner.nextInt();
                mults[r][c] = scanner.nextInt();
                if (mults[r][c] == 5) {
                    starting.add(new int[]{r, c});
                    is5[r][c] = true;
                } else if (mults[r][c] == 3) {
                    is3[r][c] = true;
                } else if (mults[r][c] == 2) {
                    is2[r][c] = true;
                }
            }
        }

        if (starting.isEmpty()) {
            for (int r = 0; r < N; r++) {
                for (int c = 0; c < N; c++) {
                    if (mults[r][c] == 3) {
                        starting.add(new int[]{r, c});
                    }
                }
            }
        }

        if (starting.isEmpty()) {
            for (int r = 0; r < N; r++) {
                for (int c = 0; c < N; c++) {
                    if (mults[r][c] == 2) {
                        starting.add(new int[]{r, c});
                    }
                }
            }
        }

        if (starting.isEmpty()) {
            for (int r = 0; r < N; r++) {
                for (int c = 0; c < N; c++) {
                    starting.add(new int[]{r, c});
                }
            }
        }

        int[] dr = {-1, -1, 0, 1, 1, 1, 0, -1};
        int[] dc = {0, 1, 1, 1, 0, -1, -1, -1};
        int[] drinv = {1, 1, 0, -1, -1, -1, 0, 1};
        int[] dcinv = {0, -1, -1, -1, 0, 1, 1, 1};
        int[] dinv = {4, 5, 6, 7, 0, 1, 2, 3};
        ArrayList<int[]> bestMoves = new ArrayList<>();
        int bestScore = 0;
        int rollouts = 0;
        int nodes = 0;
        int ncdd = 0;
        Random random = new Random();

        while ((System.nanoTime() - startTime) / 1e9 < 1) {
            rollouts++;
            boolean[][] used = new boolean[N][N];
            ArrayList<int[]> moves = new ArrayList<>();
            int[] start = starting.get(random.nextInt(starting.size()));
            int r = start[0];
            int c = start[1];
            moves.add(new int[]{r, c});
            used[r][c] = true;

            while (true) {
                nodes++;
                ArrayList<int[]> candidates = new ArrayList<>();

                for (int prevDir = 0; prevDir < 8; prevDir++) {
                    int y = r;
                    int x = c;
                    while (true) {
                        y += dr[prevDir];
                        x += dc[prevDir];
                        if (y < 0 || y >= N || x < 0 || x >= N) break;
                        if (is5[y][x] && !used[y][x] && arrows[y][x] == dinv[prevDir]) {
                            boolean vv = false;
                            for (int prevDir2 = 0; prevDir2 < 8; prevDir2++) {
                                int y2 = y;
                                int x2 = x;
                                while (true) {
                                    y2 += dr[prevDir2];
                                    x2 += dc[prevDir2];
                                    if (y2 < 0 || y2 >= N || x2 < 0 || x2 >= N) break;
                                    if (!used[y2][x2] && arrows[y2][x2] == dinv[prevDir2]) {
                                        candidates.add(new int[]{y, x});
                                        vv = true;
                                        break;
                                    }
                                }
                                if(vv)break;
                            }
                        }
                    }
                }

                if (candidates.isEmpty()) {
                    for (int prevDir = 0; prevDir < 8; prevDir++) {
                        int y = r;
                        int x = c;
                        while (true) {
                            y += dr[prevDir];
                            x += dc[prevDir];
                            if (y < 0 || y >= N || x < 0 || x >= N) break;
                            if (is3[y][x] && !used[y][x] && arrows[y][x] == dinv[prevDir]) {
                                boolean vv = false;
                                for (int prevDir2 = 0; prevDir2 < 8; prevDir2++) {
                                    int y2 = y;
                                    int x2 = x;
                                    while (true) {
                                        y2 += dr[prevDir2];
                                        x2 += dc[prevDir2];
                                        if (y2 < 0 || y2 >= N || x2 < 0 || x2 >= N) break;
                                        if (!used[y2][x2] && arrows[y2][x2] == dinv[prevDir2]) {
                                            candidates.add(new int[]{y, x});
                                            vv = true;
                                            break;
                                        }
                                    }
                                    if(vv)break;
                                }
                            }
                        }
                    }

                    if (candidates.isEmpty()) {
                        for (int prevDir = 0; prevDir < 8; prevDir++) {
                            int y = r;
                            int x = c;
                            while (true) {
                                y += dr[prevDir];
                                x += dc[prevDir];
                                if (y < 0 || y >= N || x < 0 || x >= N) break;
                                if (is2[y][x] && !used[y][x] && arrows[y][x] == dinv[prevDir]) {
                                    boolean vv = false;
                                    for (int prevDir2 = 0; prevDir2 < 8; prevDir2++) {
                                        int y2 = y;
                                        int x2 = x;
                                        while (true) {
                                            y2 += dr[prevDir2];
                                            x2 += dc[prevDir2];
                                            if (y2 < 0 || y2 >= N || x2 < 0 || x2 >= N) break;
                                            if (!used[y2][x2] && arrows[y2][x2] == dinv[prevDir2]) {
                                                candidates.add(new int[]{y, x});
                                                vv = true;
                                                break;
                                            }
                                        }
                                        if(vv)break;
                                    }
                                }
                            }
                        }

                        if (candidates.isEmpty()) {
                            for (int prevDir = 0; prevDir < 8; prevDir++) {
                                int y = r;
                                int x = c;
                                while (true) {
                                    y += dr[prevDir];
                                    x += dc[prevDir];
                                    if (y < 0 || y >= N || x < 0 || x >= N) break;
                                    if (!used[y][x] && arrows[y][x] == dinv[prevDir]) {
                                        boolean vv = false;
                                        for (int prevDir2 = 0; prevDir2 < 8; prevDir2++) {
                                            int y2 = y;
                                            int x2 = x;
                                            while (true) {
                                                y2 += dr[prevDir2];
                                                x2 += dc[prevDir2];
                                                if (y2 < 0 || y2 >= N || x2 < 0 || x2 >= N) break;
                                                if (!used[y2][x2] && arrows[y2][x2] == dinv[prevDir2]) {
                                                    candidates.add(new int[]{y, x});
                                                    vv = true;
                                                    break;
                                                }
                                            }
                                            if(vv)break;
                                        }
                                    }
                                }
                            }

                            if (candidates.isEmpty()) {
                                ncdd++;
                                break;
                            }
                        }
                    }
                }

                int[] move = candidates.get(random.nextInt(candidates.size()));
                r = move[0];
                c = move[1];
                moves.add(new int[]{r, c});
                used[r][c] = true;
            }

            int score = 0;
            for (int i = 0; i < moves.size(); i++) {
                int[] move = moves.get(moves.size() - 1 - i);
                r = move[0];
                c = move[1];
                score += (i + 1) * mults[r][c];
            }

            if (score > bestScore) {
                bestMoves = new ArrayList<>(moves);
                bestScore = score;
            }
        }

        while ((System.nanoTime() - startTime) / 1e9 < 2) {
            rollouts++;
            boolean[][] used = new boolean[N][N];
            ArrayList<int[]> moves = new ArrayList<>();
            int[] start = starting.get(random.nextInt(starting.size()));
            int r = start[0];
            int c = start[1];
            moves.add(new int[]{r, c});
            used[r][c] = true;

            while (true) {
                nodes++;
                ArrayList<int[]> candidates = new ArrayList<>();

                for (int prevDir = 0; prevDir < 8; prevDir++) {
                    int y = r;
                    int x = c;
                    while (true) {
                        y += dr[prevDir];
                        x += dc[prevDir];
                        if (y < 0 || y >= N || x < 0 || x >= N) break;
                        if (!used[y][x] && arrows[y][x] == dinv[prevDir]) {
                            boolean vv = false;
                            for (int prevDir2 = 0; prevDir2 < 8; prevDir2++) {
                                int y2 = y;
                                int x2 = x;
                                while (true) {
                                    y2 += dr[prevDir2];
                                    x2 += dc[prevDir2];
                                    if (y2 < 0 || y2 >= N || x2 < 0 || x2 >= N) break;
                                    if (!used[y2][x2] && arrows[y2][x2] == dinv[prevDir2]) {
                                        int mltp = 2*N-Math.abs(c-x) - Math.abs(r-y);

                                         if (is5[y][x]) {
                                            for (int t = 0; t < mltp*5; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else if (is3[y][x]) {
                                            for (int t = 0; t < mltp*3; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else if (is2[y][x]) {
                                            for (int t = 0; t < mltp*2; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else {
                                            candidates.add(new int[]{y, x});
                                        }
                                        vv = true;
                                        break;
                                    }
                                }
                                if(vv)break;
                            }

                        }
                    }
                }

                if (candidates.isEmpty()) {
                    ncdd++;
                    break;
                }

                int[] move = candidates.get(random.nextInt(candidates.size()));
                r = move[0];
                c = move[1];
                moves.add(new int[]{r, c});
                used[r][c] = true;
            }

            int score = 0;
            for (int i = 0; i < moves.size(); i++) {
                int[] move = moves.get(moves.size() - 1 - i);
                r = move[0];
                c = move[1];
                score += (i + 1) * mults[r][c];
            }

            if (score > bestScore) {
                bestMoves = new ArrayList<>(moves);
                bestScore = score;
            }
        }

        while ((System.nanoTime() - startTime) / 1e9 < 3) {
            rollouts++;
            int index = random.nextInt(bestMoves.size()-3);
            boolean[][] used = new boolean[N][N];
            ArrayList<int[]> moves = new ArrayList<>();
            for (int i = 0; i <= index; i++) {
                var move = bestMoves.get(i);
                int r = move[0];
                int c = move[1];
                moves.add(new int[]{r, c});
                used[r][c] = true;
            }
            int[] start = bestMoves.get(index);
            int r = start[0];
            int c = start[1];

            while (true) {
                nodes++;
                ArrayList<int[]> candidates = new ArrayList<>();

                for (int prevDir = 0; prevDir < 8; prevDir++) {
                    int y = r;
                    int x = c;
                    while (true) {
                        y += dr[prevDir];
                        x += dc[prevDir];
                        if (y < 0 || y >= N || x < 0 || x >= N) break;
                        if (!used[y][x] && arrows[y][x] == dinv[prevDir]) {
                            boolean vv = false;
                            for (int prevDir2 = 0; prevDir2 < 8; prevDir2++) {
                                int y2 = y;
                                int x2 = x;
                                while (true) {
                                    y2 += dr[prevDir2];
                                    x2 += dc[prevDir2];
                                    if (y2 < 0 || y2 >= N || x2 < 0 || x2 >= N) break;
                                    if (!used[y2][x2] && arrows[y2][x2] == dinv[prevDir2]) {

                                        int mltp = 2*N-Math.abs(c-x) - Math.abs(r-y);

                                        if (is5[y][x]) {
                                            for (int t = 0; t < mltp*5; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else if (is3[y][x]) {
                                            for (int t = 0; t < mltp*3; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else if (is2[y][x]) {
                                            for (int t = 0; t < mltp*2; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else {
                                            candidates.add(new int[]{y, x});
                                        }
                                        vv = true;
                                        break;
                                    }
                                }
                                if(vv)break;
                            }

                        }
                    }
                }

                if (candidates.isEmpty()) {
                    ncdd++;
                    break;
                }

                int[] move = candidates.get(random.nextInt(candidates.size()));
                r = move[0];
                c = move[1];
                moves.add(new int[]{r, c});
                used[r][c] = true;
            }

            int score = 0;
            for (int i = 0; i < moves.size(); i++) {
                int[] move = moves.get(moves.size() - 1 - i);
                r = move[0];
                c = move[1];
                score += (i + 1) * mults[r][c];
            }

            if (score > bestScore) {
                bestMoves = new ArrayList<>(moves);
                bestScore = score;
            }
        }

        ArrayList<int[]> curr_moves = new ArrayList<>();
        for (int i = 0; i < bestMoves.size(); i++) {
            var move = bestMoves.get(i);
            int r = move[0];
            int c = move[1];
            curr_moves.add(new int[]{r, c});
        }
        var currScore = bestScore;

        var end_time = System.nanoTime();

        while ((end_time - startTime) / 1e9 < 7) {
            rollouts++;
            int index = random.nextInt(Math.max(curr_moves.size()-3,1));

            boolean[][] used = new boolean[N][N];
            ArrayList<int[]> moves = new ArrayList<>();
            for (int i = 0; i <= index; i++) {
                var move = curr_moves.get(i);
                int r = move[0];
                int c = move[1];
                moves.add(new int[]{r, c});
                used[r][c] = true;
            }
            int[] start = curr_moves.get(index);
            int r = start[0];
            int c = start[1];

            while (true) {
                nodes++;
                ArrayList<int[]> candidates = new ArrayList<>();

                for (int prevDir = 0; prevDir < 8; prevDir++) {
                    int y = r;
                    int x = c;
                    while (true) {
                        y += dr[prevDir];
                        x += dc[prevDir];
                        if (y < 0 || y >= N || x < 0 || x >= N) break;
                        if (!used[y][x] && arrows[y][x] == dinv[prevDir]) {
                            boolean vv = false;
                            for (int prevDir2 = 0; prevDir2 < 8; prevDir2++) {
                                int y2 = y;
                                int x2 = x;
                                while (true) {
                                    y2 += dr[prevDir2];
                                    x2 += dc[prevDir2];
                                    if (y2 < 0 || y2 >= N || x2 < 0 || x2 >= N) break;
                                    if (!used[y2][x2] && arrows[y2][x2] == dinv[prevDir2]) {
                                        int mltp = 2*N-Math.abs(c-x) - Math.abs(r-y);

                                        if (is5[y][x]) {
                                            for (int t = 0; t < mltp*5; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else if (is3[y][x]) {
                                            for (int t = 0; t < mltp*3; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else if (is2[y][x]) {
                                            for (int t = 0; t < mltp*2; t++) {
                                                candidates.add(new int[]{y, x});
                                            }
                                        } else {
                                            candidates.add(new int[]{y, x});
                                        }
                                        vv = true;
                                        break;
                                    }
                                }
                                if(vv)break;
                            }

                        }
                    }
                }

                if (candidates.isEmpty()) {
                    ncdd++;
                    break;
                }

                int[] move = candidates.get(random.nextInt(candidates.size()));
                r = move[0];
                c = move[1];
                moves.add(new int[]{r, c});
                used[r][c] = true;
            }

            int score = 0;
            for (int i = 0; i < moves.size(); i++) {
                int[] move = moves.get(moves.size() - 1 - i);
                r = move[0];
                c = move[1];
                score += (i + 1) * mults[r][c];
            }

            end_time = System.nanoTime();

            if (score > currScore) {
                curr_moves = moves;
                currScore = score;
                if (score > bestScore) {
                    bestMoves = new ArrayList<>(moves);
                    bestScore = score;
                }
            } else {
                double rr = randomDouble(0,1);

                double T;

                if (end_time-startTime < 4e9)
                    T = t_start*Math.pow(t_final/t_start, (end_time-startTime-3e9)/ 1e9);
                else if (end_time-startTime < 5e9)
                    T = t_start*Math.pow(t_final/t_start, (end_time-startTime-4e9)/ 1e9);
                else if (end_time-startTime < 6e9)
                    T = t_start*Math.pow(t_final/t_start, (end_time-startTime-5e9)/ 1e9);
                else if (end_time-startTime < 7e9)
                    T = t_start*Math.pow(t_final/t_start, (end_time-startTime-6e9)/ 1e9);
                else
                    T = t_start*Math.pow(t_final/t_start, (end_time-startTime-7e9)/ 1e9);


                if (Math.exp((score - currScore)/T) > rr){
                    curr_moves = moves;
                    currScore = score;
                }
            }
        }

        System.err.println("bestScore " + bestScore);
        System.err.println("rollouts " + rollouts);
        System.err.println("ncdd " + ncdd);
        System.err.println("nodes " + nodes);
        System.err.println("nbmoves " + bestMoves.size());
        ArrayList<int[]> bestMovesBefore = new ArrayList<>(bestMoves);

        while ((System.nanoTime() - startTime) / 1e9 < 9.7) {

            ArrayList<int[]> moves = new ArrayList<>(bestMovesBefore);

            boolean[][] used = new boolean[N][N];
            for (int i = 0; i < moves.size(); i++) {
                var move = moves.get(i);
                int r = move[0];
                int c = move[1];
                used[r][c] = true;
            }

            var index = 0;
            while (index < moves.size() - 1) {

                for (int i = index; i < moves.size() - 1; i++) {

                    int[] first = moves.get(i);
                    int[] second = moves.get(i+1);
                    int r = first[0];
                    int c = first[1];
                    var inserted = false;
                    ArrayList<int[]> candidates = new ArrayList<>();

                    for (int prevDir = 0; prevDir < 8; prevDir++) {
                        int y = r;
                        int x = c;
                        while (true) {
                            y += dr[prevDir];
                            x += dc[prevDir];
                            if (y < 0 || y >= N || x < 0 || x >= N) break;
                            if (!(y==second[0] && x==second[1]) && !used[y][x] && arrows[y][x] == dinv[prevDir]) {
                                candidates.add(new int[]{y, x});
                            }
                        }
                    }

                    if (!candidates.isEmpty()) {
                        ArrayList<int[]> nCandidates = new ArrayList<>();
                        for (int j = 0; j < candidates.size(); j++) {
                            var candidate = candidates.get(j);
                            r = candidate[0];
                            c = candidate[1];
                            var v = false;

                            for (int prevDir = 0; prevDir < 8; prevDir++) {
                                int y = r;
                                int x = c;
                                while (true) {
                                    y += dr[prevDir];
                                    x += dc[prevDir];
                                    if (y < 0 || y >= N || x < 0 || x >= N) break;
                                    if (y==second[0] && x==second[1] && arrows[y][x] == dinv[prevDir]) {
                                        nCandidates.add(new int[]{r, c});
                                        v = true;
                                        break;
                                    }
                                }
                                if (v)break;
                            }
                        }
                        if (!nCandidates.isEmpty()) {
                            int[] move = nCandidates.get(random.nextInt(nCandidates.size()));
                            r = move[0];
                            c = move[1];
                            moves.add(i+1,new int[]{r, c});
                            inserted = true;

                            used[r][c] = true;
                            index = i;

                        }
                    }

                    if (inserted) {
                        break;
                    }
                    index = i+1;
                }
            }


            int score = 0;
            for (int k = 0; k < moves.size(); k++) {
                var move = moves.get(moves.size() - 1 - k);
                var r1 = move[0];
                var c1 = move[1];
                score += (k + 1) * mults[r1][c1];
            }

            if (score > bestScore) {
                bestMoves = new ArrayList<>(moves);
                bestScore = score;
            }

        }

        System.err.println("bestScore " + bestScore);
        System.err.println("nbmoves " + bestMoves.size());

        System.out.println(bestMoves.size());
        for (int i = bestMoves.size() - 1; i >= 0; i--) {
            int[] move = bestMoves.get(i);
            System.out.println(move[0] + " " + move[1]);
        }

        scanner.close();
    }
}

