""" 코드트리 빵 / 20261005 / 체감 난이도: G1
소요 시간 48분 / 시도 1 / 실행 시간 57ms (코드트리) / 메모리 16MB (코드트리)

아직 최단경로와 레벨 BFS가 숙련도가 충분하지 않아서 개고생했던 문제.
이제는 너무 쉽다. 다시 풀지 않을 문제.
"""
from collections import deque


def move(sr, sc, gr, gc):
    que = deque()
    que.append((sr, sc))
    vst = [[0] * N for _ in range(N)]
    vst[sr][sc] = 1
    path = dict()

    while que:
        cr, cc = que.popleft()
        if cr == gr and cc == gc:
            break
        for d in range(4):
            nr, nc = cr + DR[d], cc + DC[d]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if vst[nr][nc] != 0:
                continue
            if field[nr][nc] == 1:
                continue
            que.append((nr, nc))
            vst[nr][nc] = 1
            path[(nr, nc)] = (cr, cc)

    nr, nc = gr, gc
    while True:
        cr, cc = path[(nr, nc)]
        if cr == sr and cc == sc:
            return nr, nc
        nr, nc = cr, cc


def find_base(sr, sc):
    que = deque()
    que.append((sr, sc))
    vst = [[0] * N for _ in range(N)]
    vst[sr][sc] = 1
    threshold = N**3
    candidates = []

    while que:
        cr, cc = que.popleft()
        if vst[cr][cc] > threshold:
            break
        if (cr, cc) in base:
            threshold = vst[cr][cc]
            candidates.append([vst[cr][cc], cr, cc])

        for d in range(4):
            nr, nc = cr + DR[d], cc + DC[d]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if vst[nr][nc] != 0:
                continue
            if field[nr][nc] == 1:
                continue
            que.append((nr, nc))
            vst[nr][nc] = vst[cr][cc] + 1

    candidates.sort(key=lambda z: (z[0], z[1], z[2]))
    _, fr, fc = candidates[0]
    return fr, fc


if __name__ == '__main__':
    DR = (-1, 0, 0, 1)
    DC = (0, -1, 1, 0)

    N, M = map(int, input().split())
    field = [list(map(int, input().split())) for _ in range(N)]

    base = set()
    for r in range(N):
        for c in range(N):
            if field[r][c] == 1:
                base.add((r, c))
                field[r][c] = 0

    in_people = dict()
    out_people = dict()
    for i in range(1, M+1):
        x, y = map(int, input().split())
        out_people[i] = [None, None, x-1, y-1]

    time = 1
    while True:
        # 플레이어 이동
        blocked = []
        for key in list(in_people.keys()):
            sr, sc, gr, gc = in_people[key]
            sr, sc = move(sr, sc, gr, gc)
            if sr == gr and sc == gc:
                in_people.pop(key)
                blocked.append((gr, gc))
            else:
                in_people[key][0] = sr
                in_people[key][1] = sc

        # 종료 체크
        if not in_people and not out_people:
            break

        # 통행 불가 처리
        for r, c in blocked:
            field[r][c] = 1

        # 플레이어 추가 고려
        if time <= M:

            # 플레이어 베이스 캠프 진입
            in_people[time] = out_people.pop(time)
            _, _, gr, gc = in_people[time]
            sr, sc = find_base(gr, gc)
            base.discard((sr, sc))
            in_people[time][0] = sr
            in_people[time][1] = sc

            # 통행 불가 처리
            field[sr][sc] = 1

        # 시간 증가
        time += 1

    # 정답 출력
    print(time)


""" 코드트리 빵 / 20260911 / 체감 난이도: G1
소요 시간 3시간 5분 / 시도 4 / 실행 시간 57ms (코드트리) / 메모리 17MB (코드트리)

[구상]
    - 안하던 행동 1) BFS로 최단 경로 뽑는 방법이 갑자기 떠오르지 않아서 다익스트라 소환함.
        - BFS로 최단거리 뽑는 것은 익숙한데, 갑자기 경로를 뽑아오라니까 잘 생각이 나지 않았다.
        - 백트래킹도 떠오르긴 했으나, 아무리 경우의 수를 쳐낸다 하더라도 시간이 초과 될 것이라고 생각했다.
        - 과거에 다익스트라 알고리즘과 딕셔너리 재귀를 통해 경로를 뽑을 수 있는 방법을 공부했던게 떠올라서 어쩔 수 없이 선택했다.
    - 안하던 행동 2) 우선 순위 BFS에서 후보군 리스트 사용 안함.
        - 오늘따라 뭔가 괜찮을것 같아서 돌발행동을 해버렸다. 평소에 안하던 짓을 왜 시험에서?
    - 독해 실수 1) "해당 턴 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐" 이라는 문장을 잘못 해석함.
        - 사람이 편의점에서 멈추는 경우와 베이스 캠프에 입장하는 경우에 대해 동일한 문장이 두번 나온다.
        - 따져보면 베이스 캠프 입장에 대해서는 굳이 불필요한 문장이다. 어차피 모두 이동한 후에 즉시 적용되는 내용인데?
        - 일단 이 부분에서 낚여서 전부 이동, 새로운 사람 베이스 캠프 입장 후에 일괄적으로 통행 불가 처리를 해주기로 했다.

[구현]
    - 그래도 다익스트라 알고리즘의 원리를 이해하고 있어서인지, 기억을 떠올려서 구현하는 것은 가능했다.
        - 다만, 잔실수가 너무 너무 많아서 디버깅 내내 나를 괴롭게 했다.
        - 시작 위치를 그냥 0,0으로 박아두고 바꾸는걸 까먹었다.
        - 도착 위치에 도달할 수 있음이 반드시 보장되지만, 내가 실수한 경우를 대비해 체크포인트를 만들어 디버그 문구를 미리 삽입해뒀어야 했다.
    - BFS는 구현 자체는 쉽게 하긴 했는데, 정신줄 놓고 구상해서 처음부터 잘못 짰었다.
    - 그나마 다행인건, 독해 실수로 인한 파트를 제외하면 자료구조나 실행 단계에서의 실수는 없었다.

[디버깅]
    - 이번 문제는 풀면서 10번 미만 히든 테케는 다 확인해봤다.
        - 이걸 가지고 디버깅하면서 다익스트라, 독해 실수 관련 에러를 전부 잡았다.
    - 3번째 제출에서 98번째인가? 암튼 완전 뒷쪽에 있는 대형 테케 하나에서 걸려 넘어졌다.
    - 앞쪽에서 유일하게 걸고 넘어지지 않았던 BFS 파트를 다시 봐야겠다는 생각이 문득 들어서 돌아왔다.
        - 평소 내 스타일과 다른 부븐을 찾았고, 원래 방식대로 바꿔서 제출했더니 바로 정답으로 나왔다.

[후기]
    - 목, 금 기량 수직으로 하락하는거 실화냐 진짜...
"""
from heapq import heappush, heappop
from collections import deque


# TODO 1: 다익스트라 알고리즘으로 최단 경로의 첫 위치 탐색
def move(goal_r, goal_c, cur_r, cur_c):
    # 이동 경로 딕셔너리 비우기
    global routes
    routes.clear()

    # 거리(작은순), 행(작은순), 열(작은순)
    heap = [(0, cur_r, cur_c)]
    dajk = [[int(1e9)]*N for _ in range(N)]
    dajk[cur_r][cur_c] = 0

    while heap:
        # 우선순위 힙에서 값 뽑기
        dist, cr, cc = heappop(heap)
        # 목표 지점 도착했으면 즉시 종료
        if cr == goal_r and cc == goal_c:
            break
        # 이미 더 짧은 경로 존재하면 무시
        if dajk[cr][cc] < dist:
            continue

        # 이동 우선 순위: 상, 우, 좌, 하.
        for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            nr, nc = cr+dr, cc+dc

            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if blocked[nr][nc] != 0:
                continue

            if dist+1 < dajk[nr][nc]:
                dajk[nr][nc] = dist+1
                heappush(heap, (dist+1, nr, nc))
                routes[(nr, nc)] = (cr, cc)

    # 경로 딕셔너리 재귀적으로 타고 들어가서 다음 칸 위치 뽑기
    history = [(goal_r, goal_c)]
    while True:
        preceding = routes[history[-1]]
        if preceding == (cur_r, cur_c):
            break
        else:
            history.append(preceding)
    return history[-1]


# TODO 2: 조기종료 BFS로 가고 싶은 편의점과 가장 가까운 베이스 캠프 위치 탐색
def find(gr, gc):
    que = deque()
    que.append((gr, gc))
    vst = [[0]*N for _ in range(N)]
    vst[gr][gc] = 1

    radius = int(1e9)
    candidates = []

    while que:
        cr, cc = que.popleft()
        if vst[cr][cc] > radius:
            break

        for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            nr, nc = cr+dr, cc+dc
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if blocked[nr][nc] == 1:
                continue
            if vst[nr][nc] != 0:
                continue
            vst[nr][nc] = vst[cr][cc]+1
            que.append((nr, nc))

            if (nr, nc) in base_camps:
                radius = vst[nr][nc]
                candidates.append((vst[nr][nc], nr, nc))

    candidates.sort(key=lambda z: [z[0], z[1], z[1]])
    _, fr, fc = candidates[0]
    return fr, fc


if __name__ == '__main__':
    N, M = map(int, input().split())

    # 베이스 캠프 위치 파악
    base_camps = set()
    for r in range(N):
        line = list(map(int, input().split()))
        for c in range(N):
            if line[c] == 1:
                base_camps.add((r, c))

    # 격자 내부와 외부의 사람들을 분리하여 딕셔너리로 저장
    # 키: 입장 시간, 밸류: 편의점의 행,열과 현재 위치 행,열
    in_people = dict()
    out_people = dict()
    for i in range(M):
        x, y = map(int, input().split())
        out_people[i] = [x-1, y-1]

    # 시간 초기화
    time = 0

    # 이동 경로 계산을 위한 딕셔너리
    routes = dict()

    # 초기에 통행이 불가한 칸은 없는 상태로 시작한다.
    blocked = [[0]*N for _ in range(N)]

    while True:
        # 종료 조건: 격자 내의 사람이 전부 편의점에 도달한 시점.
        # 편의점에 도착하는 사람은 in_people에서 pop시킬 것이기에,
        # in_people이 비는 시점에 모두 편의점에 도달한 것으로 볼 수 있다.
        # 또한, 편의점과 베이스가 겹칠 수 없어 시작부터 종료되는 케이스는 발생하지 않는다.
        if time > 0 and not in_people:
            break

        # 이번 턴에서 통행 불가 판정을 받을 위치 저장용 임시 리스트
        to_block = []
        # 이번 턴에서 편의점에 도달한 사람들의 키를 저장할 임시 리스트
        to_pop = []

        # 1: 편의점 방향 최단 경로 이동 한칸
        for key, (gr, gc, cr, cc) in in_people.items():
            nr, nc = move(gr, gc, cr, cc)
            in_people[key][2] = nr
            in_people[key][3] = nc

            # 2: 편의점 도달하면 앞으로 통행불가 판정
            if nr == gr and nc == gc:
                to_block.append((gr, gc))
                to_pop.append(key)

        # 편의점 도착한 사람들 탈출
        for key in to_pop:
            in_people.pop(key)
        # 아니 여기서 한번 따로 막아줘야 한다고?
        for br, bc in to_block:
            blocked[br][bc] = 1

        # 3: time < m일때 t번째 사람이 가고 싶은 편의점과 가장 가까운 베이스 진입
        if time < M and out_people:
            gr, gc = out_people[time]
            out_people.pop(time)

            nr, nc = find(gr, gc)
            blocked[nr][nc] = 1
            base_camps.discard((nr, nc))
            in_people[time] = [gr, gc, nr, nc]

        # 5: 시간 증가
        time += 1

    # 정답 출력
    print(time)
