"""술래잡기 체스 / 20260901 / 체감 난이도: G3
소요 시간  / 시도 2회 / 실행 시간 55ms (코드트리) / 메모리 16MB (코드트리)

[구상]
    - 23분 정도 소요했다. 보자마자 백트래킹 문제라고 생각했다.
    - 상상 이상으로 까다로운 문제. 도둑말 조건을 실수 없이 구현하는게 상당히 어렵다.
    - 가장 까다롭게 느껴진 조건은, 도둑말이 번호가 작은 순서대로 이동을 해야한다는 점이었다.
        - 살아있는 말 중에서 번호가 작은 순으로 찾아서 이동시켜야 하기 때문에, 무식한 순회는 힘들다.
        - 이를 해결하기 위해 체스 보드, 체스 말 인덱스에 대한 방향, 위치 값을 따로 저장한 리스트 2개를 대안으로 들고나왔다.
        - 물론 백트래킹 함수에 복잡한 인자를 많이 넣는것도, 말을 하나 죽일때마다 배열 카피를 만드는 것도 부담이 크다.
        - 하지만 문제 특성상 카피를 만들지 않으면 원복이 거의 불가능하기 때문에... 별 다른 선택지가 없었다.
            - 이런 이유로 인해서 배열 크기도 4*4로 제한이 걸려있었다고 생각한다.
    - 술래말이 죽일 수 있는 타겟 후보군을 구하거나, 타겟을 죽이는 파트는 딱히 걱정이 없었다.

[구현]
    - 자료형 초기화, 입력값 분배, 술래말 초기값 설정 등은 무난하게 계획한대로 구현했다.
    - 이번 문제에서 구현이 오래 걸린 이유는 pseudo code를 짜고 들어가지 않은 점이 크게 작용한 것 같다.
        - 이 문제의 핵심 파트라고 할 수 있는 도둑말 이동 파트를 큰 골자만 잡고 세부적인 디테일을 충분히 생각하지 못했다.
        - 또한, 내 풀이는 3개의 자료형을 왔다 갔다 하면서 변경점을 업데이트 해주기 때문에, 헷갈리기 쉬웠다고 생각한다.
        - 마지막으로, 45도 반시계 회전인건 알았는데, 구현상으로는 90도 회전을 하는 방식으로 구현해버렸다.
            - 여기서 오류 2개가 발생해서 오답의 원흉을 제공했다.
            - 특히 2번 오류는 4번 넘게 회전하는 도둑말이 나와야만 보이는데, 오픈 테케에는 없는 케이스였다.
        - 그 뒤에 따라오는 술래말 관련 함수들은 그냥 평소 하던대로 잘 구현했다.
            - 일단 배열 복사를 무작정 남발하지 않고 딱 필요할 때만 해주는 것도 중요하다고 생각한다.
            - 이번 문제에서는 결국 어떤 도둑말을 죽이느냐에 따라 분기점이 발생하기 때문에, 이때만 복사를 만들었다.
        - 이러나 저러나 함수화를 잘해둔 덕분에 백트래킹 파트도 직관적으로 쉽게 작성했다.

[디버깅]
    - 1차 디버깅: 오픈 테케가 틀렸는데, 알고보니 시작할때 0,0 위치 점수를 추가해주지 않았다.
    - 2차 디버깅: 히든 테케가 틀려서 찾아보니 90도 회전을 하고 있었다.
        - 45도 회전으로 바꾸고 나서도 한동안 고군분투 했는데, 알고보니 회전 제한을 최대 4로 남겨둔 상태였던것...
        - 고치고 제출해서 정답처리를 받았다.
    - 백트래킹은 디버깅이 너무 어렵다...

[후기]
    - 문제 조건에서 실수하면 인생이 배로 힘들어진다. 집중하자.
    - 이렇게 길게 푸는 문제 아닌것 같기도 하고...
"""


def move_thieves(nb, nd, nl):
    # 1번부터 16번 도둑말까지 전부 움직인다.
    for i in range(1, 17):
        # 말이 죽어서 없으면 패스
        if not nl[i]:
            continue
        # 방향 회전 카운트
        cnt = 0
        # 현재 위치
        cr, cc = nl[i]

        # 총 8방향을 시도할 수 있다.
        for j in range(0, 8):
            # 한바퀴 돌아도 갈 곳 없었으면 패스
            if cnt == 8:
                break
            # 방향 재조정 및 한칸 앞 탐색
            cnt += 1
            mv_id = (nd[i]+j) % 8
            dr, dc = moves[mv_id]
            nr, nc = cr+dr, cc+dc
            # 범위 밖이면 패스
            if not(0 <= nr < 4 and 0 <= nc < 4):
                continue
            # 술래말 있으면 패스
            if nb[nr][nc] < 0:
                continue
            # 빈칸이면 이동
            if nb[nr][nc] == 0:
                nl[i] = (nr, nc)
                nd[i] = mv_id
                nb[cr][cc] = 0
                nb[nr][nc] = i
                break
            # 다른 도둑말이면 위치 교환
            other = nb[nr][nc]
            nl[other] = (cr, cc)
            nb[cr][cc] = other
            nl[i] = (nr, nc)
            nd[i] = mv_id
            nb[nr][nc] = i
            break
    return nb, nd, nl


def find_targets(nb, nd, nl):
    # 현재 술래말의 위치에서 타격 가능한 도둑말의 번호를 모두 출력
    targets = []
    cr, cc = nl[0]
    dr, dc = moves[nd[0]]
    for i in range(1, 4):
        nr = cr + dr * i
        nc = cc + dc * i
        if not(0 <= nr < 4 and 0 <= nc < 4):
            break
        if nb[nr][nc] <= 0:
            continue
        targets.append(nb[nr][nc])
    return targets


def kill_thief(i, B, D, L):
    # 배열 복사
    nb = [row.copy() for row in B]
    nd = D.copy()
    nl = L.copy()

    # 현황판 업데이트
    sr, sc = nl[0]
    nb[sr][sc] = 0
    tr, tc = nl[i]
    nb[tr][tc] = -1

    # 체스말 방향 업데이트
    nd[0] = nd[i]
    nd[i] = -1

    # 체스말 위치 업데이트
    nl[0] = nl[i]
    nl[i] = ()
    return nb, nd, nl


def backtrack(B, D, L, score):
    # 도둑말 움직이기
    B, D, L = move_thieves(B, D, L)

    # 후보군 뽑기
    targets = find_targets(B, D, L)

    # 후보 없으면 종료
    if not targets:
        global max_score
        if score > max_score:
            max_score = score
        return

    # 죽이고 재귀 호출
    for i in targets:
        nB, nD, nL = kill_thief(i, B, D, L)
        backtrack(nB, nD, nL, score+i)


if __name__ == '__main__':
    # 8방향 벡터
    moves = [
        (-1, 0), (-1, -1), (0, -1), (1, -1),
        (1, 0), (1, 1), (0, 1), (-1, 1)
    ]
    # 보드 현황판
    board = [[0] * 4 for _ in range(4)]
    # 0번: 술래말, 1~16번: 도둑말 방향 리스트
    directions = [0] * 17
    # 0번: 술래말, 1~16번: 도둑말 위치 리스트
    locations = [() for _ in range(17)]
    # 출력으로 사용할 최대 점수
    max_score = board[0][0]

    # 입력 깔끔하게 정리하기
    for r in range(4):
        line = list(map(int, input().split()))
        for c in range(0, 8, 2):
            board[r][c//2] = line[c]
            directions[line[c]] = line[c+1]-1
            locations[line[c]] = (r, c//2)

    # 초기화: (0, 0)에 위치한 도둑말 사살
    init_score = board[0][0]
    directions[0] = directions[board[0][0]]
    directions[board[0][0]] = -1
    locations[0] = locations[board[0][0]]
    locations[board[0][0]] = ()
    board[0][0] = -1

    # 백트래킹 (시작 위치에서 얻는 점수로 시작)
    backtrack(board, directions, locations, score=init_score)
    print(max_score)
