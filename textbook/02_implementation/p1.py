"""
상하좌우
- 여행가가 NxN 크기의 정사각형 공간에서 LRUD으로 움직인다.
- 위치는 좌표계로 설명하고, 시작 좌표는 항상 (1,1)이다.
- 여행가가 정사각형 공간을 벗어나는 움직임은 무시된다.
- 첫째 줄에 공간의 크기를 나타내는 N이 주어진다 (1<=N<=100)
- 둘째 줄에 여행가 A가 이동할 계획서 내용이 주어진다 (1<=이동 횟수<=100)
"""

import sys

def check_loc(N:int, loc:list) -> bool:
    return 1 <= loc[0] <= N and 1 <= loc[1] <= N

def move(N: int, action:str, loc:list) -> list:
    test = loc.copy()
    if action=='L':
        test[1]-=1
    elif action=='R':
        test[1]+=1
    elif action=='U':
        test[0]-=1
    elif action=='D':
        test[0]+=1
    else:
        raise Exception

    if check_loc(N, test):
        return test
    else:
        return loc

N = int(sys.stdin.readline())
plan = list(sys.stdin.readline().strip().split(' '))
loc = [1,1]

for action in plan:
    loc = move(N, action, loc)
print(loc)