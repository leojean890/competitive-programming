import java.io.PrintWriter;
import java.util.*;

public class RacingCarBest {
    private static final double carRadius = 1.0;
    private static final int minN=10;
    private static final int maxN=30;
    private static int maxTurns=3000;
    private static final int minK=3;
    private static final int maxK=20;
    private static double baseline;
    private static final int border=2;
    private static final double minDeltaStep=0.01;
    private static final double maxDeltaStep=1.0;
    private static final double minMaxVelocity=1.0;
    private static final double maxMaxVelocity=1000.0;
    private static final double maxMaxAcceleration=10.0;
    private static final double minMaxAcceleration=0.1;
    private static final int uncollectedPenalty=500;
    private static final int collisionPenalty=50;
    private static final int S = 128;
    private static int collected = 0;
    private static int turn=0;
    private static int collisions=0;
    private static int[][] type;
    private static int[][] checkpointsCrossed;
    private static double[] X;
    private static double[] Y;
    private static int[] CR;
    private static int[] CC;
    private static int[][] dirs = { {1,0}, {-1,0}, {0,1}, {0,-1} };

    static ArrayList<Integer> checkpoints = new ArrayList<>();

    private static double maxAcceleration = 2.5;
    private static double maxVelocity = 20.0;
    private static double delta_step = 0.1;

    private static double carX=0;
    private static double curr_carX=0;
    private static double carY=0;
    private static double curr_carY=0;
    private static double carAngle=0;
    private static double curr_carAngle=0;
    private static double leftWheelSpeed=0;
    private static double curr_leftWheelSpeed=0;
    private static double rightWheelSpeed=0;
    private static double curr_rightWheelSpeed=0;
    private static double leftWheelAcc=0;
    private static double rightWheelAcc=0;

    private static int car_row=0;
    private static int car_col=0;
    private static double lastCheckPointX=0;
    private static double lastCheckPointY=0;
    private static double lastCheckPointAngle=0;
    private static int lastCheckPointId=0;
    static int N, K;
    static int carRow, carCol;
    static int elapsedTime;

    private static final double t_start = 100000000d;
    private static final double t_final = 0.00000001d;
    private static double T, startTime, init_startTime;
    private static final Random random = new Random(1);
    private static int NB_MOVES = 16;
    private static int TIME = 8;
    private static int TOTAL_TIME = 9900;
    private static int nRollouts;
    private static double currScore, bestScore;
    private static double[] currLMoves = new double[NB_MOVES];
    private static double[] bestLMoves = new double[NB_MOVES];
    private static double[] currRMoves = new double[NB_MOVES];
    private static double[] bestRMoves = new double[NB_MOVES];

    static Scanner scanner = new Scanner(System.in);
    static PrintWriter writer = new PrintWriter(System.out);

    private static class CommandResult {
        public double acceleration;
        public int steps;

        public CommandResult(double acceleration, int steps) {
            this.acceleration = acceleration;
            this.steps = steps;
        }
    }

    static void getPosition() {
        scanner.useLocale(Locale.FRANCE); 

        try {
            if (scanner.hasNext())
                elapsedTime = scanner.nextInt();
        }catch(Exception e){

        }

        try {
            if (scanner.hasNext())
                carCol = scanner.nextInt();
        }catch(Exception e){

        }

        try {
            if (scanner.hasNext())
                carRow = scanner.nextInt();
        }catch(Exception e){

        }

        String raw = "";
        if (scanner.hasNext()) {

            raw = scanner.next().trim();
            raw = raw.replace(',', '.'); 
            raw = raw.replaceAll("[^0-9\\-\\.]", "");
            try {
                carX = Double.parseDouble(raw);
            }catch(Exception e){

            }
        }


        if (scanner.hasNext()) {
            raw = scanner.next().trim();
            raw = raw.replace(',', '.'); 
            raw = raw.replaceAll("[^0-9\\-\\.]", "");
            try {
                carY = Double.parseDouble(raw);
            }catch(Exception e){

            }
        }
        if (scanner.hasNext()) {
            raw = scanner.next().trim();
            raw = raw.replace(',', '.'); 
            raw = raw.replaceAll("[^0-9\\-\\.]", "");
            try {
                carAngle = Double.parseDouble(raw);
            }catch(Exception e){

            }
        }
        if (scanner.hasNext()) {

            raw = scanner.next().trim();
            raw = raw.replace(',', '.'); 
            raw = raw.replaceAll("[^0-9\\-\\.]", "");
            try {
                leftWheelSpeed = Double.parseDouble(raw);
            }catch(Exception e){

            }
        }
        if (scanner.hasNext()) {

            raw = scanner.next().trim();
            raw = raw.replace(',', '.'); 
            raw = raw.replaceAll("[^0-9\\-\\.]", "");
            try {
                rightWheelSpeed = Double.parseDouble(raw);
            }catch(Exception e){

            }
        }

    }

    static boolean publishCommand(double left, double right) {
        turn++; 
        writer.printf(Locale.US,"%.20f %.20f\n", left, right); 
        writer.flush();
        String raw = "";
        double result = 0d;
        if (scanner.hasNext()) {
            raw = scanner.next().trim();
            raw = raw.replace(',', '.').replace('\u066C', '.')  
                    .replace('\uFF0C', '.'); 

            raw = raw.replaceAll("[^0-9eE\\-\\.]", "");
            raw = raw.replaceAll("[^0-9\\-\\.]", "");
            result = Double.parseDouble(raw);

            getPosition(); 
            if (type[carRow][carCol] == 2) {
                type[carRow][carCol] = 3;
            }

        }
        return result != -1; 
    }

    public static void main(String[] args) {
        scanner.useLocale(Locale.US);
        N = scanner.nextInt();
        K = scanner.nextInt();

        String raw = scanner.next().trim();
        raw = raw.replace(',', '.'); 
        raw = raw.replaceAll("[^0-9\\-\\.]", "");
        baseline = Double.parseDouble(raw);
        raw = scanner.next().trim();
        raw = raw.replace(',', '.'); 
        raw = raw.replaceAll("[^0-9\\-\\.]", "");
        maxAcceleration = Double.parseDouble(raw);
        raw = scanner.next().trim();
        raw = raw.replace(',', '.'); 
 
        raw = raw.replaceAll("[^0-9\\-\\.]", "");
        delta_step = Double.parseDouble(raw);

        maxTurns = scanner.nextInt();

        X = new double[N + 1];
        Y = new double[N + 1];
        for (int r = 0; r <= N; r++) {
            Y[r] = scanner.nextDouble();
        }
        for (int r = 0; r <= N; r++) {
            X[r] = scanner.nextDouble();
        }

        type = new int[N][N];
        CR = new int[K];
        CC = new int[K];
        int k = 0;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                type[r][c] = scanner.nextInt();
                if (type[r][c] == 2) {
                    CR[k] = r;
                    CC[k] = c;
                    k++;
                }
            }
        }

        getPosition();

        for (int i = 0 ; i < NB_MOVES ; i++) {
            currLMoves[i] = 2*maxAcceleration*random.nextDouble()-maxAcceleration;
            currRMoves[i] = 2*maxAcceleration*random.nextDouble()-maxAcceleration;
        }


        int turn = 0;

        while (elapsedTime < TOTAL_TIME && turn < 3000) {
            turn++;


            double distToClosestCp = Double.MAX_VALUE;

            for (int kk = 0; kk < K; kk++) {
                if (type[CR[kk]][CC[kk]] == 2) {
                    double dist = Math.pow(Y[CR[kk]]-carY, 2) + Math.pow(X[CC[kk]]-carX,2);
                    if (dist < distToClosestCp) {
                        distToClosestCp = dist;

                    }
                }
            }


            List<Integer> path = new ArrayList<>();
            List<Integer> finalPath = new ArrayList<>();
            Deque<Node1> queue = new ArrayDeque<>();
            queue.add(new Node1(carRow,carCol,path));
            int[][] visited = new int[N][N];
            visited[carRow][carCol] = 1;


            while (!queue.isEmpty()) {
                Node1 current = queue.pollFirst();

                if (type[current.row][current.col] == 2) {
                    finalPath = current.path;
                    break;
                }

                for (int[] d : dirs) {
                    int nr = current.row + d[0];
                    int nc = current.col + d[1];
                    if (0 <= nr && nr < N && 0 <= nc && nc < N
                            && visited[nr][nc] == 0
                            && type[nr][nc] != 1) {
                        visited[nr][nc] = 1;
                        List<Integer> npath = new ArrayList<>(current.path);
                        npath.add(nr * N + nc); 
                        queue.addLast(new Node1(nr, nc, npath));
                    }
                }

            }

            sa(finalPath);

            publishCommand(bestLMoves[0], bestRMoves[0]);

            for (int i = 0 ; i < NB_MOVES-1 ; i++) {
                bestLMoves[i] = bestLMoves[i+1];
                bestRMoves[i] = bestRMoves[i+1];
                currRMoves[i] = bestRMoves[i+1];
                currLMoves[i] = bestLMoves[i+1];

            }
            bestLMoves[NB_MOVES-1] = 2*maxAcceleration*random.nextDouble()-maxAcceleration;
            bestRMoves[NB_MOVES-1] = 2*maxAcceleration*random.nextDouble()-maxAcceleration;

        }

        // End of the simulation, send the termination command
        writer.println("-1");
        writer.flush();
    }


    static class Node1 {
        int row;
        int col;
        List<Integer> path;

        Node1(int row, int col, List<Integer> path) {
            this.row = row;
            this.col = col;
            this.path = path;
        }
    }


    public static void sa(List<Integer> finalPath) {
            double lmove;
            double rmove;
            bestScore = Double.MAX_VALUE;
            currScore = Double.MAX_VALUE;
            startTime = System.currentTimeMillis();
            double constanteNormalisation = 200/(double)NB_MOVES;

            var elapsed = System.currentTimeMillis() - startTime;

            while (elapsed < TIME) {
                nRollouts++;

                double[] lmoves = Arrays.copyOf(currLMoves, NB_MOVES);
                double[] rmoves = Arrays.copyOf(currRMoves, NB_MOVES);

                int currMove = random.nextInt(NB_MOVES);
                lmove = 2*maxAcceleration*random.nextDouble()-maxAcceleration;
                rmove = 2*maxAcceleration*random.nextDouble()-maxAcceleration;
                lmoves[currMove] = lmove;
                rmoves[currMove] = rmove;
                int amountOfCrossedCp = 0;

                car_row = carRow;
                car_col = carCol;
                curr_carX = carX;
                curr_carY = carY;
                curr_carAngle = carAngle;
                curr_leftWheelSpeed = leftWheelSpeed;
                curr_rightWheelSpeed = rightWheelSpeed;

                checkpointsCrossed = new int[N][N];
                for (int r = 0; r < N; r++) {
                    for (int c = 0; c < N; c++) {
                        checkpointsCrossed[r][c] = type[r][c];
                    }
                }

                Double score = 0d;
                int currVisitedInPath = 0;

                for (int inc = 0 ; inc < NB_MOVES ; inc++) {

                    int bkp_carRow = car_row;
                    int bkp_carCol = car_col;
                    double bkp_carX = curr_carX;
                    double bkp_carY = curr_carY;
                    double bkp_carAngle = curr_carAngle;
                    double bkp_leftWheelSpeed = curr_leftWheelSpeed;
                    double bkp_rightWheelSpeed = curr_rightWheelSpeed;

                    Double left_acceleration = lmoves[inc];
                    Double right_acceleration = rmoves[inc];
                    int res = ApplyCommand(left_acceleration, right_acceleration);
                    
                    if (res == 1) {
                        amountOfCrossedCp += (NB_MOVES-inc);
                    }

                    else if (res == -1) {
                        car_row = bkp_carRow;
                        car_col = bkp_carCol;
                        curr_carX = bkp_carX;
                        curr_carY = bkp_carY;
                        curr_carAngle = bkp_carAngle;
                        curr_leftWheelSpeed = bkp_leftWheelSpeed;
                        curr_rightWheelSpeed = bkp_rightWheelSpeed;
                        amountOfCrossedCp -= (NB_MOVES-inc); 
                        break;
                    }

                    if (currVisitedInPath < finalPath.size()) {
                        int rw = finalPath.get(currVisitedInPath) / N;
                        int cl = finalPath.get(currVisitedInPath) % N;

                        if (rw == car_row && cl == car_col) {
                            score -= 100.0*Math.pow(100,currVisitedInPath)*(NB_MOVES-inc);
                            currVisitedInPath++;
                        } else {
                            score += 0.01*(Math.abs(Y[rw]-curr_carY) + Math.abs(X[cl]-curr_carX))*Math.pow(finalPath.size()-currVisitedInPath,2)*(NB_MOVES-inc);
                        }
                    } else {
                        double distToClosestCp = Double.MAX_VALUE;

                        for (int k = 0; k < K; k++) {
                            if (checkpointsCrossed[CR[k]][CC[k]] == 2) {
                                double dist = Math.pow(Y[CR[k]]-curr_carY, 2) + Math.pow(X[CC[k]]-curr_carX,2);
                                if (dist < distToClosestCp)
                                    distToClosestCp = dist;
                            }
                        }
                        score += 0.001*distToClosestCp*(NB_MOVES-inc);
                    }

                        double angularSpeed = Math.abs(shorten((curr_leftWheelSpeed - curr_rightWheelSpeed) / baseline));
                        if (angularSpeed > 3) {
                            score += Math.pow(angularSpeed,(inc+1)*constanteNormalisation);
                        }

                }



                score -= 10000000*amountOfCrossedCp;

                if (score < currScore) {
                    currLMoves = Arrays.copyOf(lmoves, NB_MOVES);
                    currRMoves = Arrays.copyOf(rmoves, NB_MOVES);
                    currScore = score;
                    if (currScore < bestScore) {
                        bestScore = currScore;
                        bestLMoves = Arrays.copyOf(lmoves, NB_MOVES);
                        bestRMoves = Arrays.copyOf(rmoves, NB_MOVES);

                    }
                } else {
                    double rr = random.nextDouble();

                    T = t_start*Math.pow(t_final/t_start, elapsed/TIME);

                    if (Math.exp((currScore - score)/T) > rr){
                        currScore = score;
                        currLMoves = Arrays.copyOf(lmoves, NB_MOVES);
                        currRMoves = Arrays.copyOf(rmoves, NB_MOVES);
                    }
                }
                elapsed = System.currentTimeMillis() - startTime;
            }
    }




    private static double Clamp(double x, double lim) {
        if (x < -lim) return -lim;
        if (x > lim) return lim;
        return x;
    }

    private double sq(double a) {
        return a * a;
    }

    private static double shorten(double a) {
        return (double)Math.round(a * 1000.0) / 1000.0;
    }

    private static void collectCheckPoint(int row, int col) {
        collected++;
        type[row][col] = 3;
        lastCheckPointX = carX;
        lastCheckPointY = carY;
        lastCheckPointAngle = carAngle;
        lastCheckPointId = row * N + col;
    }

    private int getScore() {
        return turn + (K - collected) * uncollectedPenalty + collisions * collisionPenalty;
    }

    private double getTimeWithPenalty() {
        return turn * delta_step + collisions * 5.0;
    }

    private static boolean moveCar(Point nextPoint) {
        if (nextPoint.x <= 0 || nextPoint.x >= S || nextPoint.y <= 0 || nextPoint.y >= S) return false;

        double tx = nextPoint.x;
        double ty = nextPoint.y;
        while (curr_carX != tx || curr_carY != ty) {
            if (type[car_row][car_col] == 1) {
                return false;
            }
            double nx = tx;
            double ny = ty;
            int nr = car_row;
            int nc = car_col;
            double bp = 1.0;
            if (tx < X[car_col]) {
                double p = (X[car_col] - curr_carX) / (tx - curr_carX);
                if (p < bp) {
                    ny = curr_carY + p * (ty - curr_carY);
                    nx = curr_carX + p * (tx - curr_carX);
                    nr = car_row;
                    nc = car_col - 1;
                    bp = p;
                }
            }
            if (tx > X[car_col + 1]) {
                double p = (X[car_col + 1] - curr_carX) / (tx - curr_carX);
                if (p < bp) {
                    ny = curr_carY + p * (ty - curr_carY);
                    nx = curr_carX + p * (tx - curr_carX);
                    nr = car_row;
                    nc = car_col + 1;
                    bp = p;
                }
            }

            if (ty < Y[car_row]) {
                double p = (Y[car_row] - curr_carY) / (ty - curr_carY);
                if (p < bp) {
                    ny = curr_carY + p * (ty - curr_carY);
                    nx = curr_carX + p * (tx - curr_carX);
                    nr = car_row - 1;
                    nc = car_col;
                    bp = p;
                }
            }
            if (ty > Y[car_row + 1]) {
                double p = (Y[car_row + 1] - curr_carY) / (ty - curr_carY);
                if (p < bp) {
                    ny = curr_carY + p * (ty - curr_carY);
                    nx = curr_carX + p * (tx - curr_carX);
                    nr = car_row + 1;
                    nc = car_col;
                    bp = p;
                }
            }
            curr_carX = nx;
            curr_carY = ny;
            car_row = nr;
            car_col = nc;
        }

        return type[car_row][car_col] != 1;
    }
    
    private static Point AccurateDynamic()
    {
        double dleft = curr_leftWheelSpeed * delta_step * 0.5;
        double dright = curr_rightWheelSpeed * delta_step * 0.5;

        curr_leftWheelSpeed += leftWheelAcc * delta_step;
        curr_rightWheelSpeed += rightWheelAcc * delta_step;

        dleft += curr_leftWheelSpeed * delta_step * 0.5;
        dright += curr_rightWheelSpeed * delta_step * 0.5;

        double da = (dleft - dright) / baseline;
        double speed = (dleft + dright) * 0.5;

        double cc = Math.cos(curr_carAngle);
        double ss = Math.sin(curr_carAngle);

        // If da is too small, speed / da might be very innacurate, also cos/sin function might not
        // be accurate, using Taylor expansion (up to the third term gives an error in O(da^3) or 1.0e-15)
        if (Math.abs(da) < 1.0e-5) {
            double dx = cc * speed * (1.0 - da * da / 6.0) - ss * speed * da / 2.0;
            double dy = ss * speed * (1.0 - da * da / 6.0) + cc * speed * da / 2.0;
            curr_carAngle += da;
            if (curr_carAngle > Math.PI) curr_carAngle -= 2 * Math.PI;
            if (curr_carAngle < -Math.PI) curr_carAngle += 2 * Math.PI;
            return new Point(curr_carX + dx, curr_carY + dy);
        }
        double R = speed / da;
        double cx = - R * ss;
        double cy = + R * cc;
        double ca = Math.cos(da);
        double sa = Math.sin(da);
        curr_carAngle += da;
        double dx = cx * (1.0 - ca) + sa * cy;
        double dy = cy * (1.0 - ca) - sa * cx;

        if (curr_carAngle > Math.PI) curr_carAngle -= 2 * Math.PI;
        if (curr_carAngle < -Math.PI) curr_carAngle += 2 * Math.PI;

        return new Point(curr_carX + dx, curr_carY + dy);
    }

    private static int ApplyCommand(double left_acceleration, double right_acceleration)
    {
        leftWheelAcc = Clamp(left_acceleration, maxAcceleration);
        rightWheelAcc = Clamp(right_acceleration, maxAcceleration);       

        Point nextPoint = AccurateDynamic();
        if (!moveCar(nextPoint)) {
            return -1; 
        }
        if (checkpointsCrossed[car_row][car_col] == 2) {
            checkpointsCrossed[car_row][car_col] = 3;
            return 1;
        }
        return 0;
    }

    public static class Point {
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Point point = (Point) obj;
            return Math.abs(point.x - x) < 1e-7 &&
                    Math.abs(point.y - y) < 1e-7;
        }

        @Override
        public int hashCode() {
            return Objects.hash((float)x, (float)y);
        }
        double x, y;

        Point(double x, double y) {
            this.x = x;
            this.y = y;
        }


        static double Square(double x) {
            return x * x;
        }

        public double distance(Point other) {
            return Math.sqrt(Square(this.x - other.x) + Square(this.y - other.y));
        }

    }

}
