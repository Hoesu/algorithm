""" 마법의 숲 탐색 / 20260918 / 체감 난이도: G4
소요 시간 1시간 44분 / 시도 1 / 실행 시간 317ms (코드트리) / 메모리 24MB (코드트리)

[구상]
    - 처음에는 좀 막막했는데, 문제를 읽다보니까 그냥 십자가로 하는 테트리스 게임이라는 생각이 들었다.
    - 골렘이 숲을 벗어나는 경우는 2차원 테트리스에서 사용했던 방식을 차용했다.
        - 기존 숲 배열의 상단에 행 길이가 3인 버퍼 존을 하나 더 붙여서, 이 안에 골렘이 떨어지는 경우 배열을 비우기로 했다.
    - 골렘의 이동은 조건 체크와 회전이 섞어 있는 형태였는데, 결국 마지막 포지션만 신경 써주면 되는지라 굉장히 편했다.
        - 하, 좌, 우 방향으로 움직일 때 상대 좌표를 사용하기로 했다.
        - 또한, 배열을 전체 회전시키는 것이 아니라, 출구 좌표만 돌려가며 회전하는 시늉을 하기로 했다.
        - 모든 이동이 끝나고 최종 위치에 도달하고 나서야 현황판에 마킹하기로 했다.
    - 정령의 이동도 출구 조건을 제외하면 까다로운 제약이 없었다.
        - 특히 최종 위치에 도달하고 나면 녀석들이 알아서 자동 퇴장해줘서 살았다.
        - 아무튼 출구 조건 파악을 위해 다른 골렘을 참조할 상황이 있는데, 딕셔너리에 고유ID를 키로 미리 저장해서 편하게 체크했다.
        - 물론 숲을 한번 싹 비울 때, 별도의 pop 없이 clear로 속시원하게 날릴 수 있어서 좋았다.

[구현]
    - 이번에 제출할 영상 살짝 의식하면서 루틴 빡세게 따랐다.
    - 실행부 주석 설계 => 검토 및 수정 => 실행부 줄 별 구현 => 검토 => 클래스, 메서드 등 메모해둔 필수 기능 구현
    - 이런 식으로 진행했는데, 중간 중간 단위 테스트도 잘 수행했고, 전반적으로 매우 편안한 구현이었다.

[디버깅]
    - 커스텀 프린트로 몇번 찍어보면서 실수 잡아냈다.
        - 버퍼 존 추가해놓고, 최종행에서 2 빼주지 않은 것.
        - 남쪽 방향 스캔할 때 상대좌표 오타난 것.
        - 출구 좌표 조건 or 해야하는데 and으로 설정한 것.

[후기]
    - 그냥 저냥 할만했다.
"""
from collections import deque


class Golem:
    DR = (-1, 0, 1, 0)
    DC = (0, 1, 0, -1)

    def __init__(self, idx, center_col, exit_dir):
        self.idx = idx
        self.cr = 1
        self.cc = center_col
        self.exit_dir = exit_dir
        self.er = None
        self.ec = None

    def imprint(self):
        board[self.cr][self.cc] = self.idx
        for x in range(4):
            nr = self.cr + Golem.DR[x]
            nc = self.cc + Golem.DC[x]
            board[nr][nc] = self.idx

    def scan(self, vectors):
        for dr, dc in vectors:
            nr = self.cr + dr
            nc = self.cc + dc
            if not(0 <= nr < R+3 and 0 <= nc < C):
                return False
            if board[nr][nc] != 0:
                return False
        return True

    def rotate(self, is_clockwise):
        if is_clockwise:
            self.exit_dir = (self.exit_dir+1) % 4
        else:
            self.exit_dir = (self.exit_dir-1) % 4

    def move(self):
        s_vectors = [(2, 0), (1, -1), (1, 1)]
        w_vectors = [(-1, -1), (0, -2), (1, -2), (1, -1), (2, -1)]
        e_vectors = [(-1, 1), (0, 2), (1, 2), (1, 1), (2, 1)]

        while True:
            s_check = self.scan(s_vectors)
            if s_check:
                self.cr += 1
                continue

            w_check = self.scan(w_vectors)
            if w_check:
                self.cr += 1
                self.cc -= 1
                self.rotate(is_clockwise=False)
                continue

            e_check = self.scan(e_vectors)
            if e_check:
                self.cr += 1
                self.cc += 1
                self.rotate(is_clockwise=True)
                continue

            if not(s_check or w_check or e_check):
                break

        self.er = self.cr + Golem.DR[self.exit_dir]
        self.ec = self.cc + Golem.DC[self.exit_dir]
        self.imprint()

    def get_center(self):
        return self.cr, self.cc

    def get_exit(self):
        return self.er, self.ec


def bfs(sr, sc, si):
    que = deque()
    que.append((sr, sc, si))
    vst = [[0] * C for _ in range(R+3)]
    vst[sr][sc] = 0
    max_row = 0

    while que:
        cr, cc, ci = que.popleft()

        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = cr + dr, cc + dc

            if not(0 <= nr < R+3 and 0 <= nc < C):
                continue
            if board[nr][nc] == 0:
                continue
            if vst[nr][nc] != 0:
                continue

            ni = board[nr][nc]
            if ci != ni:
                er, ec = golems[ci].get_exit()
                if cr != er or cc != ec:
                    continue

            if nr > max_row:
                max_row = nr
            vst[nr][nc] = 1
            que.append((nr, nc, ni))
    return max_row


def debug(gl, time, msg):
    print()
    print(f'time {time}: {msg}')
    print(f'center coords: {gl.get_center()}')
    print(f'exit coords: {gl.get_exit()}')
    for row in board:
        print(*row)


if __name__ == '__main__':
    R, C, K = map(int, input().split())

    # (R+3) * C 크기의 골렘 현황판 초기화
    # 최상단 3행은 숲의 범위를 초과하는 골렘을 잡아내기 위한 영역으로 사용
    board = [[0] * C for _ in range(R+3)]

    # 골렘 인스턴스 보관용 딕셔너리
    golems = dict()

    # 정답: 모든 정령의 최종 행의 총합
    answer = 0

    for i in range(1, K+1):
        # TODO 0: 골렘의 중앙값 열, 출구 방향 인덱스 받기
        #   골렘의 중앙값은 -1 처리를 해줄 것.
        c, d = map(int, input().split())

        # TODO 1: 골렘 인스턴스 초기화: 고유 ID, 중앙값, 출구 방향
        #   만들어진 인스턴스는 딕셔너리에 넣어서 관리하자.
        golem = Golem(i, c-1, d)
        golems[i] = golem

        # TODO 2: 골렘 이동
        #   알아서 갈 수 있는 최대한 남쪽으로 이동 후, 현황판 업데이트
        golem.move()

        # TODO 3: 범위 체크
        #   현황판의 상단 3행이 비어있는지 체크.
        #   1) 비어있다면 그대로 진행
        #   2) 골렘이 들어있다면 격자 전부 비우고 다음 골렘으로 스킵
        #       이때, 골렘 딕셔너리 클리어
        if sum(map(sum, board[:3])) > 0:
            board = [[0]*C for _ in range(R+3)]
            golems.clear()
            continue

        # debug(golem, i, 'after moving golem')

        # TODO 4: 정령의 위치는 현재 다루고 있는 골렘의 중앙 좌표
        #   BFS로 골렘으로만 이루어진 영역을 탐색하고, 최하단 행을 구해야함.
        #   이동 불가능한 경우: 격자 바깥, 골렘이 없는 영역 (0)
        #   같은 골렘 내 이동: 현황판에서 현재 칸의 번호가 같은지 체크
        #   다른 골렘 간 이동: 현황판에서 현재 위치 골렘 ID 추출, 딕셔너리로 출구 좌표 조회 가능
        #   한번 이동 끝나면 격자 내에 남아서 자리를 차지하는 개념이 아님.
        r, c = golem.get_center()
        answer += bfs(r, c, i)-2

    # 정답 출력
    print(answer)
