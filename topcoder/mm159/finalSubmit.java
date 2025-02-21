import java.io.*;
import java.util.*;

public class MiniGolf
{
     private static double T, startTime;
   //Constants other
  private static int S=10000,A,W;           // grid size
  private static final int maxDistance=(int)Math.round(S*Math.sqrt(2));
  private static final int minHitDistance=0;
  private static final int maxHitDistance=maxDistance;
  private static final int appleRadius=200;
  private static final int ballRadius=150;
  private static final int maxTurns=1000;
  private static final int appleScore=1000;
  private static final double missPenalty=0.9;
  //parameter ranges
  private static final int minA = 1, maxA = 5;      // number of apples range
  private static final int minW = 3, maxW = 15;      // number of ponds range
  private static final double minDelta1 = 0, maxDelta1 = 60;      // angle variance range
  private static final double minDelta2 = 0.05, maxDelta2 = 0.2;      // distance variance range
    private static final Random random = new Random(1);

  //Constants for polygons
  private static final int minSides=3;
  private static final int maxSides=10;
  private static final double minPolygonRadius = 250.0;
  private static final double minPolygonArea = minPolygonRadius * minPolygonRadius;
  private static final double maxPolygonRadius = 1500.0;
  private static final double irregularity = 0.75;
  private static final double spikiness = 0.75;
 static List<Point>[] ponds;
  public static void main(String[] args) throws Exception
  {           
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));    

    A=Integer.parseInt(in.readLine());
    startTime = System.currentTimeMillis();

    W=Integer.parseInt(in.readLine());
    double delta1=Double.parseDouble(in.readLine());   
    double delta2=Double.parseDouble(in.readLine());
    double D = 14142.0d;
    double D1 = 14142.0d*14142.0d;

    int[][] apples=new int[A][2];
    for (int i=0; i<A; i++)
    {
      String[] temp=in.readLine().split(" ");
      apples[i][0]=Integer.parseInt(temp[0]);
      apples[i][1]=Integer.parseInt(temp[1]);
    }

    ponds=new List[W];
    for (int i=0; i<W; i++)
    {
      int n=Integer.parseInt(in.readLine());
      ponds[i]=new ArrayList<Point>();
      for (int k=0; k<n; k++)
      {
        String[] temp=in.readLine().split(" ");
        int x=Integer.parseInt(temp[0]);
        int y=Integer.parseInt(temp[1]);        
        ponds[i].add(new Point(x,y));
      }
    }  

    String[] temp=in.readLine().split(" ");
    int ballX=Integer.parseInt(temp[0]);
    int ballY=Integer.parseInt(temp[1]);    

    int numIntervals = 8;

    int elapsedTime = 0;
    int turn = 0;
    String result = ";";
    int autourDe = 90;
    int[] cAngles=new int[A];

    while (elapsedTime < 9700)
    {
        turn += 1;

      double bestAngle=0.0d;
      double bestHitDistance=2000.0d;

      double bestScore=-1000000.0*D;

      int nbIter = 13+W;

      if (delta1 > 20) nbIter += 1;
      if (delta1 > 40) nbIter += 1;

      if (delta1 > 0.1) nbIter += 1;
      if (delta1 > 0.15) nbIter += 1;

      int MAX = nbIter;
      int counterHits = 0;
      for (int iteration = 0 ; iteration < MAX ; iteration ++) {
              double a=0.0d;
              double d=2000.0d;
              int angle = 0;
              int distance = 0;
              int ctr = 0;


            if (iteration < A){
                a=Math.floorMod((int)(Math.atan2(ballY-apples[iteration][1],apples[iteration][0]-ballX)/2/Math.PI*360),360);
                d = Math.sqrt(sq(ballX-apples[iteration][0]) + sq(ballY-apples[iteration][1]));
                distance = (int) d;
                angle = (int) a;
                cAngles[iteration] = angle;
            } else if (iteration < nbIter-4) {
              int it = iteration%A;
                angle = Math.floorMod(cAngles[it] + random.nextInt(autourDe) - (autourDe/2),360);
                distance = random.nextInt(5000);
                a = (double) angle;
                d = (double) distance;
            } else {
                angle = random.nextInt(360);
                distance = random.nextInt(5000);
                a = (double) angle;
                d = (double) distance;
            }

            double score = 0;
              Map<Double, Double> distributionAngles;
            if(delta1 == 0)
                distributionAngles = Map.of(a,1.0d);
            else
                distributionAngles = estimateDistribution(a,delta1*d/D,numIntervals);

            Map<Double, Double> distributionDistances;
            if(delta2 == 0)
                distributionDistances = Map.of(d,1.0d);
            else
            distributionDistances = estimateDistribution(d,delta2*d,numIntervals);

            for (Map.Entry<Double, Double> entry1 : distributionAngles.entrySet()) {
                for (Map.Entry<Double, Double> entry2 : distributionDistances.entrySet()) {
                    double hitAngle = entry1.getKey();
                    double hitDistance = entry2.getKey();
                    double proba1 = entry1.getValue();
                    double proba2 = entry2.getValue();

                    if (hitDistance<minHitDistance) hitDistance=minHitDistance;
                    if (hitDistance>maxHitDistance) hitDistance=maxHitDistance;

                    int newX=(int)Math.round(ballX+Math.cos(hitAngle/360.0*2*Math.PI)*hitDistance);
                    int newY=(int)Math.round(ballY-Math.sin(hitAngle/360.0*2*Math.PI)*hitDistance);
                    Point newBall=new Point(newX, newY);

                    //out of bounds
                    boolean hitOk=true;
                    if (newX-ballRadius<0 || newX+ballRadius>=S || newY-ballRadius<0 || newY+ballRadius>=S)
                      hitOk=false;

                    //check if we hit any obstacles
                    double closestDist1 = D;
                    if (hitOk)
                    {
            loop:
                      for (int i=0; i<W; i++)
                      {
                        for (int k=0; k<ponds[i].size(); k++)
                        {
                          Point p1=ponds[i].get(k);
                          Point p2=ponds[i].get((k+1)%ponds[i].size());
                          double distL = distSegment2Segment(ballX,ballY,newX,newY,p1.x,p1.y,p2.x,p2.y);
                              if (distL < closestDist1) closestDist1 = distL;
                        score += distL*proba1*proba2/60;

                          if (distL < ballRadius)
                          {
                            hitOk=false;
                            break loop;
                          }
                        }
                      }
                    }

                    if (!hitOk) {score -= D*proba1*proba2;ctr += 1;}
                    else if (!result.equals("BAD")) {
                        double closestDist = D1;
                        for (int i = 0 ; i < A ; i++) {
                              double dist = sq(newX-apples[i][0]) + sq(newY-apples[i][1]);
                              if (dist < closestDist) closestDist = dist;
                        }
                        score += (closestDist1/40-Math.sqrt(closestDist))*proba1*proba2;

                }}
            }

            if (ctr > 10) counterHits += 1;

            if (counterHits == MAX) MAX += 1;

            if (score > bestScore) {
                bestScore = score;
               bestAngle=a;
               bestHitDistance=d;

            }
      }

      System.out.println(bestAngle+" "+bestHitDistance);
      System.out.flush();   

      result=in.readLine();
      temp=in.readLine().split(" ");  
      int newX=Integer.parseInt(temp[0]);
      int newY=Integer.parseInt(temp[1]);     
      elapsedTime=Integer.parseInt(in.readLine());

      if (result.equals("BAD")) continue;       

      if (result.equals("GOOD"))
      {
        ballX=newX;
        ballY=newY;
        int n=Integer.parseInt(in.readLine());
        for (int i=0; i<n; i++)
        {
          temp=in.readLine().split(" ");
          int id=Integer.parseInt(temp[0]);
          apples[id][0]=Integer.parseInt(temp[1]);
          apples[id][1]=Integer.parseInt(temp[2]);          
        }
      }
    }    
    System.out.println("-1");
    System.out.flush();       
  }

    private static double normalPDF(double x, double mu, double sigma) {
        return (1 / (sigma * Math.sqrt(2 * Math.PI))) *
               Math.exp(-Math.pow(x - mu, 2) / (2 * Math.pow(sigma, 2)));
    }

    public static Map<Double, Double> estimateDistribution(double mu, double sigma, int numIntervals) {
        Map<Double, Double> probabilityMap = new HashMap<>();

        double minX = mu - 3.15 * sigma;
        double maxX = mu + 3.15 * sigma;
        double step = (maxX - minX) / numIntervals;

        double totalProbability = 0.0;

        for (int i = 0; i < numIntervals; i++) {
            double start = minX + i * step;
            double end = start + step;

            double midPoint = (start + end) / 2;
            double probability = normalPDF(midPoint, mu, sigma) * step;

            probabilityMap.put(midPoint, probability);
            totalProbability += probability;
        }

        for (Map.Entry<Double, Double> entry : probabilityMap.entrySet()) {
            probabilityMap.put(entry.getKey(), entry.getValue() / totalProbability);
        }

        return probabilityMap;
    }



///// GEOMETRY METHODS /////


  private static double distSegment2Segment(int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4)
  {
    if (linesIntersect(x1,y1,x2,y2,x3,y3,x4,y4)) return 0;

    double d1=distPoint2Line(new Point(x1,y1),x3,y3,x4,y4);
    double d2=distPoint2Line(new Point(x2,y2),x3,y3,x4,y4);
    double d3=distPoint2Line(new Point(x3,y3),x1,y1,x2,y2);
    double d4=distPoint2Line(new Point(x4,y4),x1,y1,x2,y2);
    double[] a={d1,d2,d3,d4};
    Arrays.sort(a);
    return a[0];
  }


  // Checks whether segments (x1,y1)-(x2,y2) and (x3,y3)-(x4,y4) intersect or touch
  // Modified Java's Line2D implementation to use integers
  // https://github.com/srisatish/openjdk/blob/master/jdk/src/share/classes/java/awt/geom/Line2D.java
  private static boolean linesIntersect(int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4)
  {
    return ((relativeCCW(x1, y1, x2, y2, x3, y3) *
             relativeCCW(x1, y1, x2, y2, x4, y4) <= 0)
            && (relativeCCW(x3, y3, x4, y4, x1, y1) *
                relativeCCW(x3, y3, x4, y4, x2, y2) <= 0));
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


  //from https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon
  private static boolean isPointInsidePoly(Point p, List<Point> poly)
  {
    boolean inside=false;
    for (int i = 0, j = poly.size()-1; i < poly.size(); j = i++)
    {
      Point p1=poly.get(i);
      Point p2=poly.get(j);
      if ( ((p1.y>p.y) != (p2.y>p.y)) &&
       (p.x < (p2.x-p1.x) * (p.y-p1.y) * 1.0 / (p2.y-p1.y) + p1.x) )
         inside = !inside;
    }
    return inside;
  }


  //check if apple overlaps any polygons
  private static boolean isCircleOk(Point p, int radius)
  {
    for (int i=0; i<W; i++)
      if (isPointInsidePoly(p, ponds[i]) || distPoint2Poly(p, ponds[i]) < radius)
        return false;

    return true;
  }

  //minimum distance from a point to a polygon
  private static double distPoint2Poly(Point p, List<Point> poly)
  {
    double min=Double.MAX_VALUE;

    for (int i=0; i<poly.size(); i++)
    {
      Point p1=poly.get(i);
      Point p2=poly.get((i+1)%poly.size());
      min=Math.min(min,distPoint2Line(p,p1.x,p1.y,p2.x,p2.y));
    }

    return min;
  }


  //from https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
  private static double distPoint2Line(Point p, int x1, int y1, int x2, int y2)
  {
    int x=p.x;
    int y=p.y;
    int A = x - x1;
    int B = y - y1;
    int C = x2 - x1;
    int D = y2 - y1;

    int dot = A * C + B * D;
    int len_sq = C * C + D * D;
    double param = -1;
    if (len_sq != 0) //in case of 0 length line
      param = dot * 1.0 / len_sq;

    double xx, yy;

    if (param < 0) {
      xx = x1;
      yy = y1;
    }
    else if (param > 1) {
      xx = x2;
      yy = y2;
    }
    else {
      xx = x1 + param * C;
      yy = y1 + param * D;
    }

    double dx = x - xx;
    double dy = y - yy;
    return Math.sqrt(dx * dx + dy * dy);
  }


  private static double areaOfPolygon(List<Point> poly)
  {
    double t=0;

    for (int i=0; i<poly.size(); i++)
    {
      Point p1=poly.get(i);
      Point p2=poly.get((i+1)%poly.size());
      t+=p1.x*p2.y-p2.x*p1.y;
    }

    return t/2;
  }


  private static int sq(int a)
  {
    return a*a;
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
  }

}
