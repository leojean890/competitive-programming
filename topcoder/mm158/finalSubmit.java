import java.io.*;
import java.util.*;

public class Kaleidoscope {
    private static final List<String> DIR = List.of("D","U","R","L");
    private static final int[][] DIRS = new int[][]{
        new int[]{1, 0},
        new int[]{-1, 0},
        new int[]{0, 1},
        new int[]{0, -1}
    };

    private static final int DOWN = 0;
    private static final int UP = 1;
    private static final int RIGHT = 2;
    private static final int LEFT = 3;
    private static final double t_start = 10d;
    private static final double t_final = 0.1d;
    private static double T, startTime;
    private static Map<Integer,List<Integer>> validMovesPerSpot = new HashMap<>();
    private static int[] availableMoves;
    private static int[] cgrid;
    private static int[][] colourMap;
    private static int[] grid;
    private static int nAvailableMoves,N,C,nRollouts,currScore,M,indexx;
    private static List<SaState> currStates = new ArrayList<>();
    private static int[] counters;
    private static final Random random = new Random(1);


    public static void sa() {

        var elapsed = System.currentTimeMillis() - startTime;
        List<Integer> move = null;

        while (elapsed < 9500) {
             nRollouts++;

             List<SaState> states = new ArrayList<>(currStates);

             for (int r=0; r<N; r++)
               for (int c=0; c<N; c++)
                 cgrid[r*N+c]=grid[r*N+c];

            int actionType = random.nextInt(3);
            int currMove = -1;
            int toMoveA = 0;
            int dir = 0;

            if (actionType == 0 && states.size() == 1) {
                actionType = 1+random.nextInt(2);
            }

            if (actionType == 1) {
                 currMove = random.nextInt(states.size());
                 toMoveA = availableMoves[random.nextInt(nAvailableMoves)];
                 move = validMovesPerSpot.get(toMoveA);
                 dir = move.get(random.nextInt(move.size()));
            } else if (actionType == 2) {
                 currMove = random.nextInt(states.size()+1);
                 toMoveA = availableMoves[random.nextInt(nAvailableMoves)];
                 move = validMovesPerSpot.get(toMoveA);
                 dir = move.get(random.nextInt(move.size()));
            } else {
                 currMove = random.nextInt(states.size());
                 states.remove(currMove);
            }

            int inc = 0;
            int L = states.size();

            while (inc < L) {

                if (inc == currMove && actionType > 0) {
                    if (actionType == 1) {
                        states.set(inc, new SaState(toMoveA,dir));
                    } else {
                        states.add(inc, new SaState(toMoveA,dir));
                        L += 1;
                    }
                }

                SaState state = states.get(inc);
                int direc = state.direction;
                int dy = DIRS[direc][0];
                int dx = DIRS[direc][1];
                int toMove = state.index;
                int y = toMove/N;
                int x = toMove%N;

                int moved = (y+dy)*N+x+dx;
                cgrid[moved] = colourMap[cgrid[toMove]][cgrid[moved]];
                cgrid[toMove] = cgrid[moved];

                inc += 1;
                if (inc == currMove && L == inc && actionType > 0) {
                    states.add(new SaState(toMoveA,dir));
                    L += 1;
                }
            }

            int score = 0;
            for (int i = 0 ; i < C ; i++) {
                counters[i] = 0;
            }

            for (int r=0; r<N; r++) {
              for (int c=0; c<N; c++) {
                if (cgrid[r*N+c] > -1) {
                    counters[cgrid[r*N+c]] += 1;
                }
              }
            }

            M = 0;

            for (int i = 0 ; i < C ; i++) {
                if (counters[i] > M) {M = counters[i];indexx = i;}
            }

            for (int i = 0 ; i < C ; i++) {
                if (i != indexx) score += counters[i];
            }

            score = score*N + states.size();

            if (score < currScore) {
                currStates = states;
                currScore = score;
            } else {
                double rr = random.nextDouble();

                T = t_start*Math.pow(t_final/t_start, elapsed/9000);

                if (Math.exp((currScore - score)/T) > rr){
                    currScore = score;
                    currStates = states;
                }
            }
            elapsed = System.currentTimeMillis() - startTime;
        }
    }


  public static void main(String[] args) throws Exception
  {           
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));    

    N = Integer.parseInt(in.readLine());
    startTime = System.currentTimeMillis();
    C = Integer.parseInt(in.readLine());

    colourMap = new int[C][C];
    for (int i=0; i<C; i++)
      for (int k=0; k<C; k++)
        colourMap[i][k] = Integer.parseInt(in.readLine());

    availableMoves = new int[N*N];

    grid = new int[N*N];
    cgrid = new int[N*N];
    for (int r=0; r<N; r++)
      for (int c=0; c<N; c++)
        grid[r*N+c] = Integer.parseInt(in.readLine());

    for (int r=0; r<N; r++) {
      for (int c=0; c<N; c++) {
        if (grid[r*N+c] > -1) {
            availableMoves[nAvailableMoves] = r*N+c;
            nAvailableMoves += 1;
            validMovesPerSpot.put(r*N+c, new ArrayList<>());
            if (r > 0 && grid[(r-1)*N+c] > -1)
                validMovesPerSpot.get(r*N+c).add(UP);
            if (c > 0 && grid[(c-1)+N*r] > -1)
                validMovesPerSpot.get(r*N+c).add(LEFT);
            if (r < N-1 && grid[(r+1)*N+c] > -1)
                validMovesPerSpot.get(r*N+c).add(DOWN);
            if (c < N-1 && grid[(c+1)+N*r] > -1)
                validMovesPerSpot.get(r*N+c).add(RIGHT);
        }
      }
    }

     for (int r=0; r<N; r++)
       for (int c=0; c<N; c++)
         cgrid[r*N+c]=grid[r*N+c];

    List<Integer> move = null;
    for (int i = 0 ; i < 3*N*N/2 ; i++) {
        int toMove = availableMoves[random.nextInt(nAvailableMoves)];
        move = validMovesPerSpot.get(toMove);
        int dir = move.get(random.nextInt(move.size()));
        int dy = DIRS[dir][0];
        int dx = DIRS[dir][1];
        int y = toMove/N;
        int x = toMove%N;
        int moved = (y+dy)*N+x+dx;
        currStates.add(new SaState(toMove, dir));
        cgrid[moved] = colourMap[cgrid[toMove]][cgrid[moved]];
        cgrid[toMove] = cgrid[moved];
    }

    counters = new int[C];

    for (int r=0; r<N; r++) {
      for (int c=0; c<N; c++) {
        if (cgrid[r*N+c] > -1) {
            counters[cgrid[r*N+c]] += 1;
        }
      }
    }

    M = 0;
    for (int i = 0 ; i < C ; i++) {
        if (counters[i] > M) {M = counters[i];indexx=i;}
    }

    for (int i = 0 ; i < C ; i++) {
        if (i != indexx) currScore += counters[i];
    }

    currScore = currScore*N + currStates.size();

    sa();

    System.err.println("score "+currScore);
    System.err.println("nRollouts "+nRollouts);

    System.out.println(currStates.size());

    for (int i=0; i<currStates.size(); i++)
    {
      SaState state = currStates.get(i);
      int num = state.index;
      int dir = state.direction;
      int r=num/N;
      int c=num%N;
      int y = r+DIRS[dir][0];
      int x = c+DIRS[dir][1];
      System.out.println(r+" "+c+" "+y+" "+x);
    }
  }

  static class SaState {
    int index;
    int direction;

    public SaState(int index, int direction) {
        this.index = index;
        this.direction = direction;
    }
  }
}
