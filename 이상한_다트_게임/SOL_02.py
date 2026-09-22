""" 메두사와 전사들 / 20260922 / 체감 난이도: P5
소요 시간 INF / 시도 4회 / 실행 시간 464ms (코드트리) / 메모리 25MB (코드트리)

[구상]
    - 문제를 소문제로 나누어 단계별로 생각하는 시간을 가졌다.
    - 메두사의 최단 경로 이동
        - 도로에는 변화가 생기지 않기 때문에, 처음 확인해보고 아예 갈 수 없다면 -1을 출력하고, 그 다음부터는 체크할 필요가 없다.
        - BFS와 딕셔너리를 사용하여 최단 경로를 뽑는 것은 이제 아주 익숙하므로 쉽게 할 수 있다고 생각했다.
    - 메두사의 시선 처리
        - 여기서 하드코딩 말고는 답이 떠오르지 않았다.
        - BFS 응용으로 가능할 것도 같은데, 어제처럼 묘수 찾기에 혈안이 되지 않기로 다짐하고 일단 넘어갔다.
        - 그리고 보는 방향을 정하고 나면 배열을 리턴해서 돌로 변신시킬 전사들을 찾아야 한다.
            - 근데 최대 50*50 배열을 매 턴마다 4번씩 복사하는게 너무 무겁지 않을까 두려웠다.
            - 하지만 별 다른 방법이 생각나지 않아서 일단 강행하기로 했다.
    - 전사의 우선 순위 이동
        - 첫번째 이동과 두번째 이동이 각기 다른 방향 우선순위를 지닌다는 것을 제외하면 특별할 것 없는 파트였다.
        - 다만, 현재 위치와 메두사의 시야각에 따라 아예 이동일 불가능한 경우도 있는지 생각해봤다.
            - 생각하다보니 머리가 복잡해져서, 그냥 움직이지 못하는 경우도 무사히 넘어가게 하는 방식으로 구현하기로 했다.
    - 전사의 공격
        - 단순한 위치 비교지만, 죽는 전사들을 안전하게 제거해주는 것이 중요하다.

[구현]
    - 실행부 정말 정말 빡세게 계획했고, 덕분에 시선처리를 제외한 모든 코드를 2시간 이전에 작성했다.
    - 시선 처리는 주석 처리하여 공란으로 비워두고, 메두사 이동 -> 전사 우선 순위 이동 -> 전사 공격을 순서대로 돌리면서 작성한 코드를 검증했다.
    - 덕분에 핵심 구현인 메두사의 시선 처리를 아직 해결하지 못했음에도 불구하고, 상대적으로 안정적인 마음가짐으로 풀이에 임할 수 있었다.
        - 만약에 어제와 같이 메두사의 시선 처리에 붙잡혀서 다른 부분을 시작조차 못했다면, 이번 문제도 제출에 실패했을 것이다.
        - 무슨 일이 있어도 루틴대로 간다, 세부 구현이 당장 생각은 안나지만 큰 그림부터 잡는다, 생각하고 가니까 끝까지 포기하지 않고 잡고 끌고 갈 수 있었다.
    - 1시간 30분 정도 메두사의 시선처리에 대해 고민하고, 구현하는 시간을 가졌다.
        - 패턴이 보이기 시작하면 BFS로 풀 수 있겠다 싶었는데, 그보다 먼저 하드코딩 솔루션이 떠올랐다.
        - 살짝 괴상하긴한데, 안정감을 가지고 시간 박으니까 안될 것도 되는 현상을 목격했다.
        - 이 함수는 개별 스크립트를 파서 따로 검증했었는데, 좀 더 엄밀하게 단위 테스트를 돌렸어야 했다.

[디버깅]
    - 첫 제출은 9번 테케에서 걸렸다.
        - 미리 만들어뒀던 커스텀 프린트로 돌려보며 메두사가 오른쪽을 봐야하는 상황에서 아래를 보고 있다는 것을 확인했다.
        - 장시간 디버깅 끝에 메두사 하드코딩에서 실수한걸 깨달았고, span값 계산에서 off-by-one 에러가 발생한 것을 알 수 있었다.
    - 2번, 3번 제출은 둘 다 런타임 에러가 발생했다.
        - 중반부 테케에서 걸려서 열어보지도 못하고 답답한 상황이었다.
        - 런타임 에러의 원인에 대한 여러가지 가설을 세워보았다.
            1) BFS 최단 경로 함수에서 좌표 인덱싱 에러가 발생했다.
            2) 메두사 시선 처리에서 범위 바깥 처리를 빼먹은 부분이 있다.
            3) 메두사를 공격하고 죽은 전사들의 인덱스 처리가 잘못되어 키 에러가 발생했다.
        - 사실 이때 풀이 시간이 약 15분 정도 남았던 시점이라, 차분하게 처음부터 끝까지 읽기보다는 감으로 의심되는 지점을 급하게 찍어서 버저비터를 던지려고 했다.
        - 1번은 템플릿이기도 하고, 도착하지 못한 케이스 한번 체크하면 무조건 작동하기 때문에 넘어갔다.
        - 2번은 방향 바꿔서 뻗어나가는 모든 시점에서 범위 체크를 해주고 있기 때문에 이 부분이 원흉이라고 생각하기 어려웠다.
        - 마지막으로 3번이 뭔가 의심스러웠는데, 키 순회 방식을 바꿔보기도 하고, 전사가 남아있는 상황에서만 시선처리와 전사 이동이 실행되게끔 조율도 해봤다.
    - 결국 시간 내에 문제를 찾지 못했다.
        - 밥 먹고 와서 처음부터 끝까지 디버깅을 돌려보다가 우연히 occupation 행렬을 따로 프린트 해봤는데.. 이게 왠걸 일부 칸에 리스트가 들어가 있었다.
        - 커스텀 프린트에서는 보기 편하려고 모든 집합을 리스트로 변환해서 출력하고 있었기 때문에 디버깅 단계에서 잡지 못했다.
        - 알고보니 메두사가 이동하면서 해당 칸에 전사들이 존재할 때, 해당 칸을 비운답시고 집합 자료형 위치에 빈 리스트를 박고 있었다.
        - 비교적 작은 테케에서는 이렇게 비워둔 칸을 다시 조회하지 않을 수도 있기에 멀쩡하게 답이 나오지만, 케이스가 커지면 리스트에 add를 하는 시도가 생기면서 런타임 오류가 발생한 것이다.
        - 이 부분민 고쳐서 제출하니까 바로 정답이 나왔다.
        - 나무박멸, 싸움땅에 이어 또, 또, 또 덮어씌우기에서 실수했다.

[후기]
    - 다음엔 BFS로 메두사 시선 처리를 해결해보자. 하드코딩 한번 해보니까 얼추 느낌 온다.
    - 막막한 상황에서의 대처법에 대한 시야가 확실하게 트인 것 같다.
        - 비록 실수해서 문제를 틀리긴 했지만, 적어도 어제처럼 무력하게 맞고 있지만은 않았다.
        - 아쉬움은 있지만, 후회나 미련이 남지는 않는다. 앞으로의 대처가 더 중요하니까.
    - 덮어씌우기 실수에 대해 기똥찬 해결책이 하나 생각났다.
        - 나는 어차피 디버거 잘 안쓰니까, 값을 덮어 씌우는 구현이 있으면 무조건 브레이크 포인트를 찍어두자.
        - 코드를 제출하기 전, 혹은 문제가 발생했을 때, 코드를 위에서부터 읽으며 브레이크 포인트가 찍혀있는 부분을 중점적으로 체크하는거다.
"""
from collections import deque


class Warrior:
    def __init__(self, i, r, c):
        self.i = i
        self.r = r
        self.c = c
        self.t = -1

    def unprint(self):
        occupation[self.r][self.c].discard(self.i)

    def imprint(self):
        occupation[self.r][self.c].add(self.i)

    def move(self, watch):
        cand_1 = []
        cand_2 = []
        total_dist = 0

        cur_dist = abs(self.r - Mr) + abs(self.c - Mc)
        for i, (dr, dc) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
            nr = self.r + dr
            nc = self.c + dc
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if watch[nr][nc] == 1:
                continue
            nxt_dist = abs(nr - Mr) + abs(nc - Mc)
            if nxt_dist < cur_dist:
                cand_1.append([nr, nc, nxt_dist, i])

        if cand_1:
            cand_1.sort(key=lambda x: [x[2], x[3]])
            self.r = cand_1[0][0]
            self.c = cand_1[0][1]
            total_dist += 1

        cur_dist = abs(self.r - Mr) + abs(self.c - Mc)
        for i, (dr, dc) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0)]):
            nr = self.r + dr
            nc = self.c + dc
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if watch[nr][nc] == 1:
                continue
            nxt_dist = abs(nr - Mr) + abs(nc - Mc)
            if nxt_dist < cur_dist:
                cand_2.append([nr, nc, nxt_dist, i])

        if cand_2:
            cand_2.sort(key=lambda x: [x[2], x[3]])
            self.r = cand_2[0][0]
            self.c = cand_2[0][1]
            total_dist += 1

        return self.r, self.c, total_dist

    def stone(self, time):
        self.t = time

    def get_loc(self):
        return self.r, self.c


def move_medusa(sr, sc):
    que = deque()
    que.append((sr, sc))
    vst = [[0] * N for _ in range(N)]
    vst[sr][sc] = 1

    # 경로 저장용 딕셔너라 초기화
    route = dict()

    while que:
        cr, cc = que.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = cr + dr, cc + dc
            # 격자 탈출 무시
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            # 재방문 무시
            if vst[nr][nc] != 0:
                continue
            # 비포장 무시
            if geography[nr][nc] != 0:
                continue
            # 새로운 칸 방문
            que.append((nr, nc))
            vst[nr][nc] = vst[cr][cc] + 1
            route[(nr, nc)] = (cr, cc)

    # 도달 불가능한 경우: 실패 처리
    if (Er, Ec) not in route:
        return None, None, False
    # 도달 가능한 경우: 한칸 이동 후 좌표 반환
    cr, cc = Er, Ec
    while True:
        nr, nc = route[(cr, cc)]
        if nr == sr and nc == sc:
            return cr, cc, True
        else:
            cr, cc = nr, nc


def watch_medusa(sr, sc):
    # 설명할 자신 없음.
    dr = [-1, -1, 0, 1, 1, 1, 0, -1]
    dc = [0, 1, 1, 1, 0, -1, -1, -1]
    adapter = [0, 4, 6, 2]
    candidates = []

    for i in range(4):
        arr = [[0] * N for _ in range(N)]
        cd = adapter[i]
        r_clock = (cd+1) % 8
        c_clock = (cd-1) % 8

        cr = sr + dr[cd]
        cc = sc + dc[cd]
        while True:
            if not(0 <= cr < N and 0 <= cc < N):
                break
            if occupation[cr][cc]:
                arr[cr][cc] = 1
                break
            arr[cr][cc] = 1
            cr += dr[cd]
            cc += dc[cd]

        for clock in [r_clock, c_clock]:
            cr = sr + dr[clock]
            cc = sc + dc[clock]

            if i == 0:
                span = cr
            elif i == 1:
                span = N-1-cr
            elif i == 2:
                span = cc
            else:
                span = N-1-cc

            while True:
                if not(0 <= cr < N and 0 <= cc < N):
                    break
                if occupation[cr][cc]:
                    arr[cr][cc] = 1
                    break

                for j in range(1, span+1):
                    nr = cr + dr[cd] * j
                    nc = cc + dc[cd] * j
                    if not (0 <= nr < N and 0 <= nc < N):
                        break
                    if occupation[nr][nc]:
                        arr[nr][nc] = 1
                        span = j-1
                        break
                    arr[nr][nc] = 1

                arr[cr][cc] = 1
                cr += dr[clock]
                cc += dc[clock]

        stone_cnt = 0
        for idx in warriors:
            wr, wc = warriors[idx].get_loc()
            if arr[wr][wc] == 1:
                stone_cnt += 1
        candidates.append([stone_cnt, i, arr])
    candidates.sort(key=lambda x: [-x[0], x[1]])
    return candidates[0]


def debug(msg):
    print(msg)
    print(f'Medusa Location: {Mr, Mc}')
    print(f'Warrior Location:')
    for row in occupation:
        print(*[list(x) for x in row])
    print(f'Warrior Information:')
    for key in warriors:
        print(f'{key}: {warriors[key].get_loc()}')
    print(f'Geography Details:')
    for row in geography:
        print(*row)
    print()


if __name__ == '__main__':
    N, M = map(int, input().split())
    Sr, Sc, Er, Ec = map(int, input().split())

    warriors = dict()
    warrior_data = list(map(int, input().split()))
    occupation = [[set() for _ in range(N)] for _ in range(N)]

    for idx in range(len(warrior_data)//2):
        wr = warrior_data[idx*2]
        wc = warrior_data[idx*2+1]
        occupation[wr][wc].add(idx+1)
        warriors[idx+1] = Warrior(idx+1, wr, wc)

    geography = [list(map(int, input().split())) for _ in range(N)]

    # TODO 0: 공원 도달 가능 여부 검사
    #   (Sr, Sc)에서 (Er, Ec)까지 도로만 따라서 BFS 돌리고, 공원 방문 가능한지 체크
    _, _, reachable = move_medusa(Sr, Sc)

    # TODO 1: 메두사 위치 초기화
    Mr, Mc = Sr, Sc

    time = 0
    while True and reachable:
        # TODO 2: 정답 출력에 사용될 값들 모음
        travelled = 0
        stoned = 0
        attacked = 0

        # TODO 3: 메두사 이동
        #   0번에서 사용했던 최단경로 BFS 함수 재활용
        #       상하좌우 이동 우선순위를 그대로 사용
        #   도로 위에서 한칸 이동하고, 해당 위치에 전사 있으면
        #       occupation에서 비우고, warriors에서 인덱스 pop하여 전사 제거
        Mr, Mc, _ = move_medusa(Mr, Mc)
        if occupation[Mr][Mc]:
            for idx in list(occupation[Mr][Mc]):
                warriors.pop(idx)
            occupation[Mr][Mc].clear()

        # TODO 4: 종료 체크
        #   메두사가 공원에 도착했다면 0 출력하고 종료
        if Mr == Er and Mc == Ec:
            print(0)
            break

        # TODO 5: 메두사 시선
        #   후보군 리스트 초기화
        #       상하좌우 순서에 맞춰 시야각 계산
        #       돌로 만든 병사의 수 계산
        #       후보군 리스트에 우선순위 방향 인덱스, 돌 병사 수 넣고 정렬
        #   최종 선발된 방향으로 시야 배열 채워서 반환
        #   시야 각에 들어간 전사 1초 스턴 걸어주기
        #       이번 턴 돌로 변한 수 1 증가
        if warriors:
            stone_cnt, _, watch = watch_medusa(Mr, Mc)
            stoned += stone_cnt
            for idx in warriors:
                wr, wc = warriors[idx].get_loc()
                if watch[wr][wc] == 1:
                    warriors[idx].stone(time)

            # TODO 6: 전사 이동
            #   메두사와 맨하탄 거리 줄이는 칸으로 이동
            #   격자 탈출 불가, 시야 내로 이동 불가
            #   1) 상하좌우, 2) 좌우상하
            # TODO 7: 전사 공격
            #   메두사와 같은 칸으로 이동한 전사 찾기
            #   메두사 공격하고 퇴장
            for idx in list(warriors.keys()):
                if warriors[idx].t == time:
                    continue

                warriors[idx].unprint()
                wr, wc, dist = warriors[idx].move(watch)
                if dist > 0:
                    travelled += dist
                if wr == Mr and wc == Mc:
                    attacked += 1
                    warriors.pop(idx)
                else:
                    warriors[idx].imprint()

        # TODO 8: 이번 턴 정답 출력
        print(travelled, stoned, attacked)

        # TODO 9: 시간 증가
        time += 1

    # TODO 10: 공원 도달 불가능하면 -1 출력
    if not reachable:
        print(-1)
