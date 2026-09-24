""" 생명과학부 랩 인턴 / 20260924 / 체감 난이도: G5
소요 시간 1시간 / 시도 2회 / 실행 시간 437ms (코드트리) / 메모리 26MB (코드트리)

아 제발 문제 아는척 하지말고 처음 읽는다는 생각으로 풀어 회수야!!
딕셔너리 숙련도가 많이 올라서 구현이 진짜 깔끔해지긴 했다.
그런데 진동함수 익숙하다고 까불다가 여기서 문제 엄청 많이 발생했다.
제발 아는척 하지 말고 건실하게 검증하면서 풀자. 체력 빠진거 같으면 쉬다와라.
"""


def debug(msg):
    print(msg)
    for k, v in fungi.items():
        print(k, v)
    print('---')


def move(row, col, speed, direction):
    if direction % 2 == 0:
        distance = speed % ((R-1) * 2)
    else:
        distance = speed % ((C-1) * 2)
    for _ in range(distance):
        if direction == 0 and row == 0:
            direction = (direction + 2) % 4
        elif direction == 2 and row == R-1:
            direction = (direction + 2) % 4
        elif direction == 1 and col == C-1:
            direction = (direction + 2) % 4
        elif direction == 3 and col == 0:
            direction = (direction + 2) % 4
        row += dr[direction]
        col += dc[direction]
    return row, col, direction


if __name__ == '__main__':
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    adapter = [0, 2, 1, 3]

    R, C, K = map(int, input().split())
    fungi = dict()
    for _ in range(K):
        x, y, s, d, b = map(int, input().split())
        fungi[(x-1, y-1)] = [s, adapter[d-1], b]

    # TODO 0: 채취한 곰팡이 크기의 총합과, 다음 세대 곰팡이 딕셔너리 초기화
    answer = 0
    next_fungi = dict()

    for c in range(C):
        # debug('')
        # TODO 1: 현재 열의 0행에서부터 아래로 내려가며 곰팡이 탐색
        #   가장 먼저 발견하는 곰팡이 크기 정답에 더해주기
        #   현재 위치를 키로 잡고 곰팡이 딕셔너리에서 pop, break
        #   (한 좌표에 반드시 하나의 곰팡이만 있음이 보장됨.)
        for r in range(R):
            if (r, c) in fungi:
                answer += fungi[(r, c)][2]
                fungi.pop((r, c))
                break

        # TODO 2: 곰팡이 이동
        #   다음 세대 곰팡이 딕셔너리 비우기
        #   방향, 속력 고려하여 다음 위치 계산 (진동함수, 모듈로 연산 필수)
        #   다음 위치가 이미 딕셔너리에 존재한다면
        #       크기 비교하여 더 큰 값을 가지는 곰팡이로 덮어쓰기
        #   다음 위치가 딕셔너리에 존재하지 않는다면
        #       새롭게 삽입
        next_fungi.clear()
        for (cr, cc), (s, d, b) in fungi.items():
            nr, nc, nd = move(cr, cc, s, d)
            if (nr, nc) in next_fungi:
                if next_fungi[(nr, nc)][2] < b:
                    next_fungi[(nr, nc)] = [s, nd, b]
            else:
                next_fungi[(nr, nc)] = [s, nd, b]

        # TODO 3: 다음 세대로 넘어가기
        fungi = next_fungi.copy()

    # 정답 출력
    print(answer)


""" 생명과학부 랩 인턴 / 20260901 / 체감 난이도: G5
소요 시간 1시간 31분 / 시도 1회 / 실행 시간 513ms (코드트리) / 메모리 29MB (코드트리)

[구상]
    - 스토리만 바꾼 원자충돌이라고 생각했다.
    - 일단 브루트포스로 풀기에 딱히 어려움이 없어보이면 반드시 시간 제한을 빡세게 준다. 계산해보니 N * 10^8.
    - 구현에 들어가기 전에 미리 계획해둔 2가지 핵심 파트는 다음과 같다.
        - 진동 함수를 이용해 벽면과 충돌 시 튕겨나오는 방식의 움직임 구현
            - 속도가 최대 1000까지 올라갈 수 있기에 시간 절약에 아주 중요하다. while 돌릴 시간 아까움.
        - 딕셔너리로 특정 좌표에 대한 곰팡이 카운트, 리스트를 기록
            - 배열 전체 순회할 필요 없이 곰팡이 위치를 핀포인트 가능하다.

[구현]
    - 구현 과정이 굉장히 길고 피곤했다.
    - 일단 진동 함수를 '개미' 문제 이후로 처음 구현해봤는데, 오랜만이라 그런지 모듈로를 어디다 찍어야 할지 헷갈렸다.
        - 개별 스크립트를 따로 파서 직접 돌려보면서 검증하는데 상당한 시간을 할애했다.
    - 익숙한 문제라고 생각하고 구현에 들어갔는데, 생각해보니까 나는 원자 충돌을 클래스로 해결했었다.
        - 그러다보니 각 곰팡이가 가지고 있는 상태를 지속적으로 체크하고 업데이트하는 과정이 살짝 어색했다.
        - 이것 때문에 실수가 하나 나왔는데, 모듈로 이동 구현은 잘 했지만, 반전된 방향 벡터를 반환하지 않았다.
        - 따라서 첫번째 이동에선 무조건 알맞은 위치로 가지만, 중간에 방향이 바꼈다면 그 뒤부턴 죄다 엉뚱하게 움직이는 해프닝이 발생했다.
    - 그래도 셋의 활용도는 이제 제법 익숙해졌다.
        - 이전 단계에서 곰팡이를 성공적으로 수거했다면, 해당 좌표를 기억해뒀다가 나중 단계에서 떨궈내는 방식으로 구현했다.
        - 또한, 전체 루프를 도는 대신에 모든 박테리아 정보를 셋에 담아두고 필요한 부분만 순회하는 방식으로 진행하였다.

[디버깅]
    - break문 인덴트 잘못 찍은거 찾느라 시간을 썼다.

[후기]
    - 관리해야 할 값들이 많아서 피로도가 상당한 문제.
"""


def move(cr, cc, dr, dc, sp):
    # 열을 따라 움직인다면 세로로 진동
    if dr != 0:
        # 속력에 모듈로를 적용하여 최소한의 움직임만 구현한다.
        step = sp % (2 * (N - 1))
        # 벽에 부딪히면 방향 벡터를 반전 시켜서 왔던 길을 돌아간다.
        while step > 0:
            if (dr == -1 and cr == 0) or (dr == 1 and cr == N-1):
                dr *= -1
            cr += dr
            step -= 1
    # 행을 따라 움직인다면 가로로 진동
    else:
        step = sp % (2 * (M - 1))
        while step > 0:
            if (dc == -1 and cc == 0) or (dc == 1 and cc == M-1):
                dc *= -1
            cc += dc
            step -= 1
    return cr, cc, dr, dc


if __name__ == '__main__':
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    N, M, K = map(int, input().split())

    # 모든 곰팡이를 셋에 담아두자.
    fungus = set()
    # 현재 곰팡이의 위치를 찍어볼 수 있는 현황판
    batch = [[0] * M for _ in range(N)]

    # 입력값 순서대로 받기
    for _ in range(K):
        x, y, s, d, b = map(int, input().split())
        dr, dc = directions[d-1]
        # 곰팡이 정보 저장
        fungus.add((x-1, y-1, s, dr, dc, b))
        # 곰팡이 위치 마킹
        batch[x-1][y-1] = b

    # 수집한 공팜이 무게의 합
    collected = 0
    # 카운터 용도로 사용할 딕셔너리
    table = dict()
    # 수거하고 버린 애들 정보 담을 셋
    to_discard = set()
    # 다음 라운드까지 살아있는 박테리아 담을 셋
    nxt_fungus = set()

    for c in range(M):
        # 0: 딕셔너리, 집합 비우기: 시간이 꽤 절약된다.
        # 인스턴스 새로 초기화하는게 은근 비용이 크다.
        table.clear()
        to_discard.clear()
        nxt_fungus.clear()

        # 1: 열을 내려가면서 탐색: 곰팡이 찾으면 버릴 목록에 추가, 현황판에서 지우고 루프 탈출.
        for r in range(N):
            if batch[r][c] > 0:
                collected += batch[r][c]
                to_discard.add((r, c))
                batch[r][c] = 0
                break

        # 2: 곰팡이 이동
        for cr, cc, s, dr, dc, b in fungus:
            batch[cr][cc] = 0
            # 현재 곰팡이 버릴 목록에 있으면 무시.
            if (cr, cc) in to_discard:
                continue
            # 이동 후 곰팡이 위치와 방향 벡터 계산하기
            nr, nc, ndr, ndc = move(cr, cc, dr, dc, s)
            # 현재 위치 저장이 처음이면 키 직접 생성하고 값 삽입
            if (nr, nc) not in table.keys():
                table[(nr, nc)] = [1, [(s, ndr, ndc, b)]]
            # 현재 위치 키가 이미 있으면 카운트 1 증가, 정보 리스트에 삽입
            else:
                table[(nr, nc)][0] += 1
                table[(nr, nc)][1].append((s, ndr, ndc, b))

        # 3: 곰팡이 포식
        for k, v in table.items():
            cr, cc = k
            # 현재 위치에 곰팡이 2개 이상이면 크기 오름차순으로 정렬
            if v[0] >= 2:
                v[1].sort(key=lambda q: q[3])
            # 크기 제일 큰 곰팡이만 뽑기
            s, dr, dc, b = v[1].pop()
            # 현황판 업데이트
            batch[cr][cc] = b
            # 다음 세대 곰팡이 집합에 추가
            nxt_fungus.add((cr, cc, s, dr, dc, b))
        # 카피 떠서 다시 원본 곰팡이 집합으로 재할당
        fungus = nxt_fungus.copy()

    # 정답 출력
    print(collected)
