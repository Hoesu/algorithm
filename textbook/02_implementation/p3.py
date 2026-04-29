"""
왕실의 나이트
- 8x8 좌표 평면의 특정 한칸에 나이트 기물이 서있다.
- 나이트는 L자 형태로만 이동할 수 있으며, 판 밖으로 나갈 수 없다.
- 나이트는 특정 위치에서 다음과 같은 2가지 경우로 이동할 수 있다.
- 1) 수평으로 두 칸 이동 후 수직으로 한칸 이동.
- 2) 수직으로 두 칸 이동 후 수평으로 한칸 이동.
- 체스판에서 좌표의 형태로 나이트의 위치가 주어졌을 때, 나이트가 이동할 수 있는 경우의 수를 출력하라.
- 행 위치는 1부터 8로, 열 위치는 a부터 h로 표현한다.
"""

import sys

col_dict = {
    'a':1,
    'b':2,
    'c':3,
    'd':4,
    'e':5,
    'f':6,
    'g':7,
    'h':8
}

loc = sys.stdin.readline().strip()
col_idx = int(col_dict[loc[0]])
row_idx = int(loc[1])
movesets = [1,-1,2,-2]
count=0

for row_move in movesets:
    for col_move in movesets:

        if abs(row_move)+abs(col_move) != 3:
            continue

        row=row_idx+row_move
        col=col_idx+col_move

        if 1<=row<=8 and 1<=col<=8:
            count+=1

print(count)