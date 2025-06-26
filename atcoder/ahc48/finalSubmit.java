import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Scanner;

public class Main {
    private static final int NB_AREAS = 40;
    private static final double[] aremainingC = new double[NB_AREAS];
    private static final double[] aremainingM = new double[NB_AREAS];
    private static final double[] aremainingY = new double[NB_AREAS];
    private static final double[] aremaining = new double[NB_AREAS];

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        in.useLocale(Locale.US);
        int N = in.nextInt(), K = in.nextInt(), H = in.nextInt(), T = in.nextInt(), D = in.nextInt();
        double[] cown = new double[K];
        double[] mown = new double[K];
        double[] yown = new double[K];
        double[] ctarget = new double[H];
        double[] mtarget = new double[H];
        double[] ytarget = new double[H];

        for (int i = 0; i < K; i++) {
            cown[i] = in.nextDouble();
            mown[i] = in.nextDouble();
            yown[i] = in.nextDouble();
            in.nextLine();
        }

        for (int i = 0; i < H; i++) {
            ctarget[i] = in.nextDouble();
            mtarget[i] = in.nextDouble();
            ytarget[i] = in.nextDouble();
            in.nextLine();
        }

        for (int i = 0; i < N; i++) {
            String out1 = "";
            for (int j = 0; j < N-2; j++) {
                if (j == 9)
                    out1 += "1 ";
                else
                    out1 += "0 ";
            }
            out1 += "0";
            System.out.println(out1);
        }

        for (int i = 0; i < N-1; i++) {
            String out1 = "";
            for (int j = 0; j < N-1; j++) {
                out1 += "1 ";
            }
            out1 += "1";
            System.out.println(out1);
        }

        List<Integer> best = new ArrayList<>();

        for (int j = 0; j < H; j++) {
            double minScore = Double.MAX_VALUE;
            boolean destroy = false;
			int bestCentralCut = 0;
			double bestRemaining = aremaining[0];
            int bestLine = 0;

            for (int line = 0; line < NB_AREAS; line++) {
                double remaining = aremaining[line];
                double remainingC = aremainingC[line];
                double remainingM = aremainingM[line];
                double remainingY = aremainingY[line];

                if (remaining > 0) {
                    double E = (remainingC - ctarget[j]) * (remainingC - ctarget[j]) + (remainingM - mtarget[j]) * (remainingM - mtarget[j]) + (remainingY - ytarget[j]) * (remainingY - ytarget[j]);
                    double score = 10000 * Math.sqrt(E) - D;
                    if (score < minScore && remaining >= 1) {
                        minScore = score;
                        best = List.of();
                        bestRemaining = remaining;
                        bestLine = line;
						bestCentralCut = 0;
                    }

                    for (int nbDiscarded = 0; nbDiscarded < remaining; nbDiscarded++) {
                        double nextRemaining = remaining - nbDiscarded;
                        double cQuantity = remainingC * nextRemaining;
                        double mQuantity = remainingM * nextRemaining;
                        double yQuantity = remainingY * nextRemaining;

                        for (int i = 0; i < K; i++) {
                            if (nextRemaining > 9) break;
                            double currC = (cQuantity + cown[i]) / (nextRemaining + 1);
                            double currM = (mQuantity + mown[i]) / (nextRemaining + 1);
                            double currY = (yQuantity + yown[i]) / (nextRemaining + 1);

                            E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                            score = 10000 * Math.sqrt(E);
                            if (score < minScore) {
                                minScore = score;
                                best = List.of(i);
                                bestRemaining = nextRemaining;
                                bestLine = line;
								bestCentralCut = 0;
                            }
                        }

                        if (D < 4000 && nextRemaining < 9) {
                            for (int i = 0; i < K; i++) {
                                for (int k = i; k < K; k++) {
                                    double currC = (cQuantity + cown[i] + cown[k]) / (nextRemaining + 2);
                                    double currM = (mQuantity + mown[i] + mown[k]) / (nextRemaining + 2);
                                    double currY = (yQuantity + yown[i] + yown[k]) / (nextRemaining + 2);

                                    E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                    score = 10000 * Math.sqrt(E) + D;
                                    if (score < minScore) {
                                        minScore = score;
                                        best = List.of(i, k);
                                        bestRemaining = nextRemaining;
                                        bestLine = line;
										bestCentralCut = 0;
                                    }
                                }
                            }
                        }

                        if (K < 14 && D < 2000 && T > 6000 && nextRemaining < 8) {
                            for (int i = 0; i < K; i++) {
                                for (int k = i; k < K; k++) {
                                    for (int l = k; l < K; l++) {
                                        double currC = (cQuantity + cown[i] + cown[k] + cown[l]) / (nextRemaining + 3);
                                        double currM = (mQuantity + mown[i] + mown[k] + mown[l]) / (nextRemaining + 3);
                                        double currY = (yQuantity + yown[i] + yown[k] + yown[l]) / (nextRemaining + 3);
                                        E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                        score = 10000 * Math.sqrt(E) + D * 2;
                                        if (score < minScore) {
                                            bestRemaining = nextRemaining;
                                            minScore = score;
                                            best = List.of(i, k, l);
                                            bestLine = line;
											bestCentralCut = 0;
                                        }
                                    }
                                }
                            }
                        }

                        if (K < 10 && D < 800 && T > 8000 && nextRemaining < 7) {
                            for (int i = 0; i < K; i++) {
                                for (int k = i; k < K; k++) {
                                    for (int l = k; l < K; l++) {
                                        for (int m = l; m < K; m++) {

                                            double currC = (cQuantity + cown[i] + cown[k] + cown[l] + cown[m]) / (nextRemaining + 4);
                                            double currM = (mQuantity + mown[i] + mown[k] + mown[l] + mown[m]) / (nextRemaining + 4);
                                            double currY = (yQuantity + yown[i] + yown[k] + yown[l] + yown[m]) / (nextRemaining + 4);


                                            E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                            score = 10000 * Math.sqrt(E) + D * 3;
                                            if (score < minScore) {
                                                bestRemaining = nextRemaining;
                                                minScore = score;
                                                best = List.of(i, k, l, m);
                                                bestLine = line;
												bestCentralCut = 0;
                                            }
                                        }
                                    }
                                }
                            }
                        }


                        if (K < 9 && D < 400 && T > 10000 && nextRemaining < 6) {
                            for (int i = 0; i < K; i++) {
                                for (int k = i; k < K; k++) {
                                    for (int l = k; l < K; l++) {
                                        for (int m = l; m < K; m++) {
                                            for (int n = m; n < K; n++) {

                                                double currC = (cQuantity + cown[i] + cown[k] + cown[l] + cown[m] + cown[n]) / (nextRemaining+5);
                                                double currM = (mQuantity + mown[i] + mown[k] + mown[l] + mown[m] + mown[n]) / (nextRemaining+5);
                                                double currY = (yQuantity + yown[i] + yown[k] + yown[l] + yown[m] + yown[n]) / (nextRemaining+5);

                                                E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                                score = 10000*Math.sqrt(E) + D*4;
                                                if (score < minScore) {
                                                    bestRemaining = nextRemaining;
                                                    minScore = score;
                                                    best = List.of(i,k,l,m,n);
                                                    bestLine = line;
													bestCentralCut = 0;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }


                        if (K < 7 && D < 200 && T > 12000 && nextRemaining < 5) {
                            for (int i = 0; i < K; i++) {
                                for (int k = i; k < K; k++) {
                                    for (int l = k; l < K; l++) {
                                        for (int m = l; m < K; m++) {
                                            for (int n = m; n < K; n++) {
                                                for (int o = n; o < K; o++) {

                                                    double currC = (cQuantity + cown[i] + cown[k] + cown[l] + cown[m] + cown[n] + cown[o]) / (nextRemaining+6);
                                                    double currM = (mQuantity + mown[i] + mown[k] + mown[l] + mown[m] + mown[n] + mown[o]) / (nextRemaining+6);
                                                    double currY = (yQuantity + yown[i] + yown[k] + yown[l] + yown[m] + yown[n] + yown[o]) / (nextRemaining+6);


                                                    E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                                    score = 10000*Math.sqrt(E) + D*5;
                                                    if (score < minScore) {
                                                        minScore = score;
                                                        bestLine = line;
                                                        bestRemaining = nextRemaining;
                                                        best = List.of(i,k,l,m,n,o);
														bestCentralCut = 0;
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
				
					if (line < 20) {
						double remaining2 = aremaining[line+20];
						double remainingC2 = aremainingC[line+20];
						double remainingM2 = aremainingM[line+20];
						double remainingY2 = aremainingY[line+20];
						if (remaining2 > 0 && remaining2 + remaining >= 1) {

							double nextRemaining = (remaining2+remaining);
							double currC = (remainingC2*remaining2 + remainingC*remaining)/nextRemaining;
							double currM = (remainingM2*remaining2 + remainingM*remaining)/nextRemaining;
							double currY = (remainingY2*remaining2 + remainingY*remaining)/nextRemaining;

							E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
							score = 10000*Math.sqrt(E) - D + (H-j)/5; // penalite pour enlever de la diversité au début
							if (score < minScore) {
								minScore = score;
								bestLine = line;
								bestRemaining = nextRemaining;
								best = List.of();
								bestCentralCut = 1;
							}
						}

					}
					
					
					if (!List.of(19,39).contains(line)) {
						double remaining2 = aremaining[line+1];
						double remainingC2 = aremainingC[line+1];
						double remainingM2 = aremainingM[line+1];
						double remainingY2 = aremainingY[line+1];
						if (remaining2 > 0 && remaining2 + remaining >= 1) {

							double nextRemaining = (remaining2+remaining);
							double currC = (remainingC2*remaining2 + remainingC*remaining)/nextRemaining;
							double currM = (remainingM2*remaining2 + remainingM*remaining)/nextRemaining;
							double currY = (remainingY2*remaining2 + remainingY*remaining)/nextRemaining;

							E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
							score = 10000*Math.sqrt(E) - D + (H-j)/5;// + (H-j)/5; // penalite pour enlever de la diversité au début
							if (score < minScore) {
								minScore = score;
								bestLine = line;
								bestRemaining = nextRemaining;
								best = List.of();
								bestCentralCut = 2;
							}
						}


					}
					
					
                }


            }

            int line = j%NB_AREAS;


            if (K < 10 && D < 200 && T > 12000) {
                for (int i = 0; i < K; i++) {
                    for (int k = i; k < K; k++) {
                        for (int l = k; l < K; l++) {
                            for (int m = l; m < K; m++) {
                                for (int n = m; n < K; n++) {
                                    for (int o = n; o < K; o++) {

                                        double currC = (cown[i] + cown[k] + cown[l] + cown[m] + cown[n] + cown[o]) / 6;
                                        double currM = (mown[i] + mown[k] + mown[l] + mown[m] + mown[n] + mown[o]) / 6;
                                        double currY = (yown[i] + yown[k] + yown[l] + yown[m] + yown[n] + yown[o]) / 6;


                                        double E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                        double score = 10000*Math.sqrt(E) + D*5;
                                        if (score < minScore) {
                                            minScore = score;
                                            best = List.of(i,k,l,m,n,o);
                                            destroy = true;
                                            bestLine = line;
											bestCentralCut = 0;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
			
            if (D < 400 && T > 10000) {
                for (int i = 0; i < K; i++) {
                    for (int k = i; k < K; k++) {
                        for (int l = k; l < K; l++) {
                            for (int m = l; m < K; m++) {
                                for (int n = m; n < K; n++) {

                                    double currC = (cown[i] + cown[k] + cown[l] + cown[m] + cown[n]) / 5;
                                    double currM = (mown[i] + mown[k] + mown[l] + mown[m] + mown[n]) / 5;
                                    double currY = (yown[i] + yown[k] + yown[l] + yown[m] + yown[n]) / 5;

                                    double E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                    double score = 10000*Math.sqrt(E) + D*4;
                                    if (score < minScore) {
                                        minScore = score;
                                        best = List.of(i,k,l,m,n);
                                        destroy = true;
                                        bestLine = line;
										bestCentralCut = 0;
                                    }
                                }
                            }
                        }
                    }
                }

            }
            if (D < 800 && T > 8000) {
                for (int i = 0; i < K; i++) {
                    for (int k = i; k < K; k++) {
                        for (int l = k; l < K; l++) {
                            for (int m = l; m < K; m++) {

                                double currC = (cown[i] + cown[k] + cown[l] + cown[m]) / 4;
                                double currM = (mown[i] + mown[k] + mown[l] + mown[m]) / 4;
                                double currY = (yown[i] + yown[k] + yown[l] + yown[m]) / 4;


                                double E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                                double score = 10000*Math.sqrt(E) + D*3;
                                if (score < minScore) {
                                    minScore = score;
                                    best = List.of(i,k,l,m);
                                    destroy = true;
                                    bestLine = line;
									bestCentralCut = 0;
                                }
                            }
                        }
                    }
                }

            }
            if (D < 2000 && T > 6000) {
                for (int i = 0; i < K; i++) {
                    for (int k = i; k < K; k++) {
                        for (int l = k; l < K; l++) {
                            double currC = (cown[i] + cown[k] + cown[l]) / 3;
                            double currM = (mown[i] + mown[k] + mown[l]) / 3;
                            double currY = (yown[i] + yown[k] + yown[l]) / 3;
                            double E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                            double score = 10000*Math.sqrt(E) + D*2;
                            if (score < minScore) {
                                minScore = score;
                                best = List.of(i,k,l);
                                destroy = true;
								bestCentralCut = 0;
                                bestLine = line;
                            }
                        }
                    }
                }

            }
            if (D < 4000) {
                for (int i = 0; i < K; i++) {
                    for (int k = i; k < K; k++) {
                        double currC = (cown[i] + cown[k]) / 2;
                        double currM = (mown[i] + mown[k]) / 2;
                        double currY = (yown[i] + yown[k]) / 2;
                        double E = (currC - ctarget[j]) * (currC - ctarget[j]) + (currM - mtarget[j]) * (currM - mtarget[j]) + (currY - ytarget[j]) * (currY - ytarget[j]);
                        double score = 10000*Math.sqrt(E) + D;
                        if (score < minScore) {
                            minScore = score;
                            best = List.of(i,k);
                            destroy = true;
                            bestLine = line;
							bestCentralCut = 0;
                        }
                    }
                }

            }

            for (int i = 0; i < K; i++) {
                double E = (cown[i] - ctarget[j]) * (cown[i] - ctarget[j]) + (mown[i] - mtarget[j]) * (mown[i] - mtarget[j]) + (yown[i] - ytarget[j]) * (yown[i] - ytarget[j]);
                double score = 10000*Math.sqrt(E);
                if (score < minScore) {
                    minScore = score;
                    best = List.of(i);
                    destroy = true;
                    bestLine = line;
					bestCentralCut = 0;
                }
            }


            int abs = 10*(bestLine/20);
            int ord = bestLine%20;
			
			if (bestCentralCut > 0) {
				int shift = bestCentralCut == 1 ? 20 : 1;
				int nextOrd = ord+1;

				if (bestCentralCut == 1)
					System.out.println("4 " + ord + " " + 9 + " " + ord + " " + 10);
				else
					System.out.println("4 " + ord + " " + abs + " " + nextOrd + " " + abs);

				double remaining = aremaining[bestLine];
				double remainingC = aremainingC[bestLine];
				double remainingM = aremainingM[bestLine];
				double remainingY = aremainingY[bestLine];
				double remaining2 = aremaining[bestLine+shift];
				double remainingC2 = aremainingC[bestLine+shift];
				double remainingM2 = aremainingM[bestLine+shift];
				double remainingY2 = aremainingY[bestLine+shift];
				double nextRemaining = (remaining2+remaining); // vaut bestRemaining normalement
				double currC = (remainingC2*remaining2 + remainingC*remaining)/nextRemaining;
				double currM = (remainingM2*remaining2 + remainingM*remaining)/nextRemaining;
				double currY = (remainingY2*remaining2 + remainingY*remaining)/nextRemaining;


				System.out.println("2 " + ord + " " + abs);
				
				nextRemaining -= 1;
								
				
				if (bestCentralCut == 1)
					System.out.println("4 " + ord + " " + 9 + " " + ord + " " + 10);
				else
					System.out.println("4 " + ord + " " + abs + " " + nextOrd + " " + abs);

				aremainingC[bestLine] = currC;
				aremainingM[bestLine] = currM;
				aremainingY[bestLine] = currY;
	
				aremainingC[bestLine+shift] = currC;
				aremainingM[bestLine+shift] = currM;
				aremainingY[bestLine+shift] = currY;	
				

				aremaining[bestLine] = nextRemaining/2;
				aremaining[bestLine+shift] = nextRemaining/2;
				
			} else {
				if (destroy) {

					// ici on cherche la pire ligne pour la dégager
					// en gros on vire celle qui sert a rien, qui a le plus gros min(parmi suivants de H)..
					double maxScore = Double.MIN_VALUE;


					for (int line1 = 0; line1 < NB_AREAS; line1++) {
						double remaining = aremaining[line1];

						if (remaining == 0.0d) {
							bestLine = line1;
							break;
						}

						double remainingC = aremainingC[line1];
						double remainingM = aremainingM[line1];
						double remainingY = aremainingY[line1];
						minScore = Double.MAX_VALUE;

						for (int i = j + 1; i < Math.min(H, j+10); i++) {

							double score = (remainingC - ctarget[i]) * (remainingC - ctarget[i]) + (remainingM - mtarget[i]) * (remainingM - mtarget[i]) + (remainingY - ytarget[i]) * (remainingY - ytarget[i]);
							if (score < minScore) {
								minScore = score;
							}
						}

						if (maxScore < minScore) {
							maxScore = minScore;
							bestLine = line1;
						}

					}

					abs = 10*(bestLine/20);
					ord = bestLine%20;

					for (int i = 0; i < Math.ceil(aremaining[bestLine]); i++) {
						System.out.println("3 " + ord + " " + abs);
					}
					aremainingC[bestLine] = 0.0d;
					aremainingM[bestLine] = 0.0d;
					aremainingY[bestLine] = 0.0d;
					aremaining[bestLine] = 0.0d;
				} else {
					for (int i = 0; i < Math.ceil(aremaining[bestLine]-bestRemaining); i++) {
						System.out.println("3 " + ord + " " + abs);
					}
					if (best.size() > 0){

						aremainingC[bestLine] *= bestRemaining;
						aremainingM[bestLine] *= bestRemaining;
						aremainingY[bestLine] *= bestRemaining;
						for (Integer integer : best) {
							aremainingC[bestLine] += cown[integer];
							aremainingM[bestLine] += mown[integer];
							aremainingY[bestLine] += yown[integer];
						}
						aremainingC[bestLine] /= (bestRemaining+best.size());
						aremainingM[bestLine] /= (bestRemaining+best.size());
						aremainingY[bestLine] /= (bestRemaining+best.size());
						aremaining[bestLine] = bestRemaining + (best.size()-1);
					}	

				}

				int size = best.size();
				for (Integer integer : best) {
					if (destroy) {
						aremainingC[bestLine] += cown[integer];
						aremainingM[bestLine] += mown[integer];
						aremainingY[bestLine] += yown[integer];
					}
					System.out.println("1 " + ord + " " + abs + " " + integer);
				}
				if (destroy) {
					aremainingC[bestLine] /= size;
					aremainingM[bestLine] /= size;
					aremainingY[bestLine] /= size;
					aremaining[bestLine] = size - 1.0d;
				} else if (best.size() == 0){
					double i = bestRemaining / aremaining[bestLine];
					aremainingC[bestLine] *= i;
					aremainingM[bestLine] *= i;
					aremainingY[bestLine] *= i;
					aremaining[bestLine] = bestRemaining - 1.0d;
				}
				System.out.println("2 " + ord + " " + abs);
			}	
        }
    }
}
