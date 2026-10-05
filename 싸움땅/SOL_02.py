""" 싸움땅 / 20261005 / 체감 난이도: G3
소요 시간 50분 / 시도 1 / 실행 시간 209ms / 메모리 23MB (코드트리)

일단 코드는 훨씬 더 정돈된 느낌, 접근 방식은 완전 동일.
그도 그럴게 이때 진짜 힘들게 디버깅 하면서 문제를 거의 외워버렸기 때문.
시간이 좀 늘어났는데, 총을 줍고 버리는 과정을 힙큐로 처리했다. 다시 안풀 문제.
"""
from heapq import heappop, heappush


class Player:
    def __init__(self, pi, pr, pc, pd, ps):
        self.idx = pi
        self.r = pr
        self.c = pc
        self.d = pd
        self.s = ps
        self.g = 0

    def imprint(self):
        p_board[self.r][self.c] = self.idx

    def unprint(self):
        p_board[self.r][self.c] = 0

    def move(self):
        nr = self.r + DR[self.d]
        nc = self.c + DC[self.d]
        if not(0 <= nr < N and 0 <= nc < N):
            nd = (self.d + 2) % 4
            nr = self.r + DR[nd]
            nc = self.c + DC[nd]
            self.r, self.c, self. d = nr, nc, nd
            return nr, nc
        self.r, self.c = nr, nc
        return nr, nc

    def retreat(self):
        for k in range(4):
            nd = (self.d + k) % 4
            nr = self.r + DR[nd]
            nc = self.c + DC[nd]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if p_board[nr][nc] > 0:
                continue
            self.r, self.c, self.d = nr, nc, nd
            return

    def drop_gun(self):
        heappush(g_board[self.r][self.c], -self.g)
        self.g = 0

    def update_gun(self):
        if g_board[self.r][self.c]:
            pick_up = -heappop(g_board[self.r][self.c])
            if self.g == 0:
                self.g = pick_up
                return
            if pick_up > self.g:
                heappush(g_board[self.r][self.c], -self.g)
                self.g = pick_up
            else:
                heappush(g_board[self.r][self.c], -pick_up)

    def fight(self, other):
        fighters = [
            [self.idx, self.s, self.g],
            [other.idx, other.s, other.g]
        ]
        fighters.sort(key=lambda z: (-(z[1]+z[2]), -z[1]))
        power_diff = abs((self.s+self.g)-(other.s+other.g))
        return fighters[0][0], fighters[1][0], power_diff


if __name__ == '__main__':
    DR = (-1, 0, 1, 0)
    DC = (0, 1, 0, -1)

    N, M, K = map(int, input().split())
    g_board = [[[] for _ in range(N)] for _ in range(N)]
    p_board = [[0] * N for _ in range(N)]
    players = dict()
    scores = [0] * M

    # 총 정보
    for r in range(N):
        line = list(map(int, input().split()))
        for c in range(N):
            if line[c] > 0:
                g_board[r][c].append(-line[c])

    # 플레이어 정보
    for i in range(1, M+1):
        x, y, d, s = map(int, input().split())
        players[i] = Player(i, x-1, y-1, d, s)
        p_board[x-1][y-1] = i

    for _ in range(K):
        for i in range(1, M+1):

            players[i].unprint()
            ir, ic = players[i].move()

            if p_board[ir][ic] == 0:
                players[i].update_gun()
                players[i].imprint()

            else:
                # 싸움으로 승자와 전력 차이 가리기
                w_id, l_id, diff = players[i].fight(players[p_board[ir][ic]])
                W = players[w_id]
                L = players[l_id]
                # 점수 정산
                scores[W.idx-1] += diff
                # 패자는 총을 버리고 도망
                L.drop_gun()
                L.retreat()
                L.update_gun()
                L.imprint()
                # 승자는 총을 업데이트
                W.update_gun()
                W.imprint()

    # 정답 출력
    print(*scores)


""" 싸움땅 / 20260914 / 체감 난이도: G3
소요 시간 INF / 시도 2 / 실행 시간 116ms (코드트리, 리팩토링 후 151) / 메모리 19MB (코드트리)

[구상]
    - 클래스 쓸 때마다 이상하게 조져서 고민 좀 했는데, 클래스가 딱 맞는 문제라고 생각했다.
        - 인스턴스의 수는 제한되어 있는데, 하나의 인스턴스가 지니는 정보나 행동이 상대적으로 많다.
        - 삼성 기출에서 클래스의 역할은 딱 여기까지인 것 같다. 그냥 커스텀 가능한 뚱뚱한 딕셔너리.
    - 그 외에 구상 단계에선 특별할 이슈가 없었다.
        - 그냥 승자와 패자가 총을 획득하고 버리는 타이밍을 서순에 잘 맞춰줘야 한다는 정도?

[구현]
    - 구현도 그냥 저냥 했는데.. 익숙하고 쉽다고 생각하는 부분에서 상대적으로 집중력이 부족했던것 같다.
    - 3차원 배열에서 총 줍기나 후퇴 메커니즘 같은건 엄밀하게 검증했는데, 가장 기본이 되는 이동 함수는 그냥 후딱 짜고 넘어갔다.

[디버깅]
    - 틀린 이유는 어이 없게도 이동 단계에서 90도씩 돌아가는 부분에서 방향 인덱스 업데이트를 이상하게 하고 있었다.
        - 불변값을 하나 따로 두고 그걸 기반으로 업데이트 해줬어야 하는데, 자기 자신을 업데이트 하고 있었다.
        - 결론적으로 한번에 풀었을 문제를 self 단 네글자 때문에 이틀이나 쳐다보고 있었다.
        - 심지어 틀린 테케가 더럽게 길어서 디버깅으로 문제를 찾기도 어려웠다.
        - 만약 다음에도 비슷한 상황이 발생한다면.. 하기 싫은 마음 꾹 참고 몸든 함수를 단계적으로 검증해야겠다.
    - 솔직히 억울하냐 하면 그렇지도 않다. 이런것도 다 실력임 ㅇㅇ
        - 이런 미세한 버그는 솔직히 인간이라면 한번씩 다 발생시키게 되어있다고 생각한다.
        - 원천차단이 불가능하다면 적어도 같은 실수라도 반복해야 하기에.. 실수 리스트에 추가했다.

[후기]
    - 이건 다시 풀어도 클래스다.
    - 관리할 값이 너무 많아서 일반 자료형 썼으면 머리 터졌을것 같다.
"""


class Player:
    DR = (-1, 0, 1, 0)
    DC = (0, 1, 0, -1)

    def __init__(self, i, x, y, d, s):
        self.idx = i
        self.r = x-1
        self.c = y-1
        self.d = d
        self.stat = s
        self.gun = 0
        self.point = 0

    def move(self):
        # 일반적인 이동: 격자 탈출 시 방향 반전하여 한칸 이동
        nd = self.d
        nr = self.r + Player.DR[nd]
        nc = self.c + Player.DC[nd]
        if not(0 <= nr < N and 0 <= nc < N):
            nd = (self.d+2) % 4
            nr = self.r + Player.DR[nd]
            nc = self.c + Player.DC[nd]
        self.r, self.c, self.d = nr, nc, nd
        return self.r, self.c

    def retreat(self):
        # 싸움 패배 후 이동: 범위 내에 다른 플레이어가 없는 칸을 찾을때까지 90도 시계방향 회전
        # 탈출 가능 보장됨 (원래 위치로 돌아가면 그만)
        for i in range(4):
            nd = (self.d+i) % 4
            nr = self.r + Player.DR[nd]
            nc = self.c + Player.DC[nd]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if ppl_field[nr][nc] != 0:
                continue
            self.r, self.c, self.d = nr, nc, nd
            break
        return self.r, self.c

    def drop_gun(self):
        # 총 떨어뜨리기
        if self.gun <= 0:
            return
        gun_field[self.r][self.c].append(self.gun)
        gun_field[self.r][self.c].sort()
        self.gun = 0

    def take_gun(self):
        # 이동한 위치에 총이 존재.
        if gun_field[self.r][self.c]:
            # 현재 총을 가지고 있지 않음.
            if self.gun == 0:
                best_gun = gun_field[self.r][self.c].pop()
                self.gun = best_gun
            # 현재 총을 가지고 있음.
            else:
                if self.gun < gun_field[self.r][self.c][-1]:
                    best_gun = gun_field[self.r][self.c].pop()
                    gun_field[self.r][self.c].append(self.gun)
                    gun_field[self.r][self.c].sort()
                    self.gun = best_gun

    def fight(self, other):
        order = sorted([
            [player.idx, player.get_power(), player.get_stats()],
            [other.idx, other.get_power(), other.get_stats()]
        ], key=lambda z: (-z[1], -z[2]))
        winner = players[order[0][0]]
        loser = players[order[1][0]]
        points = abs(order[0][1] - order[1][1])
        return winner, loser, points

    def get_power(self):
        return self.stat + self.gun

    def get_stats(self):
        return self.stat

    def get_point(self):
        return self.point

    def add_point(self, n):
        self.point += n


if __name__ == '__main__':
    N, M, K = map(int, input().split())
    gun_field = [[[] for _ in range(N)] for _ in range(N)]
    ppl_field = [[0] * N for _ in range(N)]

    for r in range(N):
        line = list(map(int, input().split()))
        for c in range(N):
            if line[c] > 0:
                gun_field[r][c].append(line[c])

    players = dict()
    for i in range(1, M+1):
        x, y, d, s = map(int, input().split())
        ppl_field[x-1][y-1] = i
        players[i] = Player(i, x, y, d, s)

    for _ in range(K):
        for idx, player in players.items():
            # 움직일 플레이어 기존 위치 지우기
            ppl_field[player.r][player.c] = 0
            # 규칙에 따라 새로운 위치 뽑기
            nr, nc = player.move()

            # 이동한 위치에 플레이어 없음.
            if ppl_field[nr][nc] == 0:
                ppl_field[nr][nc] = player.idx
                player.take_gun()

            # 이동한 방향에 플레이어 있음.
            else:
                # 다음 위치에 있는 플레이어 가져와 전투 시작
                other = players[ppl_field[nr][nc]]
                winner, loser, points = player.fight(other)

                # 이긴 플레이어 점수 추가
                winner.add_point(points)
                ppl_field[nr][nc] = winner.idx

                # 진 플레이어 총 떨어뜨리고 도망
                loser.drop_gun()
                fr, fc = loser.retreat()
                loser.take_gun()
                ppl_field[fr][fc] = loser.idx

                # 이긴 플레이어 총 줍기
                winner.take_gun()

    answer = []
    for player in players.values():
        answer.append(player.get_point())
    print(*answer)
