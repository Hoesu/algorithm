"""
큰 수의 법칙
- 다양한 수로 이루어진 배열이 있을 때 주어진 수들을 M번 더하여 가장 큰 수를 만든다.
- 단, 배열의 특정 인덱스에 해당하는 수가 연속해서 K번을 초과하여 더해질 수 없다.
- 배열의 크기 N, 숫자가 더해지는 횟수 M, 그리고 K가 주어질 때, 큰 수의 법칙에 따른 결과를 출력하라.
- 첫째 줄에 N(2<=N<=1000), M(1<=M<=10000), K(1<=K<=10000)의 자연수가 주어지며, 각 자연수는 공백으로 구분한다.
- 둘째 줄에 N개의 자연수가 주어진다. 각 자연수는 공백으로 구분한다. 단, 각각의 자연수는 1 이상 10000 이하의 수로 주어진다.
- 입력으로 주어지는 K는 항상 M보다 작거나 같다.
"""

import sys

N, M, K = map(int, sys.stdin.readline().split(' '))
arr = list(map(int, sys.stdin.readline().split()))
arr = sorted(arr, reverse=True)[:2]

call = 0
sum = 0

for i in range(M):
    if call == K:
        sum+=arr[1]
        call=0
    else:
        sum+=arr[0]
        call+=1
print(sum)

## Better Answer
div = M / (K+1)
rem = M % (K+1)

div_sum = K * arr[0] + arr[1]
rem_sum = arr[0]
total = int(div*div_sum + rem*rem_sum)
print(total)