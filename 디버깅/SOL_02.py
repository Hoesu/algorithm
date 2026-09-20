""" 디버깅 / 20260920 / 체감 난이도: G4
소요 시간 35분 / 시도 1회 / 실행 시간 322ms / 메모리 21MB (코드트리)

다시는 보기 싫은 문제였는데, 이럴수록 풀어야 한다는 마음으로 임했다.
역시 사다리 타기 파트는 배열로 접근하는게 직관적이고 쉬워서 그런지 이전 구현과 동일한 모습을 볼 수 있다.
그리고 시간초과 나면서 조합으로 안하면 무조건 터지는지 알았는데, 그냥 조기종료 조건 설정 잘 하니까 부분집합으로 접근해도 충분히 잘 된다.
아 이제 백트래킹 그만하고 싶은데~ 매번 너무 쫄린다.
"""


def simulate(arr):
    for start in range(1, N+1):
        goal = start
        for j in range(K):
            if arr[j][goal] == 1:
                goal += 1
            elif arr[j][goal-1] == 1:
                goal -= 1
            else:
                continue
        if start != goal:
            return False
    return True


def backtrack(arr, step=0):
    global answer
    if step > answer or step > 3:
        return

    if simulate(arr):
        if step < answer:
            answer = step

    for i in range(len(candidates)):
        cr, cc = candidates[i]
        if vst[i] != 1:
            vst[i] = 1
            arr[cr][cc] = 1
            backtrack(arr, step+1)
            vst[i] = 0
            arr[cr][cc] = 0


if __name__ == '__main__':
    N, M, K = map(int, input().split())
    grid = [[0] * (N+1) for _ in range(K)]

    for _ in range(M):
        a, b = map(int, input().split())
        grid[a-1][b] = 1

    candidates = []
    for r in range(K):
        for c in range(1, N):
            if grid[r][c] == 1:
                continue
            if grid[r][c-1] == 1:
                continue
            if grid[r][c+1] == 1:
                continue
            candidates.append((r, c))

    vst = [0] * len(candidates)
    answer = 4
    backtrack(grid)

    if answer == 4:
        print(-1)
    else:
        print(answer)


"""디버깅 / 20260827 / 체감 난이도: G4
소요 시간 1시간 51분 / 시도 3회 / 실행 시간 420ms (코드트리, 리팩토링 후 143) / 메모리 25MB (코드트리)

[구상]
    - 구상 시간이 17분으로, 너무 짧았다. 오늘따라 정말 집중도 안되고 산만했던게 조급함의 원인이 된 것 같다.
    - 문제의 핵심은 백트래킹으로 배치 가능한 유실선의 위치들을 뽑고, 사다리 타기를 구현하여 원점 복귀가 가능한지 판단하는 것이었다.
    - 또한, 설계를 잘못하면 중복 연산이 너무 많아서 시간 복잡도가 굉장히 위험한 문제였다
        - 나는 부분조합으로 잘못 접근했지만, 조합으로 풀어야 안전하게 풀 수 있는 문제였다. (사다리에 너무 몰두함)
        - 사다리 타기 구현은 나름 내 방식대로 잘한 것 같다. 배열을 만들어서 현재 연결 상태를 업데이트, 롤백하는 방식으로 인접 체크를 계획했다.
            - 또한 이를 그대로 활용하여 시뮬레이션 파트에서 사다리 타고 내려가는 과정을 구현하기로 했다.
        - 후보 자료형을 셋으로 초기화하여 기본으로 주어지는 연결들을 제외하고 시작한 것도 사소하지만 잘한 것 같다.
        - 하지만 문제에서 제시된 환경에 대해 보다 깊게 고민해봤어야 한다.
            - 연결이 홀수인 경우, 어떤 경우에도 출발지와 같은 번호의 도착지에 도달할 수 없다는 것은 자명하다.
            - 여기까지 사고가 이어지면, 주어지는 기본 연결의 개수에 따라 시도해봐야 하는 새로운 연결의 수가 2가지로 한정된다는 것을 알 수 있다.
            - 백트래킹은 나름 익숙하다는 거만함이 내 발목을 잡았다. 자만하지 말자.
            - 시간복잡도 계산도 게을리하지 말자. 감으로 문제 푸는 시점은 한참 지났다.

[구현]
    - 구현을 정말 오래했다. 80분 정도 걸렸다.
    - 백트래킹 + 시뮬레이션 문제를 처음 풀어본건 아닌데, 오늘 문제는 꽤 어려웠다.
    - 영상을 살펴보면 초반부터 스스로에 대한 불신으로 가득한 내 모습을 확인할 수 있었다 ㅋㅋㅋ
        - 코드를 정말 한줄 한줄 정성들여 쓰고, 주석을 꼼꼼히 남겼다.
        - 디버깅하는 미래도 보였는지, 추후 혼란을 방지하게 위해 입력도 -1처리 같은거 안하고 그대로 받아서 쓸 수 있도록 했다.
        - 결정적으로 첫 구상에서 대차게 말아먹었지만, 내 상태에 대한 메타인지가 디버깅 당시에 큰 도움이 되었다.
    - 일단 백트래킹 중간에 인접 체크를 통해 탐색 범위에 제동을 거는 부분에서 꽤 많이 고민한 흔적이 역력하다.
    - 또한, 사다리 타기를 추상적으로 접근하는 방향이 있긴할텐데, 나는 배열을 활용하는 직관적인 방법밖에 생각이 안났기에.. 구현 시간이 크게 소요되었다.

[디버깅]
    - 첫 제출은 시간 초과였다. 사실 구상 자체가 잘못되었기에 당연한 결과였고, 바로 중복 처리 제거에 들어갔다.
        - 최근 경험을 통해 시간 초과에 대한 대책을 많이 고민했던게 도움이 되었다.
        - 가지치기를 추가하였고, 홀짝 이슈도 발견하여 백트래킹 함수를 조합 생성으로 바꿔야겠다는 생각을 했다.
        - 다만 시간이 좀 촉박했기에.. 일단 부분조합으로 하되, 경우에 따라 홀/짝은 무시하게 하는 방식을 시도했다.
    - 두번째 제출은 그냥 프린트문 빼는거 깜빡했당 ㅎㅎ
    - 암튼간에 시간 내에 풀기는 했고 시간도 420ms 정도 나왔는데, 가슴에 손을 얹고 말하면 틀렸다고 생각한다.
        - 일단 히든 테케가 그렇게 악랄하지 않았을 것으로 예상한다.
        - 조합으로 풀지 않으면 무조건 터져버리는 케이스들은 없어서 겨우 턱걸이로 넘겼다고 생각한다.
    - 야자 시간에 풀이 시간 한시간 정도 남았다고 가정하고 코드 개선 및 추가 디버깅 연습을 해봤다.

[후기]
    - 거만하지 말자. 자만하지 말자. 방만하지 말자.
"""


def simulate():
    is_correct = True
    for cur in range(1, N+1):
        nxt = cur
        for level in range(1, H+1):
            if weak[level][nxt-1] == 1:
                nxt -= 1
            elif weak[level][nxt] == 1:
                nxt += 1
            else:
                continue
        if cur != nxt:
            is_correct = False
            break
    return is_correct


def backtrack(limit, step=0):
    # 가지 치기
    global min_connections
    if step > min_connections:
        return

    # 조합 뽑았으면 시뮬레이션 시작.
    if step == limit:
        if simulate():
            if step < min_connections:
                min_connections = step
        return

    for idx in range(len(candidates)):
        if vst[idx] != 1:
            # 후보 뽑아오기
            cr, cc = candidates[idx]
            # 오른칸에 유실선 이미 존재하면 넘어가기
            if cc+1 < N and weak[cr][cc+1] != 0:
                continue
            # 왼칸에 유실선 이미 존재하면 넘어가기
            elif cc-1 >= 0 and weak[cr][cc-1] != 0:
                continue
            # 유실선 설치 가능한 경우 재귀
            else:
                vst[idx] = 1
                weak[cr][cc] = 1
                backtrack(limit, step+1)
                vst[idx] = 0
                weak[cr][cc] = 0


if __name__ == '__main__':
    # 고객 수, 유실선 수, 취약점 수
    N, M, H = map(int, input().split())

    # 추가할 수 메모리 유실선 후보 집합
    candidates = set()
    for i in range(1, H+1):
        for j in range(1, N):
            candidates.add((i, j))

    # 이미 추가된 메모리 유실선 정보를 받는다.
    # 후보 집합에서 중복 제거 처리 해주고,
    # 취약 정보 배열에 기록해준다.
    weak = [[0] * (N+1) for _ in range(H+1)]
    for _ in range(M):
        r, c = map(int, input().split())
        weak[r][c] = 1
        candidates.discard((r, c))
    candidates = list(candidates)

    # 최소 연결의 초기값은 4로 지정한다.
    # 모든 연산이 끝났을 때도 값이 4라면
    # 최대 3번 이내의 연결로 해결하지 못했다는 뜻.
    min_connections = 4

    # 연결의 수가 짝수일 때만 원점 복귀가 가능하다.
    if M % 2 == 0:
        vst = [0] * len(candidates)
        backtrack(limit=0)
        backtrack(limit=2)
    else:
        vst = [0] * len(candidates)
        backtrack(limit=1)
        backtrack(limit=3)

    # 정답 출력
    if min_connections <= 3:
        print(min_connections)
    else:
        print(-1)
