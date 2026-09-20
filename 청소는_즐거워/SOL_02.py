"""청소는 즐거워 / 20260920 / 체감 난이도: G4
소요 시간 23분 / 시도 1회 / 실행 시간 271ms (코드트리) / 메모리 24MB (코드트리)

실수만 하지 않으면 되는 노가다성 문제.
"""
if __name__ == '__main__':
    N = int(input())
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    board = [list(map(int, input().split())) for _ in range(N)]
    out_of_bound = 0
    cr, cc, cd = N//2, N//2, 0

    check = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if r + c < N - 1 and r - c == 1:
                check[r][c] = 1
            if r - c < 0 and r + c == N - 1:
                check[r][c] = 1
            if r + c > N - 1 and r - c == 0:
                check[r][c] = 1
            if r - c > 0 and r + c == N - 1:
                check[r][c] = 1

    while True:
        # 종료 조건
        if cr == 0 and cc == 0:
            break

        # 위치와 방향 업데이트
        nr = cr + directions[cd][0]
        nc = cc + directions[cd][1]
        nd = (cd + 1) % 4 if check[nr][nc] == 1 else cd

        # 이동한 위치에 원래 있던 먼지
        dust = board[nr][nc]

        # 상대적 방향: 진행 방향 기준 위, 아래
        udr, udc = directions[(cd+1) % 4]
        ldr, ldc = directions[(cd-1) % 4]

        # 먼지 흩뿌릴 위치 계산
        candidates = [
            (cr+udr, cc+udc, dust//100),
            (cr+ldr, cc+ldc, dust//100),
            (nr+udr, nc+udc, 7*dust//100),
            (nr+ldr, nc+ldc, 7*dust//100),
            (nr+udr*2, nc+udc*2, 2*dust//100),
            (nr+ldr*2, nc+ldc*2, 2*dust//100),
            (nr+directions[cd][0]+udr, nc+directions[cd][1]+udc, dust//10),
            (nr+directions[cd][0]+ldr, nc+directions[cd][1]+ldc, dust//10),
            (nr+directions[cd][0]*2, nc+directions[cd][1]*2, 5*dust//100),
            (nr+directions[cd][0], nc+directions[cd][1], None),
        ]

        # 먼지 흩뿌리기
        for r, c, amount in candidates:
            if not(0 <= r < N and 0 <= c < N):
                if amount is None:
                    out_of_bound += dust
                    continue
                out_of_bound += amount
                dust -= amount
                continue
            if amount is None:
                board[r][c] += dust
            else:
                board[r][c] += amount
                dust -= amount

        # 다음 라운드 준비
        cr, cc, cd = nr, nc, nd

    # 정답 출력
    print(out_of_bound)


"""청소는 즐거워 / 20260826 / 체감 난이도: G4
소요 시간 1시간 31분 / 시도 1회 / 실행 시간 263ms (코드트리) / 메모리 25MB (코드트리)

[구상]
    - 수능 국어 9등급이 작성한 문제인건 확실하다. 일단 모두를 헷갈리게 만든 알파 설명 부분에서 뇌정지가 왔다.
    - 구상을 30분 넘게 했는데, 아무리 읽어도 지문으로는 이해가 불가능해서 예제를 손으로 직접 그려봤다.
    - 예제를 그리고 나서 문제를 명확하게 이해하였고, '//' 연산 특성상 소수점 아래는 다 버리기 때문에 알파 값이 55%로 딱 맞아떨어질리가 없었다.
    - 그래서 최대한 안전하게 먼지 * 비중 // 100으로 뿌릴 값 계산하고, 원래 먼지양에서 뿌린 양을 빼주기로 했다.
    - 먼지양도 먼지양인데, 회오리 방식으로 움직이는 방식도 어떻게 구현할지 고민을 오래했다.
        - 피보나치 배열 같기도 하고.. 하면서 보다보니 11223344 규칙이 눈에 들어왔고, N값에 따라서 패턴이 어떻게 변하는지 확실하게 체크했다.

[구현]
    - 구상 단계에서 워낙 철저하게 생각하고 넘어가서 그런지, 구현은 그냥저냥 할만했다.
    - 회오리 이동, 먼지 흩뿌리기 등을 개별적으로 검증하는 과정을 굉장히 길게 가져갔다.
    - 전역 변수 활용도 괜찮았던 것 같고, 먼지 뿌려줄 위치도 벡터 연산으로 직관적으로 구현한 것은 잘한것 같다.

[디버깅]
    - 개별 기능 단계에서 워낙 확실하게 검증했기 때문에 그냥 바로 제출했다.

[후기]
    - GSAT 도형추리 문제를 코딩으로 푸는 기분이었다.
"""


def brush(r, c, drc):
    # 전역 변수 선언
    global oob
    global cur_r, cur_c

    # 현재 바라보고 있는 방향
    dr, dc = directions[drc]
    # 이동한 위치에 있던 먼지 별도 저장
    origin = arr[r+dr][c+dc]
    # 이동한 위치에 먼지가 없었다면 조기 종료
    if origin == 0:
        cur_r += dr
        cur_c += dc
        return

    # 이동한 위치에 있었던 먼지 제거하기
    arr[r+dr][c+dc] = 0

    # 현재 방향 기준 왼쪽, 오른쪽 방향 벡터 가져오기
    lr, lc = directions[(drc + 1) % 4]
    rr, rc = directions[(drc - 1) % 4]

    # 문제 조건에 맞춰 계산해줍시다.
    # 혹시 모르니까 곱셈 먼저하고 나눠주기
    p_1 = (origin * 1) // 100
    p_2 = (origin * 2) // 100
    p_5 = (origin * 5) // 100
    p_7 = (origin * 7) // 100
    p_10 = (origin * 10) // 100
    p_alpha = origin - p_1*2 - p_2*2 - p_5 - p_7*2 - p_10*2

    # 행, 열, 추가할 값을 튜플 리스트로 정리합니다.
    # 항상 오타 안나게 조심하고, 함수 빡세게 검증 돌려야함.
    to_distribute = [
        (r+lr, c+lc, p_1),
        (r+rr, c+rc, p_1),
        (r+lr*2+dr, c+lc*2+dc, p_2),
        (r+rr*2+dr, c+rc*2+dc, p_2),
        (r+dr*3, c+dc*3, p_5),
        (r+lr+dr, c+lc+dc, p_7),
        (r+rr+dr, c+rc+dc, p_7),
        (r+lr+dr*2, c+lc+dc*2, p_10),
        (r+rr+dr*2, c+rc+dc*2, p_10),
        (r+dr*2, c+dc*2, p_alpha)
    ]

    # 만들어둔 리스트를 순회
    for nr, nc, val in to_distribute:
        # 새로운 좌표가 범위 안이면 원본 배열에 먼지 추가
        if 0 <= nr < N and 0 <= nc < N:
            arr[nr][nc] += val
        # 범위 바깥으로 떨어지면 따로 합산
        else:
            oob += val

    # 청소했으니까 현재 위치 업데이트하고 종료.
    cur_r += dr
    cur_c += dc


if __name__ == '__main__':
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]

    # 범위 바깥 먼지의 양 (Out Of Bound)
    oob = 0
    # 현재 진행 중인 루프 번호
    step = 0
    # 청소 중 발생하는 루프 횟수
    num_loops = N//2
    # 시작 위치는 항상 중간이다.
    cur_r, cur_c = N//2, N//2
    # 요긴하게 쓰일 방향 벡터 리스트 (서, 남, 동, 북)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    # N의 값에 따라서 청소 방향은 다음과 같이 이어진다.
    # 1 1 2 2 3 3 4 4 ... + 짜투리 서쪽 청소
    for _ in range(num_loops):
        # 서
        for _ in range(step+1):
            brush(cur_r, cur_c, 0)
        # 남
        for _ in range(step+1):
            brush(cur_r, cur_c, 1)
        # 동
        for _ in range(step+2):
            brush(cur_r, cur_c, 2)
        # 북
        for _ in range(step+2):
            brush(cur_r, cur_c, 3)
        step += 2
    # 서
    for _ in range(step):
        brush(cur_r, cur_c, 0)
    # 정답 출력
    print(oob)
