import java.util.*;
import java.io.*;
import java.util.concurrent.PriorityBlockingQueue;

public class Main {
    static int N, T, sigma, ss, currentActions, nRollouts, current, sq, MAX_ACTIONS;
    static long startTime;
    static List<int[]> wh = new ArrayList<>();
    static Random rng = new Random(1234);
    static State[] remainingAction;
    static Element remainingElement;
    static State[][] allActions;
    static State[][] allActions2;
    static Element[] allElements;
    static Element[] allElements2;
    static int[][] lines;
    static int[][] widths;
    static int[][] heights;
    static int[] coordPerCol;
    static int[] coordPerLig;
    static Result result;
    static Element element = new Element();
    static List<Integer> possible = new ArrayList<>();

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PriorityQueue q = new PriorityQueue();
        PriorityQueue q2 = new PriorityQueue();
        PrintWriter writer = new PrintWriter(System.out);

        String[] initialInputs = br.readLine().split(" ");
        N = Integer.parseInt(initialInputs[0]);
        T = Integer.parseInt(initialInputs[1]);
        sigma = Integer.parseInt(initialInputs[2]);

        startTime = System.currentTimeMillis();

        for (int i = 0; i < N; i++) {
            String[] dims = br.readLine().split(" ");
            wh.add(new int[]{Integer.parseInt(dims[0]), Integer.parseInt(dims[1])});
        }

        sq = (int)Math.sqrt(N)*(int)Math.sqrt(N);
        ss = (int)Math.ceil(Math.sqrt(N));

        MAX_ACTIONS = T/3;

        allElements = new Element[MAX_ACTIONS+2];
        allElements2 = new Element[MAX_ACTIONS+2];
        allActions = new State[MAX_ACTIONS+2][N];
        allActions2 = new State[MAX_ACTIONS+2][N];
        for (int i = 0; i < MAX_ACTIONS+2; i++) {
            allElements[i] = new Element();
            allElements2[i] = new Element();
            allActions[i] = new State[N];
            allActions2[i] = new State[N];
            for (int j = 0; j < N; j++) {
                allActions[i][j] = new State();
                allActions2[i][j] = new State();
            }
            allElements[i].item = allActions[i];
            allElements2[i].item = allActions2[i];
        }

        lines = new int[ss][ss];
        widths = new int[ss][ss];
        heights = new int[ss][ss];
        coordPerCol = new int[ss];
        coordPerLig = new int[ss];
        result = new Result(new State[N], 0);

        while ((System.currentTimeMillis() - startTime) / 1000.0 < 1.2) {
            mc();
            nRollouts += 1;
            q.put(element);
            if (currentActions > MAX_ACTIONS) {
                remainingElement = q.get();
                if (remainingElement != null)
                remainingAction = remainingElement.item;
            }
        }

        current = 1;
        currentActions = 0;

        while ((System.currentTimeMillis() - startTime) / 1000.0 < 2.4) {
            mc();
            nRollouts += 1;
            q2.put(element);
            if (currentActions > MAX_ACTIONS) {
                remainingElement = q2.get();
                if (remainingElement != null)
                remainingAction = remainingElement.item;
            }
        }

        System.err.println((System.currentTimeMillis() - startTime) / 1000.0);
        System.err.println(nRollouts);

         for (int aze = 2*MAX_ACTIONS; aze < T; aze++) {

            int direc = rng.nextInt(2);

            Map<Integer, Integer> dimPerIndex = new HashMap<>();
            Map<Integer, Integer> hPerIndex = new HashMap<>();
            Map<Integer, Integer> rotPerIndex = new HashMap<>();
            Map<Integer, Integer> heights = new HashMap<>();
            Map<Integer, List<Integer>> eltsPerCol = new HashMap<>();

            int currCol = 0;
            State[] prdb = new State[N];
            double moyH = 0;

            for (int i = 0; i < N; i++) {
                int rot = rng.nextInt(2); 
                dimPerIndex.put(i, rot == 0 ? wh.get(i)[0] : wh.get(i)[1]);
                hPerIndex.put(i, rot == 1 ? wh.get(i)[0] : wh.get(i)[1]);
                rotPerIndex.put(i, rot);
                moyH += (direc == 0 ? hPerIndex.get(i) : dimPerIndex.get(i));
            }
            moyH /= Math.sqrt(N);

            for (int i = 0; i <= ss; i++) {
                heights.put(i, 0);
                eltsPerCol.put(i, new ArrayList<>());
            }

            for (int i = 0; i < N; i++) {
                if (heights.get(currCol) > moyH) {
                    currCol++;
                }

                eltsPerCol.get(currCol).add(i);
                heights.put(currCol, heights.get(currCol) +
                    (direc == 0 ? hPerIndex.get(i) : dimPerIndex.get(i)));

                int value = -1;

                if (currCol > 0) {
                    int M = -1;
                    int begin = eltsPerCol.get(currCol - 1).get(0);
                    int end = eltsPerCol.get(currCol - 1)
                            .get(eltsPerCol.get(currCol - 1).size() - 1) + 1;

                    for (int j = begin; j < end; j++) {
                        int vv = direc == 0 ? dimPerIndex.get(j) : hPerIndex.get(j);
                        if (M < vv) {
                            M = vv;
                            value = j;
                        }
                    }
                }

                prdb[i] = new State();
                prdb[i].chosenRot = rotPerIndex.get(i);
                prdb[i].dir = direc;
                prdb[i].value = value;
            }

            writer.printf("%d%n", N);
            writer.flush();

            for (int i = 0; i < N; i++) {
                writer.printf("%d %d %s %d%n", i, prdb[i].chosenRot, prdb[i].dir == 0 ? "U" : "L", prdb[i].value);
                writer.flush();
            }
        }



        for (int t = MAX_ACTIONS; t < 2*MAX_ACTIONS; t++) {
            writer.printf("%d%n", N);
            writer.flush();

            State[] prdb = q.get().item;
            for (int i = 0; i < N; i++) {
                writer.printf("%d %d %s %d%n", i, prdb[i].chosenRot, prdb[i].dir == 0 ? "U" : "L", prdb[i].value);
                writer.flush();
            }
        }

         for (int t = 0; t < MAX_ACTIONS; t++) {
            writer.printf("%d%n", N);
            writer.flush();

            State[] prdb = q2.get().item;
            for (int i = 0; i < N; i++) {
                writer.printf("%d %d %s %d%n", i, prdb[i].chosenRot, prdb[i].dir == 0 ? "U" : "L", prdb[i].value);
                writer.flush();
            }
        }

        writer.close();
        System.err.println((System.currentTimeMillis() - startTime) / 1000.0);
    }

    static class Result {
        State[] actions;
        int score;

        public Result(State[] actions, int score) {
            this.actions = actions;
            this.score = score;
        }
    }

    static void mc() {
        int depth = 0;

        for (int[] line : lines) Arrays.fill(line, -1);
        for (int[] width : widths) Arrays.fill(width, -1);
        for (int[] height : heights) Arrays.fill(height, -1);
        Arrays.fill(coordPerLig, 0);
        Arrays.fill(coordPerCol, 0);
        State[] actions;

        if (currentActions <= MAX_ACTIONS) {
            if (current == 0) {
                element = allElements[currentActions];
                actions = allActions[currentActions];
            } else {
                element = allElements2[currentActions];
                actions = allActions2[currentActions];
            }

            currentActions += 1;
        } else {
            actions = remainingAction;
            element = remainingElement;
        }

        while (depth < N) {
            int direc = rng.nextInt(2);
            boolean toRetryWithL = false;

            if (direc == 1) {
                toRetryWithL = handleL(actions, lines, widths, heights, coordPerCol, coordPerLig, depth);
            }

            if (direc == 0 || toRetryWithL) {
                boolean handled = handleU(actions, lines, widths, heights, coordPerCol, coordPerLig, depth);
                if (!handled) {
                    handleL(actions, lines, widths, heights, coordPerCol, coordPerLig, depth);
                }
            }
            depth += 1;
        }

        int score = Arrays.stream(coordPerLig).max().orElse(0) + Arrays.stream(coordPerCol).max().orElse(0);
        element.item = actions;
        element.priority = score;
    }

    static boolean handleL(State[] actions, int[][] lines, int[][] widths, int[][] heights,
                           int[] coordPerCol, int[] coordPerLig, int depth) {
        possible.clear();
        int limitation = ss-1;
        if (depth >= sq || current == 0) {
            limitation += 1;
        }
        for (int i = 0; i < limitation; i++) {
            if (lines[i][limitation - 1] > -1) continue;
            possible.add(i);
            if (lines[i][0] == -1) break;

            if ((i + 1) < limitation) {
                int firstM1I = firstIndexOf(lines[i], -1);
                int firstM1Iplus1 = firstIndexOf(lines[i + 1], -1);
                if (firstM1Iplus1 >= firstM1I) break;
            }
        }

        if (!possible.isEmpty()) {
            int chosen = possible.get(rng.nextInt(possible.size()));
            int j = 0;
            while (j < limitation && lines[chosen][j] > -1) j++;
            if (j < limitation) {
                int value = -1;
                if (chosen > 0) {
                    int M = -1;
                    for (int k = j; k < limitation && lines[chosen - 1][k] > -1; k++) {
                        if (M < coordPerCol[k]) {
                            M = coordPerCol[k];
                            value = lines[chosen - 1][k];
                        }
                    }
                }

                int chosenRot = rng.nextInt(2);
                lines[chosen][j] = depth;
                heights[chosen][j] = chosenRot == 1 ? wh.get(depth)[0] : wh.get(depth)[1];
                widths[chosen][j] = chosenRot == 0 ? wh.get(depth)[0] : wh.get(depth)[1];
                coordPerLig[chosen] += widths[chosen][j];
                coordPerCol[j] = Arrays.stream(coordPerCol, j, ss).max().orElse(0) + heights[chosen][j];
                actions[depth].value = value;
                actions[depth].chosenRot = chosenRot;
                actions[depth].dir = 1;
                return false;
            }
        }

        return true;
    }

    static boolean handleU(State[] actions, int[][] lines, int[][] widths, int[][] heights,
                           int[] coordPerCol, int[] coordPerLig, int depth) {
        possible.clear();
        int limitation = ss-1;
        if (depth >= sq  || current == 0) {
            limitation += 1;
        }
        for (int i = 0; i < limitation; i++) {
            if (lines[limitation - 1][i] > -1) continue;
            possible.add(i);
            if (lines[0][i] == -1) break;

            if ((i + 1) < limitation) {
                int firstM1I = firstIndexOfColumn(lines, i, -1);
                int firstM1Iplus1 = firstIndexOfColumn(lines, i + 1, -1);
                if (firstM1Iplus1 >= firstM1I) break;
            }
        }

        if (!possible.isEmpty()) {
            int chosen = possible.get(rng.nextInt(possible.size()));
            int j = 0;
            while (j < limitation && lines[j][chosen] > -1) j++;
            if (j < limitation) {
                int value = -1;
                if (chosen > 0) {
                    int M = -1;
                    for (int k = j; k < limitation && lines[k][chosen - 1] > -1; k++) {
                        if (M < coordPerLig[k]) {
                            M = coordPerLig[k];
                            value = lines[k][chosen - 1];
                        }
                    }
                }

                int chosenRot = rng.nextInt(2);
                lines[j][chosen] = depth;
                heights[j][chosen] = chosenRot == 1 ? wh.get(depth)[0] : wh.get(depth)[1];
                widths[j][chosen] = chosenRot == 0 ? wh.get(depth)[0] : wh.get(depth)[1];
                coordPerLig[j] += Arrays.stream(coordPerLig, j, ss).max().orElse(0) + widths[j][chosen];
                coordPerCol[chosen] += heights[j][chosen];
                actions[depth].value = value;
                actions[depth].chosenRot = chosenRot;
                actions[depth].dir = 0;
                return true;
            }
        }

        return false;
    }

    static int firstIndexOf(int[] array, int value) {
        for (int i = 0; i < array.length; i++) {
            if (array[i] == value) return i;
        }
        return array.length + 1;
    }

    static int firstIndexOfColumn(int[][] array, int col, int value) {
        for (int i = 0; i < array.length; i++) {
            if (array[i][col] == value) return i;
        }
        return array.length + 1;
    }

    static class State {
        int value;
        int chosenRot;
        int dir;
    }

    static class PriorityQueue {
        PriorityBlockingQueue<Element> elements;

        public PriorityQueue() {
            elements = new PriorityBlockingQueue<>();
        }

        public boolean isEmpty() {
            return elements.isEmpty();
        }

        public void put(Element element) {
            elements.add(element);
        }

        public Element get() {
                return elements.poll();
        }

    }

    static class Element implements Comparable<Element> {
        int priority;
        State[] item;

        @Override
        public int compareTo(Element other) {
            return -Integer.compare(this.priority, other.priority);
        }
    }
}
