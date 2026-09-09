""" 냉방 시스템 / 20260909 / 체감 난이도: G2
소요 시간 1시간 53분 / 시도 1 / 실행 시간 511ms (코드트리) / 메모리 25MB (코드트리)

[구상]
    - 문제가 정말 불친절하다.
        - 인접 정보, 에어컨 방향, BFS 방향 등 방향 정보가 들어가는 연산이나 자료가 많은데, 값이 하나도 통일되어 있지 않다.
        - 좌표 값이 행,열 기준이라면서 전부 1부터 시작한다. 근데 직접적으로 언급은 하지 않고, 예제 뜯어봐야 알 수 있다.
        - 그나마 에어컨 바로 앞 격자가 범위 내에 있고, 벽이 없음이 항상 보장된다는 조건이라도 있어서 다행이었다.
    - 벽을 신경쓰면서 에어컨 바람의 확산을 관리하는 부분이 가장 어려웠다.
        - 강한 제약이 존재하는 BFS 문제라고 생각했다.
        - 벽 체크는 인접 배열 스타일을 살려서 진행하기로 했다.
            - 3차원 배열을 초기화하고, R행 C열에서 갈 수 없는 방향 인덱스 값을 해당 위치에 삽입하는 방식으로 계획을 잡았다.
            - 이때, 벽의 반대편에서도 현재 위치로 올 수 없다는 것을 명시해야 함을 생각했다.
        - 결론적으로 현재 위치 기준으로 대각선상 2칸, 직선상 1칸을 갈 수 있는지 체크하고, 가능하면 큐에 삽입하는 방식이다.
        - 최대 범위가 5이기 때문에, 에어컨 바로 앞 칸의 방문 배열 값을 5로 초기화하고, 방문값이 1인 좌표가 나올 때까지 BFS를 돌리기로 했다.
        - 사실 대각선 체크를 할 때 중복 연산이 꽤나 발생하기 때문에 살짝 걱정되었지만, 더 나은 선택지가 떠오르지 않아 강행하기로 했다.
    - 사무실이나 에어컨 위치를 계속 찾기 싫어서 별도로 셋으로 정리해두기로 했고, 쓸데없는 정보는 그냥 버리고 갔다.

[구현]
    - 입력값 부터 처리하면서, 내가 정한 방향 인덱스 기준으로 모든 것이 통일되도록 신경 썼다.
    - 인접(아님) 3차원 배열을 초기화하고, 의도대로 생성되는지 검증했다.
    - 가장 부담스러운 구현부터 해결하고 싶어서 현재 좌표와 바라보는 방향 기준 다음 칸 후보를 반환하는 함수를 작성했다.
        - 그림 그려놓은거 보면서 거진 하드코딩으로 했는데.. 방향 돌려가면서 상대적으로 위치 찾고, 벽 조건 체크하도록 했다.
        - 처음에 맞게 구현해놓고, 예제 돌려보면서 잘못 만들었다고 착각해서 시간 좀 뺏겼다. (지능 이슈)
        - 이 함수랑 인접(아님) 배열 덕분에 나머지 구현 과정이 너무 안락했다.
    - 이번 문제에는 변화량 '동시 적용' 파트도 있었는데, 새로운 시도를 해봤다.
        - 기존에는 BFS 돌리고, 중복연산된 변화량에 2를 나눠주고 썼다.
        - 이번에는 그냥 간단하게 2중 루프를 돌면서 현재 위치 기준 아래 칸, 오른쪽 칸만 보며 변화량을 계산하게 했다.
        - 첫 시도라서 살짝 고생했지만, 만들어놓고 보니 훨씬 효율적이고 간단한 것 같아서 만족스럽다.
        - 인접(아님) 배열 덕분에 벽 처리도 굉장히 단순하게 구현 가능했다.

[디버깅]
    - 딱 하나 실수한 부분이 있는데, 변화량 동시 적용 파트에서 현재 값이 0이면 무시하게 한 것이었다.
        - 이게 BFS 돌릴때는 중복연산이 있으니까 이렇게 처리하는게 맞다.
        - 근데 2중 루프는 딱 한번씩만 보기 때문에, 현재 값이 0이어도 비교 값과의 차이가 4보다 큰 경우를 생각해서 스킵하면 안된다.
    - 코드를 수정하고 나서, 테케 중간 결과물을 단계별로 찍어보면서 지문과 대조했다.
    - 특별한 엣지는 없을 것으로 판단되어 제출하기로 했다.

[후기]
    - 인접(아님) 배열 좋은데? 역발상 좋았다.
    - 하던대로 하니까 참으로 편안하고 좋았다. 클래스 나가라잇!
"""
from collections import deque


def get_next(cr, cc, cd):
    # BFS 돌릴 때 이동 가능한 위치 뽑는 함수
    result = []
    # 직진 방향 좌표
    mid = (cr + dr[cd], cc + dc[cd])
    # (상대) 상단 대각선 좌표
    top = (mid[0] + dr[(cd-1) % 4], mid[1] + dc[(cd-1) % 4])
    # (상대) 하단 대각선 좌표
    bot = (mid[0] + dr[(cd+1) % 4], mid[1] + dc[(cd+1) % 4])
    # 직진 방향 범위 내, 벽으로 막혀있지 않으면 추가
    if 0 <= mid[0] < N and 0 <= mid[1] < N:
        if cd not in not_adj[cr][cc]:
            result.append(mid)
    # 상단 대각 방향 범위 내, 벽으로 막혀있지 않으면 추가
    if 0 <= top[0] < N and 0 <= top[1] < N:
        if (cd-1) % 4 not in not_adj[cr][cc] and (cd+2) % 4 not in not_adj[top[0]][top[1]]:
            result.append(top)
    # 하단 대각 방향 범위 내, 벽으로 막혀있지 않으면 추가
    if 0 <= bot[0] < N and 0 <= bot[1] < N:
        if (cd+1) % 4 not in not_adj[cr][cc] and (cd+2) % 4 not in not_adj[bot[0]][bot[1]]:
            result.append(bot)
    return result


def operate(r, c, d):
    # 에어컨 바로 앞 칸 좌표 찾기 (조건 보장)
    r += dr[d]
    c += dc[d]
    # 큐에 추가
    que = deque()
    que.append((r, c))
    # 방문 배열에서 5 지정, 시원함 배열에 5 더하기
    vst = [[0] * N for _ in range(N)]
    vst[r][c] = 5
    cool[r][c] += 5

    while que:
        cr, cc = que.popleft()
        # 현재 칸 시원함 변화량이 1이라면, 그 다음은 볼 필요 없다.
        if vst[cr][cc] == 1:
            break
        for nr, nc in get_next(cr, cc, d):
            if vst[nr][nc] == 0:
                que.append((nr, nc))
                # 방문 배열 1씩 차감
                vst[nr][nc] = vst[cr][cc]-1
                # 시원함 배열에 현재 시원함 추가
                cool[nr][nc] += vst[nr][nc]


def normalize():
    # 변화량 저장할 배열
    delta = [[0] * N for _ in range(N)]
    for cr in range(N):
        for cc in range(N):
            # 아래 칸, 오른쪽 칸 막혀있는 경우 무시
            for cd in [2, 3]:
                if cd in not_adj[cr][cc]:
                    continue
                nr, nc = cr+dr[cd], cc+dc[cd]
                # 변화량 계산해서 작은 것엔 더하고, 큰 것으로부터는 빼기
                if 0 <= nr < N and 0 <= nc < N:
                    diff = abs(cool[cr][cc]-cool[nr][nc]) // 4
                    if cool[cr][cc] >= cool[nr][nc]:
                        delta[cr][cc] -= diff
                        delta[nr][nc] += diff
                    else:
                        delta[cr][cc] += diff
                        delta[nr][nc] -= diff
    # 변화량 동시 적용
    for cr in range(N):
        for cc in range(N):
            cool[cr][cc] += delta[cr][cc]


def decrease_edges():
    # 가장자리 시원함 1씩 차감
    for cr in range(N):
        for cc in [0, N-1]:
            cool[cr][cc] = max(0, cool[cr][cc]-1)
    for cc in range(1, N-1):
        for cr in [0, N-1]:
            cool[cr][cc] = max(0, cool[cr][cc]-1)


if __name__ == '__main__':
    # 두고 두고 우려먹을 방향 벡터
    dr = [0, -1, 0, 1]
    dc = [-1, 0, 1, 0]

    N, M, K = map(int, input().split())
    # 시원함 배열, 전부 0에서 출발
    cool = [[0] * N for _ in range(N)]
    # 에어컨 위치와 사무실 위치 저장할 셋
    sources = set()
    offices = set()

    # 입력 배열 순회하며 사무실, 에어컨 위치 등록, 나머지 무시
    for r in range(N):
        line = list(map(int, input().split()))
        for c in range(N):
            if line[c] == 1:
                offices.add((r, c))
            elif line[c] > 1:
                sources.add((r, c, line[c]-2))
            else:
                continue

    # 인접(아님) 배열 초기화 후 관계 저장하기
    not_adj = [[[] for _ in range(N)] for _ in range(N)]
    for _ in range(M):
        x, y, s = map(int, input().split())
        # 내 기준에 맞춰 좌표, 방향 잘 체크해주기
        r1, c1, d1 = x-1, y-1, 1-s
        not_adj[r1][c1].append(d1)
        r2 = r1+dr[d1]
        c2 = c1+dc[d1]
        d2 = (d1+2) % 4
        not_adj[r2][c2].append(d2)

    time = 0
    is_cool = False
    while time < 100 and not is_cool:

        # TODO 0: 사무실 위치 순회하며 시원함 체크, 가능하면 조기 종료
        cool_count = 0
        for r, c in offices:
            if cool[r][c] < K:
                break
            cool_count += 1
        if cool_count == len(offices):
            is_cool = True
            break

        # TODO 1: 각 에어컨 별로 바람 출력해서 시원함 전파하기
        for r, c, d in sources:
            operate(r, c, d)

        # TODO 2: 시원함 높은 곳에서 낮은곳으로 흘려주기
        normalize()

        # TODO 3: 외벽에 인접한 칸들 시원함 1 감소
        decrease_edges()

        # TODO 4:시간 증가
        time += 1

    if is_cool:
        print(time)
    else:
        print(-1)
