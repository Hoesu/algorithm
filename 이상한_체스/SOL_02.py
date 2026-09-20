""" 이상한 체스 / 20260919 / 체감 난이도: G5
소요 시간 34분 / 시도 2회 / 실행 시간 136ms (코드트리) / 메모리 21MB (코드트리)

아 커피를 너무 많이 마셨는지 머리가 아프다.
이전에는 거의 하드코딩으로 해결했는데, 그냥 방향 인덱스 돌려가면서 더 간결하게 구현해봤다.
dr, dc 오타났는데 오픈 테게에서 다 맞게 나와서 한번 틀렸다.
"""


def get_area(lst):
    vst_copy = [x[:] for x in vst]
    for idx, delta in enumerate(lst):
        cr, cc = locations[idx]
        piece = board[cr][cc]

        for d in table[piece]:
            dr, dc = directions[(d+delta) % 4]
            nr, nc = cr+dr, cc+dc

            while True:
                if not(0 <= nr < N and 0 <= nc < M):
                    break
                if board[nr][nc] == 6:
                    vst_copy[nr][nc] = 1
                    break
                vst_copy[nr][nc] = 1
                nr, nc = nr+dr, nc+dc
    return N*M - sum(map(sum, vst_copy))


def backtrack(lst, step=0):
    global answer
    if step == len(locations):
        area = get_area(lst)
        if area < answer:
            answer = area
        return

    for i in range(4):
        backtrack(lst+[i], step+1)


if __name__ == '__main__':
    N, M = map(int, input().split())
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    board = [list(map(int, input().split())) for _ in range(N)]
    table = [[], [0], [1, 3], [0, 1], [0, 1, 3], [0, 1, 2, 3]]
    vst = [[0] * M for _ in range(N)]

    locations = []
    for r in range(N):
        for c in range(M):
            if 0 < board[r][c] < 6:
                locations.append([r, c])
                vst[r][c] = 1
            elif board[r][c] == 6:
                vst[r][c] = 1

    answer = int(1e9)
    backtrack([])
    print(answer)


"""이상한 체스 / 20260825 / 체감 난이도: G5
소요 시간 1시간 16분 / 시도 1회 / 실행 시간 109ms (코드트리) / 메모리 19MB (코드트리)

[구상]
    - 24분 구상 시간을 가졌고, 문제는 처음부터 끝까지 최소 3번은 읽은것 같다.
    - 일단 체스말 보자마자 클래스로 말 구현해서 자손으로 폰, 나이트, 퀸.. 어쩌고 저쩌고 생각이 들었으나, 결론은 사용하지 않는게 좋겠다는 생각을 했다.
        - 상태가 자주 변하는 것도 아니고, 그냥 방향만 지정해서 칸 색칠해야 하는 태스크였기에.. 봉인했습니다.
    - 최근 들어 손설계가 익숙해지기 시작했는데, 이번 문제에서 크게 도움이 되었다고 생각한다.
        - 난해한 내용 리라이팅, 사용할 자료형 미리 정리하기, 최소한의 함수 구현 목록 등을 만들고 들어가니 꽤 수월했다.
    - N, M 제한을 확인하고 백트래킹으로 풀 수 있겠다는 생각이 들었다.
        - 바라보는 방향을 선택지로 두고, 모든 체스말에 대해 중복이 있는 순열을 뽑아서 방향을 배정해주는 문제라고 생각했다.
        - 순열을 뽑는 것 자체는 괜찮은데, 제한 범위 내에서 칸 탐색 및 색칠이 조금 부담스럽긴 했다.
        - 또한 이동하지 못하는 칸은 나머지 칸을 전부 색칠하고 남는 칸이라, 가지치기 같은건 시도할 수 없었다.

[구현]
    - 최근 문제 푸는 꼬라지를 감안하여 굉장히 천천히, 그리고 최소한의 함수/메서드 사용으로 최대한 직관적으로 풀어나가려고 노력했다.
    - 백트래킹으로 수열 뽑을 때, 5번말(퀸)의 경우엔 어차피 4방향 전부 이동 가능해서 이것만 제외하고 순열 뽑을까 생각해봤지만..
        - 일단 풀어보고 나서 나중에 최적화하기로 해서 제거했다.
    - 체스말마다 기준 방향이 정해지면 채울 칸들을 임시 리스트에 넣었고, 해당 리스트를 다시 순회하면 방문 배열을 칠했다.
        - 매번 상대말 위치를 받아 배열을 초기화하기 싫어서 리스트 컴프리헨션으로 카피를 만들어서 썼다.
        - 물론 여러번 순회해야 해서 비효율적인 부분이 있지만, 디버깅이 쉬워서 일단 냅두고 문제가 되면 개선하기로 했다.
        - 저번처럼 방문 배열에 들어갈 값들을 잘 통제하여 같은 실수를 방지했다.
        - unpacking할 값들이 많아서 중간에 코드 구조를 개편하는 과정에서 시간을 많이 썼다.

[디버깅]
    - 오픈 테스트 케이스를 전부 맞고 나서, 작은 배열에 대한 테스트를 주로 진행했다.
        - 1*1 행렬일 때 체스말이 가득 채우고 있는 경우와 그냥 빈칸인 경우
        - 3*3 행렬에서 각 체스말을 1, 1에 두고 의도한 방향으로 뻗어나가는지 모두 체크

[후기]
    - 배열 순회하면서 값 가져올 때, *를 사용하여 unpacking, 모두 개별값으로 받았는데, 이거 생각보다 시간 많이 잡아먹는다.
    - 이미 내부 구조는 내가 알고 있으니, a, b, (c ,d) 이런식으로 맞춰서 받아오자.
"""


def simulate(face_lst):
    # 원상 복귀 어려우니까 카피를 만들자.
    # deepcopy 하자는 나쁜 생각은 절대 ㄴㄴ
    vst_copy = [row.copy() for row in vst]

    # 방문 배열 채우기 목록을 만들어둡시다.
    # 행, 열, 말 타입, 바라보는 방향을 입력으로 받아서
    # 행, 열, 움직일 방향을 계산 후 리스트에 저장.
    fill_lst = []
    for (r, c, tp), fc in zip(mine, face_lst):
        if tp == 1:
            # 폰: 현재 방향
            fill_lst.append((r, c, directions[fc]))
        elif tp == 2:
            # 나이트: 현재 방향 기준 좌, 우
            fill_lst.append((r, c, directions[(fc-1) % 4]))
            fill_lst.append((r, c, directions[(fc+1) % 4]))
        elif tp == 3:
            # 룩: 현재 방향, 우
            fill_lst.append((r, c, directions[fc]))
            fill_lst.append((r, c, directions[(fc+1) % 4]))
        elif tp == 4:
            # 킹: 반대 방향 제외 전부
            fill_lst.append((r, c, directions[fc]))
            fill_lst.append((r, c, directions[(fc-1) % 4]))
            fill_lst.append((r, c, directions[(fc+1) % 4]))
        else:
            # 퀸: 모든 방향
            fill_lst.append((r, c, directions[0]))
            fill_lst.append((r, c, directions[1]))
            fill_lst.append((r, c, directions[2]))
            fill_lst.append((r, c, directions[3]))

    for r, c, (dr, dc) in fill_lst:
        cr, cc = r, c
        # 범위 내에서만 채우기 진행
        while 0 <= cr < R and 0 <= cc < C:
            # 상대방의 말이 있는 위치에 도달하면 루프 탈출
            if vst_copy[cr][cc] == -1:
                break
            # 이미 칠했거나, 내 말이 있는 위치라면 계속 진행
            if vst_copy[cr][cc] == 1:
                cr += dr
                cc += dc
                continue
            # 처음 방문하는 위치는 칠해주고 진행
            else:
                vst_copy[cr][cc] = 1
                cr += dr
                cc += dc

    # 방문 배열에서 값이 0인 칸의 개수만 셉니다.
    empty_cnt = 0
    for row in vst_copy:
        empty_cnt += row.count(0)
    return empty_cnt


def backtrack(lst=[], step=0):
    # 최대한 칠하고 남은 영역의 최소값 업데이트
    # 사실상 영역을 다 칠해봐야 남은 영역을 알 수 있기 때문에
    # 가지치기는 불가능할 것이라고 판단함.
    global min_empty
    if step == len(mine):
        empty = simulate(lst)
        if empty < min_empty:
            min_empty = empty
        return
    # 0, 1, 2, 3으로만 이루어진 순열을 뽑아보아요.
    for i in range(4):
        backtrack(lst+[i], step+1)


if __name__ == '__main__':
    R, C = map(int, input().split())
    # 방문 배열 바깥에서 초기화하고, 말이 있는 위치 표기해줄것.
    vst = [[0] * C for _ in range(R)]
    # 0: 북, 1: 동, 2: 남, 3: 서
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # 내 말들의 행, 열, 타입을 저장할 리스트
    mine = []
    for r in range(R):
        line = list(map(int, input().split()))
        for c in range(C):
            # 1~5는 차례대로 폰, 나이트, 룩, 킹, 퀸
            if 1 <= line[c] <= 5:
                mine.append((r, c, line[c]))
                vst[r][c] = 1
            # 6은 상대말이다. 음수 처리.
            elif line[c] == 6:
                vst[r][c] = -1
            else:
                continue
    # 빈칸 개수가 가장 작은 경우의 값을 출력
    min_empty = R * C + 1
    backtrack()
    print(min_empty)
