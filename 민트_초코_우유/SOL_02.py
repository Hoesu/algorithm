""" 민트 초코 우유 / 20261007 / 체감 난이도: G1
소요 시간 40분 / 시도 1회 / 실행 시간 484ms (코드트리) / 메모리 26MB (코드트리)

엥 셋으로 푸니까 더 쉽네? 역시 단순한게 최고야.
"""
from collections import deque


if __name__ == '__main__':
    DR = [-1, 1, 0, 0]
    DC = [0, 0, -1, 1]

    N, T = map(int, input().split())
    religion = [[set() for _ in range(N)] for _ in range(N)]
    for r in range(N):
        line = input().strip()
        for c in range(N):
            religion[r][c].add(line[c])
    faith = [list(map(int, input().split())) for _ in range(N)]
    defense = [[0] * N for _ in range(N)]

    time = 1
    for _ in range(T):
        # 아침
        for r in range(N):
            for c in range(N):
                faith[r][c] += 1

        # 점심
        representative = []
        vst = [[0] * N for _ in range(N)]
        for sr in range(N):
            for sc in range(N):
                if vst[sr][sc] == 0:
                    que = deque()
                    que.append((sr, sc))
                    vst[sr][sc] = 1
                    candidates = [(len(religion[sr][sc]), faith[sr][sc], sr, sc)]

                    while que:
                        cr, cc = que.popleft()
                        for i in range(4):
                            nr, nc = cr+DR[i], cc+DC[i]
                            if not(0 <= nr < N and 0 <= nc < N):
                                continue
                            if vst[nr][nc] != 0:
                                continue
                            if religion[sr][sc] != religion[nr][nc]:
                                continue
                            que.append((nr, nc))
                            vst[nr][nc] = 1
                            candidates.append((len(religion[nr][nc]), faith[nr][nc], nr, nc))

                    candidates.sort(key=lambda x: (-x[1], x[2], x[3]))
                    cnt, _, nr, nc = candidates[0]
                    for _, _, cr, cc in candidates[1:]:
                        if faith[cr][cc] > 0:
                            faith[cr][cc] -= 1
                            faith[nr][nc] += 1
                    representative.append((cnt, faith[nr][nc], nr, nc))

        # 저녁
        representative.sort(key=lambda x: (x[0], -x[1], x[2], x[3]))
        for _, _, sr, sc in representative:
            if faith[sr][sc] <= 1:
                continue
            if defense[sr][sc] == time:
                continue

            fervor = faith[sr][sc]-1
            direction = faith[sr][sc] % 4
            faith[sr][sc] = 1
            cr, cc = sr, sc

            while True:
                nr = cr + DR[direction]
                nc = cc + DC[direction]

                if not (0 <= nr < N and 0 <= nc < N):
                    break
                if fervor == 0:
                    break
                if religion[nr][nc] == religion[sr][sc]:
                    cr, cc = nr, nc
                    continue

                if fervor > faith[nr][nc]:
                    defense[nr][nc] = time
                    religion[nr][nc] = religion[sr][sc].copy()
                    fervor -= (faith[nr][nc] + 1)
                    faith[nr][nc] += 1
                else:
                    defense[nr][nc] = time
                    religion[nr][nc] = religion[nr][nc].union(religion[sr][sc])
                    faith[nr][nc] += fervor
                    fervor = 0
                cr, cc = nr, nc

        # 정답 계산
        answer = [0] * 7
        for r in range(N):
            for c in range(N):
                if religion[r][c] == {'T'}:
                    answer[6] += faith[r][c]
                elif religion[r][c] == {'C'}:
                    answer[5] += faith[r][c]
                elif religion[r][c] == {'M'}:
                    answer[4] += faith[r][c]
                elif religion[r][c] == {'C', 'M'}:
                    answer[3] += faith[r][c]
                elif religion[r][c] == {'T', 'M'}:
                    answer[2] += faith[r][c]
                elif religion[r][c] == {'T', 'C'}:
                    answer[1] += faith[r][c]
                else:
                    answer[0] += faith[r][c]
        print(*answer)

        # 시간 증가
        time += 1


""" 민트 초코 우유 / 20260923 / 체감 난이도: G1
소요 시간 3시간 / 시도 1회 / 실행 시간 466ms (코드트리) / 메모리 26MB (코드트리)

[구상]
    - 최근 기출로 올수록 보이는 패턴: 살짝 생각해야 하는 이슈를 1~2개 던져주고, 그 주위를 둘러싸는 숙제 폭탄
    - 그룹 나누기, 우선 순위 정렬, 복잡한 조건 분기 등 이미 나름의 숙련도를 갖추고 있는 작업들이 주어졌다.
    - 이번 문제에서 특이한 점이 하나 있었는데, 바로 문자열을 조합해야 했다는 것이다.
        - 이 부분에서 정말 많은 고민을 했고, 결론적으로 데이터 분석 수업에서 배웠던 내용을 차용해 인코딩을 해보기로 했다.
        - 이 방식의 장점은 벡터를 더하는 작업으로 문자열 합집합 연산을 순서에 맞춰 진행할 수 있다는 것이라고 생각한다.
        - 솔직히 그냥 문자열 집합 만들고 리스트로 변환 후 정렬할까 생각해봤는데,
        - 집합 자료형이 생각보다 무겁고, 동일한 연산을 많이 반복해야하기 때문에 시간 초과가 우려되었다.
        - 그래서 모든 인코딩 정보와 복원 정보를 딕셔너리 키, 밸류에 담아서 빠르고 간편하게 정보를 불러오고자 했다.
        - 만약에 훨씬 많은 카테고리가 있었다면 이런 수작업은 불가능에 가까웠을 것으로, 뭔가 더 일반화된 접근법도 추후에 떠올려보도록 하자.
    - 동은 프로의 손설계 강의를 들으며, 색깔팬 사용을 제대로 해보기로 했고, 이번 문제에서 큰 도움이 되었다.
        - 오타나 구상 오류를 수정한 부분은 빨간색으로, 문제를 읽으면서 애매했던 부분은 파란색으로 박스를 쳤다.
        - 파란색 영역엔 의문점을 질문 형식으로 적어두고, 문제를 읽다가 해답이 나오면 YES/NO로 답변을 추가했다.
        - 문제에서 애매했던 부분은 다음과 같다:
            - 끝까지 하나의 종교만 고수하는 학생도 있나? => 의심의 여지 없이 YES
            - 현재 간절함 이상으로 깎이면 그냥 0처리 하는건가? => 부등식 조건 때문에 0은 될 수 있어도 음수는 될 수 없다. 고려 대상에서 제외.
            - 단 1명만 있어도 그룹으로 간주할 수 있는가? => 처음 생각은 아마도 YES, 추후에 디버깅하며 아니라는 것을 깨달음.
        - "학생들은 인접한 학생들과 신봉 음식이 완전히 같은 경우에만 그룹을 형성합니다."
            - 인접 학생 중 음식이 완전히 같은 경우가 하나도 없으면 그룹을 만들 수 없다는 말 아닌가?
            - 볼드체까지 해서 적어놓긴 했는데, 테케와 설명이 정확하게 동일하다는 생각은 들지 않는다.
            - 어쨌든 강사님께서 항상 테케를 따르라고 하셨으니, 확실하지 않다는 것만 생각하고, 나중에 테케에서 확인해보기로 했다.

[구현]
    - 루틴을 지켜서 실행부를 탑다운으로 작성했고, 이번 문제는 함수화가 과하면 별로일 것 같아서 굳이 하지 않았다.
    - 주석 설계가 끝나자마자 커스텀 프린트를 작성했고, 병적으로 돌리면서 코드 구현을 진행하였다.
        - 구상을 좀 오래하고 들어가서 그런지 구현은 막힘없이 진행할 수 있었다.
        - 다만, 튜플 간 합연산을 할때 실수로 상한을 1로 정해주지 않아서 수정해야 했다.
        - 또한, 방어 모드를 구현하는 것을 깜빡해서 나중에 추가해줬다.

[디버깅]
    - 오픈 테케와 커스텀 프린트를 가지고 열심히 돌려봤는데, 첫번째 라운드는 정답이 제대로 나오고, 두번째 라운드부터 틀렸다.
        - 별의 별걸 다 체크해보다가, 이래서는 답이 없겠다 싶어서 손 계산으로 라운드 2와 3을 미리 계산해봤다.
        - 그래서 출력 찍어가면서 디버깅을 진행해봤는데, 알고보니 단일 멤버 그룹도 가능했던것...
        - 그거 고치니까 바로 정답이 나왔고, 3번 라운드도 손계산과 결과가 동일했다.

[후기]
    - 아무래도 문자열 비교는 좀 부담스러워서, 정수 인코딩을 한번 거치고 이걸로 정수-튜플 인코딩을 해볼까 했다.
    - 마침 약속시간이었던 12시까지 시간이 좀 남아있어서 다른 버전을 만들어봤는데, 문자열 비교가 더 빨랐다. 왜???
"""
from collections import deque


def debug_array(msg):
    print(msg)
    print(f'종교')
    for x in religion:
        print(*x)
    print()
    print(f'신앙심')
    for x in faith:
        print(*x)
    print('------')


def debug_representatives(msg):
    print(msg)
    print(f'종교')
    for x in religion:
        print(*x)
    print()
    print(f'신앙심')
    for x in faith:
        print(*x)
    print()
    print(f'대표자')
    temp = [[0] * N for _ in range(N)]
    for l, f, r, c in representatives:
        print(f'{religion[r][c]} 신봉자, 신앙심: {f}, 중첩: {l}, 위치: {r + 1, c + 1}')
        temp[r][c] = 1
    for x in temp:
        print(*x)
    print('------')


if __name__ == '__main__':
    DEBUG_MODE = False

    # 상, 하, 좌, 우 (우선순위 방향 벡터)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    # 민/초/우 조합 문자열을 튜플로 변환하는 딕셔너리
    string_to_tuple = {
        'T': (1, 0, 0), 'C': (0, 1, 0), 'M': (0, 0, 1),
        'TC': (1, 1, 0), 'TM': (1, 0, 1), 'CM': (0, 1, 1),
        'TCM': (1, 1, 1)
    }
    # 튜플을 민/초/우 조합으로 복구하는 딕셔너리
    tuple_to_string = {
        (1, 0, 0): 'T', (0, 1, 0): 'C', (0, 0, 1): 'M',
        (1, 1, 0): 'TC', (1, 0, 1): 'TM', (0, 1, 1): 'CM',
        (1, 1, 1): 'TCM'
    }

    N, STEP = map(int, input().split())
    religion = [list(input().strip()) for _ in range(N)]
    faith = [list(map(int, input().split())) for _ in range(N)]
    defense = [[-1] * N for _ in range(N)]

    if DEBUG_MODE:
        debug_array('INITIAL STATE:')

    time = 0
    for _ in range(STEP):
        # TODO 아침: 신앙심 1 증가
        for r in range(N):
            for c in range(N):
                faith[r][c] += 1

        if DEBUG_MODE:
            debug_array('ALL FAITH INCREASED BY 1:')

        # TODO 점심: 그룹 형성 및 대표자 탐색
        #   1) 각 그룹 별 대표자 정보 저장할 리스트 선언
        #   2) N*N 방문 배열 전역적으로 활용하며 Breadth First Search
        #       2.1) 종교가 동일한 이웃이 존재하면 같은 그룹으로 간주 (단일 그룹 존재 가능함)
        #       2.2) 후보군 리스트에 신앙심, 행, 열 정보 삽입 후 (-, +, +) 정렬
        #       2.3) 후보군 리스트 1번 인덱스부터 순회하며 해당 위치 신앙심 -1
        #       2.4) 후보군 리스트 0번 인덱스 신앙심에 전부 더해주기
        #       2.5) 대표자 정보 반환
        #   3) 2)에서 구한 대표자 정보를 1)에서 초기화한 리스트에 삽입
        #       3.1) 리스트 앞에 문자열 길이 추가, 기본 재료 중첩 개수 확인 용도
        #   4) 대표자 정보 리스트 (+, -, +, +) 정렬
        representatives = []
        vst = [[0] * N for _ in range(N)]
        for sr in range(N):
            for sc in range(N):
                if vst[sr][sc] == 0:

                    que = deque()
                    que.append((sr, sc))
                    vst[sr][sc] = 1
                    value = religion[sr][sc]
                    candidates = [(faith[sr][sc], sr, sc)]

                    while que:
                        cr, cc = que.popleft()
                        for i in range(4):
                            nr, nc = cr + dr[i], cc + dc[i]

                            if not (0 <= nr < N and 0 <= nc < N):
                                continue
                            if vst[nr][nc] != 0:
                                continue
                            if religion[nr][nc] != value:
                                continue

                            vst[nr][nc] = 1
                            que.append((nr, nc))
                            candidates.append((faith[nr][nc], nr, nc))

                    if candidates:
                        candidates.sort(key=lambda x: [-x[0], x[1], x[2]])
                        _, best_r, best_c = candidates[0]

                        for _, cr, cc in candidates[1:]:
                            faith[cr][cc] -= 1
                            faith[best_r][best_c] += 1

                        representatives.append((len(value), faith[best_r][best_c], best_r, best_c))
        representatives.sort(key=lambda x: [x[0], -x[1], x[2], x[3]])

        if DEBUG_MODE:
            debug_representatives('CANDIDATES FOUND:')

        # TODO 저녁: 종교 전파
        #   Pseudo-code 활용
        for _, _, sr, sc in representatives:
            # 방어 모드에 돌입한 대표자는 이번 턴에 전파 불가능
            if defense[sr][sc] == time:
                continue

            # 대표자 신앙심(faith) = 1, 대표자 간절함(fervor) = 신앙심-1
            # 방향은 신앙심을 4로 나눈 나머지
            fervor = faith[sr][sc] - 1
            direction = faith[sr][sc] % 4
            faith[sr][sc] = 1

            cr = sr + dr[direction]
            cc = sc + dc[direction]

            while True:
                # 격자 탈출 시 종료
                if not (0 <= cr < N and 0 <= cc < N):
                    break
                # 간절함 전부 소모 시 종료
                if fervor == 0:
                    break
                # 종교 같으면 넘어가기
                if religion[cr][cc] == religion[sr][sc]:
                    cr += dr[direction]
                    cc += dc[direction]
                    continue
                else:
                    # 피전파자 방어모드 돌입
                    defense[cr][cc] = time
                    # 강한 전파
                    if fervor > faith[cr][cc]:
                        religion[cr][cc] = religion[sr][sc]
                        fervor -= (faith[cr][cc] + 1)
                        faith[cr][cc] += 1
                    # 약한 전파
                    else:
                        # 종교 문자열을 튜플로 인코딩
                        t1 = string_to_tuple[str(religion[sr][sc])]
                        t2 = string_to_tuple[str(religion[cr][cc])]
                        # 튜플 두개 합치면 (각 자릿값 최대 1) 기본 종교를 전부 합친 종교의 키를 얻을 수 있다.
                        key = tuple([min(1, t1[i] + t2[i]) for i in range(3)])
                        religion[cr][cc] = tuple_to_string[key]
                        faith[cr][cc] += fervor
                        fervor = 0

                cr += dr[direction]
                cc += dc[direction]

        if DEBUG_MODE:
            debug_array('AFTER RELIGION TRANSMISSION:')

        # TODO: 정답 출력
        counter = {'TCM': 0, 'TC': 0, 'TM': 0, 'CM': 0, 'M': 0, 'C': 0, 'T': 0}
        answer = []
        for cr in range(N):
            for cc in range(N):
                counter[religion[cr][cc]] += faith[cr][cc]
        for count in counter.values():
            answer.append(count)
        print(*answer)

        # TODO: 시간 증가
        time += 1
