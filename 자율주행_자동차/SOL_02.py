""" 자율주행 자동차 / 20260914 / 체감 난이도: S1
소요 시간 20분 / 시도 1회 / 실행 시간 54ms (코드트리) / 메모리 17MB

엥? 과거의 나는 도대체 뭘 한거냐. 그냥 이동 함수 하나로 쉽게 풀 수 있었다.
"""


def move(cr, cc, cd):
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    for i in range(4):
        nd = (cd-1-i) % 4
        nr, nc = cr+dr[nd], cc+dc[nd]

        if arr[nr][nc] != 0:
            continue
        if vst[nr][nc] == 1:
            continue

        vst[nr][nc] = 1
        return nr, nc, nd

    nr, nc = cr-dr[cd], cc-dc[cd]
    if arr[nr][nc] == 1:
        return None, None, None
    else:
        vst[nr][nc] = 1
        return nr, nc, cd


if __name__ == '__main__':
    N, M = map(int, input().split())
    cr, cc, cd = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    vst = [[0] * M for _ in range(N)]

    vst[cr][cc] = 1
    while True:
        nr, nc, nd = move(cr, cc, cd)
        if nr is None:
            break
        else:
            cr, cc, cd = nr, nc, nd
    print(sum(map(sum, vst)))


""" 자율주행 자동차 / 20260818 / 체감 난이도: S1
소요 시간 1시간 16분 / 시도 1회 / 실행 시간 56ms (코드트리) / 메모리 17MB

[구상]
    - 문제를 읽고, 첫 구상안을 작성하기까지 17분을 사용했다.
    - 현재 보고 있는 방향을 기준으로 계속 왼쪽으로 회전하는 조건 때문에 이동경로가 잘 그려지지 않았다.
    - While문 하나에 1번부터 4번까지의 액션을 전부 담아내야 한다는 것도 파악했지만, 스크립트 형식으로 틀리지 않고 구현할 자신이 없었다.
    - 마지막으로 자동차가 바라보는 방향이 계속 변화하는데, 실수라도 했다간 이걸 추적하며 디버깅할 자신이 없었다.
    - 따라서 클래스를 구현해 인스턴스를 뽑기만 하면, 전체 문제를 여러 개의 소문제로 함수화하여 수월하게 풀 수 있으리라 생각했다.

[구현]
    - 디버깅 시간을 포함하지 않은 구현 시간은 총 41분.
    - 가장 많은 시간을 차지한 부분은 자동차 클래스의 생성자 함수였다.
        - 방향에 대한 정보가 0,1,2,3 키로 들어왔는데, 이걸 그대로 생성자에 넣어서 내부적으로 방향 벡터를 설정할지, 외부에서 방향벡터 결정하고 생성자로 넣어줄지 고민을 많이 했다.
        - 결국 후자를 선택했는데, 사실 가장 좋은 방법은 기존의 정수 키를 활용해서 0을 왼쪽으로 보내면 3, 3을 왼쪽으로 보내면 2, ... 이런식으로 하는게 편했을 것이다.
    - 두번째로 시간을 많이 쓴 부분은 뷰 함수들이었다.
        - 문제풀이를 진행하다보니, 이동을 하지 않고 주어진 방향을 체크만 하는 태스크가 있다는 것을 뒤늦게 깨달았다.
        - 현재 방향을 기준으로 '상대적' 왼쪽을 구하고, 그에 맞춰 스캔 결과를 돌려주는 부분에 대해 고민하느라 시간을 많이 썼다.
    - 마지막으로 실행부인 move 함수는 정말 편하게 짤 수 있었다.
        - 남들에 비해 코드가 길고 복잡해 보일 수도 있는 것은 사실이지만, 함수화를 잘 한 덕분에 내가 부담을 느꼈던 부분을 가장 손쉽게 처리할 수 있었다.

[디버깅]
    - 실수 1: view_left에서 방향 벡터를 받아야 하는 변수에 방향 인덱스를 할당해서 unpacking 문제 발생 -> 가볍게 해결
    - 실수 2: backward 함수에서 self.r += self.dr, self.r += self.dc 오타가 나면서 정상 종료가 안됨.
        - 이번 문제를 풀면서 한 가장 치명적인 실수였다. (디버깅 19분)
        - 구현에 시간을 많이 썼는데 결과가 잘못 나오니까 시야가 엄청 좁아져서 코드를 읽기 보다는 프린트문으로 결과 역추적부터 하기 시작했다.
        - 결론적으로 구조화된 코드 덕에 view_back과 backward 함수의 동작이 다르다는 것을 깨닫고, 수정했다.
        - 단순 오타 하나로 이렇게 괴로워질 수 있다는 사실을 깨달았고.. 앞으로는 코드부터 다시 읽어보고 디버깅에 뛰어들어야 겠다는 생각을 했다.

[후기]
    - 함수를 하나 구현할 때마다 테스트를 돌려보는 것을 잊지 말자.
    - 다른 사람들 구현은 훨씬 간결했는데, 과연 이렇게까지 구현하는게 옳은지 앞으로 기출을 많이 풀면서 고민해봐야 한다.
"""


class Car:
    def __init__(self, r, c, dr, dc):
        self.running = True
        self.r, self.c = r, c
        self.dr, self.dc = dr, dc
        self.directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.dir_id = self.directions.index((dr, dc))

    # 왼쪽 살피기
    def view_left(self):
        lft_r, lft_c = self.directions[(self.dir_id + 1) % 4]
        vst_check = vst[self.r + lft_r][self.c + lft_c]
        road_check = road[self.r + lft_r][self.c + lft_c]
        return vst_check, road_check

    # 백미러 보기 ㅋㅋ
    def view_back(self):
        road_check = road[self.r - self.dr][self.c - self.dc]
        return road_check

    # 좌회전 (이동 없이 방향전환만)
    def turn_left(self):
        self.dir_id = (self.dir_id + 1) % 4
        self.dr = self.directions[self.dir_id][0]
        self.dc = self.directions[self.dir_id][1]

    # 전진
    def forward(self):
        self.r += self.dr
        self.c += self.dc
        vst[self.r][self.c] = 1

    # 후진
    def backward(self):
        self.r -= self.dr
        self.c -= self.dc
        vst[self.r][self.c] = 1

    def move(self):
        turn_cnt = 0
        while self.running:

            # 1: 현재 방향 기준 왼쪽 미방문 => 좌회전 + 전진 1
            vc, rc = self.view_left()
            if vc != 1 and rc != 1:
                turn_cnt = 0
                self.turn_left()
                self.forward()

            # 2: 왼쪽 방향이 인도/재방문 => 좌회전 + rollback
            else:
                turn_cnt += 1
                self.turn_left()

                # 3: 2번 시도중 4방향 전부 전진 불가 => 방향 유지 + 후진 1 + rollback
                if turn_cnt == 4:

                    # 4: 3번 시도중 뒷공간 인도 => 작동 중지
                    rc = self.view_back()
                    if rc == 0:
                        turn_cnt = 0
                        self.backward()
                    else:
                        self.running = False
                        return
                    continue
                continue


if __name__ == '__main__':
    R, C = map(int, input().split())
    r, c, d = map(int, input().split())
    road = [list(map(int, input().split())) for _ in range(R)]
    vst = [[0] * C for _ in range(R)]

    # 시작 위치는 반드시 차도임이 보장된다.
    vst[r][c] = 1

    # 입력 방향은 0: 북, 1: 동, 2: 남, 3: 서
    directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    dr, dc = directions[d]

    # 자동차 클래스 인스턴스 초기화 후 가동
    car = Car(r, c, dr, dc)
    car.move()

    # 답 도출
    answer = sum([sum(row) for row in vst])
    print(answer)
