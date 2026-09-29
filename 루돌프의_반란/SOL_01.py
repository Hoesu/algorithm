""" 루돌프의 반란 / 20260916 / 체감 난이도: P5
소요 시간 3시간 22분 / 시도 2 / 실행 시간 95ms (코드트리) / 메모리 19MB (코드트리)

[구상]
    - 와 이거 진짜 너무 힘들었다. 풀긴 풀었는데, 영구적으로 뇌 기능에 손상 온거 분명함.
    - 일단 문제 설명이 코드트리 빵처럼 각 상태에 대해 체크해야 하는 조건 리스트로 주어졌는데, 정리가 힘들었다.
        - 그래서 내 워딩으로 전부 A4 용지에 적어내린 다음, 빼먹은게 없나 확인하는 체크리스트처럼 사용했다.
        - 특히 "충돌"을 하나로 묶어 설명하고 있는데, 사실상 루돌프 -> 산타, 산타 -> 루돌프 2가지 완전 다른 케이스를 포함하고 있다.
        - 이 때문에 한 스테이지에서 산타 전원 탈락 조건 체크를 루돌프 이동 후와 산타 이동 후 두번에 걸쳐해야겠다는 생각을 했다.
    - 상호작용 파트 나오자 마자 잔뜩 긴장했다. 어제 풀었던 "왕실의 기사대결"처럼 연쇄 반응 유형임을 눈치 챘다.
        - 익숙하지 않은데다가 그냥 이 유형 자체만으로 구현이 좀 빡센 편이라고 생각한다.
        - 특히 저번 문제의 기억을 살려 큐로 구현하는 방식을 채택했는데, 그냥 while문 돌리는게 나았을 것이라 판단해 풀이 후 리팩토링 했다.
            - 기사대결의 경우, 한 객체의 상태가 변할 때, 복수의 객체를 건드릴 수 있어 큐가 좋은 자료구조였다.
            - 하지만 산타나 루돌프는 한번에 단 하나와 충돌하기 때문에 굳이 이렇게 복잡한 구조를 가져갈 필요가 없었던 것이다.
    - 그래도 기절 파트는 내가 자신 있는 유통기한 유형이었다.
        - 굳이 배열에 박아두고 조회하기 보다는, 객체 만들어서 상태값 들고다니게 하고 싶었다.
    - 일단 적어내린 내용 기반으로 자료구조를 정했는데, 돌아보면 다 필요한 자료들이긴 했다.
        - 딕셔너리로 생존 산타, 탈락 산타 따로 보관하고, 키로 주거니 받거니가 편하다.
        - 배열 하나 만들어서 산타, 루돌프 위치 찍어놓는 것도 O(1)으로 충돌 대상 가려내기 위해 필수다.
        - 클래스로 산타 정의해서 인스턴스 들고 다니는 것도 나쁘지 않았다.
            - 기출 후반부에 오니까 정보량 많고, 동작 까다롭고, 수량 제한되어 있는 플레이어 구현이 자주 보인다.
            - 다시 클래스 병이 도진게 아니라, 실제로 쓸만한 기회가 늘어나서 자주 채택하는 듯.
            - 그래도 역할은 최소한으로 가져갔다. 그냥 현재 상태값 기준으로 어디 갈 수 있는지 알려주기만 하는 수준으로.

[구현]
    - 일단 산타 클래스에 기초적인 임플란트부터 박아주고 시작했다.
        - 충돌 대상에 따라서 행동이 바뀌기 때문에, 루돌프 -> 산타, 산타 -> 루돌프, 산타 -> 산타 전부 분리해서 구현했다.
        - 또한, 인스턴스 값 바꿔버리지 않고, 그냥 "너는 알려만 줘, 나머진 내가 알아서 할게" 방식으로 썼다.
    - 솔직히 산타 이동, 루돌프 이동도 이제는 너무 익숙한 탐색 우선순위에 따른 이동이라 쉽게 구현했다.
        - 결과 좌표를 받아서 실행부 구성하는게 제일 빡세다...
    - 연쇄 충돌 짜다가 정말 조상님 보러 갈뻔 했다. 진짜 너무 힘들었음..
        - 제일 힘들었던 파트는 순차적으로 처리하는 와중에 탈락자를 가려내서 이 친구 순번오면 무시하고 진행하는 파트였다.
        - 루돌프 이동이랑 산타 이동이랑 살짝 달라서 조금씩 수정하면서 썼는데, 큐까지 쓰니까 헷갈려서 힘들었던 것 같다.
        - 아 그리고 연쇄 충돌 일어나서 산타들 위치 바뀌면, 이거 바로 바로 업데이트 하지 않고 일괄 업데이트 해야 한다.
        - 그래서 to_pop, to_keep 같은 인덱스 리스트로 관리했는데, 이거 잘 체크해주는게 진짜 힘들었다.
        - 마지막으로 애들 옮겨줄 때 마다 배열 상에서 찍어뒀던 위치 지우고 새로운 위치에 찍어주는게 시점 관리가 진짜 중요하다.
        - 일단 어째 저째 하긴 했는데, 추후에 서술할 디버깅 파트에서 지옥을 맛봤다.

[디버깅]
    - 일단 루돌프는 8방향, 산타는 4방향인데, 각자 독립적으로 행동하는게 아니라 상호작용을 해버린다.
        - 예를 들어 루돌프가 대각으로 박으면 산타가 대각으로 날아감 ㅋㅋㅋ
        - 근데 산타의 행동은 전부 4방향 기준으로 작성되어 있어서 방향 인덱스 주거니 받거니가 안됐다.
        - 나는 이걸 생각 못하고 짰기 때문에 초비상이 걸렸고.. 결국 전부 행/열 델타 값을 직접 넘겨주는 방식으로 수정했다.
    - 그리고 산타 -> 루돌프 충돌할 때 산타는 반대로 튕겨나가고, 뒤에 연쇄적으로 부딫히는 산타들도 똑같이 반대방향으로 날아간다.
        - 반면에 루돌프 -> 산타의 경우, 산타는 루돌프 진행 방향으로 튕기고, 뒤의 모든 산타들도 같은 방향으로 튕긴다.
        - 이걸 사전에 생각하지 않고 hit_by_santa를 동일한 방식으로 썼더니 진행 방향이 아예 꼬여버렸다.
        - 예를 들면 루돌프가 박은 산타는 반대로 튕겨서 오른쪽으로 갔는데, 뒤따라 충돌한 산타들은 왼쪽으로 튕긴다던가...
        - 결국 눈 빠지게 충돌 위주로 디버깅 돌려서 튕기는 방향을 제대로 조정해줬다.
    - 아 그리고 이 문제 진짜 치사한게, 산타 순서대로 돌려야 한담서 산타 인덱스를 지 맘대로 주고 있다.
        - 제발 문제 못풀라고 사주하는 듯한 흉악한 방해에 치가 떨린다.
        - 암튼간에 리프레쉬 할 때 이거 위험할 수도 있겠다는 생각을 해서 sorted 한번만 써주기로 했는데, 너무 바쁜 나머지 까먹었다;;
        - 그래서 오픈 테케 다 맞고 히든 틀리자 마자 코드 첨부터 끝까지 쭉 다 읽고 이 부분만 고쳐서 제출했다.

[후기]
    - 자료구조 제발 신중하게!
    - 순차적으로 뭐 한다 싶으면 그냥 안전하게 정렬하고 쓰자.
    - 상태가 바뀔 때, 상호작용하는 대상들에 따라서 달라질 수 있는 부분을 명확히 짚자.
    - 8방향, 4방향, 2방향 등 되도록이면 통일해서 쓸 수 있는 플랜을 만들자.
"""

class Santa:
    MVDR = (-1, 0, 1, 0)
    MVDC = (0, 1, 0, -1)

    def __init__(self, santa_id, santa_row, santa_col):
        self.idx = santa_id
        self.r = santa_row
        self.c = santa_col
        self.state = -1
        self.score = 0

    def imprint(self):
        board[self.r][self.c] = self.idx

    def unprint(self):
        board[self.r][self.c] = 0

    def coma(self, t):
        self.state = t + 1

    def move_santa(self, gr, gc):
        # 현재 위치에서 루돌프까지의 거리
        candidates = []
        cdist = (self.r - gr) ** 2 + (self.c - gc) ** 2

        # 이동 가능한 네 방향 탐색
        for nd in range(4):
            nr = self.r + Santa.MVDR[nd]
            nc = self.c + Santa.MVDC[nd]

            # 격자 밖으로 나가는 경우 스킵
            if not (0 <= nr < N and 0 <= nc < N):
                continue

            # 다른 산타가 있는 칸으로는 이동 불가
            if board[nr][nc] > 0:
                continue

            # 현재 위치보다 루돌프와 가까워지는 경우만 후보에 추가
            ndist = (nr - gr) ** 2 + (nc - gc) ** 2
            if ndist < cdist:
                candidates.append([nr, nc, nd, ndist])

        # 이동할 수 있는 칸이 없으면 이동하지 않음
        if not candidates:
            return self.r, self.c, None, None

        # 거리, 방향 순으로 우선순위가 높은 후보 선택
        candidates.sort(key=lambda x: [x[-1], x[-2]])
        nr, nc, nd, _ = candidates[0]
        return nr, nc, Santa.MVDR[nd], Santa.MVDC[nd]

    def hit_rudolf(self, rr, rc, dr, dc, t):
        # 루돌프와 충돌한 산타의 처리
        self.coma(t)
        self.score += D
        # 루돌프가 이동한 방향의 반대 방향으로 D칸 튕겨나감
        nr = rr - dr * D
        nc = rc - dc * D
        return nr, nc

    def hit_by_rudolf(self, rr, rc, dr, dc, t):
        # 루돌프에게 충돌당한 산타의 처리
        self.coma(t)
        self.score += C
        # 루돌프가 이동한 방향으로 C칸 튕겨나감
        nr = rr + dr * C
        nc = rc + dc * C
        return nr, nc

    def hit_by_santa(self, dr, dc):
        # 다른 산타에게 밀려난 산타의 위치 계산
        nr = self.r + dr
        nc = self.c + dc
        return nr, nc


def move_rudolf(rr, rc):
    # 현재 루돌프 위치에서 가장 가까운 산타 탐색
    candidates = []

    for key in in_santa:
        sr = in_santa[key].r
        sc = in_santa[key].c
        dist = (rr - sr) ** 2 + (rc - sc) ** 2

        # 거리 → 행 큰 순 → 열 큰 순으로 정렬하기 위한 정보 저장
        candidates.append([dist, sr, sc])

    candidates.sort(key=lambda x: [x[0], -x[1], -x[2]])
    _, gr, gc = candidates[0]

    # 가장 가까운 산타에게 가까워지는 이동 방향 탐색
    min_dist = int(1e9)

    for i in range(8):
        nr = rr + delta_r[i]
        nc = rc + delta_c[i]

        # 격자 밖으로 나가는 경우 스킵
        if not (0 <= nr < N and 0 <= nc < N):
            continue

        # 목표 산타와의 거리가 가장 가까워지는 방향 선택
        dist = (gr - nr) ** 2 + (gc - nc) ** 2

        if dist < min_dist:
            min_dist = dist
            fr, fc, fd = nr, nc, i

    return fr, fc, delta_r[fd], delta_c[fd]


if __name__ == '__main__':
    # 루돌프의 8방향 이동 방향
    delta_r = (-1, -1, 0, 1, 1, 1, 0, -1)
    delta_c = (0, 1, 1, 1, 0, -1, -1, -1)

    N, M, P, C, D = map(int, input().split())

    # 루돌프 위치 입력 및 0-index 변환
    Rr, Rc = map(int, input().split())
    Rr, Rc = Rr - 1, Rc - 1

    # 현황 보드 초기화 후 루돌프 위치 표시
    board = [[0] * N for _ in range(N)]
    board[Rr][Rc] = -1

    # 산타 인스턴스 보관할 딕셔너리 초기화
    # 키: 산타 ID, 밸류: 산타 인스턴스
    in_santa = dict()
    out_santa = dict()

    # 산타 정보를 딕셔너리와 현황 보드에 삽입
    for _ in range(P):
        Pn, Sr, Sc = map(int, input().split())
        Sr, Sc = Sr - 1, Sc - 1

        board[Sr][Sc] = Pn
        santa = Santa(Pn, Sr, Sc)
        in_santa[Pn] = santa

    # 기절 시간 측정을 위한 시간값 초기화
    time = 0

    for _ in range(M):

        # 1. 루돌프 이동
        board[Rr][Rc] = 0

        # 루돌프의 새로운 위치와 이동 방향 계산
        Rr, Rc, Rdr, Rdc = move_rudolf(Rr, Rc)

        # 2. [루돌프 -> 산타] 충돌 체크
        if board[Rr][Rc] > 0:

            # 루돌프에게 맞은 산타의 위치
            cSr, cSc = Rr, Rc

            # 연쇄 작용 결과 저장용 리스트
            # 충돌 과정에서 산타 위치를 바로 갱신하면
            # 아직 처리하지 않은 산타의 위치를 덮어쓸 수 있으므로 일괄 반영
            to_keep = []
            to_pop = []

            # 처음 맞은 산타만 다르게 움직임
            is_first = True

            # 연쇄 작용 연산
            while True:
                # 맞은 산타 ID 뽑기
                key = board[cSr][cSc]

                # 맞은 산타 현황 보드에서 위치 지우기
                in_santa[key].unprint()

                # 처음 맞은 산타는 루돌프에게 직접 튕겨나감
                if is_first:
                    nSr, nSc = in_santa[key].hit_by_rudolf(Rr, Rc, Rdr, Rdc, time)
                    is_first = False

                # 이후 산타는 앞의 산타에게 한 칸 밀려남
                else:
                    nSr, nSc = in_santa[key].hit_by_santa(Rdr, Rdc)

                # 격자 밖으로 나가면 탈락, 연쇄 종료
                if not (0 <= nSr < N and 0 <= nSc < N):
                    to_pop.append(key)
                    break

                # 새로운 위치 저장
                to_keep.append([key, nSr, nSc])

                # 다음 위치에 산타가 없으면 연쇄 종료
                if board[nSr][nSc] == 0:
                    break

                # 다음 위치에 산타가 있으면 해당 산타를 계속 밀어냄
                cSr, cSc = nSr, nSc

            # 연쇄 과정에서 계산한 산타들의 새로운 위치 일괄 적용
            for key, Sr, Sc in to_keep:
                in_santa[key].r = Sr
                in_santa[key].c = Sc
                in_santa[key].imprint()

            # 탈락한 산타 딕셔너리 이동
            for key in to_pop:
                out_santa[key] = in_santa.pop(key)

        # 루돌프 위치 업데이트
        board[Rr][Rc] = -1

        # 3. 산타 전원 탈락하면 즉시 종료
        if not in_santa:
            break

        # 4. 산타 이동
        to_pop = set()

        # 산타 ID가 작은 순서대로 이동
        for key in sorted(in_santa.keys()):

            # 앞선 이동에서 탈락한 산타들은 무시
            if key in to_pop:
                continue

            # 기절한 산타는 무시
            if in_santa[key].state >= time:
                continue

            # 이동 전 기존 위치를 현황 보드에서 제거
            in_santa[key].unprint()

            # 산타의 새로운 위치와 이동 방향 계산
            Sr, Sc, Sdr, Sdc = in_santa[key].move_santa(Rr, Rc)

            # 이동할 수 없는 경우 기존 위치 복구 후 스킵
            if Sdr is None and Sdc is None:
                in_santa[key].imprint()
                continue

            # 5. [산타 -> 루돌프] 충돌 체크
            if Sr == Rr and Sc == Rc:

                # 연쇄 작용 결과 저장용 리스트
                # 충돌 과정에서 산타 위치를 바로 갱신하면
                # 아직 처리하지 않은 산타의 위치를 덮어쓸 수 있으므로 일괄 반영
                to_keep = []

                # 처음 충돌한 산타의 위치부터 연쇄 작용 시작
                cSr, cSc = Rr, Rc

                # 처음 충돌한 산타만 다르게 움직임
                is_first = True

                # 연쇄 작용 연산
                while True:

                    # 처음 충돌한 산타는 루돌프에게 직접 튕겨나감
                    if is_first:
                        move_key = key
                        nSr, nSc = in_santa[move_key].hit_rudolf(Rr, Rc, Sdr, Sdc, time)
                        is_first = False

                    # 이후 산타는 앞의 산타에게 한 칸 밀려남
                    else:
                        move_key = board[cSr][cSc]
                        in_santa[move_key].unprint()
                        nSr, nSc = in_santa[move_key].hit_by_santa(-Sdr, -Sdc)

                    # 격자 밖으로 나가면 탈락, 연쇄 종료
                    if not (0 <= nSr < N and 0 <= nSc < N):
                        to_pop.add(move_key)
                        break

                    # 새로운 위치 저장
                    to_keep.append([move_key, nSr, nSc])

                    # 다음 위치에 산타가 없으면 연쇄 종료
                    if board[nSr][nSc] == 0:
                        break

                    # 다음 위치에 산타가 있으면 해당 산타를 계속 밀어냄
                    cSr, cSc = nSr, nSc

                # 연쇄 과정에서 계산한 산타들의 새로운 위치 일괄 적용
                for move_key, Sr, Sc in to_keep:
                    in_santa[move_key].r = Sr
                    in_santa[move_key].c = Sc
                    in_santa[move_key].imprint()

            # 충돌하지 않은 경우 새로운 위치로 이동
            else:
                in_santa[key].r = Sr
                in_santa[key].c = Sc
                in_santa[key].imprint()

        # 탈락한 산타 딕셔너리 이동
        for move_key in to_pop:
            out_santa[move_key] = in_santa.pop(move_key)

        # 6. 산타 전원 탈락하면 즉시 종료
        if not in_santa:
            break

        # 7. 살아남은 산타 전원 1점 추가
        for key in in_santa:
            in_santa[key].score += 1

        # 8. 시간 증가
        time += 1

    # 생존/탈락 산타 전원 점수 조회
    # ID와 점수를 임시 배열에 저장
    temp = []
    for key in in_santa:
        temp.append([key, in_santa[key].score])
    for key in out_santa:
        temp.append([key, out_santa[key].score])

    # 산타 ID 순으로 정렬
    temp.sort(key=lambda x: x[0])

    # ID 순으로 점수 출력
    answer = [pair[1] for pair in temp]
    print(*answer)
