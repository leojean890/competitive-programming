import java.io.*;
import java.util.*;

public class Vagues {
    private static int nRollouts, nNodes, currScore, H=10, W=250;
    private static int[] grid;

    public static void bs() {

        PriorityQueue<State> queue = new PriorityQueue<State>();
        PriorityQueue<State> queue1 = new PriorityQueue<State>();

        int WIDTH = 800000;
        int depth = 0;

        queue.add(new State(0, 0, -1, -100, -100, new ArrayList<>()));
        while (true) {
            if (queue.isEmpty()) {
                System.err.println(depth);
                System.out.println(depth);

                if (queue1.isEmpty()) {break;}

                queue = queue1;
                queue1 = new PriorityQueue<State>();
            }
            State state = queue.poll();
            List<Integer> chosen = state.chosen;
            int score = state.score;
            depth = state.depth;
            int lastLine = state.lastLine;
            int lastChange = state.lastChange;
            int last2change = state.last2change;
            if (depth == 250) {
                System.err.println(score);
                System.err.println(chosen); // noter le dernier
            } else {
                for (int i = 0 ; i < 10 ; i++) {
                    if (i == lastLine) {
                        List<Integer> nchosen = new ArrayList<>(chosen);
                        nchosen.add(i);
                        queue1.add(new State(score + grid[i*W+depth], depth+1, i, lastChange, last2change, nchosen));
                    } else if (depth-last2change >= 5) {
                        List<Integer> nchosen = new ArrayList<>(chosen);
                        nchosen.add(i);
                        queue1.add(new State(score + grid[i*W+depth], depth+1, i, depth, lastChange, nchosen));
                    }

                   if (queue1.size() > WIDTH) {
                        queue1.poll();
                   }
                }
            }
        }
    }

    public static class State implements Comparable<State>{
        List<Integer> chosen;
        Integer score;
        int depth;
        int lastLine;
        int lastChange;
        int last2change;
        public State(Integer score, int depth, int lastLine, int lastChange, int last2change, List<Integer> chosen) {
            this.lastLine = lastLine;
            this.score = score;
            this.lastChange = lastChange;
            this.last2change = last2change;
            this.depth = depth;
            this.chosen = chosen;
        }

        @Override
        public int compareTo(State o){
            return this.score.compareTo(o.score);
        }
    }

  public static void main(String[] args) throws Exception
  {           
    Scanner in = new Scanner(System.in);

    grid = new int[W*H];
    for (int r=0; r<W*H; r++) {
        var s = in.nextInt();
        grid[r] = s;
    }

    bs();
  }

}
