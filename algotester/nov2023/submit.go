package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
    "math/rand"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	scanner.Scan()
	n, _ := strconv.Atoi(scanner.Text())

	startTime := time.Now()
	clusters := make(map[[3]int][][2]float64)
	clustersInitRsrpMoy := make(map[[3]int]float64)
	clustersInitRsrpWCMoy := make(map[[3]int]float64)

	for i := 0; i < n; i++ {
		scanner.Scan()
		inputs := strings.Fields(scanner.Text())

		cellID, _ := strconv.Atoi(inputs[1])
		gridIDX, _ := strconv.Atoi(inputs[3])
		gridIDY, _ := strconv.Atoi(inputs[4])
		rsrp, _ := strconv.Atoi(inputs[5])
		var frsrp float64 = float64(rsrp)


		clusterKey := [3]int{cellID, gridIDX, gridIDY}
		clusters[clusterKey] = append(clusters[clusterKey], [2]float64{frsrp, float64(i+1)})
		clustersInitRsrpMoy[clusterKey] += frsrp

		if rsrp < -105 {
			clustersInitRsrpWCMoy[clusterKey] += 1
		}
	}

	for cluster, _ := range clustersInitRsrpMoy {
		var flen float64 = float64(len(clusters[cluster]))

		clustersInitRsrpMoy[cluster] /= flen
		clustersInitRsrpWCMoy[cluster] /= flen
	}

	clustersValues := make([][][2]float64, 0, len(clusters))
	clustersKeys := make([][3]int, 0, len(clusters))

	for key, value := range clusters {
		clustersKeys = append(clustersKeys, key)
		clustersValues = append(clustersValues, value)
	}

	L := len(clustersKeys)
	var LL float64 = float64(L)

	chosenIndexes := make([]int, 0)

	for depth := 0; depth < L; depth++ {
		M := math.SmallestNonzeroFloat64
		var bestIndexes []int

		cluster := clustersKeys[depth]
		var initnElements float64 = float64(len(clustersValues[depth]))

		for _, rsrpIndex := range clustersValues[depth] {
			rsrp, index := rsrpIndex[0], rsrpIndex[1]
			var nwc float64 = 0.0
			if rsrp < -105 {
				nwc = 1.0
			}
			err := math.Abs(rsrp - clustersInitRsrpMoy[cluster])
			errWc := math.Abs(clustersInitRsrpWCMoy[cluster] - nwc)
			var sc float64 = 0.0
			if err < 10 {
				sc = 1 - err/10
			}
			var scWc float64 = 0.0
			if errWc < 0.2 {
			    scWc = 1 - errWc/0.2
			}
			var score float64 = (sc + scWc) * math.Min(initnElements, 20.0)

			if score > M {
				M = score
				bestIndexes = []int{int(index)}
			}
		}

		var fdpth float64 = float64(depth+1)

		for time.Since(startTime).Seconds() < 9.5*fdpth/LL {
			clusterV := make([][2]float64, len(clustersValues[depth]))
			copy(clusterV, clustersValues[depth])

			moy := clustersInitRsrpMoy[cluster]
			moyWC := clustersInitRsrpWCMoy[cluster]
			nElements := float64(len(clusterV))

			for nElements > 2 {

				currSum := moy * nElements
				currSumWC := moyWC * nElements
				rindex := randomIndex(len(clusterV))
				rsrpIndex := clusterV[rindex]
				rsrp := rsrpIndex[0]

				moy = (currSum - rsrp) / (nElements-1)
				if rsrp < -105 {
					moyWC = (currSumWC - 1) / (nElements-1)
				} else {
					moyWC = currSumWC / (nElements-1)
				}

				err := math.Abs(moy - clustersInitRsrpMoy[cluster])
				errWc := math.Abs(clustersInitRsrpWCMoy[cluster] - moyWC)
			        var sc float64 = 0
			        if err < 10 {
			            sc = 1 - err/10
			        }
			        var scWc float64 = 0
			        if errWc < 0.2 {
			            scWc = 1 - errWc/0.2
			        }
			    	var score float64 = (sc + scWc) * math.Min(initnElements/(nElements-1), 20.0)

				if score > M {
					M = score
					bestIndexes = make([]int, 0, len(clusterV)-1)
					for _, arsrpIndex := range clusterV {
						if arsrpIndex != rsrpIndex {
							bestIndexes = append(bestIndexes, int(arsrpIndex[1]))
						}
					}
				}

				if time.Since(startTime).Seconds() > 9.5*fdpth/LL {
					break
				}

				clusterV = append(clusterV[:rindex], clusterV[rindex+1:]...)

				nElements--
			}
		}
		chosenIndexes = append(chosenIndexes, bestIndexes...)
	}

	fmt.Println(len(chosenIndexes))

	for i, j := range chosenIndexes {
		if i > 0 {
			fmt.Print(" ")
		}
		fmt.Print(j)
	}
}

func randomIndex(length int) int {
	return rand.Intn(length)
}


