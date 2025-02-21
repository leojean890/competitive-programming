import java.util.*;
import java.io.*;

public class RadarCoverage {

    static final int HEIGHT = 2_000_000_000;
    static final int MAX_DIST = 5_500_000;
    static List<int[]> centers = new ArrayList<>();
    static Map<int[], List<int[]>> neighbors = new HashMap<>();

    public static void main(String[] args) {
        try (BufferedReader br = new BufferedReader(new InputStreamReader(System.in))) {
            String line;
            var startTime = System.currentTimeMillis();

            while ((line = br.readLine()) != null) {
                String[] parts = line.split(" ");
                int x = Integer.parseInt(parts[0]);
                int y = Integer.parseInt(parts[1]);
                centers.add(new int[]{x, y});
            }

            for (int i = 0; i < centers.size() - 1; i++) {
                var t = System.currentTimeMillis() - startTime;
                if (i%10000 == 0)
                    System.out.println(i + " " + centers.size() + " " + t);
                int[] p1 = centers.get(i);
                for (int j = i + 1; j < centers.size(); j++) {
                    int[] p2 = centers.get(j);
                    double d = distance(p1, p2);
                    if (d < MAX_DIST) {
                        if (! neighbors.containsKey(p1))
                            neighbors.put(p1, new ArrayList<>());
                        neighbors.get(p1).add(p2);
                        if (! neighbors.containsKey(p2))
                            neighbors.put(p2, new ArrayList<>());
                        neighbors.get(p2).add(p1);
                    }
                }
            }

            System.out.println(findMinRadius());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static double distance(int[] p1, int[] p2) {
        return Math.sqrt(Math.pow(p1[0] - p2[0], 2) + Math.pow(p1[1] - p2[1], 2));
    }

    private static boolean canCoverAll(int radius) {
        Deque<int[]> queue = new ArrayDeque<>();
        Set<int[]> visited = new HashSet<>();

        for (int[] center : centers) {
            if (center[1] <= radius && neighbors.containsKey(center)) {
                queue.addLast(center);
                visited.add(center);
            }
        }

        while (!queue.isEmpty()) {
            int[] point = queue.pollLast();

            for (int[] neighborKey : neighbors.get(point)) {
                double dist = distance(point, neighborKey);

                if (!visited.contains(neighborKey) && dist <= 2*radius) {
                    int nx = neighborKey[0];
                    int ny = neighborKey[1];

                    if (neighbors.containsKey(point))
                        queue.addLast(neighborKey);
                    visited.add(neighborKey);

                    if (ny + radius >= HEIGHT) {
                        return true;
                    }
                }
            }
        }

        return false;
    }

    private static int findMinRadius() {
        int low = 0, high = MAX_DIST, result = high;

        while (low <= high) {
            int mid = (low + high) / 2;
            System.out.println(low + " " + mid + " " + high);
            if (canCoverAll(mid)) {
                result = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

        return result;//2190669
    }
}
