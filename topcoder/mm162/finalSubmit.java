import java.util.*;

public class DaylightRobberyFinal {
    //Inputs
    private static int G;            // number of guards
    private static int C;            // number of valuables
    private static int B;            // bribe penalty multiplier

    //Constants other
    private static final int SCORE_BRIBE_PENALTY_MULT = 20;


    //pre-computed stuff
    private static List<Point>[] guardRoutes;
    private static List<List<Point>>[] guardsConeOfViewStay;
    private static List<List<Point>>[] guardsConeOfViewCrouch;
    static int[] disabledGuards;
    static int[] previous_disabledGuards;

    private static final Random random = new Random(1);

    private static final int SIZE = 10000;
    private static final int MAX_SPEED = 400;

    private static int NB_MOVES = 1000;
    private static int TIME = 9000;
    private static int nAvailable;
    private static FinalState bestState;
    private static int thiefX, thiefY;
    private static final List<List<Integer>> availableEdges = new ArrayList<>();
    private static double startTime;
    static int[][] coins;
    static ArrayList<Point> allActions = new ArrayList<>();
    static PriorityQueue<State> queue = new PriorityQueue<>();

    private static class FinalState {
        int thiefX;
        int thiefY;
        int currentDepth;
        int score;
        ArrayList<Point> allActions;
        int[] disabledGuards;

        public FinalState() {
            score = 1000000;
        }
        public FinalState(ArrayList<Point> allActions, int thiefX, int thiefY, int currentDepth, int score, int[] disabledGuards) {
            this.thiefX = thiefX;
            this.thiefY = thiefY;
            this.currentDepth = currentDepth;
            this.allActions = allActions;
            this.score = score;
            this.disabledGuards = disabledGuards;
        }
    }

    public static class State implements Comparable<State>{
        Double score;
        Point point;
        int depth;
        List<Point> actions;

        public State(Double score, Point point, int depth, List<Point> actions) {
            this.score = score;
            this.point = point;
            this.depth = depth;
            this.actions = actions;
        }

        @Override
        public int compareTo(State o){
            return this.score.compareTo(o.score);
        }
    }

    public static void dfs(int amountOfTakenCoins, int thiefX, int thiefY, ArrayList<Point> allActions, int[] takenCoins, int currentDepth, int[] disabledGuards, int currentScore) {
        if (amountOfTakenCoins == C || currentDepth > 990 || System.currentTimeMillis() - startTime > TIME) {
            return;
        }

        queue.clear();
        queue.add(new State(0d,new Point(thiefX,thiefY),currentDepth,new ArrayList<>()));

        while(true) {
            State state = queue.poll();
            int cthiefX = state.point.x;
            int cthiefY = state.point.y;
            if (state.depth > 990 || System.currentTimeMillis() - startTime > TIME) {
                break;
            }

            for (int j = 0 ; j < C ; j++) {

                if (takenCoins[j] == 0 && Math.sqrt(sq(cthiefX - coins[j][0]) + sq(cthiefY - coins[j][1])) <= MAX_SPEED && makeMoveWillGetDetected(disabledGuards, cthiefX, cthiefY, coins[j][0], coins[j][1], state.depth) == 3) {
                    ArrayList<Point> newActions = new ArrayList<>();
                    for (int i = 0; i < allActions.size(); i++) {
                        newActions.add(allActions.get(i));
                    }
                    for (int i = 0; i < state.actions.size(); i++) {
                        newActions.add(state.actions.get(i));
                    }

                    int newDepth = state.depth;

                    if (cthiefX != coins[j][0] || cthiefY != coins[j][1]) {
                        newActions.add(new Point(coins[j][0], coins[j][1]));
                        newDepth++;
                    }

                    int[] n_takenCoins = new int[C];
                    for (int i = 0 ; i < C ; i++) n_takenCoins[i] = takenCoins[i];
                    n_takenCoins[j] = 1;

                    int[] n_disabledGuards = new int[G];
                    for (int k = 0 ; k < G ; k++) n_disabledGuards[k] = disabledGuards[k];

                    int newScore = currentScore-1000+newDepth;

                    if (newScore < bestState.score) {
                        System.err.println(newScore);
                        int[] nn_disabledGuards = new int[G];
                        for (int k = 0 ; k < G ; k++) nn_disabledGuards[k] = disabledGuards[k];

                        ArrayList<Point> nnewActions = new ArrayList<>();
                        for (int i = 0; i < newActions.size(); i++) {
                            nnewActions.add(newActions.get(i));
                        }
                        bestState = new FinalState(nnewActions, coins[j][0], coins[j][1], newDepth, newScore, nn_disabledGuards);
                    }

                    dfs(amountOfTakenCoins+1, coins[j][0], coins[j][1], newActions, n_takenCoins, newDepth, n_disabledGuards, newScore);

                }
            }

            for (int i = 0 ; i < G ; i++) {
                int x = guardRoutes[i].get(state.depth%guardRoutes[i].size()).x;
                int y = guardRoutes[i].get(state.depth%guardRoutes[i].size()).y;
                if (disabledGuards[i] == 0 && Math.sqrt(sq(cthiefX-x) + sq(cthiefY-y)) <= MAX_SPEED && makeMoveWillGetDetected(disabledGuards, cthiefX, cthiefY, x, y, state.depth, i) == 3) {

                    ArrayList<Point> newActions = new ArrayList<>();
                    for (int k = 0; k < allActions.size(); k++) {
                        newActions.add(allActions.get(k));
                    }
                    for (int k = 0; k < state.actions.size(); k++) {
                        newActions.add(state.actions.get(k));
                    }

                    int newDepth = state.depth;

                    if (cthiefX != x || cthiefY != y) {
                        newActions.add(new Point(x, y));
                        newDepth++;
                    }

                    int[] n_takenCoins = new int[C];
                    int[] n_disabledGuards = new int[G];

                    for (int k = 0 ; k < C ; k++) n_takenCoins[k] = takenCoins[k];
                    for (int k = 0 ; k < G ; k++) n_disabledGuards[k] = disabledGuards[k];

                    n_disabledGuards[i] = 1;


                    int newScore = currentScore+SCORE_BRIBE_PENALTY_MULT * B;//-1000+newDepth;

                    dfs(amountOfTakenCoins, x, y, newActions, n_takenCoins, newDepth, n_disabledGuards, newScore);

                    break;

                }
            }


            int nbTrials = 0;
            int nbAdds = 0;
            while ((nbTrials < 1000 && nbAdds < 10) || queue.size() < 20) {
                if (nbTrials > 5000 && queue.size() > 18)break;
                if (nbTrials > 10000 && queue.size() > 17)break;
                if (nbTrials > 15000 && queue.size() > 15)break;
                if (nbTrials > 20000 && queue.size() > 13)break;
                if (nbTrials > 25000 && queue.size() > 11)break;
                if (nbTrials > 30000 && queue.size() > 9)break;
                if (nbTrials > 35000 && queue.size() > 7)break;
                if (nbTrials > 40000 && queue.size() > 5)break;
                if (nbTrials > 50000 && queue.size() > 4)break;
                if (nbTrials > 60000 && queue.size() > 3)break;
                if (nbTrials > 70000 && queue.size() > 2)break;
                if (nbTrials > 80000 && queue.size() > 1)break;
                if (nbTrials > 90000 && queue.size() > 0)break;
                if (nbTrials > 100000) {break;}//notFound =true;
                nbTrials++;
                int action = random.nextInt(nAvailable);
                List<Integer> act = availableEdges.get(action);
                int atX = cthiefX+act.get(0);
                int atY = cthiefY+act.get(1);
                int res = makeMoveWillGetDetected(disabledGuards, cthiefX, cthiefY, atX, atY, state.depth);
                if (res == 3) {
                    nbAdds++;
                    ArrayList<Point> newList = new ArrayList<>(state.actions);
                    newList.add(new Point(atX,atY));
                    double closestDist = Double.MAX_VALUE;
                    for (int j = 0 ; j < C ; j++) {
                        double dist = Math.sqrt(sq(cthiefX-coins[j][0]) + sq(cthiefY-coins[j][1]));
                        if (takenCoins[j] == 0 && dist < closestDist) {
                            closestDist = dist;
                        }
                    }

                    double score = 10*state.depth + closestDist;
                    queue.add(new State(score,new Point(atX,atY),state.depth+1,newList));
                }


            }
            if (nbTrials > 100000)break;


        }

    }



    public static void greedy() {

        int[] takenCoins = new int[C];
        int amountOfTakenCoins = 0;
        int currentDepth = 1;
        int[] disabledGuards = new int[G];

        bestState = new FinalState();

        dfs(amountOfTakenCoins, thiefX, thiefY, new ArrayList<>(), takenCoins, currentDepth, disabledGuards, 1000*(C+5));

        thiefX = bestState.thiefX;// bestThiefX; bestState
        thiefY = bestState.thiefY;//bestThiefY;
        currentDepth = bestState.currentDepth;//bestCurrentDepth;
        allActions = bestState.allActions;//bestAllActions;
        disabledGuards = bestState.disabledGuards;

        // go out in the end

        queue.clear();
        queue.add(new State(0d,new Point(thiefX,thiefY),currentDepth,new ArrayList<>()));

        while(true) {
            State state = queue.poll();
            int cthiefX = state.point.x;
            int cthiefY = state.point.y;
            if (state.depth > 990 || System.currentTimeMillis() - startTime > 9700) {
                break;
            }
            boolean outOfBounds = (cthiefX<0 || cthiefX>=SIZE) || (cthiefY<0 || cthiefY>=SIZE);

            if (outOfBounds) {
                for (int i = 0; i < state.actions.size(); i++) {
                    allActions.add(state.actions.get(i));
                }
                thiefX = cthiefX;
                thiefY = cthiefY;
                break;
            }

            int nbTrials = 0;
            int nbAdds = 0;
            while ((nbTrials < 1000 && nbAdds < 10) || queue.size() < 20) {
                if (nbTrials > 5000 && queue.size() > 18)break;
                if (nbTrials > 10000 && queue.size() > 17)break;
                if (nbTrials > 15000 && queue.size() > 15)break;
                if (nbTrials > 20000 && queue.size() > 13)break;
                if (nbTrials > 25000 && queue.size() > 11)break;
                if (nbTrials > 30000 && queue.size() > 9)break;
                if (nbTrials > 35000 && queue.size() > 7)break;
                if (nbTrials > 40000 && queue.size() > 5)break;
                if (nbTrials > 50000 && queue.size() > 4)break;
                if (nbTrials > 60000 && queue.size() > 3)break;
                if (nbTrials > 70000 && queue.size() > 2)break;
                if (nbTrials > 80000 && queue.size() > 1)break;
                if (nbTrials > 90000 && queue.size() > 0)break;
                if (nbTrials > 100000) {break;}
                nbTrials++;
                int action = random.nextInt(nAvailable);
                List<Integer> act = availableEdges.get(action);
                int atX = cthiefX+act.get(0);
                int atY = cthiefY+act.get(1);
                int res = makeMoveWillGetDetected(disabledGuards, cthiefX, cthiefY, atX, atY, state.depth);
                if (res != 2) {
                    nbAdds++;
                    ArrayList<Point> newList = new ArrayList<>(state.actions);
                    newList.add(new Point(atX,atY));
                    double closestDist = atY;
                    if (atX < closestDist) {
                        closestDist = atX;
                    }
                    if (SIZE-atX < closestDist) {
                        closestDist = SIZE-atX;
                    }
                    if (SIZE-atY < closestDist) {
                        closestDist = SIZE-atY;
                    }
                    double score = 20*state.depth + closestDist;
                    queue.add(new State(score,new Point(atX,atY),state.depth+1,newList));
                }

            }
            if (nbTrials > 100000)break;

        }
    }


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        C = scanner.nextInt();
        startTime = System.currentTimeMillis();
        G = scanner.nextInt();
        B = scanner.nextInt();

        guardsConeOfViewCrouch = new ArrayList[G];
        guardsConeOfViewStay = new ArrayList[G];
        guardRoutes = new ArrayList[G];
        disabledGuards = new int[G];
        previous_disabledGuards = new int[G];

        coins = new int[C][2];
        for (int i = 0; i < C; i++) {
            coins[i][0] = scanner.nextInt();
            coins[i][1] = scanner.nextInt();
        }

        int n, px, py, p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y;
        for (int i = 0; i < G; i++) {
            guardRoutes[i] = new ArrayList<>();
            guardsConeOfViewCrouch[i] = new ArrayList<>();
            guardsConeOfViewStay[i] = new ArrayList<>();
            n = scanner.nextInt();
            for (int k = 0; k < n; k++) {
                px = scanner.nextInt();
                py = scanner.nextInt();
                p1x = scanner.nextInt();
                p1y = scanner.nextInt();
                p2x = scanner.nextInt();
                p2y = scanner.nextInt();
                p3x = scanner.nextInt();
                p3y = scanner.nextInt();
                p4x = scanner.nextInt();
                p4y = scanner.nextInt();
                guardRoutes[i].add(new Point(px,py));

                List<Point> l = new ArrayList<>();
                l.add(new Point(px,py));
                l.add(new Point(p1x,p1y));
                l.add(new Point(p2x,p2y));
                guardsConeOfViewCrouch[i].add(l);

                List<Point> l1 = new ArrayList<>();
                l1.add(new Point(px,py));
                l1.add(new Point(p3x,p3y));
                l1.add(new Point(p4x,p4y));
                guardsConeOfViewStay[i].add(l1);
            }
        }

        thiefX = scanner.nextInt();
        thiefY = scanner.nextInt();
        
        scanner.close();
        for (int i = 0; i <= MAX_SPEED; i++) {
            for (int j = 0; j <= MAX_SPEED; j++) {
                if (Math.sqrt(i*i+j*j) <= MAX_SPEED) {
                    availableEdges.add(List.of(i,j));
                    availableEdges.add(List.of(i,-j));
                    availableEdges.add(List.of(-i,j));
                    availableEdges.add(List.of(-i,-j));
                }
            }
        }
        nAvailable = availableEdges.size();

        List<String> res = new ArrayList<>();

        greedy();

        for (int i = 0 ; i < allActions.size() ; i++) {
            res.add(allActions.get(i).x + " " + allActions.get(i).y);
        }

        System.out.println(res.size());
        for (String re : res) {
            System.out.println(re);

        }
    }
    private static int makeMoveWillGetDetected(int[] disabledGuards, int x, int y, int atX, int atY, int turn) {
        return makeMoveWillGetDetected(disabledGuards, x,y,atX,atY,turn,100000);
    }

    private static int makeMoveWillGetDetected(int[] disabledGuards, int x, int y, int atX, int atY, int turn, int forceCrouching) {
        var source = new Point(x, y);
        var dest = new Point(atX, atY);
        double dist = distPoint2Point(dest, source);
        boolean outOfBounds = (atX<0 || atX>=SIZE) || (atY<0 || atY>=SIZE);

        if (outOfBounds) {
            return 1;
        } else {
            boolean crouching = (dist <= 200);
            if (forceCrouching < 100000) crouching = false;
            for (int i = 0; i< G; i++)
            {
                if (1 == disabledGuards[i]) continue;
                if (i == forceCrouching) continue;
                if (isPointInsideTriangle(dest, crouching?guardsConeOfViewCrouch[i].get(turn%guardRoutes[i].size()):guardsConeOfViewStay[i].get(turn%guardRoutes[i].size())))
                {
                    return 2;
                }
            }

        }

        return 3;
    }

    private static int relativeCCW(int x1, int y1, int x2, int y2, int px, int py)
    {
        x2 -= x1;
        y2 -= y1;
        px -= x1;
        py -= y1;
        long ccw = px * y2 - py * x2;
        if (ccw == 0) {
            ccw = px * x2 + py * y2;
            if (ccw > 0) {
                px -= x2;
                py -= y2;
                ccw = px * x2 + py * y2;
                if (ccw < 0) ccw = 0;
            }
        }
        return (ccw < 0) ? -1 : ((ccw > 0) ? 1 : 0);
    }

    private static boolean isPointInsideTriangle(Point p, List<Point> triangle) {
        if (triangle.size() != 3) return false;

        Point p1 = triangle.get(0);
        Point p2 = triangle.get(1);
        Point p3 = triangle.get(2);

        // Check if point p is on the same side of all three edges
        int ccw1 = relativeCCW(p1.x, p1.y, p2.x, p2.y, p.x, p.y);
        int ccw2 = relativeCCW(p2.x, p2.y, p3.x, p3.y, p.x, p.y);
        int ccw3 = relativeCCW(p3.x, p3.y, p1.x, p1.y, p.x, p.y);

        return (ccw1 >= 0 && ccw2 >= 0 && ccw3 >= 0) || (ccw1 <= 0 && ccw2 <= 0 && ccw3 <= 0);
    }

    static class Point
    {
        int x;
        int y;

        public Point(int x2, int y2)
        {
            x=x2;
            y=y2;
        }

        public String niceStr() {
            return "("+x+","+y+")";
        }
    }

    private static int sq(int a)
    {
        return a*a;
    }

    private static double distPoint2Point(Point p1, Point p2)
    {
        return Math.sqrt(sq(p1.x-p2.x) + sq(p1.y-p2.y));
    }


}
