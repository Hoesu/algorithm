"""
시각
- 정수 N이 입력되면 00시 00분 00초부터 N시 59분 59초까지의 모든 시각 중에서 3이 하나라도 포함되는 모든 경우의 수를 구하는 프로그램을 작성하라.
- 첫째 줄에 정수 N이 입력된다. (0<=N<=23)
"""

import sys

N = int(sys.stdin.readline().strip())

def included(num_string:str) -> int():
    if '3' in num_string:
        return True

count=0

for h in range(N+1):
    for m in range(60):
        for s in range(60):
            num_string = str(h)+str(m)+str(s)
            if included(num_string):
                count+=1

print(count)