""" 색깔 폭탄 / 20260907 / 체감 난이도: G3
소요 시간 1시간 53분 / 시도 1회 / 실행 시간 207ms (코드트리) / 메모리 23MB (코드트리)

[구상]
    - 근래에 푼 문제 중에서 가장 많은 조건을 지닌 BFS 문제라고 생각된다.
    - 가장 큰 묶음을 찾기 위한 과정, 그리고 기준점을 찾기 위해 쌓아놓고 한번에 정렬시켜야 하는 데이터가 많았다.
    - 또한, 그룹을 확인하기 위해 외부에 전체 방문 배열을 하나 초기화하고, 내부적으로는 빨간색을 중복으로 보지 않게끔 별도의 방문 배열이 필요했다.
        - 빨간 폭탄 전용 방문 배열 활용 아이디어가 떠오르자 마자, 다음 단계들이 작동하는 방식이 머리 속으로 그려졌던것 같다.
    - 가장 손이 많이 가는 BFS 함수부터 처리하기로 했는데, 루틴을 잘 따르면서 주석 설계로 밑바탕부터 설계하고 들어갔다.
    - 중력, 회전 파트는 상당히 그렇게 어려운 요구사항이 없어서 특별한 손설계 없이 구현하기로 했다.

[구현]
    - 우선 순위를 제대로 맞춰주기 위해 필요한 데이터들을 적어놓고, 이를 기반으로 깔끔한 조건문을 작성하는데 심혈을 기울였다.
    - 가장 힘들었던 파트는 의외로 중력 구현이었다.
        - 핵심 파트인 BFS에 심혈을 기울인 나머지 집중력이 흐트러졌다.
        - 시간이 꽤나 남은 상태였고, 앞 부분에서 단위 테스트를 철저하게 수행하였기에 마음 편히 먹고 천천히 구현했다.

[디버깅]
    - 모든 함수에 대한 단위 테스트를 진행하는 과정에서 BFS가 출력하는 그룹 리스트를 확인하는 시간을 가졌다.
    - 혹시나 해서 N=2인 작은 샘플들을 위주로 진행하였는데, 이때 폭탄이 1개만 들어있는 그룹이 만들어진다는 사실을 알아챘다.
        - 적어놓은 내용과 대조하여 바로 수정하긴 했지만, 이걸 발견하지 못한 미래가 상상이 되어 정말 섬뜩했다.

[후기]
    - 역시 월요일이 짱이다.
    - 한번에 한 문제만 푸는게 짱이다.
"""
from collections import deque


def find_groups(r, c):
    # TODO 1.4 큐와 빨간색 칸만을 위한 별도의 방문 배열 초기화
    que = deque()
    que.append((r, c))
    grp_vst[r][c] = 1
    red_vst = [[0] * N for _ in range(N)]

    # TODO 1.5 현재 그룹의 칸 개수와 빨간색, 현재색 폭탄 좌표를 담을 리스트 초기화
    all_count = 1
    color = arr[r][c]
    red_coordinates = []
    cur_coordinates = [(r, c)]

    while que:
        cr, cc = que.popleft()
        for i in range(4):
            nr, nc = cr+dr[i], cc+dc[i]

            # TODO 1.6 다음 좌표가 범위 바깥이라면 무시하고 진행
            if not(0 <= nr < N and 0 <= nc < N):
                continue

            # TODO 1.7 다음 좌표에 검은색 돌이나 빈칸이 있다면 무시하고 진행
            if arr[nr][nc] < 0:
                continue

            # TODO 1.8 그룹 방문 배열에서 다음 좌표를 방문한 적이 있다면 무시하고 진행
            if grp_vst[nr][nc] != 0:
                continue

            # TODO 1.9 빨간 방문 배열에서 다음 좌표를 방문한 적이 있다면 무시하고 진행
            if red_vst[nr][nc] != 0:
                continue

            # TODO 1.10 다음 좌표의 폭탄이 빨간색이면 카운트 증가, 빨간 방문 배열 체크, 빨간 좌표 리스트에 추가
            if arr[nr][nc] == 0:
                all_count += 1
                red_vst[nr][nc] = 1
                red_coordinates.append((nr, nc))

            # TODO 1.11 다음 좌표의 폭탄이 빨간색이 아니며, 현재 그룹 색과 다르다면 무시하고 진행
            elif arr[nr][nc] != color:
                continue

            # TODO 1.12 다음 좌표의 폭탄이 현재 그룹 색과 같은 색이라면 카운트 증가, 그룹 방문 배열 체크, 기준점 후보에 등록
            else:
                all_count += 1
                grp_vst[nr][nc] = 1
                cur_coordinates.append((nr, nc))

            # TODO 1.13 큐에 다음 좌표 추가
            que.append((nr, nc))

    # TODO 1.14 기준점 찾기
    cur_coordinates.sort(key=lambda x: [-x[0], x[1]])
    standard_r, standard_c = cur_coordinates[0]

    # TODO 1.15 그룹 최종 정보 등록 (그룹 칸 개수, 빨간 칸 개수, 기준점 행, 기준점 열, 모든 좌표 리스트)
    #   edge: 한개의 폭탄으로만 이루어진 그룹은 존재할 수 없다.
    red_count = len(red_coordinates)
    all_coordinates = cur_coordinates + red_coordinates
    if all_count >= 2:
        groups.append([all_count, red_count, standard_r, standard_c, all_coordinates])


def gravitate():
    for r in range(N-1, -1, -1):
        for c in range(N):
            if arr[r][c] <= -1:
                continue

            drop_r = r
            for i in range(1, N-r):
                drop_r = r+i

                if arr[drop_r][c] != -2:
                    drop_r -= 1
                    break

            if drop_r != r:
                arr[drop_r][c] = arr[r][c]
                arr[r][c] = -2


def rotate():
    arr_copy = [row.copy() for row in arr]
    for r in range(N):
        for c in range(N):
            arr_copy[N-1-c][r] = arr[r][c]
    return arr_copy


if __name__ == '__main__':
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    answer = 0
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    while True:
        # TODO 1: BFS를 활용한 가장 큰 폭탄 묶음 탐색
        groups = []
        grp_vst = [[0] * N for _ in range(N)]

        for r in range(N):
            for c in range(N):

                # TODO 1.1 빈칸, 빨간 폭탄, 검은 돌 전부 무시.
                if arr[r][c] <= 0:
                    continue

                # TODO 1.2 현재 칸을 이미 방문했다면 무시하고 진행.
                if grp_vst[r][c] != 0:
                    continue

                # TODO 1.3 BFS 함수 호출
                find_groups(r, c)

        if groups:
            # TODO 2: 가장 큰 폭탄 묶음을 터뜨리고 점수 추가 (빈칸은 -2로 표시)
            groups.sort(key=lambda x: [-x[0], x[1], -x[2], x[3]])
            _, _, _, _, coordinates = groups[0]
            answer += len(coordinates) ** 2
            for r, c in coordinates:
                arr[r][c] = -2

            # TODO 3: 첫번째 중력 적용
            gravitate()

            # TODO 4: 반시계방향 90도 회전
            arr = rotate()

            # TODO 5: 두번째 중력 적용
            gravitate()

        # TODO 6: 더 이상 터뜨릴 폭탄 없으면 종료.
        else:
            break

    # TODO 7: 정답 출력
    print(answer)
