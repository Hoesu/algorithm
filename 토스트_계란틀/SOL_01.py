""" 토스트_계란틀 / 20260820 / 체감 난이도: S1
소요 시간 51분 / 시도 1회 / 실행 시간 247ms (코드트리) / 메모리 25MB (코드트리)

[구상]
    - 시작부터 제발 나 좀 BFS로 풀어달라고 땡깡 부리는 듯한 문제였다. 그래도 12분은 생각하고 들어갔음.
    - 독특한 점이 있다면, 이전에 한번 방문했던 칸이라고 해서 다시 방문하지 않아도 괜찮다는 보장이 없다는 것이었다.
    ex) 1 17 | L = 5, R = 10이고 1에서 시작했다고 가정하면 격자 스캔 과정에서 17을 볼 수 있긴하다.
        6 11 | 다만 여기서 섵불리 방문 처리를 해버리면, 나중에 11에서 17로 갈 수 있음에도 불구하고 같은 그룹으로 묶어줄 수 없다.
    - 또한 해당 라운드에 BFS 호출 횟수가 존재하는 모든 칸의 개수와 동일하면 종료 조건이 된다는 것도 파악했다.
        - 시간 이슈가 있지 않을까 고민은 해봤는데, 그래봤자 바로 종료니까 괜찮을거라는 생각이 있었다. (비슷한 문제 경험)
    - 마지막으로 평균 값으로 대체할 때, 같은 그룹에 속한 값만 동일한 평균값으로 바꿔야 했다.
        - 이는 딕셔너리를 사용해서 BFS 호출 횟수를 키로, 해당 호출에서 계산한 평균 값을 밸류로 지정해 해결했다.

[구현]
    - 구현은 22분 정도 걸려서 해결했다.
    - 자신있게 푼 만큼 한방에 맞고 싶었는데, 어차피 리뷰도 적을거 한줄 한줄 주석을 달면서 내 코드를 다시 읽어봤다.
    - 이게 의외로 도움이 됐는데, 시작 위치 방문처리를 누락한 것을 덕분에 알아챌 수 있었다.

[디버깅]
    - 오픈 테케는 처음부터 다 맞았지만, 무빙워크에서 내상을 크게 입었기 때문에.. ㅋㅋ 나름 엣지 케이스를 만들어서 돌려봤다.
        - 알고보니 딕셔너리 키로 사용한 bfs_cnt 변수를 0부터 잡고 이걸로 방문배열을 채우고 있었기 때문에 무한루프가 걸리는 상황이 있었다.
        - 그래서 bfs_cnt를 먼저 증가시켜주고 bfs 함수를 호출하여 문제를 해결할 수 있었다.

[후기]
    - 한방에 맞아서 좋긴한데, 뭔가 이미 할 줄 아는걸 잘 한것 같아서 그리 뿌듯하진 않다. 무빙워크 맞추고 싶었는데..
"""


from collections import deque


def bfs(sr, sc):
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    # 계란 값 합계와 개수. 시작 위치 반드시 포함!
    combined_sum = eggs[sr][sc]
    combined_cnt = 1
    que = deque()
    que.append([sr, sc])

    while que:
        cr, cc = que.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            # 범위 벗어나면 무시
            if not (0 <= nr < N and 0 <= nc < N):
                continue
            # 이전 칸과 현재 칸 계란 차이 계산
            diff = abs(eggs[nr][nc] - eggs[cr][cc])
            # 하한, 상한 조건 만족하고 방문 안했으면 추가
            if L <= diff <= R and vst[nr][nc] == 0:
                combined_sum += eggs[nr][nc]
                combined_cnt += 1
                # 방문 배열에는 현재 이동에서 몇번째 BFS 호출인지 저장한다.
                vst[nr][nc] = bfs_cnt
                que.append([nr, nc])
    # 평균 구해서 BFS 호출 ID: 평균값으로 테이블 업데이트
    table[bfs_cnt] = combined_sum // combined_cnt


if __name__ == '__main__':
    # 격자 크기, 차이 하한, 상한
    N, L, R = map(int, input().split())
    # 계란판
    eggs = [list(map(int, input().split())) for _ in range(N)]

    # 계란 이동 횟수 초기화
    movements = 0
    while True:
        # 이번 이동에서 BFS 호출한 횟수
        bfs_cnt = 0
        # BFS 호출 ID별로 평균값 저장할 딕셔너리
        table = dict()
        # 매 이동마다 초기화되는 방문 배열
        vst = [[0] * N for _ in range(N)]

        # 전체 계란판을 순회하면서 방문하지 못한 곳마다 BFS를 호출한다.
        for sr in range(N):
            for sc in range(N):
                if vst[sr][sc] == 0:
                    # 호출 횟수 잊지 말고 증가시켜주기
                    bfs_cnt += 1
                    # 방문 배열 체크!
                    vst[sr][sc] = bfs_cnt
                    bfs(sr, sc)

        # 만약에 모든 칸이 서로 합쳐질 수 없다면, 각 칸마다 BFS가 호출된다.
        # 따라서 호출 횟수가 N 제곱일 때, 더 이상 이동이 불가능하다는 것을 알 수 있음.
        if bfs_cnt == pow(N, 2):
            break

        # 방문 배열은 각 칸 별로 몇번째 BFS 호출에 합쳐졌는지에 대한 정보를 저장하고 있다.
        for r in range(N):
            for c in range(N):
                # 테이블에 키로 넣을 BFS 호출 ID 찾기
                key = vst[r][c]
                # 해당 키에 대한 평균값으로 원본 배열 덮어쓰기
                eggs[r][c] = table[key]
        # 이동이 한번 완료될 때마다 값 1 증가
        movements += 1
    # 정답 출력
    print(movements)
