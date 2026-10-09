""" 아기 바다거북의 대모험: 해저 화산 지대 / 20261009 / 체감 난이도: G3
소요 시간 1시간 / 시도 2회 / 실행 시간 68ms (코드트리) / 메모리 17MB (코드트리)

실수로 정답을 한줄로 출력해서 한번 틀림 ㅋㅋ;;
그냥 귀찮거 할거 많은 전형적인 삼성 기출. 연습용으로 굳.
"""
from collections import deque


class Turtle:
    def __init__(self, ti, tr, tc):
        self.idx = ti
        self.r = tr
        self.c = tc

    def imprint(self):
        occupation[self.r][self.c] = self.idx

    def unprint(self):
        occupation[self.r][self.c] = 0

    def move(self):
        que = deque()
        que.append((self.r, self.c))
        vst = [[0] * N for _ in range(N)]
        vst[self.r][self.c] = 1
        path = dict()

        while que:
            cr, cc = que.popleft()
            if cr == N-1 and cc == N-1:
                break
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = cr+dr, cc+dc
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if vst[nr][nc] != 0:
                    continue
                if geography[nr][nc] > 0:
                    continue
                if occupation[nr][nc] > 0:
                    continue
                que.append((nr, nc))
                vst[nr][nc] = 1
                path[(nr, nc)] = (cr, cc)

        if (N-1, N-1) not in path:
            return
        nr, nc = N-1, N-1
        while True:
            cr, cc = path[(nr, nc)]
            if cr == self.r and cc == self.c:
                self.r, self.c = nr, nc
                return
            nr, nc = cr, cc

    def fossilize(self):
        pass


class Volcano:
    def __init__(self, vi, vr, vc, vt):
        self.idx = vi
        self.threshold = vt
        self.pressure = 0
        self.last_eruption = -1
        self.r = vr
        self.c = vc

    def erupt(self, t):
        if self.last_eruption == t:
            return 0
        if self.pressure+heatmap[self.r][self.c] < self.threshold:
            return 0

        que = deque()
        que.append((self.r, self.c, self.threshold))
        vst = [[0] * N for _ in range(N)]
        vst[self.r][self.c] = 1

        self.last_eruption = t
        self.pressure = 0

        while que:
            cr, cc, cv = que.popleft()
            heatmap[cr][cc] += cv
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc, nv = cr+dr, cc+dc, cv//2
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if vst[nr][nc] != 0:
                    continue
                if geography[nr][nc] == 1:
                    continue
                if nv == 0:
                    continue
                que.append((nr, nc, nv))
                vst[nr][nc] = 1
        return 1


if __name__ == '__main__':
    N, M, K = map(int, input().split())
    geography = [list(map(int, input().split())) for _ in range(N)]
    occupation = [[0] * N for _ in range(N)]
    heatmap = [[0] * N for _ in range(N)]
    answer = [-1] * M

    turtles = dict()
    for i in range(1, M+1):
        r, c = map(int, input().split())
        turtles[i] = Turtle(i, r, c)
        turtles[i].imprint()

    volcanoes = dict()
    for i in range(1, K+1):
        r, c, t = map(int, input().split())
        volcanoes[i] = Volcano(i, r, c, t)

    time = 1
    while time <= 100:
        # 거북이 이동
        for k in sorted(turtles.keys()):
            turtles[k].unprint()
            turtles[k].move()
            turtles[k].imprint()

            if turtles[k].r == N-1 and turtles[k].c == N-1:
                answer[k-1] = time
                turtles[k].unprint()
                turtles.pop(k)

        # 조기 종료
        if not turtles:
            break

        # 화산 압력 증가
        for k in volcanoes:
            volcanoes[k].pressure += 10

        # 화산 연쇄 폭팔
        while True:
            eruption_cnt = 0
            for k, v in volcanoes.items():
                eruption_cnt += v.erupt(time)
            if eruption_cnt == 0:
                break

        # 거북이 화석화
        for k in sorted(turtles.keys()):
            r, c = turtles[k].r, turtles[k].c
            if heatmap[r][c] >= 20:
                turtles[k].unprint()
                turtles.pop(k)
                geography[r][c] = 2
        heatmap = [[0] * N for _ in range(N)]

        # 시간 증가
        time += 1

    # 정답 출력
    for i in answer:
        print(i)


""" 아기 바다거북의 대모험: 해저 화산 지대 / 20261001 / 체감 난이도: G3
소요 시간 1시간 20분 / 시도 1회 / 실행 시간 79ms (코드트리) / 메모리 18MB (코드트리)

[구상]
    - 평소에 자신이 있는 객체 상태 관리 유형의 문제.
    - 아마 클래스를 사용하지 않으면 변수 관리가 꽤나 귀찮을 것으로 예상된다.
    - 문제에서 가장 중요한 점은 화산의 연쇄 폭팔 관리라고 생각한다.
        - 한번 터진 애들은 더 이상 연쇄 작용의 대상에 포함되지 않아야 한다.
        - 마지막으로 분출한 시간을 어디 따로 저장해놓고, 같은 시간에 동일한 화산을
        - 1번 이상 분출시키려는 시도가 발생하면 무시하는 안전장치를 삽입할 수 있다.

[구현]
    - 문제가 굉장히 친절하고 직관적이었기에, 구현에서 크게 어려운 점은 없었다.

[디버깅]
    - 최단 경로 뽑는 과정에서 nr, nr -> nr, nc 오타가 발생하여 수정했다.

[후기]
    - 시험 문제 이렇게 나오면 정말 좋겠는데..
"""
from collections import deque


def debug_turtles(msg):
    if DEBUG_MODE:
        print()
        print(msg)
        for x in occupation:
            print(*x)
        print('---')


def debug_temperature(msg):
    if DEBUG_MODE:
        print()
        print(msg)
        for x in temperature:
            print(*x)
        print('---')


class Turtle:
    def __init__(self, ti, tr, tc):
        self.idx = ti
        self.r = tr
        self.c = tc

    def imprint(self):
        occupation[self.r][self.c] = self.idx

    def unprint(self):
        occupation[self.r][self.c] = 0

    def move(self):
        self.unprint()
        que = deque()
        que.append((self.r, self.c))
        vst = [[0] * N for _ in range(N)]
        vst[self.r][self.c] = 1
        path = dict()

        while que:
            cr, cc = que.popleft()
            if cr == N-1 and cc == N-1:
                break

            for d in range(4):
                nr, nc = cr + DR[d], cc + DC[d]
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if vst[nr][nc] != 0:
                    continue
                if geography[nr][nc] != 0:
                    continue
                if occupation[nr][nc] != 0:
                    continue

                path[(nr, nc)] = (cr, cc)
                que.append((nr, nc))
                vst[nr][nc] = 1

        if (N-1, N-1) not in path:
            self.imprint()
            return

        nr, nc = N-1, N-1
        while True:
            cr, cc = path[(nr, nc)]
            if cr == self.r and cc == self.c:
                self.r = nr
                self.c = nc
                self.imprint()
                return
            nr, nc = cr, cc

    def is_safe(self):
        if self.r == N-1 and self.c == N-1:
            return True
        return False

    def is_dead(self):
        if temperature[self.r][self.c] >= 20:
            return True
        return False

    def fossilize(self):
        geography[self.r][self.c] = 2


class Volcano:
    def __init__(self, vr, vc, vp):
        self.r = vr
        self.c = vc
        self.threshold = vp
        self.pressure = 0
        self.last_eruption = -1

    def erupt(self, call_time):
        if self.last_eruption == call_time:
            return 0
        if self.pressure + temperature[self.r][self.c] < self.threshold:
            return 0

        que = deque()
        que.append((self.r, self.c, self.pressure))
        vst = [[0] * N for _ in range(N)]
        vst[self.r][self.c] = 1

        while que:
            cr, cc, cp = que.popleft()
            temperature[cr][cc] += cp

            for d in range(4):
                nr, nc, np = cr + DR[d], cc + DC[d], cp // 2
                if not (0 <= nr < N and 0 <= nc < N):
                    continue
                if np == 0:
                    continue
                if vst[nr][nc] != 0:
                    continue
                if geography[nr][nc] == 1:
                    continue

                que.append((nr, nc, np))
                vst[nr][nc] = 1

        self.last_eruption = call_time
        self.pressure = 0
        return 1


if __name__ == '__main__':
    DEBUG_MODE = False
    DR = (0, 1, 0, -1)
    DC = (1, 0, -1, 0)

    N, M, K = map(int, input().split())
    geography = [list(map(int, input().split())) for _ in range(N)]
    occupation = [[0] * N for _ in range(N)]
    temperature = [[0] * N for _ in range(N)]
    arrivals = [-1] * M  # OB1

    turtles = dict()
    for i in range(1, M+1):
        r, c = map(int, input().split())
        turtles[i] = Turtle(i, r, c)
        turtles[i].imprint()

    volcanoes = dict()
    for i in range(1, K+1):
        r, c, p = map(int, input().split())
        volcanoes[i] = Volcano(r, c, p)

    time = 1
    while turtles and time <= 100:

        # TODO 1: 바다 거북 이동
        for key in sorted(turtles.keys()):
            turtles[key].move()
            if turtles[key].is_safe():
                arrivals[key-1] = time
                turtles[key].unprint()
                turtles.pop(key)

        # TODO 2: 화산 압력 증가
        for key in volcanoes:
            volcanoes[key].pressure += 10

        # TODO 3: 화산 분출 / 연쇄 반응
        while True:
            eruption_count = 0
            for key in volcanoes:
                erupted = volcanoes[key].erupt(time)
                eruption_count += erupted
            if eruption_count == 0:
                break

        # TODO 4: 화석화
        for key in list(turtles.keys()):
            if turtles[key].is_dead():
                turtles[key].fossilize()
                turtles[key].unprint()
                turtles.pop(key)

        # TODO 5: 환경 초기화
        temperature = [[0] * N for _ in range(N)]

        # TODO 6: 시간 증가
        time += 1

    # 정답 출력
    for time in arrivals:
        print(time)
