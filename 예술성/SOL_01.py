""" 예술성 / 20260904 / 체감 난이도: G4
소요 시간 1시간 50분 / 시도 2회 / 실행 시간 138ms (코드트리) / 메모리 21MB (코드트리)

[구상]
    - 회전, BFS, 백트래킹 등.. 전부 익숙한 주제로 이루어진 문제이고, 시키는대로만 잘 구현하면 된다고 생각한다.
    - 다만 나는 이 문제를 읽으면서 큰 실수를 하나 저질렀다.
        - 각 그룹의 숫자가 1에서 10사이로 고유한 값을 가진다고 내멋대로 판단해버렸다;;
        - 심지어 그림 예제까지 잘 체크하면서 구상해놓고, 왜 편견을 가졌을까 이해가 되지 않는다.
        - 아무튼 문제를 잘못 읽은 탓에 BFS 한번에 그룹 분할과 인접 변 카운트를 해결할 수 있으리라고 착각했다.
    - 구현 도중에 문제를 잘못 읽었다는 사실을 깨달았고, 결국은 기존에 사용하던 자료구조를 살짝 변형해서 BFS를 한번 더 돌리는 식으로 방향을 틀었다.

[구현]
    - 나머지 부분은 20분이면 해결할 수 있다고 자신했기에, 회전 함수부터 구현했다.
        - 테스트 스크립트를 따로 만들어서 직접 한줄 한줄 프린트 찍어가면서 확인했고, 다시는 돌아보지 않았다.
    - 구현 실수 때문에 일부 구현을 갈아엎어야 했지만, 그래도 자료구조를 재구성하면서 소요 시간에 대한 감을 놓지 않는 것은 잘한 것 같다.

[디버깅]
    - 처음에 런타임 에러가 발생했는데, 어디서 실수한건지 바로 눈에 들어와서 고치고 제출했다.

[후기]
    - 회전 함수는 항상 어렵게 느껴진다. 언제 한번 날 잡고 손에 익혀야겠다.
    - 문제를 잘 읽자.. 제발.. 최적화에 미쳐있지 말자.. 제발..
"""
from collections import deque


def find_group(r, c, grp_id):
    que = deque()
    que.append((r, c))

    # 그룹 방문 배열엔 각 그룹의 고유 ID 삽입
    # 그룹 딕셔너리엔 각 그룹의 고유 ID에 대하여 칸 개수, 대표 값을 저장
    grp_vst[r][c] = grp_id
    group[grp_id] = [0] * 2
    group[grp_id][0] += 1
    group[grp_id][1] = palette[r][c]

    while que:
        cr, cc = que.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            # 범위 바깥 무시
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            # 그룹을 찾는 과정에선 같은 값을 가지는 칸만 본다.
            if palette[nr][nc] != palette[r][c]:
                continue
            # 이미 방문한 칸 무시
            if grp_vst[nr][nc] != 0:
                continue
            # 그룹 범위 재계산
            grp_vst[nr][nc] = grp_id
            group[grp_id][0] += 1
            que.append((nr, nc))


def find_adjacent(r, c):
    que = deque()
    que.append((r, c))

    # 인접 방문 배열엔 1로 방문 표시
    # 인접 딕셔너리엔 각 그룹의 고유 ID를 키로 잡고, 밸류로 딕셔너리 초기화
    adj_vst[r][c] = 1
    cur_grp = grp_vst[r][c]
    adjacent[cur_grp] = dict()

    while que:
        cr, cc = que.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            # 범위 바깥 무시
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            # 그룹 방문 배열 (첫번째 BFS에서 만듦) 참조
            # 다음 위치의 그룹 ID가 현재 그룹 ID와 다르다면
            # 인접 딕셔너리에 두 그룹간 인접 카운트를 저장.
            # 굳이 딕셔너리로 하는 이유는 N이 최대 29라서
            # 배열 인덱스로 그룹 ID 접근하면 최악의 경우 29*29 길이의 배열 써야한다.
            # (모든 1*1 칸이 개별 그룹인 경우이고, 시간 초과 위험 있음.)
            if grp_vst[nr][nc] != cur_grp:
                if grp_vst[nr][nc] in adjacent[cur_grp].keys():
                    adjacent[cur_grp][grp_vst[nr][nc]] += 1
                else:
                    adjacent[cur_grp][grp_vst[nr][nc]] = 1
                continue
            # 이미 방문한 칸 무시
            if adj_vst[nr][nc] != 0:
                continue
            # 같은 그룹 내부 칸 만나면 방문 처리하고 진행
            adj_vst[nr][nc] = 1
            que.append((nr, nc))


def backtrack_score(lst=[], start=1, step=0):
    # 찾은 모든 그룹의 고유 ID에 대하여 길이 2의 조합을 만들고, 조화로움 점수 합산하여 예술성 반환.
    global current_score
    if step == 2:
        a = group[lst[0]][-1]
        b = group[lst[1]][-1]
        a_cnt = group[lst[0]][0]
        b_cnt = group[lst[1]][0]

        if lst[0] not in adjacent[lst[1]].keys():
            return
        else:
            adj_cnt = adjacent[lst[0]][lst[1]]

        score = (a_cnt + b_cnt) * a * b * adj_cnt
        if score > 0:
            current_score += score
        return

    for i in range(start, len(group.keys())+1):
        backtrack_score(lst+[i], i+1, step+1)


def rotate(array):
    # 문제의 조건을 충실히 반영한 회전 함수.
    array_copy = [row.copy() for row in array]
    for r in range(N):
        for c in range(N):
            if 0 <= r < N // 2 and 0 <= c < N // 2:
                array_copy[c][N // 2 - 1 - r] = array[r][c]
            elif 0 <= r < N // 2 and N // 2 + 1 <= c < N:
                array_copy[c - (N // 2 + 1)][N - 1 - r] = array[r][c]
            elif N // 2 + 1 <= r < N and 0 <= c < N // 2:
                array_copy[c + N // 2 + 1][N - 1 - r] = array[r][c]
            elif N // 2 + 1 <= r < N and N // 2 + 1 <= c < N:
                array_copy[c][N - (r - N // 2)] = array[r][c]
            else:
                array_copy[N - c - 1][r] = array[r][c]
    return array_copy


if __name__ == '__main__':
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    N = int(input())
    palette = [list(map(int, input().split())) for _ in range(N)]
    group = dict()
    adjacent = dict()
    total_score = 0

    for _ in range(4):
        # TODO 0: 그룹 딕셔너리 비우기
        group.clear()
        adjacent.clear()

        # TODO 1: N*N 방문 배열 초기화 (그룹 분할용, 인접 체크용)
        grp_vst = [[0] * N for _ in range(N)]
        adj_vst = [[0] * N for _ in range(N)]

        # TODO 2: BFS 돌리면서 그룹을 분할하고, 고유 ID 부여하기
        group_id = 0
        for r in range(N):
            for c in range(N):
                if grp_vst[r][c] == 0:
                    group_id += 1
                    find_group(r, c, group_id)

        # TODO 3: BFS 한번 더 돌려서 인접한 변 개수 체크하기
        for r in range(N):
            for c in range(N):
                if adj_vst[r][c] == 0:
                    find_adjacent(r, c)

        # TODO 4: 백트래킹으로 예술성 계산
        current_score = 0
        backtrack_score()
        total_score += current_score

        # TODO 5: 배열 회전
        palette = rotate(palette)

    # TODO 6: 정답 출력
    print(total_score)

