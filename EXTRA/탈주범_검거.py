""" 탈주범 검거 / 20261007 / 체감 난이도: G5
소요 시간 30분 / 시도 1회 / 실행 시간 163ms (SWEA) / 메모리 62,208KB (SWEA)

파이프 연결 신경 써야 한다.
"""
from collections import deque


def get_next(cr, cc, arr):
    v = arr[cr][cc]
    if v == 1:
        return [0, 1, 2, 3]
    elif v == 2:
        return [0, 1]
    elif v == 3:
        return [2, 3]
    elif v == 4:
        return [0, 3]
    elif v == 5:
        return [1, 3]
    elif v == 6:
        return [1, 2]
    else:
        return [0, 2]


def is_connected(cd, nr, nc, arr):
    if arr[nr][nc] == 1:
        return True
    if cd == 0 and arr[nr][nc] in (2, 5, 6):
        return True
    elif cd == 1 and arr[nr][nc] in (2, 4, 7):
        return True
    elif cd == 2 and arr[nr][nc] in (3, 4, 5):
        return True
    elif cd == 3 and arr[nr][nc] in (3, 6, 7):
        return True
    else:
        return False


if __name__ == '__main__':
    DR = [-1, 1, 0, 0]
    DC = [0, 0, -1, 1]

    TEST_CASE = int(input())
    for TC in range(1, TEST_CASE+1):
        print(f'#{TC}', end=' ')

        N, M, R, C, L = map(int, input().split())
        sewer = [list(map(int, input().split())) for _ in range(N)]
        que = deque()
        que.append((R, C))
        vst = [[-1] * M for _ in range(N)]
        vst[R][C] = 0

        while que:
            cr, cc = que.popleft()
            for d in get_next(cr, cc, sewer):
                nr, nc = cr+DR[d], cc+DC[d]
                if not(0 <= nr < N and 0 <= nc < M):
                    continue
                if vst[nr][nc] != -1:
                    continue
                if sewer[nr][nc] == 0:
                    continue
                if not is_connected(d, nr, nc, sewer):
                    continue
                que.append((nr, nc))
                vst[nr][nc] = vst[cr][cc] + 1

        answer = 0
        for r in range(N):
            for c in range(M):
                if 0 <= vst[r][c] < L:
                    answer += 1
        print(answer)
