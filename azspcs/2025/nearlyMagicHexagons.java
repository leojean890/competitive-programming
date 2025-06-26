import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class mainv13finalcleaned {
    private static final double t_start = 10d;
    private static final double t_final = 0.1d;
    private static double T, T1;

    public static void main(String[] args) {
        Map<Integer, Map<Double, Integer>> target = new HashMap<>();
        Map<Integer, Set<Integer>> linesPerIndex = new HashMap<>();

        T1 = Double.parseDouble(args[1]);

        int N = Integer.parseInt(args[0]);
        int nelts = Integer.parseInt(args[2]);
        int scoreToBeat = Integer.parseInt(args[3]);
        Scanner scanner = new Scanner(System.in);
        String[] currentBest = scanner.nextLine().split("\\),\\(");

        System.out.println(N);
        System.out.println(T1);
        System.out.println(nelts);
        System.out.flush();
        var startTime = System.currentTimeMillis();
        int middle = N - 1;
        int MM = 2 * N - 1;
        int cellCount = 3*N*(N-1) + 1;
        int rowsPerAxis = 2*N - 1;
        int cellSum = cellCount*(cellCount+1)/2;
        int MAX = cellCount-1;
        Random random = new Random(1);
        int currentSize = N;
        int counter = 0;
        int counter1 = 0;
        List<List<Integer>> toBeComputed = new ArrayList<>();

        for (int i = 0; i < N; i++) {
            target.put(i, new HashMap<>());
            target.put(MM - 1 - i, new HashMap<>());

            double start = Math.abs(middle - i) / 2.0;

            for (int j = 0; j < currentSize; j++) {
                counter++;
                if (i != N - 1) {
                    target.get(i).put(start + j, counter);
                }
                target.get(MM - 1 - i).put(start + currentSize - 1 - j, MAX - counter1 + 1);
                counter1++;
            }
            if (i != N - 1) {
                toBeComputed.add(target.get(i).values().stream().map(a -> a-1).toList());
            }
            toBeComputed.add(target.get(MM - 1 - i).values().stream().map(a -> a-1).toList());
            currentSize += 1;

        }

        for (double key : target.get(0).keySet()) {
            List<Integer> currentLine = new ArrayList<>();
            double delta = 0.5, x = key;
            int y = 0;

            while (target.containsKey(y) && target.get(y).containsKey(x)) {
                currentLine.add(target.get(y).get(x)-1);
                y+=1;
                x+=delta;
            }

            toBeComputed.add(currentLine);

            currentLine = new ArrayList<>();
            delta = -0.5;
            x = key;
            y = 0;

            while (target.containsKey(y) && target.get(y).containsKey(x)) {
                currentLine.add(target.get(y).get(x)-1);
                y+=1;
                x+=delta;
            }

            toBeComputed.add(currentLine);
        }

        for (int yInit = 1 ; yInit < N ; yInit++) {
            double xInit = target.get(yInit).keySet().stream().min(Double::compareTo).orElseThrow();

            List<Integer> currentLine = new ArrayList<>();
            double delta = 0.5, x = xInit;
            int y = yInit;

            while (target.containsKey(y) && target.get(y).containsKey(x)) {
                currentLine.add(target.get(y).get(x)-1);
                y+=1;
                x+=delta;
            }
            toBeComputed.add(currentLine);

            xInit = target.get(yInit).keySet().stream().max(Double::compareTo).orElseThrow();

            currentLine = new ArrayList<>();
            delta = -0.5;
            x = xInit;
            y = yInit;

            while (target.containsKey(y) && target.get(y).containsKey(x)) {
                currentLine.add(target.get(y).get(x)-1);
                y+=1;
                x+=delta;
            }
            toBeComputed.add(currentLine);
        }

        int[] currentState = new int[MAX+1];

        for (int i = 0; i < MM; i++) {

            String[] current = currentBest[i].split(",");

            int j = 0;

            for (double key : target.get(i).keySet().stream().sorted().toList()) {

                currentState[target.get(i).get(key) - 1] = Integer.parseInt(current[j]);
                j++;
            }
        }

        double score = 0;
        double[] scoresPerIndex = new double[toBeComputed.size()];
        int ii = 0;

        for (List<Integer> elts : toBeComputed) {
            int value = elts.stream().mapToInt(i -> currentState[i]).sum();

            long temp = (long) value * rowsPerAxis - cellSum; 
            double term = ((double) temp * temp) / rowsPerAxis;

            score += term;
            scoresPerIndex[ii] = term;
            for (Integer elt : elts) {
                if (!linesPerIndex.containsKey(elt))
                    linesPerIndex.put(elt, new HashSet<>());
                linesPerIndex.get(elt).add(ii);
            }

            ii += 1;
        }

        double currentScore = score / 2;
        double bestScore = score / 2;

        System.out.println(currentScore);

        for (int i = 0; i < MM; i++) {

            System.out.print("(");

            int j = 0;

            for (double key : target.get(i).keySet().stream().sorted().toList()) {
                System.out.print(currentState[target.get(i).get(key) - 1]);

                if (j < target.get(i).size() - 1)
                    System.out.print(",");

                j++;
            }
            System.out.print("),");
        }

        System.out.print("\n");
        System.out.flush();
        
        var elapsed = System.currentTimeMillis() - startTime;

        while (elapsed < T1 && bestScore > scoreToBeat) {
            int i1 = random.nextInt(MAX+1);
            int i2 = random.nextInt(MAX+1);
            
            score = currentScore*2;
            
            Set<Integer> union = Stream.concat(linesPerIndex.get(i1).stream(), linesPerIndex.get(i2).stream()).collect(Collectors.toSet());

            for (Integer elt : union) {
                score -= scoresPerIndex[elt];
            }
            
            int temp1 = currentState[i1];

            currentState[i1] = currentState[i2];
            currentState[i2] = temp1;

            Map<Integer,Double> tempScoresPerIndex = new HashMap<>();

            for (Integer elt : union) {
                List<Integer> elts = toBeComputed.get(elt);
                int value = elts.stream().mapToInt(i -> currentState[i]).sum();
                long temp = (long) value * rowsPerAxis - cellSum;
                double term = ((double) temp * temp) / rowsPerAxis;
                tempScoresPerIndex.put(elt,term);

                score += term;
            }

            score = score / 2;

            if (currentScore > score) {
                currentScore = score;

                for (int elt : tempScoresPerIndex.keySet())
                    scoresPerIndex[elt] = tempScoresPerIndex.get(elt);

                if (currentScore < bestScore) {
                    bestScore = currentScore;
                    if (currentScore < nelts) {
                        System.out.println(currentScore);

                        for (int i = 0; i < MM; i++) {

                            System.out.print("(");

                            int j = 0;

                            for (double key : target.get(i).keySet().stream().sorted().toList()) {
                                System.out.print(currentState[target.get(i).get(key) - 1]);

                                if (j < target.get(i).size() - 1)
                                    System.out.print(",");

                                j++;
                            }
                            System.out.print("),");
                        }

                        System.out.print("\n");
                        System.out.flush();
                    }
                }
            } else {
                double rr = random.nextDouble();

                T = t_start*Math.pow(t_final/t_start, elapsed/T1);

                if (Math.exp((currentScore - (score))/T) > rr){
                    currentScore = score;
                    for (int elt : tempScoresPerIndex.keySet())
                        scoresPerIndex[elt] = tempScoresPerIndex.get(elt);

                } else {
                    currentState[i2] = currentState[i1];
                    currentState[i1] = temp1;
                }
            }
            elapsed = System.currentTimeMillis() - startTime;
        }

        System.out.println(bestScore);
        System.out.println(Arrays.toString(currentState));
        System.out.flush();
    }
}

