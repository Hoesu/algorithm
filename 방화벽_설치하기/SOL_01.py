""" 방화벽 설치하기 / 20260818 / 체감 난이도: G5
소요 시간 33분 / 시도 1회 / 실행 시간 377ms (코드트리) / 메모리 24MB (코드트리)

[구상]
    - 보자마자 BFS + Backtracking 문제라는 생각이 들었다.
    - 최대 8x8 행렬이기 때문에, 길이 3의 빈칸 좌표 조합을 완전 탐색할 수 있다고 생각했다.
    - 핵심은 최적의 방벽 조합으로 불이 번지지 못하는 영역을 최대화하는 것임을 명확히 인지했다.
    - 예외를 따져봤으나, 방화벽을 제외한 모든 영역이 불로 시작하는 것은 조건상 불가능하기 때문에, 별 문제가 없다고 생각했다.

[구현]
    - 처음부터 조합을 만들어야 한다는 것은 알았지만, 실수로 부분집합을 만드는 코드로 시작했다가 바로 방향을 수정했다.
    - 새로운 방벽 조합을 시도할 때마다 배열 복사본을 만들고 싶지 않았기 때문에, BFS 전후로 값을 변경해주는 기믹을 추가했다. (마음에 듦)

[디버깅]
    - 워낙 자신있는 문제기도 했고, 한번에 오픈 테케를 다 맞았다는 사실에 취해버려서 바로 제출해버렸다.

[후기]
    - 다음부턴 코드 완성 후 처음부터 복기하고, 커스텀 케이스를 돌려보는 습관을 들이자.
    - 제출해서 한방에 맞으면 기분은 좋지만, 반대로 틀려버리면 멘탈이 더욱 흔들릴 수 있다.
"""
from collections import deque


def backtrack(start=0, step=0, lst=[]):
    # 길이 3인 인덱스 조합을 모두 찾아서 컴비네이션 배열에 저장.
    if step == 3:
        combinations.append(lst.copy())
        return
    for i in range(start, len(free)):
        backtrack(i+1, step+1, lst+[i])


def bfs():
    # 4방향 벡터
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    # 방문 배열, 큐 초기화
    vst = [[0] * C for _ in range(R)]
    que = deque()

    # 초기에 불이 있는 좌표를 전부 큐에 추가하고, 방문 배열에서 1 처리.
    for fr, fc in fire:
        vst[fr][fc] = 1
        que.append([fr, fc])

    while que:
        cr, cc = que.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not (0 <= nr < R and 0 <= nc < C):
                continue
            if arr[nr][nc] != 0:
                continue
            if vst[nr][nc]:
                continue
            vst[nr][nc] = 1
            que.append([nr, nc])

    # 불타지 않은 영역 넓이 계산
    unburnt = 0
    for r in range(R):
        for c in range(C):
            if arr[r][c] == 0 and vst[r][c] == 0:
                unburnt += 1
    area.append(unburnt)


if __name__ == '__main__':
    R, C = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(R)]

    # 지도에서 불타는 칸과 빈 칸의 좌표를 리스트에 저장
    fire = []
    free = []
    for r in range(R):
        for c in range(C):
            if arr[r][c] == 2:
                fire.append((r, c))
            elif arr[r][c] == 0:
                free.append((r, c))
            else:
                continue

    # 빈칸 좌표들을 인덱스로 표현하면 0, 1, ..., N
    # 이걸로 백트래킹 돌려서 길이 3의 가능한 조합을 모두 뽑고 저장한다.
    combinations = []
    backtrack()

    # 불이 닿지 못한 영역 케이스 별로 저장할 리스트
    area = []
    # 모든 조합 시도
    for cb in combinations:
        # 현재 지도에 방화벽 3개 추가
        for i in range(3):
            wr, wc = free[cb[i]]
            arr[wr][wc] = 1
        # BFS 돌리기
        bfs()
        # 다음 케이스 돌리기 전에 지도 원상 복구
        for i in range(3):
            wr, wc = free[cb[i]]
            arr[wr][wc] = 0

    # 가장 큰 값 도출
    print(max(area))
