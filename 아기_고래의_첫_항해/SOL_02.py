""" 아기 고래의 첫 항해 / 20261009 / 체감 난이도: S1
소요 시간 30분 / 시도 1회 / 실행 시간 111ms (코드트리) / 메모리 21MB (코드트리)

EZ.
"""
from collections import deque


def move(cr, cc, cd):
    delta = [0, -1, 1, 2]
    for i in delta:
        nd = (cd+i) % 4
        nr = cr + DR[nd]
        nc = cc + DC[nd]
        if not(0 <= nr < N and 0 <= nc < N):
            continue
        if ocean[nr][nc] != 0:
            continue
        ocean[nr][nc] = 2
        answer.append((nr, nc))
        return nr, nc, nd, True
    return cr, cc, cd, False


def find(sr, sc, sd):
    que = deque()
    que.append((sr, sc, sd))
    vst = [[0] * N for _ in range(N)]
    vst[sr][sc] = 1
    threshold = int(1e9)
    candidates = []

    while que:
        cr, cc, cd = que.popleft()
        if threshold < vst[cr][cc]:
            break
        if ocean[cr][cc] == 0:
            threshold = vst[cr][cc]
            candidates.append((vst[cr][cc], cr, cc, cd))

        for nd in range(3, -1, -1):
            nr, nc = cr+DR[nd], cc+DC[nd]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if vst[nr][nc] != 0:
                continue
            if ocean[nr][nc] == 1:
                continue
            que.append((nr, nc, nd))
            vst[nr][nc] = vst[cr][cc]+1

    if not candidates:
        return None, None, None
    candidates.sort(key=lambda x: (x[0], x[1], x[2]))
    _, fr, fc, fd = candidates[0]
    answer.append((fr, fc))
    ocean[fr][fc] = 2
    return fr, fc, fd


if __name__ == '__main__':
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]
    adapter = [0, 2, 3, 1]

    N, R, C, D = map(int, input().split())
    Wr, Wc, Wd = R-1, C-1, adapter[D-1]
    ocean = [list(map(int, input().split())) for _ in range(N)]
    ocean[Wr][Wc] = 2
    answer = [(Wr, Wc)]

    while True:
        Wr, Wc, Wd, moved = move(Wr, Wc, Wd)
        if not moved:
            Wr, Wc, Wd = find(Wr, Wc, Wd)
        if Wd is None:
            break

    for r, c in answer:
        print(r+1, c+1)


""" 아기 고래의 첫 항해 / 20261002 / 체감 난이도: S1
소요 시간 1시간 6분 / 시도 2회 / 실행 시간 119ms (코드트리) / 메모리 21MB (코드트리)

[구상]
    - 이거 기출이 아닌가? 싶을 정도로 간단한 문제.
    - 쉬우면 뭐하나. 문제를 잘못 읽었다.
        - 선택한 칸까지 최단 거리 후보 찾는 전형적인 레벨 BFS인데, 사람 헷갈리게 쓸데없는 말을 끼워넣고 있다.
        - 선택한 칸까지 이동 우선 순위를 가지고 최단 경로로 이동하는 것이 사실상 의미가 없다.
        - 왜냐면 최단거리, 행, 열 우선순위만 만족하는 바다를 찾으면 경로고 뭐고 필요가 없기 때문이다.
        - 우선 순위를 지키며 이동하는 과정에서 다른 뭔가와 상호작용하는게 아니라면 쓸모가 없다.
    - 오늘 문제 읽을 때 집중이 좀 안된다고 느끼긴 했는데, 조심하지 않고 틀려버린게 좀 아쉽다.
        - 아무튼 처음엔 방향 우선순위를 지키며 가장 먼저 찾는 칸을 선정하는 방식을 채택했다.

[구현]
    - 얼레벌레 대충대충 한건 절대 아니고, 이제 워낙 익숙한 구현이라 빨랐다.

[디버깅]
    - 2번 테케가 초대형 테케였는데, 거기서 오답이 나왔다.
    - 솔직히 좀 당황스럽긴 했다. 모든 바다칸으로의 이동 가능성이 반드시 보장되기 때문에 엣지가 없다고 생각했기 때문.
    - 생각해보니 bfs 함수 말고는 틀릴 부분이 없겠다 싶어서 문제를 다시 읽었다.
    - 보자마자 아 이거 그냥 후보군 뽑고 정렬하는 BFS구나, 하고 코드를 수정해서 제출했다.

[후기]
    - 좀 치사한데?
"""
from collections import deque


def debug(msg):
    print()
    print(msg)
    for x in ocean:
        print(*x)
    print()
    for x in visit:
        print(*x)
    print('---')


def move(cr, cc, cd):
    for delta in [0, 1, -1, 2]:
        nd = (cd + delta) % 4
        nr = cr + DR[nd]
        nc = cc + DC[nd]

        if not(0 <= nr < N and 0 <= nc < N):
            continue
        if ocean[nr][nc] == 1:
            continue
        if visit[nr][nc] != 0:
            continue
        visit[nr][nc] = visit[cr][cc]+1
        return nr, nc, nd
    return None, None, None


def find_ocean(sr, sc, sd):
    que = deque()
    que.append((sr, sc, sd))
    vst = [[0] * N for _ in range(N)]
    vst[sr][sc] = 1

    threshold = N**3
    candidates = []

    while que:
        cr, cc, cd = que.popleft()
        if vst[cr][cc] > threshold:
            break
        if visit[cr][cc] == 0:
            threshold = vst[cr][cc]
            candidates.append((cr, cc, cd, vst[cr][cc]))

        for i in range(4):
            nr = cr + DR[i]
            nc = cc + DC[i]
            nd = i

            if not (0 <= nr < N and 0 <= nc < N):
                continue
            if vst[nr][nc] != 0:
                continue
            if ocean[nr][nc] == 1:
                continue
            vst[nr][nc] = vst[cr][cc]+1
            que.append((nr, nc, nd))

    if not candidates:
        return None, None, None
    candidates.sort(key=lambda x: (x[3], x[0], x[1]))
    fr, fc, fd, _ = candidates[0]
    visit[fr][fc] = visit[sr][sc] + 1
    return fr, fc, fd


if __name__ == '__main__':
    DR = (0, 1, 0, -1)
    DC = (-1, 0, 1, 0)
    adapter = [3, 1, 0, 2]

    N, R, C, D = map(int, input().split())
    ocean = [list(map(int, input().split())) for _ in range(N)]
    visit = [[0] * N for _ in range(N)]

    Wr, Wc, Wd = R-1, C-1, adapter[D-1]
    trajectory = [(Wr, Wc)]
    visit[Wr][Wc] = 1

    while True:

        # TODO 1: 인접 이동
        while True:
            nWr, nWc, nWd = move(Wr, Wc, Wd)
            if nWd is None:
                break
            else:
                Wr, Wc, Wd = nWr, nWc, nWd
                trajectory.append((Wr, Wc))

        # TODO 2: 가장 가까운 바다 이동
        nWr, nWc, nWd = find_ocean(Wr, Wc, Wd)
        if nWd is None:
            break
        else:
            Wr, Wc, Wd = nWr, nWc, nWd
            trajectory.append((Wr, Wc))

    # 정답 출력
    for r, c in trajectory:
        print(r+1, c+1)
