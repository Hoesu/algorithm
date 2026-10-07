""" 핀볼 게임 / 20261007 / 체감 난이도: G5
소요 시간 1시간 10분 / 시도 1회 / 실행 시간 2,766ms (SWEA) / 메모리 81,280KB (SWEA)

솔직히 문제 좀 별로다. 핀볼 이동에 대한 설명이 살짝 아쉽달까?
그냥 패딩 박고, 갈 수 없는 블럭이 없다는 전제를 깔고 방향 전환을 잘 시켜주면 해결은 가능하다.
"""


def get_next(cr, cc, cd):
    nr, nc = cr+DR[cd], cc+DC[cd]
    # 웜홀
    if (nr, nc) in wormholes:
        nr, nc = wormholes[(nr, nc)]
        return nr, nc, cd, 0
    # 빈칸
    if board[nr][nc] <= 0:
        return nr, nc, cd, 0
    # 5번 블럭
    if board[nr][nc] == 5:
        return nr, nc, (cd+2) % 4, 1

    if cd == 0:
        if board[nr][nc] in (1, 4):
            return nr, nc, (cd+2) % 4, 1
        elif board[nr][nc] == 2:
            return nr, nc, 1, 1
        elif board[nr][nc] == 3:
            return nr, nc, 3, 1
    elif cd == 1:
        if board[nr][nc] in (1, 2):
            return nr, nc, (cd + 2) % 4, 1
        elif board[nr][nc] == 3:
            return nr, nc, 2, 1
        elif board[nr][nc] == 4:
            return nr, nc, 0, 1
    elif cd == 2:
        if board[nr][nc] in (2, 3):
            return nr, nc, (cd + 2) % 4, 1
        elif board[nr][nc] == 1:
            return nr, nc, 1, 1
        elif board[nr][nc] == 4:
            return nr, nc, 3, 1
    else:
        if board[nr][nc] in (3, 4):
            return nr, nc, (cd + 2) % 4, 1
        elif board[nr][nc] == 1:
            return nr, nc, 0, 1
        elif board[nr][nc] == 2:
            return nr, nc, 2, 1


def start_game(sr, sc, sd):
    global answer
    cr, cc, cd = sr, sc, sd
    collisions = 0

    while True:
        nr, nc, nd, m = get_next(cr, cc, cd)
        collisions += m
        if board[nr][nc] == -1:
            break
        if nr == sr and nc == sc:
            break
        cr, cc, cd = nr, nc, nd

    if collisions > answer:
        answer = collisions


if __name__ == '__main__':
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]

    TEST_CASE = int(input())
    for TC in range(1, TEST_CASE+1):
        print(f'#{TC}', end=' ')

        N = int(input())
        board = [[5] * (N+2) for _ in range(N+2)]
        for r in range(1, N+1):
            board[r][1:N+1] = list(map(int, input().split()))

        temp = [[] for _ in range(11)]
        for r in range(N+2):
            for c in range(N+2):
                if 6 <= board[r][c] <= 10:
                    temp[board[r][c]].append((r, c))
                    board[r][c] = 0

        wormholes = dict()
        for i in range(6, 11):
            if temp[i]:
                wormholes[temp[i][0]] = temp[i][1]
                wormholes[temp[i][1]] = temp[i][0]

        answer = 0
        for r in range(N+2):
            for c in range(N+2):
                if board[r][c] == 0 and (r, c) not in wormholes:
                    for d in range(4):
                        start_game(r, c, d)
        print(answer)
