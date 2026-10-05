""" 꼬리잡기 / 20261004 / 체감 난이도: G1
소요 시간 1시간 30분 / 시도 2 / 실행 시간 97ms (코드트리) / 메모리 18MB (코드트리)

몰랐는데, 이거 BFS 풀이가 가능하네? 근데 하기 싫은 맘으로 억지로 하다가 런타임 에러 한번 나왔다.
암튼간에 자료구조 신중히 정해서 잘 써야 하는데, 이게 참 까다로운 문제다. 다시 풀자...
공 던지는 방향은 이번에도 하드코딩 하긴 했는데, 훨씬 깔끔한듯.
"""
from collections import deque


def follow_track(sr, sc, idx):
    que = deque()
    que.append((sr, sc))
    vst[sr][sc] = 1
    path = [(sr, sc)]
    stt_idx = 0
    end_idx = None

    while que:
        cr, cc = que.popleft()
        if 0 < field[cr][cc] < 4:
            field[cr][cc] = idx
        else:
            field[cr][cc] = 0

        for i in range(4):
            nr, nc = cr + DR[i], cc + DC[i]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if vst[nr][nc] != 0:
                continue
            if field[nr][nc] == 0:
                continue
            if cr == sr and cc == sc and field[nr][nc] != 2:
                continue
            if field[nr][nc] == 3:
                end_idx = len(path)
            path.append((nr, nc))
            que.append((nr, nc))
            vst[nr][nc] = 1
            break
    return path, stt_idx, end_idx


if __name__ == '__main__':
    DR = (0, -1, 0, 1)
    DC = (1, 0, -1, 0)

    N, M, K = map(int, input().split())
    field = [list(map(int, input().split())) for _ in range(N)]
    teams = dict()

    vst = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if field[r][c] == 1 and vst[r][c] == 0:
                team_id = len(teams)+1
                track, stt, end = follow_track(r, c, team_id)
                teams[team_id] = [track, stt, end, -1]

    time = 0
    answer = 0
    for _ in range(K):
        # 머리 이동
        for k, v in teams.items():
            track, stt, end, delta = v
            track_length = len(track)
            field[track[end][0]][track[end][1]] = 0
            v[1] = (v[1] + v[3]) % track_length
            v[2] = (v[2] + v[3]) % track_length
            field[track[v[1]][0]][track[v[1]][1]] = k

        # 공 던지기
        bd = (time // N) % 4
        if bd == 0:
            br, bc = time%N, 0
        elif bd == 1:
            br, bc = N-1, time%N
        elif bd == 2:
            br, bc = N-1-time%N, N-1
        else:
            br, bc = 0, N-1-time%N

        while True:
            if not(0 <= br < N and 0 <= bc < N):
                break
            if field[br][bc] > 0:
                team_id = field[br][bc]
                cur_track = teams[team_id][0]
                cur_stt = teams[team_id][1]
                cur_end = teams[team_id][2]
                cur_delta = teams[team_id][3]
                cur_idx = cur_stt
                cur_ord = 1

                while True:
                    if cur_track[cur_idx] == (br, bc):
                        answer += cur_ord ** 2
                        break
                    cur_idx = (cur_idx - cur_delta) % len(cur_track)
                    cur_ord += 1

                teams[team_id][1] = cur_end
                teams[team_id][2] = cur_stt
                teams[team_id][3] *= -1
                break
            br += DR[bd]
            bc += DC[bd]
        time += 1
    print(answer)


""" 꼬리잡기 / 20260910 / 체감 난이도: G1
소요 시간 2시간 40분 / 시도 2 / 실행 시간 88ms (코드트리) / 메모리 18MB (코드트리)

[구상]
    - 진짜 어려웠는데, 문제의 제약을 활용해서 겨우 겨우 풀었다.
    - 이동 선의 각 칸은 반드시 2개의 인접한 칸만이 존재한다 = 이동선은 자기 자신이나, 다른 이동선과 절대 겹칠 수 없다.
    - N은 반드시 3 이상이다 = 머리가 꼬리에 바로 붙어있다면, 반드시 한바퀴 돌아서 머리가 꼬리의 뒤에 붙어있는 경우 밖에 없다.
    - 위 조건 덕분에 머리 사람을 찾기만 하면, 여기를 시작으로 격자를 타고 따라가면서 현재 팀의 구성원과 이동선을 추적해낼 수 있으리라 생각했다.
    - 결국 이동선을 타고 가다가 벗어나면 방향 전환을 해야하고, 이때 분기 처리를 잘 해줘야겠다고 생각했다.
    - 문제는 이걸 하기 위해서 자료구조를 어떻게 초기화하고, 실행부 밑그림을 어떻게 그려야 할지 감이 너무 안왔다.
    - 그래서 일단 테스트로 입력 받아두고, 그걸 기반으로 이동선 타기 함수를 짜서, 결과물 검증 및 자료구조를 개선하는 방식을 선택했다.
        - 결론적으로 이게 시간과 체력을 많이 빼앗긴 원흉이라고 생각한다.
        - 기억상 목요일이 오면서 체력도 털리고 머리도 안돌아가서 그냥 해보자는 마인드로 뛰어든 것 같은데...

[구현]
    - 분기 처리가 좀 힘들었다. 현재 칸의 번호에 따라 다음에 올 수 있는 번호의 종류가 달라질 수 있기 때문이었다.
    - 또한, 전체 탐색 과정에서 이동 경로와, 현재 사람이 있는 위치를 인덱스로 분리해서 저장해야 했다.
        - 첫 구현 때는 여기에 방향이 꺾이는 지점의 좌표까지 따로 저장해뒀는데, 구현 막바지에 가서 쓸모없는 정보임을 깨달았다.
        - 그래서 해당 부분만 지워주니까 코드가 훨씬 간결해지는 것을 보면서, 구상이 부족해서 괜한 고생 했다는 생각을 했다.
    - 방향이 꺾이는 지점에서만 4방향 탐색을 돌리는 파트도 꽤 신경을 썼는데, 이미 지나왔던 경로는 무시하게 해야했다.
    - 암튼 뭐 굳이 잘한거 하나 뽑자면.. 트랙 정보 다 뽑아놓고, 현재 사람이 있는 위치만 인덱스로 표시해줬더니 나머지 구현은 편했다.
    - 다만, 집중력 다 빠진 상태에서 시간에 따라 공 던지는 방향이 바뀌는 부분을 구현할 때 인덱스 실수해버렸다.

[디버깅]
    - 한번 틀렸을 때 바로 공 던지는 방향에 대한 구현이 불확실해서 점검했더니 답이 바르게 나왔다.

[후기]
    - 좀 어렵게 푼거 같은데.. 더 쉬운 방법도 있을것 같다.
"""


# 머리의 진행 방향을 기준으로 다음에 이동할 방향 찾기
def search_radius(prev_r, prev_c, prev_dr, prev_dc):
    for i in range(4):
        view_dr, view_dc = directions[i]
        # 현재 진행 방향의 반대쪽은 볼 필요 없음
        if view_dr == -prev_dr and view_dc == -prev_dc:
            continue
        # 보드 밖이면 다음 방향 확인
        if not (0 <= prev_r + view_dr < N and 0 <= prev_c + view_dc < N):
            continue
        # 이동선이나 사람이 있는 방향을 찾으면 해당 방향으로 진행
        if arr[prev_r + view_dr][prev_c + view_dc] >= 1:
            next_dr = view_dr
            next_dc = view_dc
            break
    return next_dr, next_dc


# 머리(1)부터 시작해서 꼬리(3)까지 그룹의 전체 경로 탐색
def find_group(hr, hc):
    # body: 현재 그룹에서 사람이 위치한 track의 인덱스
    # track: 그룹이 이동할 수 있는 전체 경로
    bd_r, bd_c = None, None
    bd_dr, bd_dc = None, None
    group_body = [0]
    group_track = [(hr, hc)]

    # 머리 주변에서 몸통(2)을 찾아 시작 방향 결정
    for i in range(4):
        dr, dc = directions[i]
        nr, nc = hr + dr, hc + dc

        if not (0 <= nr < N and 0 <= nc < N):
            continue
        if arr[nr][nc] == 2:
            group_body.append(len(group_track))
            group_track.append((nr, nc))
            # 현재 몸통 위치와 진행 방향 저장
            bd_r, bd_c = nr, nc
            bd_dr, bd_dc = dr, dc

    # 몸통 → 꼬리 → 이동 경로 순서로 탐색
    while True:
        nr, nc = bd_r + bd_dr, bd_c + bd_dc
        # 진행 방향에 칸이 있으면 해당 칸의 종류에 따라 처리
        if 0 <= nr < N and 0 <= nc < N:
            # 다음 사람이 머리(1)라면 한 바퀴 순회 완료
            if arr[nr][nc] == 1:
                break
            # 몸통(2) 또는 꼬리(3)는 실제 사람
            elif arr[nr][nc] == 2 or arr[nr][nc] == 3:
                group_body.append(len(group_track))
                group_track.append((nr, nc))
                bd_r, bd_c = nr, nc
            # 이동 경로(4)는 사람이 아니지만 그룹의 이동 경로에는 포함
            elif arr[nr][nc] == 4:
                group_track.append((nr, nc))
                bd_r, bd_c = nr, nc
            # 빈칸을 만나면 현재 진행 방향을 다시 탐색
            else:
                bd_dr, bd_dc = search_radius(bd_r, bd_c, bd_dr, bd_dc)
        # 보드 밖으로 나가면 다음 진행 방향을 다시 탐색
        else:
            bd_dr, bd_dc = search_radius(bd_r, bd_c, bd_dr, bd_dc)
    return group_body, group_track


if __name__ == '__main__':
    N, M, K = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    groups = []

    # TODO: 처음 주어진 맵에서 각 그룹의 전체 이동 경로 탐색
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 1:
                body, track = find_group(r, c)
                groups.append([-1, body, track])

    # 사람(1, 2, 3)이 있는 위치만 그룹 번호로 다시 표시
    # 이후 공을 던질 때 그룹 번호를 바로 확인하기 위함
    arr = [[0] * N for _ in range(N)]
    for i in range(len(groups)):
        for j in groups[i][1]:
            r, c = groups[i][2][j]
            arr[r][c] = i + 1
    time = 1
    score = 0

    for _ in range(K):
        # TODO 0: 머리 사람 따라서 한 칸씩 이동
        for i in range(len(groups)):
            delta, body, track = groups[i]
            # delta에 따라 머리가 다음 track 위치로 이동
            new_head = (body[0] + delta) % len(track)
            # 기존 꼬리 위치는 사람 표시 제거
            cr, cc = track[body[-1]]
            arr[cr][cc] = 0
            # 새 머리 위치에 그룹 번호 표시
            nr, nc = track[new_head]
            arr[nr][nc] = i + 1
            # body의 순서를 한 칸씩 밀어서 새로운 머리 반영
            body = [new_head] + body
            body.pop()
            groups[i][1] = body

        # TODO 1: 시간에 맞춰서 공을 던질 행/열과 방향 결정
        #         해당 직선에서 처음 만나는 그룹 찾기
        check = (time - 1) % (N * 4)
        side, offset = divmod(check, N)
        if side == 0:  # 행, 오
            r, c = offset, 0
            dr, dc = 0, 1
        elif side == 1:  # 열, 위
            r, c = N - 1, offset
            dr, dc = -1, 0
        elif side == 2:  # 행, 왼
            r, c = N - 1 - offset, N - 1
            dr, dc = 0, -1
        else:  # 열, 아
            r, c = 0, N - 1 - offset
            dr, dc = 1, 0

        hit_id, hit_r, hit_c = -1, -1, -1
        # 공이 이동하는 방향으로 진행하면서 처음 만나는 사람 탐색
        while 0 <= r < N and 0 <= c < N:
            if arr[r][c] > 0:
                hit_id = arr[r][c]
                hit_r, hit_c = r, c
                break
            r += dr
            c += dc

        # TODO 2: 맞은 사람이 그룹에서 몇 번째인지 확인하고 점수 추가
        #         공에 맞은 팀은 머리와 꼬리 방향 반전
        if hit_id > 0:
            order = 1
            for idx in groups[hit_id - 1][1]:
                if groups[hit_id - 1][2][idx] == (hit_r, hit_c):
                    break
                else:
                    order += 1
            score += order ** 2
            # 이후 이동 방향을 반대로 변경
            groups[hit_id - 1][0] *= -1
            # body 순서도 머리 ↔ 꼬리 방향으로 반전
            groups[hit_id - 1][1].reverse()
        # TODO 3: 시간 증가
        time += 1
    # 정답 출력
    print(score)
