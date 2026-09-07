""" 승자독식 모노폴리 / 20260903 / 체감 난이도: G4
소요 시간 1시간 43분 / 시도 1회 / 실행 시간 198ms (코드트리) / 메모리 22MB (코드트리)

[구상]
    - 자료구조로 시작해서 자료구조로 끝나는 문제. 이것만 잘 정하고 들어가면 80%는 해결된다.
    - 문제에서 제시한 조건들은 대부분 명료하고 복잡한 내용이 없었다.
        - 자연스럽게 드는 생각: 시간 초과 당하기 싫으면 효율적으로 풀이 진행해야겠지?
    - 딱 하나 의문점이 있었다면, "특정 플레이어가 제거되면 해당 플레이어의 독점 기록도 말소되는가?"였다.
        - 그림 예제를 살펴보니 2번이 죽었음에도 불구하고 시간이 만료되기 전까지 기록이 남아있는 것을 확인했다.
        - 다만, 2번이 죽는 단계에 대한 표현이 좀 애매했는데, 그냥 문장 그대로 따르기로 했다.
    - 문제를 이해하고 나서는 사용할 자료구조들을 논리정연하게 정리하는 시간을 꽤 오래 가졌다.
        - 이전 방향을 기준으로 하는 이동 방향 우선순위를 담을 딕셔너리
        - 방향 벡터를 보관할 리스트
        - 현재 독점 내역을 관리할 3차원 리스트
            - r행 c열에 현재 독점자 ID, 독점 기간을 저장
        - 각 플레이어의 위치와 현재 바라보고 있는 방향 ID를 담을 딕셔너리
        - 한번에 이동하고 난 뒤 중복 처리를 위한 카운터 딕셔너리 <- 얘가 진짜 효자임 ㅋㅋ
    - 입출력 조건도 확실하게 확인하고 들어갔다.
    - 마지막으로, 나무 박멸의 제초제 파트가 떠올랐다.
        - 물론 해당 문제는 대차게 말아먹어서 주말에 풀어야 하지만...
        - 제초제, 독점기간 같이 유통기한이 정해진 값들을 배열에 올려놓고 매 턴마다 배열 순회하면서 1씩 차감하는건 너무 비효율적이다.
        - 대신 라운드마다 시간을 증가시키고, 현재 시간과, 과거에 찍어둔 유통기한을 비교하면 동일한 작업을 쉽고 빠르게 처리할 수 있다.

[구현]
    - 일단 입력값을 받는 초기화 단계는 바로 구현으로 들어갔다.
        - 내가 구상한 자료구조를 초기화하고, 입력값을 올바르게 받는지 검증했다.
    - 다음은 실행부였는데, 단계가 많은 문제 특성상 while문 하나에 다 박는게 명료하고 편하다고 생각했다.
        - 주석 설계를 처음부터 끝까지 적으면서 여러번 검토했고, 별로 특색 있는 구현은 없었다.
        - 굳이 하나 뽑자면 중복 제거할 애들은 정보 딕셔너리 인덱스 기준으로 팝 해준 정도?
    - 주석 설계가 끝나고 천천히 코드를 top-down으로 작성했다.
        - 이때 살짝 실수해서 break문 빠뜨렸고, 나중에 오픈 테케 돌릴때 엥 왜 안되지.. 이러고 있었다.
        - 주석 설계 잘 해놓고 왜 니가 쓴걸 안읽냐고

[디버깅]
    - break문 빠진거 찾고 나서 처음부터 끝까지 꼼꼼히 읽어봤는데 별로 문제 없어 보여서 제출했다.

[후기]
    - 손설계 + 주석설계 방법이 슬슬 정착하고 있는것 같다.
    - 시뮬레이션 문제를 대할 때의 마음가짐에 대해 이런 저런 생각을 하게된다.
    - 예전에는 그냥 모든 순간 열심히 하면 저절로 되는거 아닌가? 하는 생각을 많이 했다.
        - 물론 열심히 해야 하는건 맞는데... 단계 별로 다른 형태의 노력을 해야한다는 생각이 든다.
        - 독해: 표독하고 깐깐해져야 한다. 출제자가 사기꾼이라고 생각하고 정신을 바짝 차려야 한다.
        - 손 설계: 쿨한(?) 자린고비가 되어야 한다. 줄건 주되, 너무 비효울적인 연산에 대해선 인색하게 굴어야 한다.
        - 주석 설계: 내가 나와 논리 배틀을 한다는 느낌으로 전투적으로, 치열하게 주고 받아야 한다.
        - 구현: 조급하지 않아야 한다. 다만, 너무 여유롭게 굴다가 이전 단계의 내가 치열하게 고민한 흔적을 놓쳐선 안된다.
    - 검증에 대한 자세는 좀 더 고민해봐야 한다.
"""

if __name__ == '__main__':
    N, M, K = map(int, input().split())
    info = dict()
    priority = dict()
    board = [[[0] * 2 for _ in range(N)] for _ in range(N)]
    directions = [(), (-1, 0), (1, 0), (0, -1), (0, 1)]

    # 보드 독점 현황 초기화
    for r in range(N):
        line = list(map(int, input().split()))
        for c in range(N):
            if line[c] > 0:
                board[r][c][0] = line[c]
                board[r][c][1] = K
                info[line[c]] = [r, c]

    # 플레이어 초기 방향 입력
    current_directions = list(map(int, input().split()))
    for p, d in enumerate(current_directions):
        info[p+1].append(d)

    # 플레이어 방향 우선 순위 입력
    for p in range(1, M+1):
        priority[p] = {}
        for d in range(1, 5):
            priority[p][d] = list(map(int, input().split()))

    time = 0
    counter = dict()
    finished = False

    while not finished and time < 1000:
        # TODO 0: 시간 증가
        time += 1

        # TODO 1: 카운터 비우기
        counter.clear()

        # TODO 2: info 순회하며 플레이어 별 cr, cc, cd 받아오기
        #   플레이어는 주어진 위치에서 네 방향을 총 두번씩 체크해야 한다.
        #   1) priority[플레이어 ID][cd] 에서 탐색 방향 우선 순위 받기
        #   2) 빈칸 이동 가능 여부 확인용 불리언 값
        #   2) 우선 순위 첫번째 순회
        #       nr, nc 계산, board[nr][nc][1]이 현재 시간보다 작은지 체크
        #       발견 시 break, nd = 현재 방향
        #   3) 우선 순위 두번째 순회
        #       이미 2번에서 갈 곳 찾았으면 해당 루프 스킵
        #       nr, nc 계산, board[nr][nc][0]이 나와 같은지 체크
        #       발견 시 break, nd = 현재 방향
        #   4) info[플레이어 ID] 값 nr, nc nd로 업데이트
        #   5) 카운터[(nr, nc)] 업데이트.
        for pid, (cr, cc, cd) in info.items():
            found = False
            fr, fc, fd = None, None, None

            for did in priority[pid][cd]:
                nr = cr + directions[did][0]
                nc = cc + directions[did][1]

                if not(0 <= nr < N and 0 <= nc < N):
                    continue

                if board[nr][nc][1] < time:
                    found = True
                    fr, fc, fd = nr, nc, did
                    break

            if not found:
                for did in priority[pid][cd]:
                    nr = cr + directions[did][0]
                    nc = cc + directions[did][1]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if board[nr][nc][0] == pid and board[nr][nc][1] >= time:
                        fr, fc, fd = nr, nc, did
                        break

            info[pid] = [fr, fc, fd]
            if (fr, fc) not in counter.keys():
                counter[(fr, fc)] = [1, [pid]]
            else:
                counter[(fr, fc)][0] += 1
                counter[(fr, fc)][1].append(pid)

        # TODO 3: 카운터 키, 밸류 순회하며 중복 칸 체크
        #   v[0] 값이 2보다 같거나 크면 별도 처리해야 함.
        #       v[1] 오름차순 정렬, [1:] 슬라이싱 하면 제거해야 할 애들만 볼 수 있음.
        #       제거해야 할 애들 순회하면서 info 딕셔너리 키 pop으로 제거
        #   이제 딱 하나 남은 키 플레이어 번호 기준으로 보드 독점 현황 업데이트
        for k, v in counter.items():
            players = sorted(v[1])

            if v[0] >= 2:
                for pid in players[1:]:
                    info.pop(pid)

            cr, cc, _ = info[players[0]]
            board[cr][cc][0] = players[0]
            board[cr][cc][1] = time + K

        # TODO 4: info에 키 값 1밖에 없으면 종료 선언
        if list(info.keys()) == [1]:
            finished = True
            break

    if finished:
        print(time)
    else:
        print(-1)
