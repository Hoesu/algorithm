""" AI 로봇청소기 / 20260930 / 체감 난이도: G3
소요 시간 2시간 / 시도 1회 / 실행 시간 139ms (코드트리) / 메모리 20MB (코드트리)

[구상]
    - 인정하기 싫지만, 좋은 문제라는 생각이 들었다.
    - 겉으로 보면 매우 간단한 구현 문제이고, 까보면 몇가지 더러운 엣지가 숨어있는 화전양면전술의 대가.
    - 구상 단계에서 생각해둬야 하는 예외 케이스를 몇가지 나열해보면 다음과 같다.
        1) 오염된 격자 전멸: 먼지 총합이 한번 0이 되면 끝날 때까지 먼지는 늘어나지 않는다.
        2) 현재 청소기 위치에 이미 먼지 존재: BFS에서 기본적으로 처리되긴 하지만, 시작 조건 체크는 중요하다.
        3) 1회 최대 청소량 초과하는 먼지량은 따지지 않음: "한번에 청소할 수 있는"이라는 공포스러운 워딩이 있다.
        4) 먼지가 물건으로 둘러쌓여 있다: 무슨 짓을 해도 청소가 불가능하여 먼지 무한증식
        5) 로봇이 물건으로 둘러쌓여 있다: 무슨 짓을 해도 청소가 불가능하여 먼지 무한증식
    - 문제 내용 정리본을 기반으로 주석 설계를 진행하면서 아차, 싶었던 구간이 여러번 나올 정도로 교묘하게 느껴졌다.
    - 기출을 풀면서 하도 뚜드려 맞아서 그런지, 경험적으로 예외 케이스들을 잡아냈지 않나 싶다.
    - 시간 초과의 가능성도 염두에 두고 풀이를 진행해야 했다.
        - 로봇 청소기 수는 많은데, 물건으로 막혀있는 로봇이 많을 경우, 우선순위 BFS의 조기종료가 불가능한 상황이 빈번하게 발생한다.
        - 다만 BFS 조기종료와 0 무한 출력 케이스를 제외한 최적화 솔루션이 떠오르지 않았고, 구상 단계에서 지나친 묘수 탐색은 자제하고자 했다.
        - 그 결과, 먼지의 축적과 확산 단계에서 뺀질거리지 않고 건실하게 완탐하기로 했다.

[구현]
    - 철저하게 루틴을 따라서 설계 후 코드를 작성했다.
    - 우선순위 BFS를 특히 신경 써서 작성하였다.
    - 청소 함수도 루프 횟수 줄이겠답시고 나댈 수 있었지만, 최대한 안전하게 작동하도록 구현하였다.
    - 주석을 잘 달아두고 막상 구현 단계에서 빼먹는 경우가 종종 있다.
        - 실행부에서 주석 단물 다 빨아먹고, 함수 짤 때 함수 기능에 해당하는 주석만 위로 가져와서 복기하며 코드를 작성했다.
        - 앞으로도 동일한 방식으로 진행하는 것이 좋을것 같아서 루틴을 수정했다.

[디버깅]
    - 오픈 테케를 가지고 디버깅하며 독해 실수를 잡아냈다.
        - 처음에는 1번 로봇 이동 -> 1번 로봇 청소 -> 2번 로봇 이동 -> ... 과 같은 방식으로 생각했다.
        - 알고보니 모든 로봇을 순서대로 이동시키고, 다시 모든 로봇에게 순서대로 청소 명령을 내려야 했다.
        - 문제에서 명시를 하진 않지만, 굳이 단계를 나누어 설명한 것으로 보아 내 책임이 더 크다고 볼 수 있다.
    - 값이 정답보다 미세하게 크게 나와서, -1로 표시된 물건 위치가 덮어쓰기 당했을 수 있겠다는 직감이 들었다.
        - 나의 최대 약점을 파악하고, 뭔가 잘못 되었을 때 그 부분부터 의심 해보는 것이 정말 유용한 것 같다. 체크리스트가 이래서 필요한 것.
        - 브레이크 포인트 찍어둔 부분을 차례대로 읽다보니, 아니나 다를까 청소 함수에서 실수한 것이 드러났다.
    - 팀원들과 같은 시간에 제출하기로 미리 말을 맞춰뒀기에, 남은 시간 동안은 소형 케이스, 대형 케이스를 전부 만들어서 돌려봤다.
        - 소형 케이스는 내가 파악한 예외 상황들을 전부 테스트하는 용도로 사용했다.
        - 대형 케이스는 답은 모르겠고, 그냥 시간초과 체크하는 용도로 사용했다.
            - 위에서 말했던 탈출 불가능한 로봇이 많은 경우를 만들어서 돌렸다.

[후기]
    - 무서운 문제다. 시험장에선 마주치고 싶지 않다.
    - 운의 요소가 꽤 크다고 느껴진다. 에외 상황이 보이냐, 안보이느냐.
"""
from collections import deque


def debug(t, msg):
    if DEBUG_MODE:
        print()
        print(msg)
        print(f'STEP {t}: DUST STATUS')
        for x in geography:
            print(*x)
        print()
        print(f'STEP {t}: BOT STATUS')
        for x in occupation:
            print(*x)
        print('-----')


def move(sx, sy, si):
    # TODO: MOVE
    #   우선순위: (이동 거리(+), 행(+), 열(+)) [DONE]
    #   통행 불가: 물건, 다른 청소기 [DONE]
    #   시간 초과 위험: 조기 종료 필수 [DONE]
    #   예외 케이스 1: 오염된 격자 전멸. [CHECKED]
    #   예외 케이스 2: 현재 청소기 위치에 이미 먼지 존재. [CHECKED]
    que = deque()
    que.append((sx, sy))
    vst = [[-1] * N for _ in range(N)]
    vst[sx][sy] = 0
    candidates = []
    threshold = N**3

    while que:
        cx, cy = que.popleft()
        if vst[cx][cy] > threshold:
            break
        if geography[cx][cy] > 0:
            threshold = vst[cx][cy]
            candidates.append((vst[cx][cy], cx, cy))

        for cd in range(4):
            nx = cx + DR[cd]
            ny = cy + DC[cd]
            if not(0 <= nx < N and 0 <= ny < N):
                continue
            if vst[nx][ny] != -1:
                continue
            if geography[nx][ny] == -1:
                continue
            if occupation[nx][ny] > 0:
                if occupation[nx][ny] != si:
                    continue
            que.append((nx, ny))
            vst[nx][ny] = vst[cx][cy]+1

    if not candidates:
        return None, None
    candidates.sort(key=lambda z: [z[0], z[1], z[2]])
    _, x, y = candidates[0]
    return x, y


def clean(sx, sy):
    # TODO: CLEAN
    #   현재 위치, 방향 기준: 상, 하, 좌, 우 먼지량 계산 (상한 20) [DONE]
    #   현재 방향 기준: 'ㅗ'모양 탐색 영역 방향 인덱스로 설정 [DONE]
    #   각 탐색 영역에 대해 (청소할 수 있는 먼지량(-), 방향 인덱스(+)) 정렬 [DONE]
    #   우선 순위 최고 영역에 대하여 먼지 최대 20 차감, 0 바닥 보장. (덮어쓰기 주의) [DONE]
    #   예외 케이스 3: 1회 최대 청소량 초과하는 먼지량은 따지지 않음. [CHECKED]
    dusts = [0, 0, 0, 0]
    for cd in range(4):
        nx, ny = sx + DR[cd], sy + DC[cd]
        if not(0 <= nx < N and 0 <= ny < N):
            continue
        if geography[nx][ny] <= 0:
            continue
        dusts[cd] = min(20, geography[nx][ny])

    candidates = []
    for cd in range(4):
        stt = dusts[cd]
        lft = dusts[(cd-1) % 4]
        rgt = dusts[(cd+1) % 4]
        candidates.append([stt + lft + rgt, cd])
    candidates.sort(key=lambda z: [-z[0], z[1]])
    _, bd = candidates[0]

    geography[sx][sy] = max(0, geography[sx][sy]-20)
    for cd in [bd, (bd-1) % 4, (bd+1) % 4]:
        nx, ny = sx + DR[cd], sy + DC[cd]
        if not (0 <= nx < N and 0 <= ny < N):
            continue
        if geography[nx][ny] > 0:
            geography[nx][ny] = max(0, geography[nx][ny]-20)


if __name__ == '__main__':
    DEBUG_MODE = False
    DR = [0, 1, 0, -1]
    DC = [1, 0, -1, 0]

    N, K, L = map(int, input().split())
    geography = [list(map(int, input().split())) for _ in range(N)]
    occupation = [[0] * N for _ in range(N)]

    # 기억해라, 로봇 인덱스와 배열에 찍은 수는 1 차이
    robots = []
    for i in range(1, K+1):
        r, c = map(lambda x: int(x)-1, input().split())
        occupation[r][c] = i
        robots.append([r, c])

    time = 0
    last = None

    for _ in range(L):
        # TODO: 무의미한 연산 방지
        #   last 값이 0이면, 앞으로도 먼지는 존재할 수 없음.
        if last and last == 0:
            print(0)
            continue

        for i in range(K):
            # TODO: i번째 청소기 이동
            #   REDIRECT TO FUNCTION: MOVE
            cr, cc = robots[i][0], robots[i][1]
            nr, nc = move(cr, cc, i+1)
            if nr is None and nc is None:
                continue

            robots[i][0] = nr
            robots[i][1] = nc
            occupation[cr][cc] = 0
            occupation[nr][nc] = i+1

        for i in range(K):
            # TODO: i번째 청소
            #   REDIRECT TO FUNCTION: CLEAN
            cr, cc = robots[i][0], robots[i][1]
            clean(cr, cc)

        # TODO: 먼지 축적
        #   오염된 칸 + 5
        for cr in range(N):
            for cc in range(N):
                if geography[cr][cc] > 0:
                    geography[cr][cc] += 5

        # TODO: 먼지 확산
        #   깨끗한 칸 + (인접 4방향 먼지 합) // 10
        delta = [[0] * N for _ in range(N)]
        for cr in range(N):
            for cc in range(N):
                if geography[cr][cc] == 0:
                    dust_sum = 0
                    for d in range(4):
                        nr = cr + DR[d]
                        nc = cc + DC[d]
                        if not(0 <= nr < N and 0 <= nc < N):
                            continue
                        if geography[nr][nc] <= 0:
                            continue
                        dust_sum += geography[nr][nc]
                    delta[cr][cc] += dust_sum // 10

        # TODO: 출력
        #   동시 변화량 더해주며 격자 내 먼지 합 출력
        #   가장 최근 출력값 업데이트
        answer = 0
        for cr in range(N):
            for cc in range(N):
                geography[cr][cc] += delta[cr][cc]
                answer += max(0, geography[cr][cc])
        time += 1
        last = answer
        print(answer)
