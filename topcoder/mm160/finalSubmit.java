import java.util.*;

public class BioSlime {
    static int N, C, H, dd = 'd', s = 's', hh = 'H', w = 'W';
    static int[] hr, hc, load;
    static int[][] grid;
    static int[] dr = {1, 0, -1, 0};
    static int[] dc = {0, 1, 0, -1};
    static String[] dname = {"D", "R", "U", "L"};

    static class Point {
        int r, c;
        Point(int r, int c) {
            this.r = r;
            this.c = c;
        }
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Point point = (Point) obj;
            return r == point.r && c == point.c;
        }
        @Override
        public int hashCode() {
            return Objects.hash(r, c);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        N = sc.nextInt();
        C = sc.nextInt();
        H = sc.nextInt();

        hr = new int[H];
        hc = new int[H];
        load = new int[H];

        for (int h = 0; h < H; h++) {
            hr[h] = sc.nextInt();
            hc[h] = sc.nextInt();
            load[h] = 0;
        }

        grid = new int[N][N];
        int nbSlime = 0;

        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                grid[r][c] = sc.next().charAt(0);
                if (grid[r][c] == s) nbSlime++;
            }
        }

        for (int turn = 0; turn < 1000; turn++) {
            StringBuilder cmd = new StringBuilder();
            Set<Integer> chosen = new HashSet<>();

            Map<Point, List<Point>> closestSlimesPerDepot = new HashMap<>();

            if (nbSlime > 0) {

                for (int r = 0; r < N; r++) {
                    for (int c = 0; c < N; c++) {
                        if (grid[r][c] == dd) {

                            Queue<int[]> q = new ArrayDeque<>();
                            Set<Integer> visited = new HashSet<>();
                            q.add(new int[]{r,c});
                            visited.add(N*r+c);
                            Point depotPoint = new Point(r, c);
                            closestSlimesPerDepot.put(depotPoint, new ArrayList<>());

                            while (!q.isEmpty() && closestSlimesPerDepot.get(depotPoint).size() < Math.min(12, nbSlime)) {

                                int[] node = q.poll();
                                int y = node[0], x = node[1];

                                for (int d = 0; d < 4; d++) {
                                    int nr = y + dr[d];
                                    int nc = x + dc[d];
                                    int key = N*nr + nc;

                                    if (isValid(nr, nc) && !visited.contains(key) && grid[nr][nc] != w) {
                                        visited.add(key);
                                        if (grid[nr][nc] == s) {
                                            closestSlimesPerDepot.get(depotPoint).add(new Point(nr, nc));
                                        }
                                        else if (grid[nr][nc] != dd) {
                                            q.add(new int[]{nr, nc});
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            for (int h = 0; h < H; h++) {
                if (load[h] > 0) {
                    boolean found = false;
                    for (int d = 0; d < 4; d++) {
                        int nr = hr[h] + dr[d];
                        int nc = hc[h] + dc[d];
                        if (isValid(nr, nc) && grid[nr][nc] == dd) {
                            cmd.append(h).append(" ").append(dname[d]).append(" ");
                            found = true;
                            break;
                        }
                    }
                    if (found) continue;
                }

                Queue<int[]> q = new ArrayDeque<>();
                Set<Integer> visited = new HashSet<>();
                q.add(new int[]{hr[h], hc[h], -1, 0, 0});
                visited.add(N*hr[h]+hc[h]);

                int[] bestDepot = null;
                int[] bestSlime1 = null;
                Map<Point, int[]> bestSlimes = new HashMap<>();

                while (!q.isEmpty() && !(bestDepot != null && bestSlime1 != null)) {
                    int[] node = q.poll();
                    int r = node[0], c = node[1], firstMove = node[2], nSlime = node[3], depth = node[4];

                    for (int d = 0; d < 4; d++) {
                        int nr = r + dr[d];
                        int nc = c + dc[d];
                        int key = N*nr + nc;

                        if (isValid(nr, nc) && !visited.contains(key) && grid[nr][nc] != w && grid[nr][nc] != hh && !(grid[nr][nc] == s && load[h] + nSlime >= C)) {
                            if (grid[nr][nc] == s && !chosen.contains(key)) {
                                bestSlimes.put(new Point(nr, nc), new int[]{nr, nc, firstMove == -1 ? d : firstMove, depth + 1});
                                if (null == bestSlime1)
                                    bestSlime1 = new int[]{nr, nc, firstMove == -1 ? d : firstMove, depth + 1};
                            }
                            if (grid[nr][nc] == dd && bestDepot == null && depth > 0) {
                                bestDepot = new int[]{nr, nc, firstMove == -1 ? d : firstMove, depth + 1};
                            }
                            if (grid[nr][nc] != dd) {
                                q.add(new int[]{nr, nc, firstMove == -1 ? d : firstMove, nSlime + (grid[nr][nc] == s ? 1 : 0), depth + 1});
                            }
                            visited.add(key);
                        }
                    }
                }

                int[] best = null;
                if (bestDepot != null && bestSlime1 != null) {
                    int[] bestSlime = null;

                    Point coord = new Point(bestDepot[0], bestDepot[1]);

                    int[] bs = closestSlimesPerDepot.get(coord).stream().filter(point -> bestSlimes.containsKey(point))
                        .map(point -> bestSlimes.get(point))
                        .findFirst().orElse(null);

                    if (bs != null)
                        bestSlime = bs;

                    if (null == bestSlime)
                        bestSlime = bestSlime1;

                    if (bestDepot[2] == bestSlime[2] || load[h] > C - 1) {
                        best = bestDepot;
                    } else if (Math.abs(bestSlime[0] - bestDepot[0]) + Math.abs(bestSlime[1] - bestDepot[1]) < 3) {
                        best = bestSlime;
                        chosen.add(N*bestSlime[0] + bestSlime[1]);
                    } else if (nbSlime <= 11 * H && turn < 970-nbSlime) {
                        best = bestDepot;
                    } else if (load[h] == 0) {
                        chosen.add(N*bestSlime[0] + bestSlime[1]);
                        best = bestSlime;
                    } else if (load[h] + bestSlime[3] > bestDepot[3] + C / 6.0) {
                        best = bestDepot;
                    } else {
                        chosen.add(N*bestSlime[0] + bestSlime[1]);
                        best = bestSlime;
                    }
                } else if (bestDepot != null) {
                    best = bestDepot;
                } else if (bestSlime1 != null) {
                    chosen.add(N*bestSlime1[0] + bestSlime1[1]);
                    best = bestSlime1;
                } else {
                    cmd.append(h).append(" X ");
                }

                if (best != null) {
                    grid[hr[h]][hc[h]] = '.';
                    cmd.append(h).append(" ").append(dname[best[2]]).append(" ");
                    hr[h] += dr[best[2]];
                    hc[h] += dc[best[2]];
                    grid[hr[h]][hc[h]] = hh;
                }
            }

            System.out.println(cmd.toString().trim());
            System.out.flush();

            int tm = sc.nextInt();
            for (int h = 0; h < H; h++) {
                load[h] = sc.nextInt();
            }

            nbSlime = 0;
            for (int r = 0; r < N; r++) {
                for (int c = 0; c < N; c++) {
                    grid[r][c] = sc.next().charAt(0);
                    if (grid[r][c] == s) nbSlime++;
                }
            }
        }
        sc.close();
    }

    static boolean isValid(int r, int c) {
        return r >= 0 && r < N && c >= 0 && c < N;
    }
}
