import java.io.*;
import java.util.*;

public class Collecte {
    private static final List<Character> DIR1 = List.of('v','^','>','<');
    private static final List<Character> DIRB1 = List.of('S','N','E','O');
    private static final List<String> DIR = List.of("v","^",">","<");
    private static final List<String> DIRB = List.of("S","N","E","O");
    private static final List<Integer> getReversed = List.of(2,3,0,1,6,7,4,5);
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
    private static final double t_start = 1d;
    private static final double t_final = 0.00001d;
    private static double T, startTime, MM = 100000000;
    private static List<Boat> initboats;
    private static List<Boat> boats;
    private static List<Boat> cboats;
    private static int[] cgrid;
    private static int[] grid;
    private static int[] cstate;
    private static int[] nbDechetsEnDessous;
    private static int[] nbDechetsEnDessous2Bases;
    private static int[] countersDessous;
    private static int[] acc_countersDessous;
    private static int[] nbDechetsADroite;
    private static int[] nbDechetsADroite2Bases;
    private static int[] countersDroite;
    private static int[] acc_countersDroite;
    private static int[] visited;
    private static int[] takenDessous;
    private static int[] takenDessous2Bases;
    private static int[] takenDroite;
    private static int[] takenDroite2Bases;
    private static int a,b,DD=20,nAvailableMoves,W,H,nRollouts,currScore,M,indexx,nDechets,nBases,score,bestScore;
    private static int HHH=36,WWW=6,HH=45,CC=7,HH1=45,CC1=11,HH2=44,CC2=9,HH3=45,CC3=9,HH4=45,CC4=14,HH5=45,CC5=14,HH6=45,CC6=11,HH7=45,CC7=11,HH8=45,CC8=11,HH9=45,CC9=11,HH10=45,CC10=11,HH11=45,CC11=11,HH12=45,CC12=11,HH13=45,CC13=11,HH14=45,CC14=6,HH15=31,CC15=11,HH16=14,CC16=18;
    private static int[] nbCoords;
    private static final Random random = new Random(5);


    public static boolean noPass2Bases(int y, int x) {
        if (y == 0 && x > 4) return true;
        return false;
    }

    public static boolean noPass(int y, int x) {
        if (y == 0 && x > 4) return true;
        if (List.of(1,2,22,23,24,21).contains(y) && x > 5) return true;
        if (y > 30 && x > 5) return true;

        return false;
    }

  public static void main(String[] args) throws Exception
  {           
    Scanner in = new Scanner(System.in);

    H = in.nextInt();
    startTime = System.currentTimeMillis();
    W = in.nextInt();
    nBases = in.nextInt();
    System.err.println(H);
    System.err.println(W);
    System.err.println(nBases);

    grid = new int[W*H];
    cgrid = new int[W*H];
    nbDechetsEnDessous = new int[W*H];
    nbDechetsEnDessous2Bases = new int[W*H];
    countersDessous = new int[HH2*CC2];
    acc_countersDessous = new int[HH2*CC2];
    nbDechetsADroite = new int[W*H];
    nbDechetsADroite2Bases = new int[W*H];
    countersDroite = new int[HH2*CC2];
    acc_countersDroite = new int[HH2*CC2];
    Map <Integer, List<Integer>> eltsPerCounterDessous = new HashMap<>();
    Map <Integer, List<Integer>> eltsPerCounterDessous2Bases = new HashMap<>();
    Map <Integer, List<Integer>> eltsPerCounterDroite = new HashMap<>();
    Map <Integer, List<Integer>> eltsPerCounterDroite2Bases = new HashMap<>();

    for (int r=0; r<H; r++) {
        var s = in.next().toCharArray();

        for (int c=0; c<W; c++) {

            if (s[c] == 'X') {
                grid[r*W+c] = 1;
                nDechets += 1;
            }
            else
                grid[r*W+c] = 0;
       }
    }



    // 2 bases

    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            for (int u=0; u<HHH; u++) {
                int y=(r+u)%W;
                for (int v=0 ; v < WWW ; v++) {
                    int x=(c+v)%W;

                    if (grid[y*W+x] == 1 && ! noPass2Bases(u,v)) {
                        nbDechetsEnDessous2Bases[r*W+c] += 1;
                    }
                }
            }
       }
    }

    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            for (int u=0; u<WWW; u++) {
                int y=(r+u)%W;
                for (int v=0 ; v < HHH ; v++) {
                    int x=(c+v)%W;
                    if (grid[y*W+x] == 1 && ! noPass2Bases(u,v)) {
                        nbDechetsADroite2Bases[r*W+c] += 1;
                    }
                }
            }
       }
    }

    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            if (!eltsPerCounterDroite2Bases.containsKey(nbDechetsADroite2Bases[r*W+c])) {
                eltsPerCounterDroite2Bases.put(nbDechetsADroite2Bases[r*W+c], new ArrayList<>());
            }
            eltsPerCounterDroite2Bases.get(nbDechetsADroite2Bases[r*W+c]).add(r*W+c);
        }
    }

    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            if (!eltsPerCounterDessous2Bases.containsKey(nbDechetsEnDessous2Bases[r*W+c])) {
                eltsPerCounterDessous2Bases.put(nbDechetsEnDessous2Bases[r*W+c], new ArrayList<>());
            }
            eltsPerCounterDessous2Bases.get(nbDechetsEnDessous2Bases[r*W+c]).add(r*W+c);
        }
    }

    // 3 bases

    int moyDessous = 0;
    int sumDessous = 0;

    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            for (int u=0; u<HH2; u++) {
                int y=(r+u)%W;
                for (int v=0 ; v < CC2 ; v++) {
                    int x=(c+v)%W;

                    if (grid[y*W+x] == 1 && ! noPass(u,v)) {
                        nbDechetsEnDessous[r*W+c] += 1;
                    }
                }
            }
            countersDessous[nbDechetsEnDessous[r*W+c]] += 1;
            moyDessous += nbDechetsEnDessous[r*W+c];
            sumDessous += 1;

       }
    }

    moyDessous /= sumDessous;
    int moyDroite = 0;
    int sumDroite = 0;
    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            for (int u=0; u<CC2; u++) {
                int y=(r+u)%W;
                for (int v=0 ; v < HH2 ; v++) {
                    int x=(c+v)%W;
                    if (grid[y*W+x] == 1 && ! noPass(u,v)) {
                        nbDechetsADroite[r*W+c] += 1;
                    }
                }
            }
            countersDroite[nbDechetsADroite[r*W+c]] += 1;
            moyDroite += nbDechetsADroite[r*W+c];
            sumDroite += 1;
       }
    }

    moyDroite /= sumDroite;

    acc_countersDessous[0] = countersDessous[0];
    acc_countersDroite[0] = countersDroite[0];

    for (int r=1; r<HH2*CC2; r++) {
        acc_countersDessous[r] = countersDessous[r] + acc_countersDessous[r-1];
        acc_countersDroite[r] = countersDroite[r] + acc_countersDroite[r-1];
    }

    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            if (!eltsPerCounterDroite.containsKey(nbDechetsADroite[r*W+c])) {
                eltsPerCounterDroite.put(nbDechetsADroite[r*W+c], new ArrayList<>());
            }
            eltsPerCounterDroite.get(nbDechetsADroite[r*W+c]).add(r*W+c);
        }
    }

    for (int r=0; r<H; r++) {
        for (int c=0; c<W; c++) {
            if (!eltsPerCounterDessous.containsKey(nbDechetsEnDessous[r*W+c])) {
                eltsPerCounterDessous.put(nbDechetsEnDessous[r*W+c], new ArrayList<>());
            }
            eltsPerCounterDessous.get(nbDechetsEnDessous[r*W+c]).add(r*W+c);
        }
    }

    int maxDroite = acc_countersDroite[HH2*CC2-1];
    int maxDessous = acc_countersDessous[HH2*CC2-1];

    int sqr = (int)(Math.ceil(Math.sqrt(nBases)));
    int longueur = (int)(Math.ceil(W/sqr));

    int[][] template2Bases = new int[HHH][WWW];
    int[][] templateTemp = new int[HH2][CC2];

    String fileName2 = "data/template_3_bases_new2.txt";//45 11
    String fileNameM2 = "data/template_2_bases_new.txt";

    try {
        BufferedReader reader = new BufferedReader(new FileReader(fileName2));
        String line;

        int rowIndex = 0;

        while ((line = reader.readLine()) != null) {
            for (int colIndex = 0; colIndex < line.length(); colIndex++) {
                if (DIR1.contains(line.charAt(colIndex)))
                    templateTemp[rowIndex][colIndex] = DIR1.indexOf(line.charAt(colIndex));
                else
                    templateTemp[rowIndex][colIndex] = 4+DIRB1.indexOf(line.charAt(colIndex));
            }
            rowIndex++;
        }
        reader.close();


        reader = new BufferedReader(new FileReader(fileNameM2));

        rowIndex = 0;
        while ((line = reader.readLine()) != null) {
            for (int colIndex = 0; colIndex < line.length(); colIndex++) {
                if (DIR1.contains(line.charAt(colIndex)))
                    template2Bases[rowIndex][colIndex] = DIR1.indexOf(line.charAt(colIndex));
                else
                    template2Bases[rowIndex][colIndex] = 4+DIRB1.indexOf(line.charAt(colIndex));
            }
            rowIndex++;
        }
        reader.close();

    } catch (IOException e) {
        System.err.println("Erreur lors de la lecture du fichier : " + e.getMessage());
    }
    int ccc = 2;
    while (System.currentTimeMillis() - startTime < MM){

        cstate = new int[W*H];
        visited = new int[W*H];
        takenDessous = new int[W*H];
        takenDessous2Bases = new int[W*H];
        takenDroite = new int[W*H];
        takenDroite2Bases = new int[W*H];

         for (int r=0; r<H; r++)
           for (int c=0; c<W; c++)
             cgrid[r*W+c]=grid[r*W+c];

        boats = new ArrayList<>();

        int ii = 0, tempHH = HH2, tempCC = CC2;

        while (nBases - ii == 3 || nBases - ii > 4) {

            int reversedDabord = random.nextInt(2);
            int reversed = reversedDabord;

            int indexI = random.nextInt(H);
            int indexJ = random.nextInt(W);

            for (int nDechets=HH2*CC2-1; nDechets>-1; nDechets--) {

                if (reversedDabord == 0) {
                    if (eltsPerCounterDessous.containsKey(nDechets)) {
                        var lst = eltsPerCounterDessous.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDessous[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDessous[lst.get(eltChosen)] == 0) {
                            takenDessous[lst.get(eltChosen)] = 1;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                    if (eltsPerCounterDroite.containsKey(nDechets)) {
                        var lst = eltsPerCounterDroite.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDroite[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDroite[lst.get(eltChosen)] == 0) {
                            takenDroite[lst.get(eltChosen)] = 1;
                            reversed = 1;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                } else {
                    if (eltsPerCounterDroite.containsKey(nDechets)) {
                        var lst = eltsPerCounterDroite.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDroite[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDroite[lst.get(eltChosen)] == 0) {
                            takenDroite[lst.get(eltChosen)] = 1;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                    if (eltsPerCounterDessous.containsKey(nDechets)) {
                        var lst = eltsPerCounterDessous.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDessous[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDessous[lst.get(eltChosen)] == 0) {
                            takenDessous[lst.get(eltChosen)] = 1;
                            reversed = 0;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                }


            }

            boolean found = false;
            int newArrowsAmount = 0,newArrowsAmount2 = 0,newArrowsAmount3 = 0;

            int aaa = random.nextInt(3);
            if (aaa==0) newArrowsAmount = random.nextInt(7);
            if (aaa==1) newArrowsAmount2 = random.nextInt(7);
            if (aaa==2) newArrowsAmount3 = random.nextInt(7);

            var ctrD = 0;
            var nbD = 0;

            for (int r=0; r<tempHH; r++) {
                int limit = tempCC;
                if (List.of(4,5,6,7,8,3).contains(r))
                    limit += newArrowsAmount;

                if (List.of(9,10,11,12,13,14).contains(r))
                    limit += newArrowsAmount2;

                if (List.of(15,16,17,18,19,20).contains(r))
                    limit += newArrowsAmount3;

                for (int c=0; c<limit; c++) {
                    int y = (indexI+r)%W;
                    int x = (indexJ+c)%W;
                     if (reversed == 0 && visited[y*W+x] == 1) {
                        found = true;
                        break;
                     }
                    if (reversed == 1 && visited[x*W+y] == 1) {
                        found = true;
                        break;
                     }
                }
                if (found) break;

               int nra = -1;

                if (List.of(4,5,3).contains(r))
                    nra = newArrowsAmount;

                if (List.of(9,10,11).contains(r))
                    nra = newArrowsAmount2;

                if (List.of(15,16,17).contains(r))
                    nra = newArrowsAmount3;

                if (nra > 0) {
                     for (int c=5; c<5+nra; c++) {
                        int y = (indexI+r)%W;
                        int x = (indexJ+c)%W;
                        if (reversed == 1) {
                            x = (indexI+r)%W;
                            y = (indexJ+c)%W;
                        }
                         if (grid[y*W+x] == 1)
                            ctrD += 1;
                         nbD += 1;
                    }
                }

                nra = -1;

                if (List.of(6,7,8).contains(r))
                    nra = newArrowsAmount;

                if (List.of(12,13,14).contains(r))
                    nra = newArrowsAmount2;

                if (List.of(18,19,20).contains(r))
                    nra = newArrowsAmount3;

                if (nra > 0) {
                     for (int c=6; c<6+nra; c++) {
                        int y = (indexI+r)%W;
                        int x = (indexJ+c)%W;
                        if (reversed == 1) {
                            x = (indexI+r)%W;
                            y = (indexJ+c)%W;
                        }
                         if (grid[y*W+x] == 1)
                            ctrD += 1;
                         nbD += 1;
                    }
                }
            }

            if (ctrD*W*H <= 2*nDechets*nbD) {
                newArrowsAmount = 0;
                newArrowsAmount2 = 0;
                newArrowsAmount3 = 0;
            }

            if (found) continue;

            for (int r=0; r<tempHH; r++) {

                int vv = 6;

                if (List.of(3,4,5,9,10,11,15,16,17,29,27,28).contains(r)) {
                    vv = 5;
                }

                for (int c=0; c<vv; c++) {

                    int y = (indexI+r)%W;
                    int x = (indexJ+c)%W;
                    int value = templateTemp[r][c];
                    if (reversed == 1) {
                        x = (indexI+r)%W;
                        y = (indexJ+c)%W;
                        value = getReversed.get(templateTemp[r][c]);
                    }
                     cstate[y*W+x]=value;
                     visited[y*W+x]=1;
                     if (value > 3) {
                        Boat boat = new Boat(y,x,value-4);
                        boats.add(boat);
                     }
                }

                int limit = 0;
                if (List.of(4,5,6,7,8,3).contains(r))
                    limit = newArrowsAmount;

                if (List.of(9,10,11,12,13,14).contains(r))
                    limit = newArrowsAmount2;

                if (List.of(15,16,17,18,19,20).contains(r))
                    limit = newArrowsAmount3;

                for (int c=vv+limit; c<tempCC+limit; c++) {
                    int y = (indexI+r)%W;
                    int x = (indexJ+c)%W;
                    int value = templateTemp[r][c-limit];
                    if (reversed == 1) {
                        x = (indexI+r)%W;
                        y = (indexJ+c)%W;
                        value = getReversed.get(templateTemp[r][c-limit]);
                    }
                     cstate[y*W+x]=value;
                     visited[y*W+x]=1;
                     if (value > 3) {
                        Boat boat = new Boat(y,x,value-4);//porte 0
                        boats.add(boat);
                     }
                }

                int nra = -1;

                if (List.of(4,5,3).contains(r))
                    nra = newArrowsAmount;

                if (List.of(9,10,11).contains(r))
                    nra = newArrowsAmount2;

                if (List.of(15,16,17).contains(r))
                    nra = newArrowsAmount3;

                if (nra  > 0) {
                     for (int c=5; c<5+nra; c++) {
                        int y = (indexI+r)%W;
                        int x = (indexJ+c)%W;
                        int value = 2;
                        if (reversed == 1) {
                            x = (indexI+r)%W;
                            y = (indexJ+c)%W;
                            value = getReversed.get(value);
                        }
                         cstate[y*W+x]=value;
                         visited[y*W+x]=1;
                         //nDechets - W*H
                         if (grid[y*W+x] == 1)
                            ctrD += 1;
                         nbD += 1;
                    }
                }

                nra = -1;

                if (List.of(6,7,8).contains(r))
                    nra = newArrowsAmount;

                if (List.of(12,13,14).contains(r))
                    nra = newArrowsAmount2;

                if (List.of(18,19,20).contains(r))
                    nra = newArrowsAmount3;

                if (nra > 0) {
                     for (int c=6; c<6+nra; c++) {
                        int y = (indexI+r)%W;
                        int x = (indexJ+c)%W;
                        int value = 3;
                        if (reversed == 1) {
                            x = (indexI+r)%W;
                            y = (indexJ+c)%W;
                            value = getReversed.get(value);
                        }
                         cstate[y*W+x]=value;
                         visited[y*W+x]=1;
                         if (grid[y*W+x] == 1)
                            ctrD += 1;
                         nbD += 1;
                    }
                }
            }

            ii += 3;
        }
        while (nBases - ii > 1) {
            boolean found = false;

            int reversedDabord = random.nextInt(2);
            int reversed = reversedDabord;

            int indexI = random.nextInt(H);
            int indexJ = random.nextInt(H);

            for (int nDechets=HHH*WWW-1; nDechets>-1; nDechets--) {

                if (reversedDabord == 0) {
                    if (eltsPerCounterDessous2Bases.containsKey(nDechets)) {
                        var lst = eltsPerCounterDessous2Bases.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDessous2Bases[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDessous2Bases[lst.get(eltChosen)] == 0) {
                            takenDessous2Bases[lst.get(eltChosen)] = 1;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                    if (eltsPerCounterDroite2Bases.containsKey(nDechets)) {
                        var lst = eltsPerCounterDroite2Bases.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDroite2Bases[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDroite2Bases[lst.get(eltChosen)] == 0) {
                            takenDroite2Bases[lst.get(eltChosen)] = 1;
                            reversed = 1;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                } else {
                    if (eltsPerCounterDroite2Bases.containsKey(nDechets)) {
                        var lst = eltsPerCounterDroite2Bases.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDroite2Bases[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDroite2Bases[lst.get(eltChosen)] == 0) {
                            takenDroite2Bases[lst.get(eltChosen)] = 1;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                    if (eltsPerCounterDessous2Bases.containsKey(nDechets)) {
                        var lst = eltsPerCounterDessous2Bases.get(nDechets);
                        int eltChosen = random.nextInt(lst.size());
                        int counterr = 0;
                        while (takenDessous2Bases[lst.get(eltChosen)] == 1 && counterr < 100) {
                            eltChosen = random.nextInt(lst.size());
                            counterr += 1;
                        }
                        if (takenDessous2Bases[lst.get(eltChosen)] == 0) {
                            takenDessous2Bases[lst.get(eltChosen)] = 1;
                            reversed = 0;
                            indexI = lst.get(eltChosen) / W;
                            indexJ = lst.get(eltChosen) % W;
                            break;
                        }
                    }
                }
            }

            for (int r=0; r<HHH; r++) {
                for (int c=0; c<WWW; c++) {
                    int y = (indexI+r)%W;
                    int x = (indexJ+c)%W;

                     if (reversed == 0 && visited[y*W+x] == 1) {
                        found = true;
                        break;
                     }
                    if (reversed == 1 && visited[x*W+y] == 1) {
                        found = true;
                        break;
                     }
                }
                if (found) break;
            }

            if (found) continue;

            for (int r=0; r<HHH; r++) {
                for (int c=0; c<WWW; c++) {

                    int y = (indexI+r)%W;
                    int x = (indexJ+c)%W;
                    int value = template2Bases[r][c];
                    if (reversed == 1) {
                        x = (indexI+r)%W;
                        y = (indexJ+c)%W;
                        value = getReversed.get(template2Bases[r][c]);
                    }
                     cstate[y*W+x]=value;
                     visited[y*W+x]=1;
                     if (value > 3) {
                        Boat boat = new Boat(y,x,value-4);
                        boats.add(boat);
                     }
                }
            }
            ii += 2;
        }

        nRollouts += 1;
        currScore = 0;

        for (int turn = 0 ; turn < 1000 ; turn++) {
            nbCoords = new int[W*H];
            for (int i = 0 ; i < nBases ; i++) {
                Boat boat = boats.get(i);
                int y = boat.y;
                int x = boat.x;
                int coord = y*W+x;
                nbCoords[coord] += 1;
            }
            for (int i = 0 ; i < nBases ; i++) {
                Boat boat = boats.get(i);
                int y = boat.y;
                int x = boat.x;
                int coord = y*W+x;
                int dir = cstate[coord];

                if (nbCoords[coord] > 1) {
                    dir = boat.dir;
                } else if (boat.dechets < 2 && cgrid[coord] == 1) {
                    cgrid[coord] = 0;
                    boat.dechets += 1;
                }
                if (cstate[coord] > 3) {
                    dir = boat.dir;
                    currScore += boat.dechets;
                    boat.dechets = 0;
                }
                boat.y = Math.floorMod(y+DIRS[dir][0],H);
                boat.x = Math.floorMod(x+DIRS[dir][1],W);
            }
        }

        if (bestScore < currScore) {
            bestScore = currScore;
            System.err.println("score "+currScore);
            System.out.println("score "+currScore);
            System.err.println("nRolloutG "+nRollouts);
            System.out.println("nRolloutG "+nRollouts);
            var e = System.currentTimeMillis() - startTime;
            System.err.println("time "+e);
            System.out.println("time "+e);

            for (int i=0; i<H; i++) {
                for (int j=0; j<W; j++) {
                var coord = i*W+j;
                    if (cstate[coord] > 3) {
                        System.out.print(DIRB.get(cstate[coord]-4));
                    } else {
                        System.out.print(DIR.get(cstate[coord]));
                    }
                }
                System.out.println();
            }
        }
    }
  }

  static class Boat {
    int x;
    int y;
    int dir;
    int dechets;

    public Boat(int y, int x, int dir) {
        this.x = x;
        this.y = y;
        this.dir = dir;
    }
  }
}
