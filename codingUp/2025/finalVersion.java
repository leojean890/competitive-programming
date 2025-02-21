import java.io.*;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.annotation.JsonValue;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.List;

public class CodingUp {

    private static final Random random = new Random(1);
    private static double T, startTime, currScore, bestScore;
    private static Params params;
    private static int nRollouts;
    private static List<String> bestMoves = new ArrayList<>();
    private static List<List<Integer>> seedsNeighbors = new ArrayList<>();
    private static List<Integer> curr_plantsOrder = new ArrayList<>();
    private static List<Integer> curr_plantsNeighOrder = new ArrayList<>();
    private static List<Integer> curr_seedsOrder = new ArrayList<>();

  public static void main(String[] args) throws Exception
  {
        String jsonString = "data\\1_exemple.json";
        jsonString = "data\\3_hydroponique.json";
        jsonString = "data\\1_exemple.json";
        jsonString = "data\\4_clusters.json";
        jsonString = "data\\2_champ.json";
        jsonString = "data\\5_maxiculture.json";
        int indexxx = 0;

        String outt = "seed5.json";
        startTime = System.currentTimeMillis();

        ObjectMapper objectMapper = new ObjectMapper();
        try {
            params = objectMapper.readValue(new File(jsonString), Params.class);
            System.out.println("seedCapacity: " + params.seedCapacity);
            System.out.println("maxDistance: " + params.maxDistance);
            System.out.println("range: " + params.range);

            seedsNeighbors.add(List.of(0,0));

            for (int dy = -params.range ; dy < params.range + 1; dy++) {
                int dx = params.range - Math.abs(dy);
                seedsNeighbors.add(List.of(dy,-dx));
                if (dx > 0)
                seedsNeighbors.add(List.of(dy,dx));
            }

            for (int i = 0 ; i < params.plants.size(); i++) {
                curr_plantsNeighOrder.add(0);
            }

            int distance = 0;
            int nSeeds = 0,x = 0,y = 0, currPlantIndex = 0, currSeedIndex = 0, turn = 0;

            List<String> moves = new ArrayList<>();
            int[] takenPlants = new int[params.plants.size()];
            int[] takenSeeds = new int[params.seeds.size()];

            while (distance < params.maxDistance && currPlantIndex < params.plants.size()) {

                int bestDist = 2100000000;
                int best = 1000000000;
                int best2 = 3;

                if (nSeeds > 0) {
                    for (int i = 0 ; i < params.plants.size(); i++) {
                        if (takenPlants[i] == 0) {
                            List<Integer> position = params.plants.get(i);
                            int nextX = position.get(0);
                            int nextY = position.get(1);
                            int d = Math.abs(x-nextX) + Math.abs(y-nextY);
                            if (d < bestDist) {bestDist = d; best = i; best2 = 0;};
                        }
                    }
                }

               if (nSeeds == 0){
                   for (int i = 0 ; i < params.seeds.size(); i++) {
                        if (takenSeeds[i] == 0) {
                            List<Integer> position = params.seeds.get(i);
                            int nextX = position.get(0);
                            int nextY = position.get(1);
                            int d = Math.abs(x-nextX) + Math.abs(y-nextY);
                            if (d < bestDist) {bestDist = d; best = i; best2 = 1;};
                        }
                    }
                }
                if (best2 == 3 || distance + bestDist > params.maxDistance) break;
                if (best2 == 0) {
                        List<Integer> position = params.plants.get(best);

                    takenPlants[best] = 1;
                    if (bestDist > params.range) {
                            int nextX = position.get(0);
                            int nextY = position.get(1);
                         for (int i = 0 ; i < seedsNeighbors.size() ; i++) {
                            int candidateX = position.get(0) + seedsNeighbors.get(i).get(0);
                            int candidateY = position.get(1) + seedsNeighbors.get(i).get(1);
                            int d = Math.abs(x-candidateX) + Math.abs(y-candidateY);
                            if (d < bestDist) {
                                bestDist = d;
                                nextX = candidateX;
                                nextY = candidateY;

                            }
                         }

                        distance += bestDist;

                       x = nextX;
                       y = nextY;
                        moves.add("MOVE " + nextX + " " + nextY);
                    }

                    nSeeds -= 1;
                    bestScore += 1;
                    moves.add("PLANT " + position.get(0) + " " + position.get(1));
                    curr_plantsOrder.add(best);

                } else {
                    List<Integer> position = params.seeds.get(best);
                    int nextX = position.get(0);
                    int nextY = position.get(1);
                    distance += bestDist;
                    takenSeeds[best] = 1;
                    x = nextX;
                    y = nextY;
                    nSeeds = params.seedCapacity;
                     moves.add("MOVE " + nextX + " " + nextY);
                    moves.add("COLLECT");
                       curr_seedsOrder.add(best);
                }
            }

            for (int i = 0 ; i < params.plants.size(); i++) {
                if (takenPlants[i] == 0)
                    curr_plantsOrder.add(i);
            }

            for (int i = 0 ; i < params.seeds.size(); i++) {
                if (takenSeeds[i] == 0)
                    curr_seedsOrder.add(i);
            }
            if (bestScore == (double)params.plants.size()) {bestScore *= (double)params.maxDistance/(double)distance;}

            System.out.println("bestScore: " + bestScore);
            currScore = bestScore;
            bestMoves = moves;


            var elapsed = System.currentTimeMillis() - startTime;
            var TT = 36000000;//5h;  180 5h - 216 6h - 252 7h - 360 10h,

            while (elapsed < TT) {
                 nRollouts++;

                distance = 0; double score=0.0d;
                nSeeds = 0;x = 0;y = 0; currPlantIndex = 0; currSeedIndex = 0; turn = 0;
                List<Integer> potentielsX = List.of(0);
                List<Integer> potentielsY = List.of(0);

                moves = new ArrayList<>();
                takenPlants = new int[params.plants.size()];
                takenSeeds = new int[params.seeds.size()];
                int mmm = 20;//40 serait mieux ?
                int mmm3 = 40;//40 serait mieux ?

                int seuil = mmm + (int) ( (300 - mmm) * (1 - Math.cos(2*Math.PI * elapsed*30/1000))) ;
                int seuil3 = mmm3 + (int) ( (1000 - mmm3) * (1 - Math.cos(2*Math.PI * elapsed*30/1000))) ;
                //int seuil = mmm + (int) ( (1000 - mmm) * (1 - Math.cos(2*Math.PI * elapsed*30/1000))) ;
                //int seuil2 = 1 + (int) ((params.seedCapacity - 1) * (1 - Math.cos(2*Math.PI * elapsed*45/1000))) ;
                int seuil2 = 1 + (int) ((params.seedCapacity - 2) * (1 - Math.cos(2*Math.PI * elapsed*45/1000))) ;
                while (distance < params.maxDistance && currPlantIndex < params.plants.size()) {

                    int bestDist = 2100000000;
                    int secondBestDist = 2100000000;
                    int thirdBestDist = 2100000000;
                    int best = 1000000000;
                    int secondBest = 1000000000;
                    int thirdBest = 1000000000;
                    int best2 = 3;
                    int secondBest2 = 3;
                    int thirdBest2 = 3;
                    int bestIndice = 0;
                    int secondBestIndice = 0;
                    int thirdBestIndice = 0;

                    for (int indice = 0 ; indice < potentielsX.size() ; indice++) {
                        x = potentielsX.get(indice);
                        y = potentielsY.get(indice);
                        if (x==y&&x==2100000000)continue;

                        if (nSeeds > 0) {
                            for (int i = 0 ; i < params.plants.size(); i++) {
                                if (takenPlants[i] == 0) {
                                    List<Integer> position = params.plants.get(i);
                                    int nextX = position.get(0);
                                    int nextY = position.get(1);
                                    int d = Math.abs(x-nextX) + Math.abs(y-nextY);
                                    if (d < bestDist) {thirdBestIndice=secondBestIndice;secondBestIndice=bestIndice;bestIndice = indice;thirdBest2 = secondBest2;secondBest2 = best2;best2 = 0;thirdBestDist=secondBestDist;secondBestDist=bestDist;bestDist = d;thirdBest=secondBest;secondBest=best;best = i; }
                                    else if (d < secondBestDist) {thirdBestIndice=secondBestIndice;secondBestIndice=indice; thirdBestDist=secondBestDist;secondBestDist = d; thirdBest=secondBest;secondBest = i;thirdBest2 = secondBest2;secondBest2 = 0;}
                                    else if (d < thirdBestDist) {thirdBestIndice=secondBestIndice; thirdBestDist=secondBestDist; thirdBest = i;thirdBest2 = 0;};
                                }
                            }
                        }

                        int seuil2ToChose = 1+random.nextInt(seuil2);

                       if (nSeeds < seuil2ToChose) {
                           for (int i = 0 ; i < params.seeds.size(); i++) {
                                if (takenSeeds[i] == 0) {
                                    List<Integer> position = params.seeds.get(i);
                                    int nextX = position.get(0);
                                    int nextY = position.get(1);
                                    int d = Math.abs(x-nextX) + Math.abs(y-nextY);

                                    if (d < bestDist) {thirdBestIndice=secondBestIndice;secondBestIndice=bestIndice;bestIndice = indice;thirdBest2 = secondBest2;secondBest2 = best2;best2 = 1;thirdBestDist=secondBestDist;secondBestDist=bestDist;bestDist = d;thirdBest=secondBest;secondBest=best;best = i; }
                                    else if (d < secondBestDist) {thirdBestIndice=secondBestIndice;secondBestIndice=indice; thirdBestDist=secondBestDist;secondBestDist = d; thirdBest=secondBest;secondBest = i;thirdBest2 = secondBest2;secondBest2 = 1;}
                                    else if (d < thirdBestDist) {thirdBestIndice=secondBestIndice; thirdBestDist=secondBestDist; thirdBest = i;thirdBest2 = 1;};
                                }
                            }
                        }
                    }
                    if (best2 == 3 || distance + bestDist > params.maxDistance) break;
                    int bst = best;

                    if(random.nextInt(seuil3) == 1) bst = thirdBest;
                    else if(random.nextInt(seuil) == 1) bst = secondBest;

                    if (bst == 1000000000)bst=best;
                    if (bst == secondBest) best2 = secondBest2;
                    else if (bst == thirdBest) best2 = thirdBest2;

                    if (bst == best) {
                        x = potentielsX.get(bestIndice);
                        y = potentielsY.get(bestIndice);

                        if (potentielsX.size() > 1) {
                            moves.add(moves.size()-1,"MOVE " + x + " " + y);
                        }

                        potentielsX = List.of(x);
                        potentielsY = List.of(y);
                    } else if (bst == secondBest) {
                        x = potentielsX.get(secondBestIndice);
                        y = potentielsY.get(secondBestIndice);

                        if (potentielsX.size() > 1) {
                            moves.add(moves.size()-1,"MOVE " + x + " " + y);
                        }

                        potentielsX = List.of(x);
                        potentielsY = List.of(y);
                    } else {
                        x = potentielsX.get(thirdBestIndice);
                        y = potentielsY.get(thirdBestIndice);

                        if (potentielsX.size() > 1) {
                            moves.add(moves.size()-1,"MOVE " + x + " " + y);
                        }

                        potentielsX = List.of(x);
                        potentielsY = List.of(y);
                    }

                    if (best2 == 0) {
                        takenPlants[bst] = 1;
                        nSeeds -= 1;
                        score += 1;
                        List<Integer> position = params.plants.get(bst);
                        double iaa = bestDist;
                    if (bst == secondBest) iaa = secondBestDist;
                    else if (bst == thirdBest) iaa = thirdBestDist;


                        if (iaa > params.range) {
                            HashMap<Integer,Integer> distPerCandidate = new HashMap<>();

                             for (int i = 0 ; i < seedsNeighbors.size() ; i++) {
                                int candidateX = position.get(0) + seedsNeighbors.get(i).get(0);
                                int candidateY = position.get(1) + seedsNeighbors.get(i).get(1);
                                int d = Math.abs(x-candidateX) + Math.abs(y-candidateY);
                                distPerCandidate.put(i,d);
                                if (d < iaa) {
                                    iaa = d;
                                }
                             }

                             distance += iaa;

                             potentielsX = new ArrayList<>();
                             potentielsY = new ArrayList<>();

                             for (int i = 0 ; i < seedsNeighbors.size() ; i++) {
                                if (distPerCandidate.get(i) == iaa) {
                                    potentielsX.add(position.get(0) + seedsNeighbors.get(i).get(0));
                                    potentielsY.add(position.get(1) + seedsNeighbors.get(i).get(1));
                                }
                             }

                             potentielsX.add(2100000000);
                             potentielsY.add(2100000000);

                        }

                        moves.add("PLANT " + position.get(0) + " " + position.get(1));

                    } else {
                        List<Integer> position = params.seeds.get(bst);
                        int nextX = position.get(0);
                        int nextY = position.get(1);
                        double iaa = bestDist;
                    if (bst == secondBest) iaa = secondBestDist;
                    else if (bst == thirdBest) iaa = thirdBestDist;
                        distance += iaa;
                        takenSeeds[bst] = 1;
                        x = nextX;
                        y = nextY;
                        nSeeds = params.seedCapacity;
                         moves.add("MOVE " + nextX + " " + nextY);
                        moves.add("COLLECT");
                        potentielsX = List.of(x);
                        potentielsY = List.of(y);
                    }
                }
                elapsed = System.currentTimeMillis() - startTime;
                x = potentielsX.get(0);
                y = potentielsY.get(0);
				
                if (potentielsX.size() > 1) {
                    moves.add(moves.size()-1,"MOVE " + x + " " + y);
                }
                if (score == (double)params.plants.size()) {score *= (double)params.maxDistance/(double)distance;}
                if (score > bestScore) {
                    bestMoves = moves;
                    bestScore = score;
                    System.out.println("bestScore: " + bestScore);

                    File file = new File(outt+indexxx);
                    indexxx +=1;
                    objectMapper.writerWithDefaultPrettyPrinter().writeValue(file, bestMoves);

                    byte[] jsonBytes = Files.readAllBytes(file.toPath());
                    String jsonUtf8 = new String(jsonBytes, StandardCharsets.UTF_8);
                    Files.write(file.toPath(), jsonUtf8.getBytes(StandardCharsets.UTF_8));

                    System.out.println("✅ Fichier JSON généré avec succès : " + file.getAbsolutePath());

                }
            }

            System.out.println("bestScore: " + bestScore);
            System.out.println("nRollouts: " + nRollouts);

            File file = new File(outt);
            objectMapper.writerWithDefaultPrettyPrinter().writeValue(file, bestMoves);

            byte[] jsonBytes = Files.readAllBytes(file.toPath());
            String jsonUtf8 = new String(jsonBytes, StandardCharsets.UTF_8);
            Files.write(file.toPath(), jsonUtf8.getBytes(StandardCharsets.UTF_8));

            System.out.println("✅ Fichier JSON généré avec succès : " + file.getAbsolutePath());


        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    static class Params {

      public Params (){}

      @JsonCreator
        public Params (@JsonProperty("maxDistance") int maxDistance, @JsonProperty("seedCapacity") int seedCapacity,
        @JsonProperty("range") int range, @JsonProperty("seeds") List<List<Integer>> seeds, @JsonProperty("plants") List<List<Integer>> plants) {
            this.maxDistance = maxDistance;
            this.seedCapacity = seedCapacity;
            this.range = range;
            this.seeds = seeds;
            this.plants = plants;

        }
        int maxDistance;
        int seedCapacity;
        int range;
        List<List<Integer>> seeds;
        List<List<Integer>> plants;

    }
}
