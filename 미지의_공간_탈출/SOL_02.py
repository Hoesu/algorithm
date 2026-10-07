""" 미지의 공간 탈출 / 20261006 / 체감 난이도: P5
소요 시간 2시간 / 시도 1 / 실행 시간 76ms (코드트리) / 메모리 18MB (코드트리)

주석 지우는거 깜빡해서 런타임 한번 발생했다. 찐으로 원트함.
워낙 고민 많이 했던 문제기도 하고, 컨디션도 좋은 상태에서 집중해서 하니까 풀만하긴 헀다.
여전히 구현 차력쇼라는 생각은 들지만, 그래도 전체 상태를 2단계로 나눠서 생각하니까 훨씬 편리하게 구현할 수 있었다.
전개도는 그대로 사용했고, 뭔가 다시 풀고 싶진 않다. 너무 끔찍함 ㅋㅋ
"""
from collections import deque


def get_space():
    diagram = [list(map(int, input().split())) for _ in range(N)]
    for sr in range(N):
        for sc in range(N):
            if diagram[sr][sc] == 3:
                w_r, w_c = sr, sc
                for i in range(M+2):
                    for j in range(M+2):
                        if diagram[w_r-1+i][w_c-1+j] == 0:
                            i_r, i_c = w_r-1+i, w_c-1+j
                            if i_r == w_r-1:
                                o_r, o_c = 0, M+i_c-w_c
                            elif i_r == w_r+M:
                                o_r, o_c = M*3-1, M+i_c-w_c
                            elif i_c == w_c-1:
                                o_r, o_c = M+i_r-w_r, 0
                            else:
                                o_r, o_c = M+i_r-w_r, M*3-1
                            return diagram, i_r, i_c, o_r, o_c


def get_walls():
    sr, sc = 0, 0
    diagram = [[9] * (M*3) for _ in range(M*3)]
    e = [list(map(int, input().split())) for _ in range(M)]
    w = [list(map(int, input().split())) for _ in range(M)]
    s = [list(map(int, input().split())) for _ in range(M)]
    n = [list(map(int, input().split())) for _ in range(M)]
    u = [list(map(int, input().split())) for _ in range(M)]
    e = [x for x in zip(*e)][::-1]
    w = [x[::-1] for x in zip(*w)]
    n = [x[::-1] for x in n][::-1]
    for cr in range(M):
        for cc in range(M):
            if u[cr][cc] == 2:
                sr, sc = M+cr, M+cc
                u[cr][cc] = 0
    for cr in range(M):
        diagram[cr][M:M*2] = n[cr][0:M]
    for cr in range(M, M*2):
        diagram[cr][0:M] = w[cr-M][0:M]
    for cr in range(M, M*2):
        diagram[cr][M*2:M*3] = e[cr-M][0:M]
    for cr in range(M, M*2):
        diagram[cr][M:M*2] = u[cr-M][0:M]
    for cr in range(M*2, M*3):
        diagram[cr][M:M*2] = s[cr-M*2][0:M]
    return diagram, sr, sc


def walls_bfs(sr, sc, gr, gc, t):
    que = deque()
    que.append((sr, sc))
    vst = [[0] * (M*3) for _ in range(M*3)]
    vst[sr][sc] = 1
    div = (M*3)//2

    while que:
        cr, cc = que.popleft()
        if cr == gr and cc == gc:
            return vst[cr][cc]-1

        for i in range(4):
            nr, nc = cr + DR[i], cc + DC[i]
            if not (0 <= nr < M*3 and 0 <= nc < M*3):
                continue
            if walls[nr][nc] == 9:
                if (nr < div and nc < div) or (nr > div and nc > div):
                    tr, tc = cc, cr
                    nr, nc = tr, tc
                else:
                    tr, tc = M*3-1-cc, M*3-1-cr
                    nr, nc = tr, tc
            if vst[nr][nc] != 0:
                continue
            if walls[nr][nc] == 1:
                continue
            que.append((nr, nc))
            vst[nr][nc] = vst[cr][cc] + 1
    return 0


def space_bfs(sr, sc, t):
    que = deque()
    que.append((sr, sc))
    vst = [[0] * N for _ in range(N)]
    vst[sr][sc] = 1

    while que:
        cr, cc = que.popleft()
        if space[cr][cc] == 4:
            return vst[cr][cc]

        for i in range(4):
            nr, nc = cr+DR[i], cc+DC[i]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if vst[nr][nc] != 0:
                continue
            if 0 < space[nr][nc] < 4:
                continue
            if space[nr][nc] < 0:
                continue
            que.append((nr, nc))
            vst[nr][nc] = vst[cr][cc]+1
    return 0


if __name__ == '__main__':
    DR = (0, 0, 1, -1)
    DC = (1, -1, 0, 0)
    N, M, F = map(int, input().split())
    space, Ir, Ic, Or, Oc = get_space()
    walls, Sr, Sc = get_walls()

    anomalies = dict()
    for key in range(F):
        r, c, d, v = map(int, input().split())
        anomalies[key] = [r, c, d, v]
        space[r][c] = -2

    turn = 1
    answer = -1

    while True:
        # 시간 이상 현상 확장
        for key in list(anomalies.keys()):
            r, c, d, v = anomalies[key]
            if turn % v != 0:
                continue

            r += DR[d]
            c += DC[d]

            if not(0 <= r < N and 0 <= c < N):
                anomalies.pop(key)
                continue
            if space[r][c] > 0:
                anomalies.pop(key)
                continue

            space[r][c] = -2
            anomalies[key][0] = r
            anomalies[key][1] = c

        # 입구 막힘 체크
        if space[Ir][Ic] == -2:
            break

        # 타임 머신 이동 체크
        w_dist = walls_bfs(Sr, Sc, Or, Oc, turn)
        s_dist = space_bfs(Ir, Ic, turn)

        # 이동 불가 체크
        if s_dist == 0:
            break

        # 이동 시간 체크
        if w_dist + s_dist <= turn:
            answer = turn
            break

        # 턴 증가
        turn += 1

    # 정답 출력
    print(answer)


""" 미지의 공간 탈출 / 20260921 / 체감 난이도: P5
소요 시간 INF / 시도 3 / 실행 시간 87ms (코드트리) / 메모리 19MB (코드트리)
"""
from collections import deque


def get_wall(n, w, t, e, s):
    sr, sc = None, None
    result = [[9] * (M*3) for _ in range(M*3)]
    # 북쪽 180도 회전
    n = [x[::-1] for x in n][::-1]
    # 서쪽 시계방향 90도 회전
    w = [x[::-1] for x in zip(*w)]
    # 동쪽 반시계방향 90도 회전
    e = [x for x in zip(*e)][::-1]
    # 북쪽 채워넣기
    for i in range(M):
        for j in range(M):
            result[i][M+j] = n[i][j]
    # 서쪽 채워넣기
    for i in range(M):
        for j in range(M):
            result[M+i][j] = w[i][j]
    # 동쪽 채워넣기
    for i in range(M):
        for j in range(M):
            result[M+i][M*2+j] = e[i][j]
    # 남쪽 채워넣기
    for i in range(M):
        for j in range(M):
            result[M*2+i][M+j] = s[i][j]
    # 위쪽 채워넣기 (출발 좌표 체크)
    for i in range(M):
        for j in range(M):
            if t[i][j] == 2:
                sr, sc = M+i, M+j
                t[i][j] = 0
            result[M+i][M+j] = t[i][j]
    return result, sr, sc


def find_entrance():
    for cr in range(N):
        for cc in range(N):
            if world[0][cr][cc] == 3:
                for i in range(4):
                    nr, nc = cr+dr[i], cc+dc[i]
                    if world[0][nr][nc] == 0:
                        return nr, nc, (i+2) % 4


def find_exit(i_r, i_c, i_d):
    for cr in range(N):
        for cc in range(N):
            if world[0][cr][cc] == 3:

                i_r = i_r + dr[i_d] - cr
                i_c = i_c + dc[i_d] - cc
                o_d = (i_d + 2) % 4

                if i_r == 0 and o_d == 0:
                    return 0, M+i_c, o_d
                elif i_r == M-1 and o_d == 2:
                    return 3*M-1, M+i_c, o_d
                elif i_c == 0 and o_d == 3:
                    return M+i_r, 0, o_d
                else:
                    return M+i_r, 3*M-1, o_d


def space_move(idx, cr, cc, cd):
    if cr == in_r and cc == in_c and cd == in_d:
        return 1, out_r, out_c
    nr, nc = cr+dr[cd], cc+dc[cd]
    if not(0 <= nr < N and 0 <= nc < N):
        return None, None, None
    if world[0][nr][nc] == 1:
        return None, None, None
    if world[0][nr][nc] == 2:
        return None, None, None
    return idx, nr, nc


def wall_move(idx, cr, cc, cd):
    if cr == out_r and cc == out_c and cd == out_d:
        return 0, in_r, in_c
    nr, nc = cr + dr[cd], cc + dc[cd]
    if not(0 <= nr < M*3 and 0 <= nc <= M*3):
        return None, None, None
    if world[1][nr][nc] == 1:
        return None, None, None
    if world[1][nr][nc] == 2:
        return None, None, None
    if world[1][nr][nc] != 9:
        return idx, nr, nc

    if (cr < M+2 and cc < M+2) or (cr >= M*2-1 and cc >= M*2-1):
        if world[idx][cc][cr] == 1:
            return None, None, None
        if world[idx][cc][cr] == 2:
            return None, None, None
        return idx, cc, cr
    else:
        if world[idx][M*3-1-cc][M*3-1-cr] == 1:
            return None, None, None
        if world[idx][M*3-1-cc][M*3-1-cr] == 2:
            return None, None, None
        return idx, M*3-1-cc, M*3-1-cr


def get_next(idx, cr, cc):
    result = []
    for cd in range(4):
        if idx == 0:
            nidx, nr, nc = space_move(idx, cr, cc, cd)
            if nidx is not None:
                result.append([nidx, nr, nc])
        else:
            nidx, nr, nc = wall_move(idx, cr, cc, cd)
            if nidx is not None:
                result.append([nidx, nr, nc])
    return result


def find_goal():
    for r in range(N):
        for c in range(N):
            if space[r][c] == 4:
                return r, c


def bfs(sidx, sr, sc):
    que = deque()
    que.append((sidx, sr, sc))
    space_vst = [[0] * N for _ in range(N)]
    wall_vst = [[0] * (M*3) for _ in range(M*3)]
    vst = [space_vst, wall_vst]
    vst[sidx][sr][sc] = 1

    while que:
        cidx, cr, cc = que.popleft()
        if cidx == 0 and cr == goal_r and cc == goal_c:
            # for row in space_vst:
            #     print(*row)
            # print()
            # for row in wall_vst:
            #     print(*row)
            # print()
            return vst[cidx][cr][cc]-1

        for nidx, nr, nc in get_next(cidx, cr, cc):
            if vst[nidx][nr][nc] == 0:
                vst[nidx][nr][nc] = vst[cidx][cr][cc]+1
                que.append((nidx, nr, nc))
    return None


def debug(msg):
    print(msg)
    print('미지의 공간')
    print(f'환승: {in_r, in_c}에서 {dr[in_d], dc[in_d]} 방향')
    for row in world[0]:
        print(*row)
    print()
    print('시간의 벽')
    print(f'출발: {start_r, start_c}')
    print(f'환승: {out_r, out_c}에서 {dr[out_d], dc[out_d]} 방향')
    for row in world[1]:
        print(*row)
    print()


if __name__ == '__main__':
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    adapter = [1, 3, 2, 0]

    N, M, K = map(int, input().split())
    space = [list(map(int, input().split())) for _ in range(N)]
    east = [list(map(int, input().split())) for _ in range(M)]
    west = [list(map(int, input().split())) for _ in range(M)]
    south = [list(map(int, input().split())) for _ in range(M)]
    north = [list(map(int, input().split())) for _ in range(M)]
    top = [list(map(int, input().split())) for _ in range(M)]

    # 목적지 좌표 찾기
    goal_r, goal_c = find_goal()

    # 시간의 벽 전개도와 전개도 상에서 출발 좌표 구하기
    wall, start_r, start_c = get_wall(north, west, top, east, south)

    # 세계: 0: 미지의 공간, 1: 시간의 벽
    world = [space, wall]

    # 미지의 공간에서 시간의 벽 안으로 들어오는 좌표와 방향
    in_r, in_c, in_d = find_entrance()

    # 시간의 뱍에서 미지의 공간으로 나가는 좌표와 방향
    out_r, out_c, out_d = find_exit(in_r, in_c, in_d)

    # 시간 이상 현상 받기
    anomalies = []
    for _ in range(K):
        r, c, d, v = map(int, input().split())
        anomalies.append([0, r, c, adapter[d], v])
        world[0][r][c] = 2

    time = 0
    answer = -1

    while True:

        for i in range(K):
            lvl, r, c, d, v = anomalies[i]

            if time > 0 and time % v == 0:
                if lvl == 0:
                    nlvl, nr, nc = space_move(lvl, r, c, d)
                else:
                    nlvl, nr, nc = wall_move(lvl, r, c, d)

                if nlvl is not None:
                    if world[nlvl][nr][nc] != 4:
                        world[nlvl][nr][nc] = 2
                        anomalies[i][0] = nlvl
                        anomalies[i][1] = nr
                        anomalies[i][2] = nc

        dist = bfs(1, start_r, start_c)
        if dist is not None:
            if dist <= time:
                answer = time
                break
            else:
                time += 1
        else:
            break

    # debug('')
    print(answer)
