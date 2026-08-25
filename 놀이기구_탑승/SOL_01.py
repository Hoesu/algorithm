""" 놀이기구_탑승 / 20260821 / 체감 난이도: S5
소요 시간 55분 / 시도 1회 / 실행 시간 49ms (코드트리) / 메모리 16MB (코드트리)

[구상]
    - 25분 정도 구상하는 시간을 가졌다.
    - 솔직히 처음엔 엄청 막막했는데, 생각해보니 초기 위치는 항상 고정되어 있다는 것을 깨달았다.
    - 나머지는 그냥 주어진 규칙대로만 구현하면 되었고, 우선순위 큐를 사용하면 쉽게 해결 가능할 것 같았다.
    - 딱 한가지 걱정거리가 있었다면, 남아있는 자리를 찾기 위해 전체 배열을 매번 순회하면 또 시간초과빔을 맞을 것 같았다.
        - 평소 정말 필요한 경우가 아니라면 set을 잘 쓰지 않지만, n이 최대 20이라서 튜플 400개 정도는 감당할 수 있을 것 같았다.
        - 따라서 모든 좌석을 집합에 넣어놓고, 좌석을 점유할 때마다 하나씩 discard로 제거해주기로 했다.

[구현]
    - 첫 문제를 시간초과 걸리고 와서 그런지 급하게 30분 컷으로 구현했다.
    - 구현하면서 뒤늦게 추가한 점은, 새롭게 좌석을 배치할 때마다 전체 점수에 변경이 생길 수 있다는 점이었다.
        - 따라서 최종 점수는 모든 좌석 배치가 끝난 뒤에 전체 배열을 순회하며 계산할 수 밖에 없었다.
        - 이를 위해서 좋아하는 친구에 대한 정보들을 딕셔너리에 미리 담아둘 필요가 있었다.

[디버깅]
    - 솔직히 마음이 급해서 검증 시간을 따로 가져보진 않았다.
    - 오픈 테케가 다 맞았고, 솔직히 대단한 예외가 발생하기 어려운 문제라고 생각했다.

[후기]
    - 힙큐 사랑해요
"""
from heapq import heappush, heappop


def find_best(n1, n2, n3, n4):
    heap = []
    for cr, cc in available:
        # 친구 수, 빈칸 수
        friends = 0
        empty = 0
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            # 이것도 앞으로는 직접 비교로 바꾸는게 좋을까?
            # 암튼 인접한 위치에 호감 친구 있으면 친구 수 증가
            if seats[nr][nc] in (n1, n2, n3, n4):
                friends += 1
            # 빈칸이면 빈칸 수 증가
            if seats[nr][nc] == 0:
                empty += 1
        # 친구(최대), 빈칸(최대), 행(최소), 열(최소)
        heappush(heap, [-friends, -empty, cr, cc])
    # 우선 순위 가장 높은 위치 하나 뽑기!
    _, _, r, c = heappop(heap)
    return r, c


if __name__ == '__main__':
    N = int(input())
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
    # 좌석 배열 초기화
    seats = [[0] * N for _ in range(N)]
    # 좋아하는 친구 정보 저장할 룩업 딕셔너리
    favorites = dict()
    # 현재 비어있는 좌석 집합. (최대 400!)
    available = set()
    for r in range(N):
        for c in range(N):
            available.add((r, c))

    # 첫번째 친구는 무조건 1,1에 들어간다.
    n0, n1, n2, n3, n4 = map(int, input().split())
    favorites[n0] = [n1, n2, n3, n4]
    seats[1][1] = n0
    available.discard((1, 1))

    # 다음 친구부터는 규칙에 따라 배치된다.
    for _ in range(pow(N, 2)-1):
        n0, n1, n2, n3, n4 = map(int, input().split())
        favorites[n0] = [n1, n2, n3, n4]
        best_r, best_c = find_best(n1, n2, n3, n4)
        seats[best_r][best_c] = n0
        # 좌석 하나를 차지할 때마다 기존 집합에서 해당 위치 제거!
        available.discard((best_r, best_c))

    # 점수 계산
    score_sum = 0
    # 인접한 호감 친구 수를 바로 인덱스로 활용할 수 있게끔 리스트 미리 만들어두기.
    score_rule = [0, 1, 10, 100, 1000]
    for cr in range(N):
        for cc in range(N):
            score_idx = 0
            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if seats[nr][nc] in favorites[seats[cr][cc]]:
                    score_idx += 1
            score_sum += score_rule[score_idx]
    # 정답 출력
    print(score_sum)
