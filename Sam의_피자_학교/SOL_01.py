""" Sam의 피자학교 / 20260908 / 체감 난이도: G2
소요 시간 1시간 53분 / 시도 1회 / 실행 시간 139ms (코드트리) / 메모리 21MB (코드트리)

[구상]
    - 밀가루 더하기, 도우 말기, 도우 누르기, 반으로 접기 등, 단계적으로 주어진 소문제를 잘 해결하는게 중요하다.
    - 그리고 도우를 말아주는 파트를 제외하면 나머지는 전부 들러리로, 그냥 시간 뺏어먹기 위해 존재하는 파트같다.
        - 정말 오랜 시간을 구상 했는데, 두 방법 사이에서 꽤 고민했다.
        - 1) K**2 >= N를 만족하는 가장 작은 K를 찾아서 K*K 배열 초기화, 정중앙에서부터 달팽이 그리기
            - 이러면 외곽 지대 잘라주고, 너비 조건 만족 못하면 롤백하고, 다시 회전을 시켜야 하는 등의 후처리가 너무 많다..
            - 뭔가 더 똑똑하게 대처할 수 있을 것 같은데, 모르겠어서 PASS.
        - 2) 다음은 패턴을 눈여겨 봤다. (묘수 X, 말로 설명하기 어려움)
            - 일단 도우를 말면, 기존 리스트의 0번 인덱스에 위치한 값으로부터 달팽이 방식으로 기어나올 수 있다.
            - 이때, 도우를 말면 말수록 여러 값 들이 규칙성 있게 변하는 것을 확인할 수 있다.
            - 2.1) 말려 올라가는 블럭의 규격 => 1x1, 2x1, 2x2, 3x2, 3x3, 4x3, 4x4, ...
            - 2.2) 0번 인덱스에서 달팽이 형태로 기어나오기 위해 시작해야 하는 방향 => 우 하 좌 상
            - 2.3) 좌상단 칸으로부터 0번 인덱스 값의 행/열 거리
                - 직전 턴 이동 방향 (하) => 열 1 증가
                - 직전 턴 이동 방향 (상) => 행 1 증가
            - 이것들만 잘 추적하면 도우를 최대한 말았을 때 2차원 배열로 직관적으로 표현할 수 있다.
            - 이렇게 푸는 문제 아닌거 같긴하다. 내가 아니라 컴퓨터가 일을 더 많이 해야 하는데...
    - 암튼 방법론 2안으로 확정 짓고 바로 구현으로 들어갔다.

[구현]
    - 예상한대로 도우 마는 부분에서 약 1시간 정도로 가장 많은 시간을 사용했다.
    - 종이에 그려놓은 패턴 전개도를 가지고 하다보니까 대단한 주석 설계나 pseudo-code는 필요 없었다.
    - 다만 roll 함수가 하는 역할이 굉장히 많다보니까 작은 문제 하나를 해결할때마다 철저히 테스트를 돌렸다.
    - 그 외에 BFS나 리스트 자르고 붙이기 같은 사소한 기능들은 빠르게 해결할 수 있었다.

[디버깅]
    - 입력 조건에 1 <= N <= 100이라고 적혀있길래 N이 1이거나 굉장히 작은 소형 케이스에 대해 예외처리와 디버깅을 진행했다.
    - 사실 N은 무조건 4의 배수라서 딱히 볼 필요는 없었지만, 작은 케이스를 가지고 각 기능에 대한 검증을 쉽게 할 수 있어서 나쁘지 않았다.
    - 오픈 테케 1번도 중간 과정들을 전부 검증하는데 사용했기에, 제출하기로 했다.

[후기]
    - 좀 더 쉽게 말아올리는 방법 없을까?
"""
from collections import deque


def roll(lst):
    # 방향 벡터: 우, 하, 좌, 상
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # 달팽이 형태로 이동할 때 각 방향으로 이동하는 칸 수 (최대 100)
    movements = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
    # 현재 0번 인덱스의 위치와 이동 방향
    cr, cc, cd = 0, 0, 0
    # 현재까지 말려 올라간 블럭의 크기
    box_r, box_c = 1, 1
    # 블럭의 가로/세로 확장 순서 추적
    rep = 0

    while True:
        # 더 이상 말아올릴 밀가루가 없으면 종료
        if len(lst) == 1:
            break

        # 말아올릴 때마다 세로, 가로 순서로 블럭 크기를 확장
        if rep % 2 == 0:
            nbox_r = box_r+1
            nbox_c = box_c
        else:
            nbox_r = box_r
            nbox_c = box_c+1
        rep += 1

        # 새롭게 확장되는 블럭에서 0번 인덱스가 위치할 좌표 계산
        if cd == 1:
            nr = cr
            nc = cc+1
        elif cd == 2:
            nr = cr+1
            nc = cc
        else:
            nr = cr
            nc = cc

        # 다음 달팽이 진행 방향
        nd = (cd+1) % 4

        # 현재 밀가루 개수로 만들 수 없는 크기면 종료
        if len(lst) < nbox_r * nbox_c:
            break
        else:
            cr, cc, cd = nr, nc, nd
            box_r, box_c = nbox_r, nbox_c

    # 최대한 말아올린 뒤 남는 밀가루는 가로로 이어붙임
    residuals = len(lst) - box_r*box_c
    box_c += residuals

    # 최종 도우를 담을 2차원 배열 생성
    arr = [[0] * box_c for _ in range(box_r)]
    arr[cr][cc] = lst[0]

    # 0번 인덱스를 제외한 나머지는 역순으로 준비
    lst = lst[1:]
    lst.reverse()

    # 0번 인덱스를 기준으로 달팽이 형태로 밀가루 배치
    for move_idx in range(len(movements)):
        # 바닥까지 내려왔다면 남은 밀가루는 오른쪽으로 일렬 배치
        if cr == box_r - 1:
            while lst:
                nr, nc = cr, cc + 1
                arr[nr][nc] = lst.pop()
                cr, cc = nr, nc
            break

        # 현재 방향으로 이동할 횟수
        move_rep = movements[move_idx]
        for _ in range(move_rep):
            dr, dc = directions[cd]
            nr, nc = cr+dr, cc+dc
            arr[nr][nc] = lst.pop()
            cr, cc = nr, nc
        # 달팽이 방향 전환: 우 -> 하 -> 좌 -> 상
        cd = (cd-1) % 4
    return arr


def press(arr):
    # 방향 벡터
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    # 큐 초기화. (0, 0)엔 항상 밀가루가 있다.
    que = deque()
    que.append((0, 0))
    # 방문 배열 초기화.
    vst = [[0] * len(arr[0]) for _ in range(len(arr))]
    vst[0][0] = 1
    # 밀가루 변화량 추적용 배열 초기화
    diff = [[0] * len(arr[0]) for _ in range(len(arr))]

    while que:
        cr, cc = que.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            # 범위 바깥 무시
            if not(0 <= nr < len(arr) and 0 <= nc < len(arr[0])):
                continue
            # 밀가루 없는 칸 무시
            if arr[nr][nc] == 0:
                continue

            # 변화량 0 이상인 케이스만 연산
            delta = abs(arr[cr][cc]-arr[nr][nc]) // 5
            if arr[cr][cc] > arr[nr][nc]:
                diff[cr][cc] -= delta
                diff[nr][nc] += delta
            else:
                diff[cr][cc] += delta
                diff[nr][nc] -= delta

            # 미방문 지역에 한해서 진행
            if vst[nr][nc] != 1:
                vst[nr][nc] = 1
                que.append((nr, nc))

    # 눌러서 출력
    lst = []
    for c in range(len(arr[0])):
        for r in range(len(arr)-1, -1, -1):
            if arr[r][c] == 0:
                continue
            # 중복 연산 때문에 2로 나눠줘야 한다.
            lst.append((arr[r][c] + diff[r][c] // 2))
    return lst


def fold(lst):
    t = len(lst) // 4
    l1 = lst[0: t]
    l2 = lst[t: t*2]
    l3 = lst[t*2: t*3]
    l4 = lst[t*3: t*4]
    l1.reverse()
    l3.reverse()
    return [l3, l2, l1, l4]


if __name__ == '__main__':
    N, K = map(int, input().split())
    flour = list(map(int, input().split()))

    time = 0
    while True:
        # TODO 0: 항상 종료를 먼저 체크하기
        if max(flour)-min(flour) <= K:
            break

        # TODO 1: 더하기: 밀가루 양 최소인 위치에 전부 1씩 추가
        min_flour = min(flour)
        for i in range(len(flour)):
            if flour[i] == min_flour:
                flour[i] += 1

        # TODO 2: 도우 말기: 바닥 밀가루보다 위에 있는 밀가루 너비가 넓지 않은 최대 롤
        dough = roll(flour)

        # TODO 3: 도우 눌러주기
        pressed_dough = press(dough)

        # TODO 4: 두번에 걸쳐 반으로 접기
        folded_dough = fold(pressed_dough)

        # TODO 5:누르기 반복
        flour = press(folded_dough)

        # TODO 6: 시간 증가
        time += 1

    print(time)
