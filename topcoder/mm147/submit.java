import java.io.*;
import java.util.*;
import java.security.SecureRandom;

public class SurfaceReconstruction
{
    public static final int randomInt(int origin, int boundInclusive) {
        if (boundInclusive <= origin) return origin;
        return rnd.nextInt(boundInclusive - origin + 1) + origin;
    }

    public static final int randomInt(int[] range, int minRange, int maxRange) {
        int origin = range[0];
        int boundInclusive = range[1];
        if (origin < minRange) origin = minRange;
        if (origin > maxRange) origin = maxRange;
        if (boundInclusive > maxRange) boundInclusive = maxRange;
        if (boundInclusive < minRange) boundInclusive = minRange;
        return randomInt(origin, boundInclusive);
    }

    public static final int randomInt(int[] range) {
        return randomInt(range[0], range[1]);
    }

    public static final double randomDouble(double[] range) {
        return randomDouble(range[0], range[1]);
    }

    public static final double randomDouble(double origin, double bound) {
        if (bound <= origin) return origin;
        double r = (rnd.nextLong() >>> 11) * 0x1.0p-53;
        if (origin < bound) {
            r = r * (bound - origin) + origin;
            if (r >= bound) r = Double.longBitsToDouble(Double.doubleToLongBits(bound) - 1);
        }
        return r;
    }

    public static final double randomDouble(double[] range, double minRange, double maxRange) {
        double origin = range[0];
        double bound = range[1];
        if (origin < minRange) origin = minRange;
        if (origin > maxRange) origin = maxRange;
        if (bound > maxRange) bound = maxRange;
        if (bound < minRange) bound = minRange;
        return randomDouble(origin, bound);
    }

    public static void applySlope(double[][] dsurface, int offx, int offy, double s1, double s2)
    {
      for (int y=0;y<N;y++)
        for (int x=0;x<N;x++)
        {
          dsurface[y][x] += (x-offx)*s1-(y-offy)*s2;
        }
    }
    public static void applySinCos(double[][] dsurface, int offx, int offy, double s1, double s2, double amp)
    {
      for (int y=0;y<N;y++)
        for (int x=0;x<N;x++)
        {
          dsurface[y][x] += amp*(Math.sin((x-offx)*s1)+Math.cos((y-offy)*s2));
        }
    }
    public static void applyXY2(double[][] dsurface, int offx, int offy, double rx, double ry, double amp)
    {
      for (int y=0;y<N;y++)
        for (int x=0;x<N;x++)
        {
          double dx = (double)(x-offx)*(double)(x-offx)*rx;
          double dy = (double)(y-offy)*(double)(y-offy)*ry;
          dsurface[y][x] += amp*Math.exp(-(dx+dy));
        }
    }

    public static void applyXOR(double[][] dsurface, int offx, int offy)
    {
      for (int y=0;y<N;y++)
        for (int x=0;x<N;x++)
        {
          dsurface[y][x] += (x-offx) ^ (y-offy);
        }
    }

    public static void normalize(double[][] dsurface, int[][] surface)
    {
      double vmin = 1e30;
      double vmax = -vmin;
      for (int y=0;y<N;y++)
        for (int x=0;x<N;x++)
        {
          vmin = Math.min(vmin, dsurface[y][x]);
          vmax = Math.max(vmax, dsurface[y][x]);
        }
      for (int y=0;y<N;y++)
        for (int x=0;x<N;x++)
        {
          surface[y][x] = (int)((dsurface[y][x]-vmin)*255/(vmax-vmin));
        }
    }

  private static double A;
  private static int N;
  private static SecureRandom rnd;
  private static long startTime;
  private static final long MAX_TIME = 8500L;
  private static final int SINCOS = 0;
  private static final int XY2 = 1;
  private static final int SLOPE = 2;
  private static final int XOR = 3;
  private static final double t_start = 90;
  private static final double t_final = 100;

  public static void main(String[] args) throws Exception
  {           
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));    
    
    A = Double.parseDouble(in.readLine());
    startTime = System.currentTimeMillis();
    N = Integer.parseInt(in.readLine());

    rnd = SecureRandom.getInstance("SHA1PRNG");
    rnd.setSeed(0);
         
    int[][] grid = new int[N][N];

    int nbSamples = Math.max(4,Math.min(5,(int)(N/7)));

    int gapSamples = (int)(N/nbSamples);

    for (int i = 1 ; i < nbSamples ; i++) {
        int sy = (int)(i*gapSamples);
        for (int j = 1 ; j < nbSamples ; j++) {
            int sx = (int)(j*gapSamples);
        System.out.println(sy+" "+sx);
        System.out.flush();

        // Read in the 3x3 sampling result
        for (int dy=-1;dy<=1;dy++)
          for (int dx=-1;dx<=1;dx++)
          {
            int nx = sx+dx;
            int ny = sy+dy;
            String s = in.readLine();
            int v = Integer.parseInt(s);
            grid[ny][nx] = v;
          }
        // read the remaining time
        int timevalue = Integer.parseInt(in.readLine());
    }
    }


    int[][] best = new int[N][N];
    int bestMse = Integer.MAX_VALUE;
    List<Equation> bestEqua = new ArrayList<>();

    int[][] current = new int[N][N];
    int currentMse = Integer.MAX_VALUE;
    List<Equation> currentEqua = new ArrayList<>();

    while (System.currentTimeMillis()-startTime < MAX_TIME) {

        int E = randomInt(1,30);
        int cut = 0;
        if (!currentEqua.isEmpty())
            cut = randomInt(1,currentEqua.size());
        int[][] surface = new int[N][N];
        double[][] dsurface = new double[N][N];
        List<Equation> currEqua = new ArrayList<>();
        for (int e=0;e<Math.min(cut,E);e++)
        {
            Equation eq = currentEqua.get(e);
            if (eq.type == SLOPE) {
                Slope slope = (Slope) eq;
                currEqua.add(slope);
                applySlope(dsurface, slope.offx, slope.offy, slope.s1, slope.s2);
            }
            else if (eq.type == SINCOS) {
                SinCos sincos = (SinCos) eq;
                currEqua.add(sincos);
                applySinCos(dsurface, sincos.offx, sincos.offy, sincos.s1, sincos.s2, sincos.amp);
             }
            else if (eq.type == XOR) {
                currEqua.add(eq);
                applyXOR(dsurface, eq.offx, eq.offy);
            }
            else if (eq.type == XY2) {
                SinCos sincos = (SinCos) eq;
                currEqua.add(sincos);//XY2
                applyXY2(dsurface, sincos.offx, sincos.offy, sincos.s1, sincos.s2, sincos.amp);
            }
        }
        for (int e=cut;e<E;e++)
        {
            // select the equation
            int r = randomInt(0,10);
            // select offset
            int offx = randomInt(0,N);
            int offy = randomInt(0,N);
            if (r==0) {
                double s1 = randomDouble(-10,10);
                double s2 = randomDouble(-10,10);
                currEqua.add(new Slope(offx, offy, s1, s2, SLOPE));
                applySlope(dsurface, offx, offy, s1, s2);
            }
            else if (r==1) {
                double s1 = randomDouble(-0.4,0.4);
                double s2 = randomDouble(-0.4,0.4);
                double amp = randomDouble(10,100);
                currEqua.add(new SinCos(offx, offy, s1, s2, amp, SINCOS));
                applySinCos(dsurface, offx, offy, s1, s2, amp);
             }
            else if (r==2) {
                currEqua.add(new Equation(offx, offy, XOR));
                applyXOR(dsurface, offx, offy);
            }
            else if (r>2) {
                double rx = randomDouble(0.001,0.1);
                double ry = randomDouble(0.001,0.1);
                double amp = randomDouble(10,100);
                currEqua.add(new SinCos(offx, offy, rx, ry, amp, XY2));
                applyXY2(dsurface, offx, offy, rx, ry, amp);
            }
        }

        // Normalize the surface
        normalize(dsurface, surface);

        // Calculate error
        int mse = 0;
        for (int y=0;y<N;y++)
          for (int x=0;x<N;x++)
            if (grid[y][x]!=0)
                mse += (surface[y][x]-grid[y][x])*(surface[y][x]-grid[y][x]);
        mse /= (9*(nbSamples-1)*(nbSamples-1));

        if (mse < currentMse){
            currentMse = mse;
            current = surface;
            currentEqua = currEqua;

            if (mse < bestMse){
                bestMse = mse;
                best = surface;
                bestEqua = currEqua;
            }
        } else {
            double r = randomDouble(0,1);
            double T = t_start*Math.pow(t_final/t_start, (System.currentTimeMillis()-startTime)/MAX_TIME);
            if (Math.exp((bestMse - mse)/T) > r){
                currentMse = mse;
                current = surface;
                currentEqua = currEqua;
            }
        }
    }

    System.out.println("done");
    // output the predicted surface
    for (int y=0;y<N;y++)
      for (int x=0;x<N;x++)
        if (grid[y][x]==0)
          System.out.println( best[y][x] );
        else
          System.out.println( grid[y][x]);
    System.out.flush();
  }

  public static class Equation {
    public int offx;
    public int offy;
    public int type;

    public Equation(int offx, int offy, int type) {
        this.offx = offx;
        this.offy = offy;
        this.type = type;
    }
  }

  public static class XY2 extends Equation {
    public int s1;
    public int s2;

    public XY2(int offx, int offy, int s1, int s2, int type) {
        super(offx, offy, type);
        this.s1 = s1;
        this.s2 = s2;
    }
  }

  public static class Slope extends Equation {
    public double s1;
    public double s2;

    public Slope(int offx, int offy, double s1, double s2, int type) {
        super(offx, offy, type);
        this.s1 = s1;
        this.s2 = s2;
    }
  }

  public static class SinCos extends Slope {
    public double amp;

    public SinCos(int offx, int offy, double s1, double s2, double amp, int type) {
        super(offx, offy, s1, s2, type);
        this.amp = amp;
    }
  }
}
