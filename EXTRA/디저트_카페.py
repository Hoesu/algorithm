""" 디저트 카페 / 20261007 / 체감 난이도: G5
소요 시간 28분 / 시도 1회 / 실행 시간 336ms (SWEA) / 메모리 63,104KB (SWEA)

종전의 열화판. 쉽다.
"""


def travel(sr, sc, i, j):
    food = set()
    for d, t in enumerate((i, j, i, j)):
        for _ in range(t):
            nr, nc = sr+DR[d], sc+DC[d]
            if not(0 <= nr < N and 0 <= nc < N):
                return False
            if cafe[nr][nc] in food:
                return False
            food.add(cafe[nr][nc])
            sr, sc = nr, nc
    return True


if __name__ == '__main__':
    DR = [-1, -1, 1, 1]
    DC = [1, -1, -1, 1]

    TEST_CASE = int(input())
    for TC in range(1, TEST_CASE+1):
        print(f'#{TC}', end=' ')

        N = int(input())
        cafe = [list(map(int, input().split())) for _ in range(N)]
        candidates = []

        for r in range(2, N):
            for c in range(1, N-1):
                for p in range(2, max(r, c)+1):
                    for q in range(1, p):
                        if travel(r, c, q, p-q):
                            candidates.append(p*2)

        if not candidates:
            print(-1)
        else:
            candidates.sort()
            print(candidates[-1])
