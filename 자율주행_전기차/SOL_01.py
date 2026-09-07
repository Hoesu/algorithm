""" 자율주행 전기차 / 20260904 / 체감 난이도: G4
소요 시간 3시간 / 시도 6회 / 실행 시간 55ms (코드트리) / 메모리 17MB (코드트리)

[구상]
    - 무조건 다시 풀어볼 문제. 조기종료 BFS를 생각치도 못했다.
    - 현재 위치에서 가장 가까운 승객을 찾고, 승객의 목적지까지 이동하는 과정을 반복하는 방식으로 구현하기로 했다.
    - 승객 선택 시 거리 → 행 → 열 순으로 우선순위를 적용해야 하므로 BFS 탐색 중 최단 거리의 승객들을 따로 저장한 뒤 정렬하여 선택.
    - 승객을 찾은 뒤에는 다시 BFS를 수행하여 목적지까지의 거리를 구하기로 했다.

[구현]
    - 현재 위치에서 승객을 찾는 BFS와 승객에서 목적지까지의 거리를 구하는 BFS를 분리했다.
    - 승객 탐색 BFS는 가장 가까운 승객을 발견하면 해당 거리까지만 탐색하도록 탐색 반경을 줄여 불필요한 탐색을 방지했다.
    - 같은 거리에 있는 승객이 여러 명일 수 있으므로 해당 거리의 승객들을 모두 저장한 뒤 행, 열 기준으로 정렬하여 첫번째를 가져와 사용했다.
    - 승객을 태우고 목적지까지 이동할 때 배터리를 거리만큼 소모하고, 목적지 도착 후 이동 거리의 2배만큼 충전했다.
    - 출발지 또는 목적지에 도달할 수 없거나 배터리가 부족한 경우 즉시 실패 처리하였다. (핵심)

[디버깅]
    - 처음에는 승객을 찾기 위해 BFS를 끝까지 돌렸는데, 가까운 승객을 찾은 이후에도 계속 탐색하여 불필요한 연산이 발생했다.
    - BFS 특성상 먼저 발견한 승객의 거리가 최단 거리라는 점을 이용하여 현재까지 찾은 승객의 거리까지만 탐색하도록 수정했다.
    - 단순히 승객을 하나 찾았다고 바로 종료하면 같은 거리의 다른 승객 중 행, 열 우선순위를 비교할 수 없기 때문에 해당 거리까지는 계속 탐색해야 하는 점을 주의했다.
    - 제출을 여러번 한 이유는 코드 구조를 수정하면서 엣지 케이스를 걸러낼 수 있게 하는 과정에서 수많은 시행착오가 있었기 때문이다.
        - 문제를 처음 푸는 시점부터 에이 설마~ 하면서 경로가 막힌 경우를 상정했는데...
        - 침착하게 구조를 수정하지 않고 되는대로 하다보니까 여기저기서 에러가 너무 많이 발생했다.

[후기]
    - 컨디션이 좋지 않다는 핑계로 제출에만 목메는 모습을 보였다.
    - 다음부터는 이딴 식으로 문제 맞추지 말자.
"""
from collections import deque


def fast_bfs(sr, sc, gr, gc):
    que = deque()
    que.append((sr, sc))
    vst = [[-1] * N for _ in range(N)]
    vst[sr][sc] = 0

    while que:
        cr, cc = que.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if road[nr][nc] == 1:
                continue
            if vst[nr][nc] >= 0:
                continue
            vst[nr][nc] = vst[cr][cc] + 1
            que.append((nr, nc))

            if nr == gr and nc == gc:
                return vst[nr][nc]
    return -1


# TODO 1: 배열 전체를 순회하며 갈 수 있는 모든 위치에 대해 최단 거리 탐색
#   입력: 현재 전기차 좌표
#   출력: 승객 ID, 출발 좌표, 도착 좌표, 현재 위치에서 출발지까지 최단 거리, 출발지에서 도착지까지 최단 거리
def bfs(cr, cc):

    # TODO 1.1 큐, 방문 배열(모든 위치 -1, 현재 위치 0) 초기화
    que = deque()
    que.append((cr, cc))
    vst = [[-1] * N for _ in range(N)]
    vst[cr][cc] = 0

    # TODO 1.2 탐색한 출발지 저장할 배열과, 최근 거리 저장할 변수 초기화
    found_starts = []
    search_radius = 400

    # TODO 1.3 시작 위치가 바로 출발 지점이라면 탐색 건너뛰기
    if (cr, cc) in passengers.keys():
        found_starts.append((cr, cc))

    # TODO 1.4 4방향 탐색
    if not found_starts:
        while que:
            cr, cc = que.popleft()
            # TODO 1.4.1 탐색 반경 벗어나면 즉시 탈출
            if vst[cr][cc] > search_radius:
                break

            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]

                # TODO 1.4.2 범위 벗어나면 무시
                if not(0 <= nr < N and 0 <= nc < N):
                    continue

                # TODO 1.4.3 벽 만나면 무시
                if road[nr][nc] == 1:
                    continue

                # TODO 1.4.4 이미 방문한 지역이면 무시
                if vst[nr][nc] >= 0:
                    continue

                # TODO 1.4.5 위 조건 모두 통과했으면 거리 +1
                vst[nr][nc] = vst[cr][cc] + 1
                que.append((nr, nc))

                # TODO 1.4.6 출발지 찾으면 탐색 반경 현재 거리로 업데이트, 출발지 목록에 추가
                if (nr, nc) in passengers.keys():
                    search_radius = vst[nr][nc]
                    found_starts.append((nr, nc))

    # TODO 1.5 탐색 후에도 출발지를 찾지 못했다면 예외처리
    if not found_starts:
        return [-1] * 6

    candidates = []
    for xs, ys in found_starts:
        if vst[xs][ys] < 0:
            return [-1] * 6
        sd = vst[xs][ys]
        xe, ye = passengers[(xs, ys)][0], passengers[(xs, ys)][1]
        gd = fast_bfs(xs, ys, xe, ye)
        if gd < 0:
            return [-1] * 6
        candidates.append([xs, ys, xe, ye, sd, gd])
    return sorted(candidates, key=lambda x: [x[4], x[0], x[1]])[0]


if __name__ == '__main__':
    dr = [-1, 0, 0, 1]
    dc = [0, -1, 1, 0]

    N, M, battery = map(int, input().split())
    road = [list(map(int, input().split())) for _ in range(N)]

    car_x, car_y = map(int, input().split())
    car_x -= 1
    car_y -= 1

    passengers = dict()
    for _ in range(M):
        Xs, Ys, Xe, Ye = list(map(int, input().split()))
        passengers[(Xs-1, Ys-1)] = (Xe-1, Ye-1)

    completed = True
    while True:
        # BFS 돌려서 다음 승객 정보와 이동 계획 받아오기
        sr, sc, gr, gc, sd, gd = bfs(car_x, car_y)

        # 만약 벽으로 막혀서 출발지나 도착지가 갈 수 없는 위치에 있다면 (에이 설마)
        if sd == -1 or gd == -1:
            completed = False
            break

        # 만약 현재 배터리로 출발지에서 픽업, 도착지 도달까지 가능하다면
        if battery >= sd+gd:
            # 전기 자동차의 위치를 목적지로 변경하고
            car_x, car_y = gr, gc
            # 배터리에 출발->도착 거리의 2배를 충전시켜주기
            battery -= sd
            battery += gd
            # 승객 딕셔너리에서 운행 완료한 승객 제거하기
            passengers.pop((sr, sc))
        # 만약 현재 배터리로 다음 운행이 불가능하다면?
        else:
            completed = False
            break

        # 남아있는 승객 체크
        if not passengers:
            break

    # 승객들 다 처리했으면 남은 배터리 출력
    if completed:
        print(battery)
    # 실패했으면 -1 출력
    else:
        print(-1)
