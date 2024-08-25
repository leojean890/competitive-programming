import java.io.*;
import java.util.*;

public class main
{
    public static void main(String args[])
    {


        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        long startTime = System.nanoTime();
        int T = in.nextInt();
        int c = in.nextInt();

        double[][] p = new double[n][T + 1];
        int[] L = new int[n];
        int[] FCTR1 = new int[n];
        int[] FCTR2 = new int[n];
        double[][] k = new double[n][T];
        double[][] e = new double[n][T];
        double[][][] a = new double[n][n][T];
        double[] b = new double[T];
        Random random = new Random();

        double[][] bestQ = new double[n][T];
        double bestScore = 0;
        double sumL = 0;

        for(int i = 0; i < n; i++)
        {
            p[i][0] = in.nextDouble();
            L[i] = in.nextInt();
            FCTR1[i] = (int)(L[i]/T);
            FCTR2[i] = (int)(sumL*L[i]/(T*c));
            sumL += L[i];
        }
        for(int i = 0; i < n; i++)
        {
            for(int t = 0; t < T; t++)
            {
                k[i][t] = in.nextDouble();
            }
        }
        for (int i = 0; i < n; i++)
        {
            for (int t = 0; t < T; t++)
            {
                e[i][t] = in.nextDouble();
            }
        }
        for (int i = 1; i < n; i++)
        {
            for (int j = 0; j < i; j++)
            {
                for(int t = 0; t < T; t++)
                {
                    a[i][j][t] = in.nextDouble();
                }
            }
        }
        for (int t = 0; t < T; t++)
        {
            b[t] = in.nextDouble();
        }

        for (int t = 0; t < T - 1; t++)
        {
            for (int i = 0; i < n; i++)
            {
                bestQ[i][t] = 0;
            }
        }
        int currC = c;
        for (int i = 0; i < n; i++)
        {
            int cur = Math.min(currC, L[i]);
            currC -= cur;
            bestQ[i][T-1] = cur;
        }

        int FCTR = (int)(sumL/c);
        int[] curr_L = new int[n];
        double[][] curr_delta_p = new double[n][T + 1];
        double[][] curr_Q = new double[n][T];
        while ((System.nanoTime() - startTime) / 1e9 < 2) {

            for(int i = 0; i < n; i++)
            {
                curr_L[i] = L[i];
            }

            int curr_c = c;
            for (int t = 0; t < T-1; t++)
            {
                for (int i = 0; i < n; i++)
                {
                    int cur = Math.min(curr_c, curr_L[i]);
                    int chosen = 0;
                    int factor = FCTR;
                    if (factor > 0) {
                        factor = random.nextInt(factor)+1;
                    } else {
                        factor = 1;
                    }
                    //int factor = random.nextInt((int)(sumL/c)+1)+1;

                    //int factor = (int)(sumL*L[i]/(T*c));// sumL*L[i]/(T*(c-1));
                    factor *= FCTR1[i];

                    if (cur > factor+1) {
                        chosen = random.nextInt(3);//excluded
                        chosen += factor;
                    }
                    else if (cur == factor) {
                        chosen = factor;
                    }
                    else if (cur == factor+1) {
                        chosen = random.nextInt(2);//excluded
                        chosen += factor;
                    }
                    else if (cur > FCTR2[i]+1) {
                        chosen = random.nextInt(3);//excluded
                        chosen += FCTR2[i];
                    } else if (cur > 0){
                        chosen = random.nextInt(cur);
                    }
                    // random sur l'intervalle entre 1 et sumL/T => DONE
                    // choix random entre L[i]/T et factor => TODO
                    // attention aux arrondis car on consid�re des entiers
 
                    // TODO HC SA
                    curr_c -= chosen;
                    curr_L[i] -= chosen;
                    curr_Q[i][t] = chosen;

                    curr_delta_p[i][t] = p[i][t] * (1-1/Math.exp(curr_Q[i][t]*k[i][t]/(curr_L[i]+1))) + e[i][t]*p[i][t];
                    double somme1 = 0;
                    for (int j = 0 ; j < i ; j++) {
                        somme1 += a[i][j][t] * curr_delta_p[j][t]/Math.log(Math.max(Math.exp(1), (p[i][t]-p[j][t])));
                    }
                    double somme2 = 0;

                    for (int s = 0 ; s < t ; s++) {
                        somme2 += b[s] * curr_Q[i][t-s];
                    }

                    curr_delta_p[i][t] += somme1 + somme2;
                    p[i][t+1] = p[i][t] + curr_delta_p[i][t];//[i][t]
                }
            }
            for (int t = T-1; t < T; t++) {

                for (int i = 0; i < n; i++)
                {

                    int cur = Math.min(curr_c, curr_L[i]);
                    curr_c -= cur;
                    curr_L[i] -= cur;
                    curr_Q[i][t] = cur;

                    curr_delta_p[i][t] = p[i][t] * (1-1/Math.exp(curr_Q[i][t]*k[i][t]/(curr_L[i]+1))) + e[i][t]*p[i][t];
                    double somme1 = 0;
                    for (int j = 0 ; j < i ; j++) {
                        somme1 += a[i][j][t] * curr_delta_p[j][t]/Math.log(Math.max(Math.exp(1), (p[i][t]-p[j][t])));
                    }

                    double somme2 = 0;
                    for (int s = 0 ; s < t ; s++) {
                        somme2 += b[s] * curr_Q[i][t-s];
                    }

                    curr_delta_p[i][t] += somme1 + somme2;
                    p[i][t+1] = p[i][t] + curr_delta_p[i][t];
                }

            }

            double sc1 = 0;
            double sc2 = 0;

            for (int i = 0; i < n; i++) {
                sc1 += p[i][0];
                sc2 += Math.abs(p[i][T]-p[i][0]);
            }

            sc1 *= 10;

            double score = Math.max(0,10000000*(sc1 - sc2)/sc1);

            if (score > bestScore) {
                bestScore = score;
                for (int t = 0; t < T; t++)
                {
                    for (int i = 0; i < n; i++)
                    {
                        bestQ[i][t] = curr_Q[i][t];
                    }
                }
            }

        }

        for (int t = 0; t < T ; t++)
        {
            for (int i = 0; i < n; i++)
            {
                System.out.print((int)bestQ[i][t]);
                System.out.print(' ');
            }
            System.out.println();
        }

    }
}





