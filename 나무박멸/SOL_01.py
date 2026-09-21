""" 나무박멸 / 20260915 / 체감 난이도: G4
소요 시간 48분 / 시도 1회 / 실행 시간 386ms (코드트리) / 메모리 27MB (코드트리)

[구상]
    - 쓸데 없는 기교 부리지 않고 정확하게 제시된 내용만 따르면서 풀었다.
    - 예전에 풀지 못한 상태에서 코드리뷰에 참석했었는데, 대단한 묘리가 숨어있다기 보단 내가 그냥 말을 제대로 안들은 탓이었다.
    - 내용을 적당히 잊을만한 기간을 스스로에게 주고, 오늘 다시 풀어봤다.

[구현]
    - 문제 내용 잘 정리해둔걸로 열심히 구현했다.
    - 딕셔너리, 셋 같은 자료형 굳이 굳이 끼워 넣거나, 여러 단계를 한번에 합치는 등 나대지 않았다.
    - 그냥 순서대로 구현했다.

[디버깅]
    - 디버깅 하면서 예전에 내가 왜 틀렸는지 정확히 찾아낼 수 있었다.
    - 배열에서 나무 그루와 지형 정보를 분리해서 보지 않았는데,
    - 제초제가 벽을 만날 때 멈추는건 잘 처리했지만, 나무를 지운답시고 여기를 0으로 만들어버렸다.
    - 다행히 디버깅 중 이슈를 잡아내서 처리하였다. 실수 모음 +1
    - 정보는 종류에 맞춰 다른 배열을 사용하는게 나을 것 같다.

[후기]
    - 디버깅 중 발견한 문제점을 기반으로 이전 코드를 수정했는데, 여전히 오답이 나왔다.
    - 마찬가지로 코드를 읽다보니 어떤 부분이 문제가 되었는지 알 수 있었다.
        - 처음 시도할 당시에, 제초제는 나무에다 뿌려야 한다는 고정관념에 사로잡혀 있었다.
        - 즉, 모든 칸이 벽이거나 빈칸인 경우에는 제초제 자체를 뿌리지 않으므로, 정답보다 많은 수의 나무가 살아남았던 것이다.
    - 근데 이게 참 무서운게, 재풀이 시점에서 당연하다는 듯이 고쳐지는 파트가 있는 반면, 똑같은 실수를 그대로 재현하여 디버깅 단계에서나 발견할 수도 있다는 것이다.
    - 이번 문제를 최대한 실수 없이 푸는 방법은, 나무를 제외한 지형지물을 한 배열에, 나무의 정보를 다른 배열에 저장히여 따로 관리하는것 같다.
        - 굳이? 라고 생각할 수도 있는데, 값 덮어씌우는 실수를 자주하는 편이기에 나 한정 해결책이다.
"""


def debug(msg):
    print()
    print(msg)
    for row in land:
        print(*row)


def grow():
    delta = [[0] * N for _ in range(N)]
    for cr in range(N):
        for cc in range(N):
            if land[cr][cc] > 0:
                for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    nr, nc = cr+dr, cc+dc
                    if not(0 <= nr < N and 0 <= nc < N):
                        continue
                    if land[nr][nc] <= 0:
                        continue
                    delta[cr][cc] += 1

    for cr in range(N):
        for cc in range(N):
            land[cr][cc] += delta[cr][cc]


def reproduce():
    delta = [[0] * N for _ in range(N)]
    for cr in range(N):
        for cc in range(N):
            if land[cr][cc] > 0:
                candidates = []

                for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    nr, nc = cr + dr, cc + dc
                    if not (0 <= nr < N and 0 <= nc < N):
                        continue
                    if chem[nr][nc] >= time:
                        continue
                    if land[nr][nc] == 0:
                        candidates.append((nr, nc))

                for nr, nc in candidates:
                    delta[nr][nc] += land[cr][cc] // len(candidates)

    for cr in range(N):
        for cc in range(N):
            land[cr][cc] += delta[cr][cc]


def spread(cr, cc):
    result = [land[cr][cc], [(cr, cc)]]
    if land[cr][cc] <= 0:
        return result

    for dr, dc in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
        for rep in range(1, K + 1):
            nr, nc = cr+dr*rep, cc+dc*rep
            if not (0 <= nr < N and 0 <= nc < N):
                continue
            if land[nr][nc] <= 0:
                result[1].append((nr, nc))
                break
            result[0] += land[nr][nc]
            result[1].append((nr, nc))
    return result


def kill(time):
    global answer
    candidates = []
    for cr in range(N):
        for cc in range(N):
            if land[cr][cc] >= 0:
                kills, coords = spread(cr, cc)
                candidates.append([kills, cr, cc, coords])
    candidates.sort(key=lambda x: [-x[0], x[1], x[2]])

    kills, _, _, coords = candidates[0]
    for cr, cc in coords:
        if land[cr][cc] > 0:
            land[cr][cc] = 0
        chem[cr][cc] = time+C
    answer += kills


if __name__ == '__main__':
    N, M, K, C = map(int, input().split())
    land = [list(map(int, input().split())) for _ in range(N)]
    chem = [[-1] * N for _ in range(N)]

    answer = 0
    time = 0

    for _ in range(M):
        grow()
        # debug('after growth')
        reproduce()
        # debug('after reproduction')
        kill(time)
        # debug('after kills')
        time += 1

    print(answer)
