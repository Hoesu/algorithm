"""회전하는 빙하 / 20260826 / 체감 난이도: G3
소요 시간 1시간 51분 / 시도 2회 / 실행 시간 1772ms (코드트리, 리팩토링 후 421ms) / 메모리 27MB (코드트리)

[구상]
    - 25분 정도 구상하고 들어갔다.
    - 내용을 이해하는데 오랜 시간이 걸리진 않았고, 비교적 익숙한 맛의 내용들도 있었다 (완탐, DFS, BFS)
    - 문제는 부분 배열 회전이었고, 미리 pseudo code를 작성해봤다(여태 한 구상 중에 가장 정성스럽게 함).
        - 일단 부분 배열을 4등분하면 몇 사분면인지에 따라 내부 값들이 이동하는 방향이 결정된다는 것을 파악했다.
        - 또한, 이동하는 거리는 항상 2^(LEVEL-1)만큼이었다.
    - 얼음 녹이기, 덩어리 영역 구하기는 이미 아는 내용이라서 바로 구현에 들어갔다.

[구현]
    - 여기서 엄청난 고역을 치뤘다. 부분배열 회전 구상이 틀리진 않았는데, 너무 복잡하게 생각했다.
    - 그러다보니 구현과정에서 자잘한 실수들을 많이 저질렀고, 검증 단계에서 정상 작동하게 만드느라 시간을 너무 많이 썼다.
    - 결국 완료하고 얼음 녹이기와 덩이리 크기 계산만 남겨둔 상태에서 시간이 정말 없다는 것을 깨달았다.
    - 그때, 어디선가 제 2의 자아가 튀어나와서 나에게 외쳤다. "어서 타! 설명할 시간이 없어!!!"
        - 절대 틀리지는 않는데, 최적화는 고려하지 않는다는 마인드로 미친듯이 질주했다.
        - DFS 갑자기 생각안나서 BFS로 땜빵치고, 녹이기 완탐 가지치기 같은거 없이 그냥 막 적었다.
        - 어찌저찌 끝은 내고 오픈 테케가 다 맞는지 서둘러 확인했다.

[디버깅]
    - 첫 제출은 시간초과였다... 물론 이때도 시간은 가고 있었고, 코드를 재빨리 읽으면서 최적화할만한 구석을 찾았다.
    - 마침 melt 함수에서 얼음 없는 칸에서도 탐색 돌리고 있다는 것을 포착했고, 가지치기를 껴넣어서 겨우 겨우 2초 안으로 돌아가게 만들었다.

[후기]
    - 사실 이 문제는 풀이 당시보다, 야자 시간에 시간 단축을 위한 디버깅을 하면서 정말 많이 배웠다.
    - 일단 랜덤 모듈을 활용해서 대형 테케를 만드는 것을 숙달할 수 있었다.
    - 또한, 타임 모듈 응용도도 꽤 올렸다고 생각한다.
        - 예를 들면 같은 for문 안에서 rotate, melt가 같이 돌아가고 있어서 각자 실행시간을 따로 보기 힘들었다.
        - 그래서 함수별로 시간을 따로 재서 바깥에 있는 합산 시간에 계속 추가해주는 방식을 시도했다.
        - 그렇게 하니까 몇백번씩 돌아가도, 어떤 함수에서 병목이 발생하는지 분리해서 볼 수 있었다.
    - 이런 방식으로 개선해야할 범위를 계속 좁히니까, 이전에는 보이지 않던 문제가 명확히 보였다.
        - 시간 초과의 가장 큰 원흉은 회전 정보 저장을 위한 임시 배열을 불필요하게 자주 생성한 것이었다.
    - 구현량이 이렇게 많은 문제는 처음 풀어보는거 같은데.. 피로도가 상당했다.
"""


def rotate(level):
    # 전체 배열을 2**level * 2**level 크기의 사각형으로 분할하고 다시 4등분하면,
    # 1사분면 (남), 2사분면 (동), 3사분면 (북), 4사분면 (서)로 나누어 생각할 수 있다.
    step = pow(2, level) // 2
    # 회전 후 빙하 정보를 기록할 임시 배열
    result = [row.copy() for row in glacier]

    # 현재 보고 있는 격자의 회전 방향을 알기 위한 플래그
    r_flag = 0
    c_flag = 0

    # 전체 배열을 2**(level-1) 단위로 분할하고
    # 왼쪽 상단 모서리 좌표를 기준으로 생각하자.
    for r in range(0, limit, step):
        for c in range(0, limit, step):
            # r_flag, c_flag의 홀짝 여부로 현재 격자가 몇 사분면인지 알 수 있다.
            r_mod = r_flag % 2
            c_mod = c_flag % 2

            # 제 1사분면 (남)
            if r_mod == 0 and c_mod == 1:
                dr, dc = 1, 0
            # 제 2사분면 (동)
            elif r_mod == 0 and c_mod == 0:
                dr, dc = 0, 1
            # 제 3사분면 (북)
            elif r_mod == 1 and c_mod == 0:
                dr, dc = -1, 0
            # 제 4사분면 (서)
            else:
                dr, dc = 0, -1
            # 임시 배열[이동 후 위치] = 원본 배열[이동 전 위치]
            for cr in range(r, r+step):
                for cc in range(c, c+step):
                    result[cr + dr*step][cc + dc*step] = glacier[cr][cc]

            c_flag = (c_flag + 1) % limit
        r_flag = (r_flag + 1) % limit
    return result


def melt():
    # 얼음 녹이는 과정은 완탐 아니면 방법이 없다.
    vst = [[0] * limit for _ in range(limit)]
    for cr in range(limit):
        for cc in range(limit):
            # 다만 얼음이 없는 칸은 녹일 수 없으므로 무시 가능
            if glacier[cr][cc] == 0:
                continue

            glacier_cnt = 0
            for i in range(4):
                nr, nc = cr + delta_r[i], cc + delta_c[i]
                # 범위 바깥은 얼음이 없다고 친다.
                if not(0 <= nr < limit and 0 <= nc < limit):
                    continue
                if glacier[nr][nc] == 0:
                    continue
                glacier_cnt += 1
            # 얼음 카운트가 3 미만이면 방문 배열에 기록
            if glacier_cnt < 3:
                vst[cr][cc] = -1
    # 전부 탐색한 다음 한꺼번에 녹이기
    for r in range(limit):
        for c in range(limit):
            glacier[r][c] += vst[r][c]


def dfs(r, c):
    # 전역 변수로 값 업데이트
    global cur_size
    vst[r][c] = 1
    cur_size += 1

    for i in range(4):
        nr, nc = r + delta_r[i], c + delta_c[i]
        if not(0 <= nr < limit and 0 <= nc < limit):
            continue
        if vst[nr][nc] == 1:
            continue
        if glacier[nr][nc] == 0:
            continue
        dfs(nr, nc)


if __name__ == '__main__':
    N, Q = map(int, input().split())
    glacier = [list(map(int, input().split())) for _ in range(2**N)]
    commands = list(map(int, input().split()))
    delta_r = [-1, 1, 0, 0]
    delta_c = [0, 0, -1, 1]
    # 전체 배열 길이 매번 계산하기 싫어요
    limit = pow(2, N)

    # 주어진 회전 명령 순회
    for lv in commands:
        # 회전 레벨 0이면 녹이기만 하고 넘어가기.
        if lv == 0:
            melt()
            continue
        # 회전 레벨 0보다 크면 회전 + 녹이기
        glacier = rotate(lv)
        melt()

    # DFS에서 전역 변수로 사용할 현재 군집 크기
    cur_size = 0
    # 출력으로 사용될 최대 군집 크기
    max_size = 0
    # 방문 배열은 한번만 초기화
    vst = [[0] * limit for _ in range(limit)]

    # 군집 크기는 DFS로 측정
    for r in range(limit):
        for c in range(limit):
            # 얼음 없는 칸 무시
            if glacier[r][c] == 0:
                continue
            # 이미 방문한 칸 무시
            if vst[r][c] == 1:
                continue
            # DFS 시작
            dfs(r, c)
            # 최대 크기 업데이트
            if cur_size > max_size:
                max_size = cur_size
            cur_size = 0

    # 남아있는 얼음 합 출력
    print(sum([sum(row) for row in glacier]))
    # 최대 덩어리 크기 출력
    print(max_size)
