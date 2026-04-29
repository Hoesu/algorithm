"""
게임 개발
- 캐릭터가 있는 장소는 1x1 크기의 정사각형으로 이뤄진 NxM 크기의 직사각형이다.
- 각각의 칸은 육지 또는 바다이다.
- 캐릭터는 동서남북 중 한 곳을 바라본다.
- 맵의 각 칸은 (A,B)로 나타낼 수 있고, A는 북쪽으로부터 떨어진 칸의 개수, B는 서쪽으로부터 떨어진 칸의 개수
- 캐릭터는 상하좌우로 움직일 수 있고, 바다로 되어 있는 공간에는 갈 수 없다.
- 캐릭터의 움직임을 설정하기 위해 정해놓은 매뉴얼은 아래와 같다:
- 1) 현재 위치에서 현재 방향을 기준으로 왼쪽 방향(반시계 방향으로 90도 회전한 방향)부터 차례대로 갈 곳을 정한다.
- 2) 캐릭터의 바로 왼쪽 방향에 아직 가보지 않은 칸이 존재한다면, 왼쪽 방향으로 회전한 다음 왼쪽으로 한칸을 전진한다. 왼쪽 방향에 가보지 않은 칸이 없다면, 왼쪽 방향으로 회전만 수행하고 1단계로 돌아간다.
- 3) 만약 네 방향 모두 이미 가본 칸이거나 바다로 되어있는 칸인 경우에는, 바라보는 방향을 유지한 채로 한 칸 뒤로 가고 1단계로 돌아간다. 단, 이때 뒤쪽 방향이 바다인 칸이라 뒤로 갈 수 없는 경우에는 움직임을 멈춘다.
- 결국 캐릭터가 방문한 칸의 수를 출력하라.

- 첫째 줄에 맵의 세로 크기 N과 가로 크기 M을 공백으로 구분하여 입력한다.
- 둘째 줄에 게임 캐릭터가 있는 칸의 좌표(A,B)와 바라보는 방향 d가 각각 서로 공백으로 구분하여 주어진다.
- 방향 d의 값으로는 0:북, 1:동, 2:남, 3:서
- 셋째 줄부터 맵이 육지인지 바다인지에 대한 정보가 주어진다. N개의 줄에 맵의 상태가 북쪽부터 남쪽 순서대로, 각 줄의 데이터는 서쪽부터 동쪽 순서대로 주어진다. 맵의 외곽은 항상 바다로 되어 있다. 0:육지, 1:바다
- 처음에 게임 캐릭터가 위치한 칸의 상태는 항상 육지이다.
"""

# Test Case
# echo "4 4\n1 1 0\n1 1 1 1\n1 0 0 1\n1 1 0 1\n1 1 1 1" | python textbook/02_implementation/p4.py 

import sys

N, M = map(int, sys.stdin.readline().split())
A, B, d = map(int, sys.stdin.readline().split())

loc = [A,B]
field = []
for _ in range(N):
    row = list(map(int, sys.stdin.readline().split()))
    field.append(row)
field[loc[0]][loc[1]]=2

VISITED = 1
MOVE_DICT = {
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}

def check(loc, field):
    cand1=[x + y for x, y in zip(loc, MOVE_DICT[0])]
    cand2=[x + y for x, y in zip(loc, MOVE_DICT[1])]
    cand3=[x + y for x, y in zip(loc, MOVE_DICT[2])]
    cand4=[x + y for x, y in zip(loc, MOVE_DICT[3])]
    if (field[cand1[0]][cand1[1]]==0 or
        field[cand2[0]][cand2[1]]==0 or
        field[cand3[0]][cand3[1]]==0 or
        field[cand4[0]][cand4[1]]==0):
        return True
    else:
        return False

def forward(loc:list, d:int, field:list) -> list[list, int, list]:
    global VISITED

    if not check(loc, field):
        return backward(loc, d, field)

    d=d+3 if d==0 else d-1
    new_loc = [x + y for x, y in zip(loc, MOVE_DICT[d])]

    if field[new_loc[0]][new_loc[1]]!=0:
        return forward(loc, d, field)
    else:
        VISITED+=1
        field[new_loc[0]][new_loc[1]]=2
        return new_loc, d, field

def backward(loc: list, d: int, field: list) -> list[list, int, list]:
    global VISITED

    new_loc = [x - y for x, y in zip(loc, MOVE_DICT[d])]

    if field[new_loc[0]][new_loc[1]]==1:
        return None
    elif field[new_loc[0]][new_loc[1]]==2:
        return new_loc, d, field
    else:
        VISITED+=1
        field[new_loc[0]][new_loc[1]]=2
        return new_loc, d, field

while True:
    move = forward(loc, d, field)
    print(f'move: {move}')

    if move is None:
        break
    
    else:
        loc=move[0]
        d=move[1]
        field=move[2]

print(VISITED)