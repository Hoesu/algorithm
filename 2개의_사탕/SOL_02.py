""" 2개의 사탕 / 20260928 / 체감 난이도: G3
소요 시간 44분 / 시도 1회 / 실행 시간 752ms / 메모리 26MB (코드트리)

실행 시간이 여전히 길긴한데, 이전에 여러번 리팩토링을 걸쳐 달성한 시간임을 감안하면 준수하다고 생각된다.
이거 뭐 BFS로 푸는 방법도 있었던거 같은데, 그걸 아는 상태에서 방법을 떠올려보는건 좀 반칙인거 같아서
그냥 내가 느끼기에 가장 자연스러운 방법대로 풀었다.

솔직히 이번 풀이는 너무 쉽게 느껴졌다.
굳이 다른 점을 뽑자면 배열을 굳이 변환하지 않았다는 것과
이동 방향에 따라서 우선 순위 정렬 후 사탕 이동을 하나의 함수에서 한방에 처리했다는 점이다.
다시 풀지는 않을 문제. 아니다, 다음엔 BFS?
"""


def tilt(br, bc, rr, rc, d):
    movers = [[br, bc, 'B'], [rr, rc, 'R']]
    if d == 0:
        movers.sort(key=lambda x: x[0])
    elif d == 1:
        movers.sort(key=lambda x: -x[0])
    elif d == 2:
        movers.sort(key=lambda x: x[1])
    else:
        movers.sort(key=lambda x: -x[1])

    escaped = []
    cr1, cc1, m1 = movers[0]
    while True:
        nr, nc = cr1 + dr[d], cc1 + dc[d]
        if board[nr][nc] == '#':
            break
        if board[nr][nc] == 'O':
            cr1, cc1 = nr, nc
            escaped.append(m1)
            break
        cr1, cc1 = nr, nc

    cr2, cc2, m2 = movers[1]
    while True:
        nr, nc = cr2 + dr[d], cc2 + dc[d]
        if board[nr][nc] == '#':
            break
        if board[nr][nc] == 'O':
            cr2, cc2 = nr, nc
            escaped.append(m2)
            break
        if not escaped and nr == cr1 and nc == cc1:
            break
        cr2, cc2 = nr, nc

    positions = [(cr1, cc1, m1), (cr2, cc2, m2)]
    positions.sort(key=lambda x: x[-1])
    br, bc, _ = positions[0]
    rr, rc, _ = positions[1]
    return escaped, br, bc, rr, rc


def backtrack(br, bc, rr, rc, escaped=[], step=0):
    global answer
    if escaped:
        if len(escaped) == 1:
            if escaped[0] == 'R':
                if step < answer:
                    answer = step
        return

    if step >= answer:
        return

    if step == 10:
        return

    for d in range(4):
        next_escaped, nbr, nbc, nrr, nrc = tilt(br, bc, rr, rc, d)
        backtrack(nbr, nbc, nrr, nrc, next_escaped, step+1)


if __name__ == '__main__':
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    N, M = map(int, input().split())
    board = [list(input().strip()) for _ in range(N)]

    Br, Bc, Rr, Rc = 0, 0, 0, 0
    for r in range(N):
        for c in range(M):
            if board[r][c] == 'B':
                Br, Bc = r, c
                board[r][c] = '.'
            if board[r][c] == 'R':
                Rr, Rc = r, c
                board[r][c] = '.'

    answer = int(1e9)
    backtrack(Br, Bc, Rr, Rc)
    if answer == int(1e9):
        print(-1)
    else:
        print(answer)


""" 2개의 사탕 / 20260902 / 체감 난이도: G3
소요 시간 1시간 3분 / 시도 1회 / 실행 시간 3045ms (코드트리, 리팩토링 후 808ms) / 메모리 27MB (코드트리)

[구상]
    - 코드 트리에는 천재들만 있는것인가?
    - 요즘 새로운 루틴을 시도 중이기에 구상 시간은 10분으로 매우 짧게 가져갔다.
    - 구상만 하는 시간에는 문제를 2번 읽었다.
        - 1) 처음 읽을 때는 한줄 한줄 중요한 핵심 정보를 나만의 언어로 재해석하며 필기했다.
        - 2) 두번째 읽을 때는 내가 적은 내용과 문제를 대조하며 잘못 읽은 부분은 없는지 체크하였다.
    - 순수 구상만 10분 하고, TODO를 할용한 pseudo 코드 작성하는 시간을 가졌다. (구상과 구현 그 사이의 어딘가에 있음)
        - 완전 아이디어형 문제를 제외하면, 보통 이 문제는 이렇게 풀어야겠구나, 하고 큰 그림은 그려진다.
            - 이번 문제는 백트래킹으로 풀 수 있다는 생각을 했다.
                - 기울이는 방향에 따라 발생하는 분기점
                - 10 * 10으로 제한된 격자 넓이
                - 무려 10초(?)라는 처음보는 시간 제한..
        - 하지만 나는 천재가 아니기에.. 아무리 머릿속으로 그려봐야 구현 단계에서 항상 예상치 못한 것들이 튀어나온다.
        - 하지만 주석으로 pseudo 코드를 난잡하게 질러놓고, 하나씩 점검하면서 로직에 문제가 없는지 체크하다보면 하나씩 잡아지는 것을 경험했다.
            - 예를 들면 이번 문제에서 가장 까다로운 것은 파란 사탕의 존재였다.
            - 그런데 주석을 적다보니, 어쨌든 사탕이 탈출하는 순간을 잘 포착해서 종료처리만 해주면 된다는 것을 깨달았다.
            - 또한, 기울이는 방향에 따라서 어떤 사탕이 먼저 움직이는지 결정할 수 있다는 것도 깨달았다.
                - 세부적인 디테일로 들어가서 마커를 활용하여 두 사탕을 구별하기로 했다.
                - 좌,우로 기울이는데 두 사탕의 열이 같다면, 둘의 우선 순위가 상관없어진다는 것도 체크했다.

[구현]
    - 구현은 그냥 주석 써놓은거 보고 그대로 따라서 타자치는 시간이었다.
    - 단, 내가 써놓은 내용을 비판적으로 보면서 일부 수정한 내용도 있다.
        - 빨간색 사탕 탈출 시 종료 처리 조건 개선
        - navigate 함수에서 현재 사탕 탈출 여부 불리언 값으로 반환
        - 사탕 2개밖에 없으니까 for문 안돌리고, 하드코딩으로 개별 처리

[디버깅]
    - 오픈 테케를 처음부터 다 맞긴 했는데, 돌아가는 시간이 영 시원찮다는 느낌을 받았다.
    - 혹시 몰라서 10*10 케이스 만들어서 돌려보긴 했는데, 느낌이 좀 쎄했다.
    - 적어도 내 구현에서 불필요한 연산이나 비효율적인 메서드가 많다고 느끼진 않았다.
    - 시간초과 나면 눈치채지 못한 실수가 있거나, 그냥 방법론을 잘못 골랐다는 뜻으로 받아들이기로 하고 제출.

[후기]
    - 맞긴 맞았는데 영 개운하지가 않다. 이 근본 없는 3045ms는 도대체 뭐란 말인가...
    - 심지어 강사님 코드는 시간이 82ms인 것을 보고 엥? 엥? 엥? 만 반복했다.
    - 이를 통해 내가 도출한 경우의 수는 두 가지다.
        1) 백트래킹 같은 완전탐색 방법으로 풀라고 의도한 문제인데, 사람들이 빈틈을 잘 공략했다.
        2) 원래는 시간 제한이 빡빡해서 정석 풀이가 아니면 답도 없는데, 코드트리에서 나 같은 사회적 약자들을 배려하여 시간을 10초로 늘려줬다.
    - 진실은 무엇일까... 암튼 더 나은 답을 찾아봐야겠다.
        - (개선 후) 비효율적이지 않긴 개뿔... get_order, navigate 모두 과도한 메서드, 패키지 사용으로 너무 비쌌다.
        - 또한, 최소 조건을 구하는 경우 가지치기가 가능한데도 적용하지 않고 있었다.
        - 재밌는 사실: 가지치기 > 인지 >=인지 항상 생각하고 하자. 시간차이 꽤 난다. (약 500ms)
    - 결론: 시간 제한 1초도 충분히 많고, 걍 이 문제 틀린거나 다름 없음.
"""


# TODO 1: 백트래커 함수: 0~3 사이의 방향 벡터 인덱스로 길이 10의 중복있는 순열 생성.
def backtrack(rr, rc, br, bc, r_esp=False, b_esp=False, step=0):
    # TODO 1.0 가지치기
    global answer
    if step >= answer:
        return

    # TODO 1.1 파란 사탕이 먼저 탈출하거나 같이 탈출
    if b_esp:
        return

    # TODO 1.2 빨간 사탕만 탈출, 가능하면 정답 업데이트
    if r_esp:
        if step <= answer:
            answer = step
        return

    # TODO 1.3 종료 조건: step=10
    if step == 10:
        return

    # TODO 1.4 상하좌우 기울이고 재귀 호출
    for i in range(4):
        # TODO 1.4.1 빨간 사탕과 파란 사탕 이동 우선 순위 정하기
        cr1, cc1, m1, cr2, cc2, m2 = get_order(rr, rc, br, bc, i)

        # TODO 1.4.2 각 사탕을 우선 순위에 맞춰 이동시키고, 새로운 좌표와 탈출여부 파악하기
        nr1, nc1, escp1 = navigate(cr1, cc1, i, beware=[])
        nr2, nc2, escp2 = navigate(cr2, cc2, i, beware=[nr1, nc1])

        # TODO 1.4.3 재귀 호출
        if m1 == 'r':
            backtrack(nr1, nc1, nr2, nc2, escp1, escp2, step+1)
        else:
            backtrack(nr2, nc2, nr1, nc1, escp2, escp1, step+1)


# TODO 2: 기울일 방향 정해지면 먼저 움직이는 사탕 찾기: 메서드 사용 최소화
def get_order(rr, rc, br, bc, direction_id):
    # 북, 행 작을수록 높음
    if direction_id == 0 and rr <= br:
        r_first = True
    # 동, 열 클수록 높음
    elif direction_id == 1 and rc >= bc:
        r_first = True
    # 남, 행 클수록 높음
    elif direction_id == 2 and rr >= br:
        r_first = True
    # 서, 열 작을수록 높음
    elif direction_id == 3 and rc <= bc:
        r_first = True
    else:
        r_first = False

    if r_first:
        return rr, rc, 'r', br, bc, 'b'
    else:
        return br, bc, 'b', rr, rc, 'r`'


# TODO 3: One-way 이동 함수
def navigate(cr, cc, direction_id, beware: list):
    # 큐 쓰지 말라고 이놈아
    dr, dc = directions[direction_id]
    nr, nc = cr, cc

    while True:
        cr, cc = nr, nc
        nr, nc = nr + dr, nc + dc
        # 장애물 만나면 중지, 현재 좌표 반환
        if arr[nr][nc] == 1:
            return cr, cc, False
        # 탈출구 만나면 중지, 탈출 성공 표시
        # 좌표는 아무거나 줘도 상관 없음.
        if arr[nr][nc] == 2:
            return 0, 0, True
        # 다른 사탕이 먼저 움직였고, 해당 위치에 사탕이 존재하면 중지.
        if beware and nr == beware[0] and nc == beware[1]:
            return cr, cc, False


if __name__ == '__main__':
    answer = int(1e9)
    R, C = map(int, input().split())
    arr = [[1] * C for _ in range(R)]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # 파란 사탕, 빨간 사탕 위치만 따로 저장
    blue_loc = None
    red_loc = None

    # 0: 빈칸, 1: 장애물, 2: 탈출구, 사탕 위치는 0으로 치환
    for r in range(R):
        line = input().strip()
        for c in range(C):
            if line[c] == '.':
                arr[r][c] = 0
            elif line[c] == '#':
                continue
            elif line[c] == 'B':
                arr[r][c] = 0
                blue_loc = [r, c]
            elif line[c] == 'R':
                arr[r][c] = 0
                red_loc = [r, c]
            else:
                arr[r][c] = 2

    # 백트래킹 호출.
    backtrack(red_loc[0], red_loc[1], blue_loc[0], blue_loc[1])

    # 정답 출력
    if answer <= 10:
        print(answer)
    else:
        print(-1)
