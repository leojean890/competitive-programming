
import sys

planches = [int(i) for i in input().split()]
m = min(planches)
M = max(planches)

low, high = m-1, M+1
low, high = 1, 1000*(M+1)
low, high = 10000000000000, 100000000000000
result = high

while low <= high:
    mid = (low + high) // 2
    nb = 0
    for planche in planches:
        nb += planche // mid
    if nb < 1000000:
        high = mid - 1
    else: # on augmente la taille car c'est passé au dessus du million avec la taille préc
        low = mid + 1
        result = mid # car ce côté est bon

print(result) #47643645070124
