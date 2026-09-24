""" 이상한 윷놀이 / 20260924 / 체감 난이도: G5
소요 1시간 9분 / 시도 3회 / 실행 시간 74ms (코드트리) / 메모리 17MB (코드트리)

진짜 왜 이럼? 틀린 이유 분석해봤다.
1) 조건문 복잡하게 짜기 너무 싫어서 그냥 패딩 붙였는데, 거기다가 한 라운드에 K번 도는걸
    FOR문 쓰기 싫어서 그냥 모듈로로 돌렸다. 그 결과 스텝과 시간을 따로 관리해줘야 했는데
    딱 맞아 떨어질 때는 몫을 가져가고, 초과하면 몫+1을 가져가야 하는데 누락했다.
2) 위에거 고치느라 정신 팔려서 또 종료 조건 까먹었다.
사실 슬슬 지쳐서 루틴 느슨하게 따랐는데 바로 틀렸다.
"""
if __name__ == '__main__':
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    adapter = [0, 1, 3, 0, 2]

    N, K = map(int, input().split())
    board = [[[] for _ in range(N+2)] for _ in range(N+2)]

    color = [[2] * (N+2) for _ in range(N+2)]
    for r in range(1, N+1):
        line = list(map(int, input().split()))
        for c in range(1, N+1):
            color[r][c] = line[c-1]

    piece = dict()
    for i in range(K):
        r, c, d = map(int, input().split())
        board[r][c].append(i)
        piece[i] = [r, c, adapter[d]]

    time = 0
    step = 0
    answer = -1
    found = False

    while True and time < 1000:
        # TODO 종료 조건
        if found:
            if step > 0:
                answer = time+1
            else:
                answer = time
            break

        # TODO: 이동시킬 말의 번호 계산 (모듈로)
        cur_id = step % K

        # TODO: 이동시킬 말의 좌표와 이동 방향 조회
        cr, cc, cd = piece[cur_id]

        # TODO: 이동시킬 말이 나올 때까지 해당 위치 리스트에서 값 뽑기
        buffer = []
        while True:
            value = board[cr][cc].pop()
            buffer.append(value)
            if value == cur_id:
                break
        buffer.reverse()

        # TODO: 이동 연산
        nr = cr + dr[cd]
        nc = cc + dc[cd]
        fr, fc = nr, nc

        if color[nr][nc] == 2:
            cd = (cd + 2) % 4
            nr = cr + dr[cd]
            nc = cc + dc[cd]
            fr, fc = nr, nc

            if color[nr][nc] == 2:
                fr, fc = cr, cc

            elif color[nr][nc] == 1:
                buffer.reverse()

        elif color[nr][nc] == 1:
            buffer.reverse()

        # TODO 방향 업데이트
        piece[cur_id][2] = cd

        # TODO 위치 이동
        for i in buffer:
            piece[i][0] = fr
            piece[i][1] = fc
        board[fr][fc].extend(buffer)

        # TODO 종료 조건 업데이트
        if len(board[nr][nc]) >= 4:
            found = True

        # TODO 시간 증가
        step += 1
        if step == K:
            step = 0
            time += 1

    # 정답 출력
    print(answer)


"""이상한 윷놀이 / 20260901 / 체감 난이도: G5
소요 1시간 16분 / 시도 2회 / 실행 시간 77ms (코드트리) / 메모리 18MB (코드트리)

[구상]
    - 이번 문제는 어떤 자료구조를 사용할지에 대해서 꽤 많은 고민을 했다.
        - 결국 보드의 칸별 색깔 정보를 저장할 배열과, 말들의 상태를 저장할 3차원 배열을 따로 만들어서 쓰기로 했다.
            - 특히 3차원 배열은 각 리스트 하나 하나가 스택이라고 생각하고 풀이를 진행했다.
            - 먼저 놓인 말이 가장 아래에 있어야 하고, 특정 말을 찾기 위해 그 위의 말들을 전부 건드려야 하는 점이 문제 상황에 가장 알맞다고 생각했다.
        - 또한 말들의 수가 적고 순서대로 입력이 들어온다는 점에서 착안하여 딕셔너리로 위치, 방향 정보를 저장하기로 했다.
            - 이렇게 하면 말들에 대한 정보 조회와 업데이트가 굉장히 단순해진다는 장점이 있다.
            - 단, 배열 상에서 위치를 바꿀 때 까먹지 말고 꼭 딕셔너리도 같이 업데이트 해줘야 한다.
    - 분기 처리가 좀 귀찮아서 그렇지, 문제 자체가 어렵고 아이디어가 필요한 타입은 아니었다.

[구현]
    - 분기 처리 많은 문제 특) 구상 잘해서 들어가도 구현에서 실수하기 딱 좋음
    - 마지막 문제인지라 슬슬 체력이 떨어져서 디버깅할 체력이 없었다. 그래서 오랜만에 비장의 한 수를 꺼내봤는데...
    - 절대 오류가 발생하지 않게 구현해야 하는데 그럴 힘은 없을 때 항상 든든한 TODO를 활용하기로 했다.
    - 일단 처음은 그냥 정리한 내용 앞에 두고 생각나는대로 move 함수의 실행 과정을 그려나갔다.
        - 한번, 두번에 걸쳐 항목들을 지우고 추가하기를 반복하다 보니까 자연스럽게 조심해야 할 부분들이 눈에 들어왔다.
    - 적어놓은 실행 과정을 마지막으로 한번 검토하고 순서대로 구현하면서 내가 초기에 생각한 내용과 실제 구현에 따라 달라지는 부분이 눈에 잘 들어와서 편했다.
        - 예를 들면 처음에는 모든 말에 대하여 r행 c열에서 해당 말의 높이도 기록하고 있었는데, 그냥 순서만 맞춰서 잘 쌓고 높이 체크만하면 된다는 것을 깨달았다.

[디버깅]
    - 계획표 상세하게 짜두면 뭐하나~ 문제를 똑바로 안읽는데~
    - 1000번 이상 진행하면 -1 출력해야 하는데 빼먹었다.. 반성합니다..

[후기]
    - 항상 마지막 문제에서 체력 관리의 중요성을 느낀다.
    - 앞으로도 TODO 계속 써볼까? 뭔가 마음에 들었다.
"""


def move(n):
    # TODO 1: n번째 말의 위치와 방향 벡터를 딕셔너리에서 불러오기: cr, cc, dr, dc
    cr, cc, dr, dc = table[n]

    # TODO 2: stack[cr][cc]에서 n이 나올 때까지 팝, 전부 임시 리스트에 스택 후 순서 반전.
    lst = []
    while True:
        num = stack[cr][cc].pop()
        lst.append(num)
        if num == n:
            break
    lst.reverse()

    # TODO 3: W, R, B에 맞춰서 이동할 위치 찾기: fr, fc
    fr, fc = 0, 0
    # TODO 3.1 n번말의 현재 위치, 방향에 따라 다음 칸 위치 뽑기: nr, nc
    nr, nc = cr + dr, cc + dc

    # TODO 3.2 범위 아웃 or board[nr][nc] == 2, BLUE
    if not(0 <= nr < N and 0 <= nc < N) or board[nr][nc] == 2:
        # TODO 3.2.1 n번째 말 방향 전환하여 딕셔너리 업데이트 (가장 아랫말만 반전)
        dr, dc = -dr, -dc
        table[n][2] = dr
        table[n][3] = dc
        # TODO 3.2.2 반대칸 무슨 색인지 확인
        nr, nc = cr + dr, cc + dc
        # TODO 3.2.3 색 파란색이거나 범위 아웃이면 cr, cc 반환
        if not(0 <= nr < N and 0 <= nc < N) or board[nr][nc] == 2:
            fr, fc = cr, cc
        # TODO 3.2.4 색 파란색 아니면 nr, nc 반대편 좌표로 대체 후 3.1.2, 3.1.3 동일하게 진행
        elif board[nr][nc] == 0:
            fr, fc = nr, nc
        else:
            lst.reverse()
            fr, fc = nr, nc

    # TODO 3.3 board[nr][nc] == 0, WHITE
    elif board[nr][nc] == 0:
        # TODO 3.3.1 바로 nr, nc 최종 위치로 반환
        fr, fc = nr, nc

    # TODO 3.4 board[nr][nc] == 1, RED
    else:
        # TODO 3.4.1 바로 nr, nc 최종 위치로 반환, 임시 리스트 순서 반전.
        lst.reverse()
        fr, fc = nr, nc

    # TODO 4: 임시 리스트 순회하며, 최종적으로 위치 업데이트하기
    for i in lst:
        table[i][0] = fr
        table[i][1] = fc
        # TODO 4.1 스택에 값 쌓기
        stack[fr][fc].append(i)

    # TODO 5: 이번 턴에 쌓은 말의 높이가 4이상이라면 게임을 종료 신호를 보낸다.
    global finished
    if len(stack[fr][fc]) >= 4:
        finished = True


if __name__ == '__main__':
    finished = False
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    N, K = map(int, input().split())

    # 칸의 색깔 정보를 저장할 배열, 0, 1 or 2
    board = [list(map(int, input().split())) for _ in range(N)]
    # N*N 스택 묶음. 그냥 리스트인데 스택 같이 쓰겠다는 뜻.
    stack = [[[] for _ in range(N)] for _ in range(N)]
    # 각 말의 번호를 인덱스로 하여 위치, 방향을 저장하고 업데이트할 딕셔너리
    table = dict()

    # 1번부터 K번 말 정보 받아오기
    for i in range(1, K+1):
        # 입력 좌표는 시작값이 1인 것을 명심하자.
        x, y, d = map(int, input().split())
        # 방향 번호도 1빼서 사용하자.
        dr, dc = directions[d-1]
        # 주어진 행과 열에 위치한 스택에 말 번호를 삽입하자.
        stack[x-1][y-1].append(i)
        # i번째 말에 대한 추가적인 정보도 딕셔너리에 업데이트.
        table[i] = [x-1, y-1, dr, dc]

    # 최대 1000 라운드 동안 시뮬레이션 진행.
    stage = 0
    while not finished:
        stage += 1
        if stage > 1000:
            break
        for i in range(1, K+1):
            move(i)

    # 정답 출력
    if not finished:
        print(-1)
    else:
        print(stage)
