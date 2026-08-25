"""전투 로봇 / 20260824 / 체감 난이도: G4
소요 시간 INF / 시도 4회 / 실행 시간 59ms (코드트리) / 메모리 16MB (코드트리)

[구상]
    - 구상 시간 총 23분. 이번에도 클래스로 풀어보려고 했다.
    - 로봇의 행동을 최단거리 스캔, 가장 가까운 타겟 탐색, 이동과 처치로 나누어 생각했다.
    - 탐색은 BFS로 했고, 순위는 우선순위 큐를 사용하여 따지기로 하였다.

[구현]
    - 구현 과정에서 큰 실수를 두가지 범했다. 생각해보면 풀만한 문제였지만, 그냥 실력으로 깨졌다.
        1) 로봇의 레벨이 6보다 높아질 수 있다는 것을 간과했다. -> 인덱스 에러
        2) 로봇이 갈 수 없는 칸의 방문 배열 값 처리를 잘못하여 음수가 거리 값으로 들어왔다. -> 오답

[디버깅]
    - 솔직히 현재 구조를 그대로 가져간다면 똑같은 실수를 또 반복했을것 같다.
    - 첫번째 실수는 시간 초과를 피하려고 나름의 최적화를 시도하는 과정에서 발생했다.
        - 기존에는 검사 대상들을 전부 리스트에 넣던가 해서 IN 연산을 함으로써 항상 시간초과의 위험에 놓여있었다.
        - 이를 개선하기 위해서 SET 자료형과 DISCARD(O[1]) 함수를 활용하기 시작했다.
        - 이번 문제에서는 몬스터를 찾기 위해 매번 원본 배열을 순회하는 것을 방지하기 위해 먹을 수 있는 범위의 레벨만 살펴보고, 처치한 몬스터에 대한 정보는 셋에서 삭제하려고 했다.
        - 하지만 전투 로봇의 레벨이 7을 초과하면 인덱스 에러가 발생하게 된다.
        - 최적화에 집착하다보니, 오히려 이런 사소한 에러에 대해 취약해지는 스스로를 발견할 수 있었다.
    - 두번째 에러 같은 경우, 레벨은 낮은데 방문할 수 없는 칸을 0처리 후 힙큐에 넣을때 1을 빼주게 되면서 음수가 되어버린 케이스였다.
        - 내가 직접 짠 코드이기에 방문 배열 값이 0인 경우가 나올 수 있다는 사실을 알고 있었다. (뒷단에서 예외 처리도 하고 있었음)
        - 하지만 오류가 한번 안보이기 시작하면 끝도 없기 때문에...
        - 어떻게 하면 처음부터 이런 버그를 방지할 수 있을지 고민이다.
    - 암튼 간에 어떻게든 정답을 맞춰보려고 별의별 예제들을 뽑아서 다 해봤다.
        - 가로막혀 있어서 한마리도 처치하지 못하는 시나리오도 시도해봤지만, 그 벽 넘어 처치할 수 있는 몬스터가 존재하는 시나리오 까지 확장하지 못했다.
        - 버그 찾기 너무 어렵다. 아예 지우고 처음부터 다시 짜봤어야 하나?

[후기]
    - 결국 모든 버그는 get_target 함술로부터 비롯되었다.
        - 우선순위 큐를 과신하여 음수 체크고 뭐고 뜯어볼 생각을 안했다. -> 그리고 생각해보니 이거 굳이 쓸 필요도 없었음.
        - 셋 자료형 활용해서 탐색 범위 관리하는 연습하면서 숙련도를 올릴 필요가 있다.
"""
from collections import deque
from heapq import heappush, heappop


class Robot:
    def __init__(self, sr, sc):
        self.r = sr
        self.c = sc
        self.level = 2
        self.kills = 0
        self.age = 0
        self.run = True

    def scan_area(self):
        vst = [[0] * N for _ in range(N)]
        vst[self.r][self.c] = 1
        que = deque()
        que.append([self.r, self.c])
        while que:
            cr, cc = que.popleft()
            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if battlefield[nr][nc] > self.level:
                    continue
                if vst[nr][nc] != 0:
                    continue
                vst[nr][nc] = vst[cr][cc] + 1
                que.append([nr, nc])
        return vst

    def get_target(self, vst):
        # 현재 위치에서 가장 가까운 죽일만한 몬스터 위치 체크
        wanted = []
        for lv, ms in enumerate(monsters):
            if self.level <= lv:
                continue
            for nr, nc in ms:
                if vst[nr][nc] == 0:
                    continue
                heappush(wanted, [vst[nr][nc]-1, nr, nc, lv])
        if wanted:
            d, nr, nc, lv = heappop(wanted)
            monsters[lv].discard((nr, nc))
            return d, nr, nc
        return None, None, None

    def kill(self):
        self.kills += 1
        battlefield[self.r][self.c] = 0
        if self.kills == self.level:
            self.level += 1
            self.kills = 0

    def move(self):
        # 주어진 위치로 이동, 시간 기록, 몬스터 살해.
        vst = self.scan_area()
        distance, gr, gc = self.get_target(vst)
        # 더 이상 갈 수 있는 곳이 없으면 종료
        if distance is None:
            self.run = False
            return
        # 현재 위치 이동
        self.r, self.c = gr, gc
        # 이동한 시간만큼 나이 추가
        self.age += distance
        # 이동한 위치에서 몬스터 살해
        self.kill()


if __name__ == '__main__':
    N = int(input())
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
    monsters = [set() for _ in range(7)]
    battlefield = [[0] * N for _ in range(N)]
    sr, sc = 0, 0

    for r in range(N):
        line = list(map(int, input().split()))
        for c in range(N):
            if 1 <= line[c] <= 6:
                # 몬스터의 레벨을 인덱스로 하여 위치 저장.
                monsters[line[c]].add((r, c))
                battlefield[r][c] = line[c]
            elif line[c] == 9:
                # 전투로봇의 시작 위치를 추출.
                sr, sc = r, c
                battlefield[r][c] = 0
            else:
                continue

    # 시뮬레이션 시작
    robot = Robot(sr, sc)
    while robot.run:
        robot.move()
    print(robot.age)
