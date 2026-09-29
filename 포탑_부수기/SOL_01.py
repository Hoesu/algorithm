""" 포탑 부수기 / 20260914 / 체감 난이도: G4
소요 시간 1시간 41분 / 시도 1 / 실행 시간 243ms (코드트리) / 메모리 23MB (코드트리)

[구상]
    - 문제를 빠지는 부분 없이 잘 읽도록 노력했다.
    - 크게 어렵게 느껴지는 부분은 없었고, 최단 경로를 뽑는 방법에 대해서 아이디어를 확실하게 잡고 들어갔다.
        - 어떤 위치에서 어떤 방향으로 이동하던 간에 비용은 항상 같으므로, BFS에 경로 딕셔너리를 사용할 수 있다고 생각했다.
        - 다익스트라는 상황에 따라 비용이 계속 변화하는 환경에서 활용해보자.

[구현]
    - 한번에 돌릴 수 있는걸 여러번에 걸쳐서 연산하고 있어 시간 소요가 다소 크긴하다.
    - 다만, 한번에 모든걸 처리하려다가 피를 본적이 워낙 많다보니 그냥 따로 구현했다.
    - 4방향, 8방향을 위해 굳이 방향 벡터를 따로 만들어 쓰지 않고, 인덱싱으로 해결했다.
    - 우선 순위도 람다 정렬로 평소와 다름 없이 잘 구현했고...
    - 레이저 공격도 일단 시도는 해보고 안된다는걸 체크해야 되기 때문에 안되는 경우엔 빈 리스트 반환, 포탄으로 전환하게 처리했다.

[디버깅]
    - 오픈 테케를 가지고 디버깅을 좀 했다. 내가 문제를 잘못 이해한 부분이 2가지 정도 있었다.
        - 핸디캡은 한번 추가해주면 영원하다. (핸디캡은 일시적이라는 나의 편견 반영...)
        - 공격자만 '마지막 공격 시간'을 업데이트 해줘야 한다. (피해를 입은 모두를 업데이트 해주고 있었다.)

[후기]
    - 흠.. 편견을 가지고 문제를 읽지 말자.
    - 이젠 아름다운 코드, 실행시간이 빠른 코드 보다도 안정성이 뛰어난 코드를 짜고 싶다는 생각을 한다.
        - 입력값을 내가 원하는 형태로 가공하는 과정을 강건하게 처리할 수 있는 알고리즘이 좋다.
"""
from collections import deque


# TODO 1: 레이저 공격 구현 (BFS)
#   입력: 현재 좌표, 목표 좌표
#   출력: 공격 대상이 되는 칸의 좌표와 데미지를 쌍으로 묶어 저장한 리스트
def lazer(sr, sc, gr, gc):
    que = deque()
    que.append((sr, sc))
    vst = [[0] * M for _ in range(N)]
    vst[sr][sc] = 1
    routes = dict()

    while que:
        cr, cc = que.popleft()
        if cr == gr and cc == gc:
            break

        for i in range(0, 8, 2):
            dr, dc = directions[i]
            nr = (cr+dr) % N
            nc = (cc+dc) % M

            if field[nr][nc] == 0:
                continue
            if vst[nr][nc] != 0:
                continue

            vst[nr][nc] = 1
            que.append((nr, nc))
            routes[(nr, nc)] = (cr, cc)

    if (gr, gc) not in routes:
        return []

    towers[(sr, sc)][0] += (N+M)
    towers[(sr, sc)][1] = time
    damage = towers[(sr, sc)][0]
    targets = [(gr, gc, damage)]

    while True:
        nr, nc = routes[(gr, gc)]
        if sr == nr and sc == nc:
            break
        targets.append((nr, nc, damage//2))
        gr, gc = nr, nc
    return targets


# TODO 2: 폭탄 공격 구현
#   입력: 현재 좌표, 목표 좌표
#   출력: 공격 대상이 되는 칸의 좌표와 데미지를 쌍으로 묶어 저장한 리스트
def bomb(sr, sc, gr, gc):
    towers[(sr, sc)][0] += (N+M)
    towers[(sr, sc)][1] = time
    damage = towers[(sr, sc)][0]
    targets = [(gr, gc, damage)]

    for i in range(8):
        dr, dc = directions[i]
        nr = (gr+dr) % N
        nc = (gc+dc) % M

        if sr == nr and sc == nc:
            continue
        if field[nr][nc] == 0:
            continue

        targets.append((nr, nc, damage//2))
    return targets


if __name__ == '__main__':
    N, M, K = map(int, input().split())

    directions = [
        (0, 1), (1, 1), (1, 0), (1, -1),
        (0, -1), (-1, -1), (-1, 0), (-1, 1)
    ]

    field = [list(map(int, input().split())) for _ in range(N)]

    towers = dict()
    for r in range(N):
        for c in range(M):
            if field[r][c] > 0:
                towers[(r, c)] = [field[r][c], -1]
                field[r][c] = 1

    time = 0
    while time < K:
        # 종료 조건
        if len(towers.keys()) == 1:
            break

        # 모든 포탑에 대해 우선 순위 정렬하여 공격자와 공격 대상 찾기
        priority = []
        for (tr, tc), (power, last_attack) in towers.items():
            priority.append([power, last_attack, tr, tc])
        priority.sort(key=lambda x: [x[0], -x[1], -(x[2]+x[3]), -x[3]])
        atk_r, atk_c = priority[0][2], priority[0][3]
        hit_r, hit_c = priority[-1][2], priority[-1][3]

        # 공격 범위에 들어가는 칸 모두 찾기
        victims = lazer(atk_r, atk_c, hit_r, hit_c)
        if not victims:
            victims = bomb(atk_r, atk_c, hit_r, hit_c)

        # 피해 입은 칸을 전부 순회하며 피해 반영
        destroyed = []
        touched = set()
        touched.add((atk_r, atk_c))

        for vr, vc, damage in victims:
            towers[vr, vc][0] -= damage
            touched.add((vr, vc))
            if towers[vr, vc][0] <= 0:
                destroyed.append((vr, vc))

        # 파괴된 타워들 삭제
        for tr, tc in destroyed:
            towers.pop((tr, tc))
            field[tr][tc] = 0

        # 피해 입지 않은 칸을 전부 순회하며 체력 증가
        for tr, tc in towers:
            if (tr, tc) not in touched:
                towers[(tr, tc)][0] += 1

        # 시간 증가
        time += 1

    # 정답 출력
    answer = 0
    for key, value in towers.items():
        if value[0] > answer:
            answer = value[0]
    print(answer)
