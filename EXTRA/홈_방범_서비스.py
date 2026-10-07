""" 홈 방범 서비스 / 20261007 / 체감 난이도: G5
소요 시간 40분 / 시도 3회 / 실행 시간 948ms (SWEA) / 메모리 63,232KB (SWEA)

손해를 보지 않는다 = 수익이 0원인 경우도 괜찮다. 문제 똑바로 읽자.
"""


def count_house(sr, sc, sd):
    # 대각선으로 생각하자. 좌표 범위 벗어나도 유효하다.
    top = (sr-sd+1, sc)
    bot = (sr+sd-1, sc)
    cnt = 0
    for (cr, cc) in houses:
        condition_1 = top[0]+top[1] <= cr+cc <= bot[0]+bot[1]
        condition_2 = top[0]-top[1] <= cr-cc <= bot[0]-bot[1]
        if condition_1 and condition_2:
            cnt += 1
    return cnt


if __name__ == '__main__':
    test_case = int(input())
    for tc in range(1, test_case+1):
        print(f'#{tc}', end=' ')
        N, M = map(int, input().split())

        # 집 좌표 모음 집합 생성 후 배열 정보 버리기.
        houses = set()
        for r in range(N):
            line = list(map(int, input().split()))
            for c in range(N):
                if line[c] == 1:
                    houses.add((r, c))

        max_count = -1
        for d in range(1, N*2):
            cost = d**2 + (d-1)**2
            for r in range(N):
                for c in range(N):
                    count = count_house(r, c, d)
                    profit = M * count - cost
                    if profit >= 0 and count > max_count:
                        max_count = count
        print(max_count)
