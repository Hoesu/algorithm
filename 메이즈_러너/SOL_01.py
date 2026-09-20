""" 메이즈 러너 / 20260920 / 체감 난이도: P5
소요 시간 1시간 38분 / 시도 1회 / 실행 시간 53ms (코드트리) / 메모리 16MB (코드트리)

[구상]
    - 회전, 최소 정사각형 찾기 같은 내용들은 따로 분리하면 쉬운데, 사람 정보와 합쳐지니까 너무 어렵게 느껴졌다.
    - 예를 들어 3차원 부분 배열을 회전시키면, 그 안에 있는 사람과 출구 좌표들도 마찬가지로 회전된다.
        - 일단 이 부분부터 좌표 변환 기반 회전이 압도적으로 유리한지라, 그 부분을 완벽하게 숙지하고 나서야 이 문제로 돌아왔다.
        - 처음 풀이할 때의 나는 슬라이싱 및 집으로 승부를 보려고 했는데, 솔직히 어려울 것이라는 것을 알면서도 어쩔 수 없이 뛰어든 것이었다.
        - 또한, 딕셔너리로 각 사람들의 정보를 관리하려고 했었는데, 회전한 부분배열 상의 정보를 역으로 딕셔너리에 다시 반영하는게 골치 아팠다.
    - 이번에 다시 시도하면서 고민한 결과, 이동거리나 탈출 인원 같은 정보들은 그냥 전역변수로 관리해도 되겠다는 생각을 했다.
    - 또한, 어차피 최대 10*10 배열인데, 굳이 딕셔너리 말고 그냥 배열 순회하면서 사람 찾기로 했다.

[구현]
    - 루틴 빡세게 안지키면 분명히 중간에서 꼬이고, 나중가면 어디서 틀렸는지도 찾기 힘든 문제라는걸 알기에 차근 차근 설계했다.
    - 동은 프로가 팩맨 문제를 풀면서 만들었던 커스텀 프린트 방식이 떠올라서, 사람과 미로 정보를 side-by-side로 보여주는 프린트 문을 만들어서 썼다.
        - 사람의 이동과 미로 상의 제약을 한 눈에 볼 수 있어서 무척이나 편했다.
    - 실행부는 끝까지 변경하지 않을 정도로 치밀하게 계획해서 짰고, 개별 함수 구현도 큰 어려움은 없었다.
        - 역시 부분 배열 회전 함수를 열심히 공부한 것이 큰 도움이 되었다.
    - 3차원 배열 카피를 만들어본건 이번이 처음이었는데, 아마 안해도 잘 돌아가긴 할거다.
        - people_copy는 2차원 배열까지만 얕은 복사되므로 내부 참가자 리스트 객체는 공유한다.
        - 하지만 회전 과정에서는 내부 리스트의 내용을 수정하는 것이 아니라 리스트 객체 자체를 각 위치에 재할당하므로 문제가 없다.
[디버깅]
    - 디버깅에 꽤 오랜 시간을 쏟았는데, 이번에도 값 덮어쓰기 문제가 발생했다.
        - 3차원 배열 상 현재 위치에서 다음 위치로 리스트 값 넘겨줄 때 extend를 썼어야 하는데 그냥 = 으로 덮어쓰고 있었다.
        - 미치겠다 정말... 재수 없으면 대형 테케 나와서 이런거 디버깅하며 눈으로 찾기도 힘들다.
        - 그래도 동은 프로에게 전수받은 커스텀 프린트가 결국 큰일을 해서 찾긴 찾았다...

[후기]
    - 실수 모음집 +1
    - 아직 3차원 배열에서 리스트 자체를 재할당하는 것과 리스트의 원소를 추가하는 것의 차이가 익숙하지 않다.
"""


def move(cr, cc, er, ec):
    candidates = []
    cur_dist = abs(cr-er) + abs(cc-ec)

    for i in range(4):
        nr, nc = cr+dr[i], cc+dc[i]
        if not(0 <= nr < N and 0 <= nc < N):
            continue
        if maze[nr][nc] > 0:
            continue

        nxt_dist = abs(nr-er) + abs(nc-ec)
        if nxt_dist >= cur_dist:
            continue
        candidates.append([nr, nc, nxt_dist, i])

    if not candidates:
        return cr, cc
    else:
        candidates.sort(key=lambda x: [x[2], x[3]])
        return candidates[0][0], candidates[0][1]


def min_square(er, ec):
    d = int(1e9)
    for cr in range(N):
        for cc in range(N):
            if people[cr][cc]:
                check = max([abs(cr-er), abs(cc-ec)])
                if check < d:
                    d = check+1

    for cr in range(N-d+1):
        for cc in range(N-d+1):
            if not(cr <= er < cr+d):
                continue
            if not(cc <= ec < cc+d):
                continue
            ppl_cnt = 0
            for i in range(d):
                for j in range(d):
                    ppl_cnt += len(people[cr+i][cc+j])
            if ppl_cnt > 0:
                return cr, cc, d


def partial_rotate(sr, sc, er, ec, d):
    exit_found = False
    maze_copy = [x[:] for x in maze]
    people_copy = [x[:] for x in people]

    for i in range(d):
        for j in range(d):
            maze[sr+j][sc+d-1-i] = max(0, maze_copy[sr+i][sc+j]-1)
            people[sr+j][sc+d-1-i] = people_copy[sr+i][sc+j]
            if er == sr+i and ec == sc+j and not exit_found:
                er = sr+j
                ec = sc+d-1-i
                exit_found = True
    return er, ec


def debug(msg, er, ec):
    print(msg)
    print(f'exit: {er, ec}')
    for cr in range(N):
        print(f'{people[cr]}    {maze[cr]}')
    print()


if __name__ == '__main__':
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    # 격자 크기, 참가자 수, 라운드 수
    N, M, K = map(int, input().split())

    # 미로 정보
    maze = [list(map(int, input().split())) for _ in range(N)]

    # 사람 정보 (3차원 배열)
    people = [[[] for _ in range(N)] for _ in range(N)]

    # 참가자 좌표 목록
    for pid in range(M):
        r, c = map(lambda x: int(x)-1, input().split())
        people[r][c].append(pid)

    # 출구 좌표
    exit_r, exit_c = map(lambda x: int(x)-1, input().split())

    # 탈출한 사람 수
    escaped = 0

    # 이동거리 합
    travelled = 0

    for step in range(1, K+1):
        # TODO: 참가자 이동
        #   - 모든 참가자 동시 이동, 벽을 제외한 상하좌우 방향 이동 가능.
        #   - 움직인 칸은 머물러 있던 칸보다 출구까지의 맨하탄 거리가 반드시 짧음.
        #   - 상하로 이동하는 것이 우선
        #   - 움직일 수 없는 상황이라면 이동하지 않음.
        #   - 한칸에 2명 이상 참가자 존재 가능.
        changes = []
        for cur_r in range(N):
            for cur_c in range(N):
                if people[cur_r][cur_c]:
                    nxt_r, nxt_c = move(cur_r, cur_c, exit_r, exit_c)
                    if nxt_r == cur_r and nxt_c == cur_c:
                        continue
                    elif nxt_r == exit_r and nxt_c == exit_c:
                        escaped += len(people[cur_r][cur_c])
                        travelled += len(people[cur_r][cur_c])
                        people[cur_r][cur_c] = []
                    else:
                        travelled += len(people[cur_r][cur_c])
                        changes.append((nxt_r, nxt_c, people[cur_r][cur_c]))
                        people[cur_r][cur_c] = []

        for nxt_r, nxt_c, pid_list in changes:
            people[nxt_r][nxt_c].extend(pid_list)

        # debug(f'after movement at step {step}', exit_r, exit_c)

        # TODO: 조기종료
        #   - 모든 참가자 탈출한 경우
        if escaped == M:
            break

        # TODO: 한명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 찾기
        #   - 좌상단 행, 열이 작은 순으로 우선순위
        #   - 선택한 정사각형 시계방향 90도 회전
        #   - 회전된 영역의 벽은 내구도 1씩 감소
        stt_r, stt_c, side = min_square(exit_r, exit_c)
        exit_r, exit_c = partial_rotate(stt_r, stt_c, exit_r, exit_c, side)

        # debug(f'after rotation at step {step}', exit_r, exit_c)

    # TODO: 정답 출력
    print(travelled)
    print(exit_r+1, exit_c+1)
