""" 왕실의 기사대결 / 20260915 / 체감 난이도: G1
소요 시간 2시간 30분 / 시도 2회 / 실행 시간 97ms (코드트리) / 메모리 19MB (코드트리)

[구상]
    - 이 문제에서 가장 어려운 부분은 연쇄적인 이동의 구현이라고 생각한다.
        - 지령을 받은 기사가 움직이면, 그에 따라 인접한 기사들이 움직인다.
        - 이때, 이들이 움직일 수 있는지를 결정하는 요인이 마지막 기사의 위치다.
            - 예를 들어 마지막 기사가 벽에 붙어있다면 이동이 불가능하고, 빈칸이 존재하다면 이동이 가능한 구조.
        - 각종 반례를 찾아보며 "all or nothing" 문제라는 결론을 내리는데 시간이 좀 걸렸다.
    - 관리할 상태값, 행동이 꽤나 있는 편이고, 객체 수도 30으로 제한되어 있어 그냥 클래스 쓰기로 했다.
        - 사실 문제에서 제시한 조건에 맞춰 객체를 설계하는 파트는 대부분의 경우 쉽다.
        - 단, 내가 만든 객체가 문제에서 요구하는 과정을 따라가기에 적합한 형태인지가 무척 중요하다.
        - 그렇기 때문에 한번 잘못 만들어두면 실행부를 작성하는 파트에서 꼬이거나, 방향성을 잃을 수 있다.
        - 여러번 클래스를 활용한 구현에 실패하면서, 객체 안에 최소한의 행동을 담는 것이 낫다는 결론을 내렸다.
            - 예를 들면 객체 내부적으로 연쇄작용을 전부 계산하는 것이 아니라,
            - 연쇄작용 계산에 필요한 단위 행동들을 인스턴스 메서드로 구현하여 레고 조립하듯이 실행부를 구성하는 것.
            - 복잡한 과정을 단순하게 표현하여 나의 삶을 윤택하게 만들어주는 정도. 딱 그 정도다.
    - 그리고 문제 특성상 뭐 이리도 쓸데없는 중복값들이 많은지... 집합 자료를 잘 써야했다.
        - 근데 이게 구상 단계에서 자료구조 다 짜고 들어갔다가 안좋은 경험을 많이 해서..
        - 그냥 큰 뼈대만 잡고 필요할 때 적절하게 추가해주는 방식으로 하나씩 추가했다.
        - 결정적으로 한 기사가 동시에 여러 기사를 밀어내는 경우에 대한 중복처리를 누락해서 틀려버렸다. 젠장.

[구현]
    - 역시 입력값 정리, 객체 설계 파트는 쉽게 쉽게 구현했다. 이때가 제일 행복함.
        - 가장 잘한 부분은 역시 스캔과 이동을 분리한 것이라고 생각한다. 조건이 맞아야 일괄 이동이 가능하기 때문.
        - 스캔 부분도 무식하게 해야하나 잠깐 고민했지만, 경계좌표면을 활용하여 필요한 칸들만 조회한 것이 좋았다고 생각한다.
            - 방향 별로 봐야하는 범위만 따로 추리고, 나머지는 동일한 방식으로 처리해서 코드 깔끔해지는건 덤이고.
            - 정확히 이쯤에서 부터 중복값에 대한 걱정이 들어 스캔 결과를 집합으로 처리하기로 했다.
                - 어차피 어떤 종류의 지형과 기사를 만났는지만 중요하기 때문이다!
    - 실행부의 문턱에서 고민을 많이 했다.
        - 연쇄작용을 재귀적으로 처리할지, 순차적으로 처리할지를 두고 머리가 복잡했기 때문이다.
        - 이게 만약 내가 생각한대로 all or nothing 문제가 아니라면 재귀적으로 들어가서 트리 구조로 부모-자식 관계를 구축해야 한다고 생각했다.
        - 이때가 약 1시간 20분째 였는데, 잠깐 나가서 머리 좀 식히고 돌아왔다.
    - 솔직히 나갔다 오는 것에 대한 효능을 아직도 잘 체감하지 못하고 있었다.
        - 근데 강제로가 아니라 그냥 내가 답답할 때 다녀오니까 의외로 효과가 있었다.
        - 먼저 all or nothing이 확실하니 버퍼를 활용한 순차처리가 가능함을 확실하게 결론내렸다.
        - 또한, 기사가 이동할 때 기존 위치에 있던 표식들을 전부 지우는 메커니즘이 필요하단 생각도 들었다.
        - 좁은 공간이라 하더라고 조금씩 걸으면서 생각하니까 흐릿했던 부분들이 전부 뚜렷해져 연결고리가 생겼다.

[디버깅]
    - 스캔 함수 단위 테스트 정말 빡세게 돌렸다.
        - 이놈한테 코드 복잡도를 싹다 몰아줬기 때문에, 실수 나올 수 밖에 없다고 생각했다.
        - 검증 덕분에 오류 싹다 잡음.
    - 대충 2시간 쯤에 구현을 다 마치고 검증을 앞두고 있었는데, 강제 이주 정책이 펼쳐졌다.
        - 에잉 모르겠다, 하고 제출하고 갔다왔는데 틀렸음 ㅋㅋㅋ
        - 3번 틀렸길래 까보니까 아주 친절한 테케가 나왔다. (오픈 1개만 주는건 진짜 너무 매너 없는거 아닌가?)
        - 몇번 돌려보니까 기사 한명이 여러명 동시에 건드릴 때 중복해서 이동시켰다는게 보였다.
        - 이번 구현 워낙 깔끔하게 하기도 했고, 디버깅도 쉬운 테케라 바로 문제를 파악할 수 있었다.
    - 30분 동안 할게 없어서 질릴때까지 테케 만들어서 돌렸다. (처음부터 이러셨어야지. 왜 이제와서..?)
        - 꾹 참고 30분 지나서 제출하니 정답이 나왔다.
        - 검증 똑바로 해야겠죠? 작은 테케 많이 만들어서 돌려봐요 좀...

[후기]
    - 손이 근질근질근질근질
"""
from collections import deque


class Knight:
    # 방향 정보 클래스 변수로 선언 (불변)
    DR = (-1, 0, 1, 0)
    DC = (0, 1, 0, -1)

    def __init__(self, i, r, c, h, w, k):
        self.id = i
        self.r = r-1
        self.c = c-1
        self.h = h
        self.w = w
        self.health = k
        self.damage = 0
        self.geo_info = set()
        self.occ_info = set()

    # TODO 0: occupation 배열에 현재 자신의 위치를 ID로 표기하는 함수
    def imprint(self):
        for x in range(self.h):
            for y in range(self.w):
                occupation[self.r+x][self.c+y] = self.id

    # TODO 1: occupation 배열에 현재 자신의 위치를 비우는 함수
    def unprint(self):
        for x in range(self.h):
            for y in range(self.w):
                occupation[self.r+x][self.c+y] = 0

    # TODO 2: 해당 방향의 모든 경계 좌표를 1만큼 이동 시킬 때,
    #  geography와 occupation에서 만나는 값들에 대한 정보를 반환하는 함수
    def scan(self, d):
        self.geo_info.clear()
        self.occ_info.clear()

        if d == 0:
            scope = [(self.r, self.r+1), (self.c, self.c+self.w)]
        elif d == 1:
            scope = [(self.r, self.r+self.h), (self.c+self.w-1, self.c+self.w)]
        elif d == 2:
            scope = [(self.r+self.h-1, self.r+self.h), (self.c, self.c+self.w)]
        else:
            scope = [(self.r, self.r+self.h), (self.c, self.c+1)]

        for cr in range(scope[0][0], scope[0][1]):
            for cc in range(scope[1][0], scope[1][1]):
                nr = cr + Knight.DR[d]
                nc = cc + Knight.DC[d]

                if not(0 <= nr < L and 0 <= nc < L):
                    self.geo_info.add(2)
                    continue

                self.geo_info.add(geography[nr][nc])
                self.occ_info.add(occupation[nr][nc])
        return self.geo_info, self.occ_info

    # TODO 3: 주어진 방향으로 좌상단 좌표 값을 업데이트하는 함수
    def move(self, d):
        self.r = self.r + Knight.DR[d]
        self.c = self.c + Knight.DC[d]

    # TODO 4: 현재 기사가 밟고 있는 함정의 개수를 세고, 체력을 감소시키는 함수
    def trap(self):
        for x in range(self.h):
            for y in range(self.w):
                if geography[self.r+x][self.c+y] == 1:
                    self.health -= 1
                    self.damage += 1


if __name__ == '__main__':
    # 격자 크기, 기사의 수, 명령의 수
    L, N, Q = map(int, input().split())
    # 빈칸, 함정, 그리고 벽의 정보를 담은 배열
    geography = [list(map(int, input().split())) for _ in range(L)]
    # 현재 각 기사가 차지하는 칸의 정보를 담은 배열
    occupation = [[0] * L for _ in range(L)]
    # 각 기사의 ID와 인스턴스 객체를 담아둘 딕셔너리
    knights = dict()

    for i in range(1, N+1):
        r, c, h, w, k = map(int, input().split())
        kn = Knight(i, r, c, h, w, k)
        kn.imprint()
        knights[i] = kn

    for _ in range(Q):
        idx, direction = map(int, input().split())

        # 생존한 기사에 한해서 명령 수행
        if idx not in knights:
            continue

        # 큐를 초기화하여 연쇄작용 계산
        movable = True
        buffer = deque([idx])
        movers = set()

        while buffer:
            # 다음 기사 인덱스 뽑기
            cur_idx = buffer.popleft()
            movers.add(cur_idx)
            # 호출된 기사를 주어진 방향으로 이동 시키면
            # geography, occupation에서 어떤 정보를 만나는지 반환
            geo_info, occ_info = knights[cur_idx].scan(direction)
            # geo_info: 벽(2)이 있으면 갈 수 없음
            if 2 in geo_info:
                movable = False
                break
            # occ_info: 이동하려는 칸에 다른 기사가 있으면 밀쳐냄
            # 중복 이동 방지: 힌번 이동한건 다시 연산 안함!
            occ_info.discard(0)
            for nxt_idx in occ_info:
                if nxt_idx not in movers:
                    buffer.append(nxt_idx)

        # 이동 불가능하면 다음 명령으로 전환
        if not movable:
            continue

        for kn_idx in movers:
            # 새로운 위치로 기사를 이동
            knights[kn_idx].unprint()
            knights[kn_idx].move(direction)
            # 지령을 받은 기사를 제외한 모든 기사들에게 함정으로 인한 피해 적용
            if kn_idx != idx:
                knights[kn_idx].trap()
                # 만약 체력이 0이하로 떨어졌다면 제거
                if knights[kn_idx].health <= 0:
                    knights.pop(kn_idx)

        # 배열에 정보 일괄적으로 업데이트
        for key in knights:
            knights[key].imprint()

    # 살아남은 기사들에게 누적된 피해합 출력
    answer = 0
    for key in knights:
        answer += knights[key].damage
    print(answer)
