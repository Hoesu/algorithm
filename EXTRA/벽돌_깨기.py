""" 벽돌 깨기 / 20261007 / 체감 난이도: G5
소요 시간 30분 / 시도 1회 / 실행 시간 567ms (SWEA) / 메모리 75,392KB (SWEA)

또트래킹. 그래도 중력 BFS 연습할 수 있다.
"""

from collections import deque


def find_start(arr, i):
    for cr in range(R):
        if arr[cr][i] != 0:
            return cr, i
    return None, None


def drop_ball(arr, i):
    sr, sc = find_start(arr, i)
    if sr is None and sc is None:
        return arr, 0

    que = deque()
    que.append((sr, sc))
    vst = [[0] * C for _ in range(R)]
    vst[sr][sc] = 1
    cnt = 0

    while que:
        cr, cc = que.popleft()
        cv = arr[cr][cc]
        arr[cr][cc] = 0
        cnt += 1

        for d in range(4):
            for k in range(1, cv):
                nr, nc = cr+DR[d]*k, cc+DC[d]*k
                if not(0 <= nr < R and 0 <= nc < C):
                    continue
                if vst[nr][nc] != 0:
                    continue
                if arr[nr][nc] == 0:
                    continue
                que.append((nr, nc))
                vst[nr][nc] = 1

    for cc in range(C):
        P = R-1
        for cr in range(R-1, -1, -1):
            if arr[cr][cc] > 0:
                if cr != P:
                    arr[P][cc] = arr[cr][cc]
                    arr[cr][cc] = 0
                P -= 1
    return arr, cnt


def backtrack(arr, sm=0, step=0):
    global max_destroyed, answer
    if step == N:
        if sm > max_destroyed:
            max_destroyed = sm
            blocks_left = 0
            for r in range(R):
                for c in range(C):
                    if arr[r][c] > 0:
                        blocks_left += 1
            answer = blocks_left
        return

    for i in range(C):
        arr_copy = [x[:] for x in arr]
        arr_copy, score = drop_ball(arr_copy, i)
        backtrack(arr_copy, sm+score, step+1)


if __name__ == '__main__':
    DR = [-1, 1, 0, 0]
    DC = [0, 0, -1, 1]

    TEST_CASE = int(input())
    for TC in range(1, TEST_CASE+1):
        print(f'#{TC}', end=' ')
        N, C, R = map(int, input().split())
        board = [list(map(int, input().split())) for _ in range(R)]

        answer = None
        max_destroyed = 0
        backtrack(board)
        print(answer)
