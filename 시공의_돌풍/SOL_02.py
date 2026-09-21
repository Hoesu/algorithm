""" 시공의 돌풍 / 20260917 / 체감 난이도: S1
소요 시간 36분 / 시도 1 / 실행 시간 422ms (코드트리) / 메모리 24MB (코드트리)

시공의 돌풍님, 당신이 없었다면 저는 강해질 수 없었을 것입니다.
예전처럼 while문 써서 그냥 하는게 더 직관적이었을수도?
그래도 방향 벡터에 대한 숙련도가 올라 이런식으로도 쉽게 구현할 수 있다는 사실이 기쁘다.
"""


def find_storm():
    for cr in range(R):
        if arr[cr][0] == -1:
            arr[cr][0] = 0
            arr[cr+1][0] = 0
            return cr, cr+1


def spread():
    delta = [[0] * C for _ in range(R)]
    for cr in range(R):
        for cc in range(C):
            # 돌풍은 무시
            if cr in (up, lo) and cc == 0:
                continue
            for i in range(4):
                nr = cr + directions[i][0]
                nc = cc + directions[i][1]
                if not(0 <= nr < R and 0 <= nc < C):
                    continue
                if nr in (up, lo) and nc == 0:
                    continue
                diff = arr[cr][cc] // 5
                delta[nr][nc] += diff
                delta[cr][cc] -= diff

    for cr in range(R):
        for cc in range(C):
            arr[cr][cc] += delta[cr][cc]


def clean():
    up_corners = {(0, 0), (0, C-1), (up, C-1)}
    cr, cc, cd = up-1, 0, 0
    while True:
        if (cr, cc) in up_corners:
            nd = (cd+1) % 4
        else:
            nd = cd
        nr = cr + directions[nd][0]
        nc = cc + directions[nd][1]
        arr[cr][cc] = arr[nr][nc]
        cr, cc, cd = nr, nc, nd
        if cr == up and cc == 0:
            break

    lo_corners = {(R-1, 0), (R-1, C-1), (lo, C-1)}
    cr, cc, cd = lo+1, 0, 2
    while True:
        if (cr, cc) in lo_corners:
            nd = (cd-1) % 4
        else:
            nd = cd
        nr = cr + directions[nd][0]
        nc = cc + directions[nd][1]
        arr[cr][cc] = arr[nr][nc]
        cr, cc, cd = nr, nc, nd
        if cr == lo and cc == 0:
            break


if __name__ == '__main__':
    R, C, T = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(R)]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    up, lo = find_storm()

    for _ in range(T):
        spread()
        clean()

    print(sum(map(sum, arr)))


""" 시공의 돌풍 / 20260821 / 체감 난이도: S1
소요 시간 INF / 시도 INF / 실행 시간 422ms (코드트리) / 메모리 24MB (코드트리)

[구상]
    - 첫 문제부터 잘 풀고 싶어서 23분 정도 구상에 힘썼다. 결론적으론 참패했지만...
    - 일단 어떤 방식을 써도 먼지 확산 단계는 N 제곱의 시간이 걸릴 수 밖에 없다고 생각했다.
    - 돌풍으로 확산되지 않아야 한다는 점, 모든 구역의 확산이 끝난 후에 먼지 변화량을 더해줘야 한다는 점에 집중했다.
    - 마지막으로 먼지가 돌풍으로 빨려들어가는 형태가 수없이 풀었던 달팽이 모양과 같다는 것을 파악했고, while문 4개씩 돌려야 겠다는 생각을 했다.

[구현]
    - 33분 정도 걸려서 내 기준 꽤 빠르게 구현을 마쳤다.
    - 특히 청소 관련 함수들은 범위 실수가 치명적이기에 하나 하나 디버깅 찍어가면서 함수 완성했다.

[디버깅]
    - 굉장히 자신 있게 풀었는데 시간 초과가 나서 살짝 당황스러웠지만, 시험 시간은 길고 남은 문제도 있어서 나중에 돌아와서 보기로 했다.
    - 나머지 두 문제도 1승 1패를 한 상황에서 다시 시간 초과의 원인을 분석해봤다.
        - 확실한건 청소 단계의 while문이 시간 초과의 원인일 수 없다고 생각했다.
        - 그렇다면 확산 함수가 잘못 되었다는 건데, 별 의미가 없을거라는걸 알면서도 que로 구현해보고, 별 짓을 다했다.
        - 결국 원흉을 잡아내지 못하고 제출에 실패하였다.

[후기]
    - 야자 시간에 확산함수를 다시 살펴보면서 다르게 표현할 수 있는 부분은 없나 살펴봤다.
    - 그러다보니 먼지 // 5가 0이 되는 경우는 나머지 연산을 하지 않아도 된다는 점을 발견했고, 수정해봤으나 여전히 시간초과였다.
    - 결국 이유를 알아내긴 했는데, 돌풍 지역을 방문하는 것을 방지하기 위해 튜플 좌표의 리스트에 in 연산을 수행하는 부분이었다.
        - (현재x, 현재y) in [upper, lower] 이런식으로 했었다.
        - 코드 짧게 쓰고 싶어서 in 연산을 활용해봤던 것인데, 이 과정에서 리스트와 튜플을 매번 새로 만드는 비용이 든다고 한다.
        - 또한, 해당 연산을 멍청하게 2번씩이나 하고 있었다.
        - 조건 잘 체크해서 돌풍 지역을 갈 수 없도록 처리해놓고, 그래도 걱정됐는지 루프 바깥에서도 똑같은 체크를 했다.
        - 다음부터는 귀찮더라도 set에 대해서 in 연산을 하거나, 그냥 다이렉트로 대조해보자.
"""


def spread(u, l):
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    # 확산에 의해 추가해야 하는 먼지 저장 배열
    add = [[0] * C for _ in range(R)]

    for cr in range(R):
        for cc in range(C):
            # 확산할 먼지 없으면 패스
            delta = arr[cr][cc] // 5
            if delta == 0:
                continue
            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]
                # 범위 벗어나면 무시
                if not(0 <= nr < R and 0 <= nc < C):
                    continue
                # 시공의 돌풍에는 확산되지 않음
                if (nr == u[0] and nc == u[1]) or (nr == l[0] and nc == l[1]):
                    continue
                # 다음 칸에 확산 추가
                add[nr][nc] += delta
                # 현재 칸에 확산 제거
                arr[cr][cc] -= delta

    # 확산 계산 끝나면 변화 적용
    for cr in range(R):
        for cc in range(C):
            arr[cr][cc] += add[cr][cc]


def clean_upper(u):
    # 북, 동, 남, 서
    ur, uc = u[0]-1, u[1]
    while ur > 0:
        arr[ur][uc] = arr[ur-1][uc]
        ur -= 1
    while uc < C-1:
        arr[ur][uc] = arr[ur][uc+1]
        uc += 1
    while ur < u[0]:
        arr[ur][uc] = arr[ur+1][uc]
        ur += 1
    while uc > u[1]+1:
        arr[ur][uc] = arr[ur][uc-1]
        uc -= 1
    arr[ur][uc] = 0


def clean_lower(l):
    # 남, 동, 북, 서
    lr, lc = l[0]+1, l[1]
    while lr < R-1:
        arr[lr][lc] = arr[lr+1][lc]
        lr += 1
    while lc < C-1:
        arr[lr][lc] = arr[lr][lc+1]
        lc += 1
    while lr > l[0]:
        arr[lr][lc] = arr[lr-1][lc]
        lr -= 1
    while lc > l[1]+1:
        arr[lr][lc] = arr[lr][lc-1]
        lc -= 1
    arr[lr][lc] = 0


if __name__ == '__main__':
    R, C, T = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(R)]

    # 시공의 돌풍 윗칸, 아랫칸 찾기 (0열)
    upper = None
    lower = None
    for r in range(R):
        if arr[r][0] == -1:
            arr[r][0] = 0
            arr[r+1][0] = 0
            upper = (r, 0)
            lower = (r+1, 0)
            break

    # T초 동안
    for _ in range(T):
        # 확산
        spread(upper, lower)
        # 청소 (달팽이 움직임)
        clean_upper(upper)
        clean_lower(lower)
    # 먼지 합 출력
    print(sum([sum(row) for row in arr]))
