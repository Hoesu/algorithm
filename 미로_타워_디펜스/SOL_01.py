"""미로 타워 디펜스 / 20260907 / 체감 난이도: G3
소요 시간 1시간 33분 / 시도 1회 / 실행 시간 75ms (코드트리) / 메모리 17MB (코드트리)

[구상]
    - 넉넉하게 30분 정도 구상하고 들어갔다.
    - 주어진 환경을 좀 더 일반화하면 단계별 풀이 과정이 무척 쉬워질 것이라고 생각했다.
    - 가장 중요한 부분은 2차원 배열 형태로 들어오는 입력값을 1차원으로 변환하는 과정이라고 생각했다.
        - 동서남북으로 몬스터를 죽이기 위해 좌표를 찾아야 하는데, 1차원 배열로 변환하는 과정에서 위치 정보가 손실된다. 따라서 패턴이 보이지 않으면 해당 접근법을 포기하기로 했다.
        - 정중앙을 0번으로 잡고 달팽이 모양으로 번호를 메긴 결과, 네 방향으로 뻗어나가는 좌표들의 1차원 상에서의 인덱스가 패턴을 가지는 것을 확인할 수 있었다.
    - 나머지 부분은 버퍼를 활용한 중복 체크나 다름 없기에 자신감을 가지고 구현으로 들어갔다.

[구현]
    - 일단 달팽이 모양의 입력을 1차원으로 펴는 부분은 함수로 구현했다. 최근 익숙해진 대각선 접근법으로 쉽게 해결했고, 검증까지 엄밀하게 진행했다.
    - 동서남북 방향의 킬존 인덱스를 특정짓는 부분도 pseudo 코드를 미리 작성해뒀기에 수월하게 진행하였다.
        - 결과 배열을 반환하는 과정에서, 문제에서 제시한 동서남북 인코딩에 맞춰 행 순서를 재구성했더니 편리했다.
    - 1차원 리스트 중복 체크는 버퍼 리스트를 활용해서 쉽게 쉽게 구현했다.
        - 다만, 루프가 끝나고 버퍼 내부에 남아있는 잔여 값들을 잘 처리해줘야 함을 검증 단계에서 뒤늦게 확인했다.
        - 또한, 문제에서 요구하는 페어 변환은 중복 체크 단계에서 동시에 처리할 수 있다는 것을 깨달아서 바로 적용했다.
        - 마지막으로, 중복 제거 도중엔 굳이 리스트 원래 사이즈로 원복 시킬 필요도 없었다.
        - 소요 시간이 가장 크게 줄어들었던 원인이 바로 이 부분이 아닐까 생각한다.

[후기]
    - 일반화를 시도하기 전에, 문제가 나에게 주는 값들이 내 구상을 실현하는데 있어 유리하게 작용하는지 고민해보도록 하자.
    - 대놓고 1차원 배열로 풀라고 이쁘게 값을 정리해서 주는 문제는 아니었기에, 1차원 변환이 시간을 꽤 잡아 먹는 리스크가 있었다.
"""


def flatten(array):
    # 정중앙 기준 미로는 서, 남, 동, 북 순으로 뻗어나간다.
    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    # 정중앙에서 서쪽을 바라보며 출발.
    cr, cc, cd = N//2, N//2, 0
    # 결과를 저장할 1차원 배열 초기화.
    flattened_lst = [array[cr][cc]]

    for i in range(pow(N, 2)-1):
        dr, dc = moves[cd]
        nr, nc = cr + dr, cc + dc
        cr, cc = nr, nc
        flattened_lst.append(array[nr][nc])

        # 방향 꺾어야 하는 지점만 조건 처리 (같은 대각선 상)
        if nr <= N//2 and nr-nc == 1:
            cd = (cd+1) % 4
        elif nr > N//2 and nr-nc == 0:
            cd = (cd+1) % 4
        elif nr < N//2 and nr+nc == N-1:
            cd = (cd+1) % 4
        elif nr > N//2 and nr+nc == N-1:
            cd = (cd+1) % 4
        else:
            continue
    return flattened_lst


def get_killzones():
    # 2차원 미로를 1차원 배열로 변환하면
    # 정중앙 기준으로 4방향으로 뻗어나가는 모든 칸들의 좌표를
    # 1차원 상의 인덱스로 특정 지을 수 있다.
    idx = 0
    start = 1
    within_loop = 2
    inter_loop = 3
    zones = [[] for _ in range(N//2)]

    for i in range(N//2):
        for j in range(4):
            idx = start + within_loop * j
            zones[i].append(idx)
        start = idx + inter_loop
        within_loop += 2
        inter_loop += 2

    # 행렬 전치, 각 행이 하나의 방향 보관
    zones = list(map(list, zip(*zones)))
    # 문제 상황에 맞게 순서 재배열
    ordered_zones = []
    ordered_zones.append(zones[2])
    ordered_zones.append(zones[1])
    ordered_zones.append(zones[0])
    ordered_zones.append(zones[3])
    return ordered_zones


def dup_check(lst):
    # 중복 제거 후 필드
    result = [0]
    # 중복 제거 후 페어
    pairs = [0]
    # 중복 체크용 임시 버퍼
    buffer = []
    # 현재 인덱스
    cur_idx = 1
    # 현재 값
    cur_val = 0
    # 현재 중복 횟수
    cur_cnt = 0
    # 현재 점수
    cur_score = 0

    while cur_idx < len(lst):
        # 0 만나면 무시하고 진행
        if lst[cur_idx] == 0:
            cur_idx += 1
            continue
        # 버퍼 비어있으면 그냥 0이 아닌 첫 값 박아주기
        if not buffer:
            buffer.append(lst[cur_idx])
            cur_val = lst[cur_idx]
            cur_cnt = 1
            cur_idx += 1
            continue
        # 같은 값 만나면 중복 체크
        if cur_val == lst[cur_idx]:
            buffer.append(lst[cur_idx])
            cur_cnt += 1
        # 아니면 버퍼 길이 체크하고 길이 4 이상이면 점수에 추가, 결과에서 제거
        # 버퍼 길이 4보다 짧으면 그냥 결과에 붙여주고 다시 시작
        else:
            if cur_cnt >= 4:
                cur_score += cur_val * cur_cnt
            else:
                pairs.extend([cur_cnt, cur_val])
                result.extend(buffer)
            buffer = [lst[cur_idx]]
            cur_val = lst[cur_idx]
            cur_cnt = 1
        # 인덱스 증가 까먹지 맙시다
        cur_idx += 1

    # 버퍼에 남은 찌꺼기도 깔끔하게 처리해주기
    if buffer:
        if cur_cnt >= 4:
            cur_score += cur_val * cur_cnt
        else:
            pairs.extend([cur_cnt, cur_val])
            result.extend(buffer)
    return result, pairs, cur_score


if __name__ == '__main__':
    # 격자 사이즈, 라운드 수
    N, M = map(int, input().split())

    # 입력으로 받은 2차원 배열 진행 순서에 맞춰 1차원 배열로 형태 변형시키기.
    field = flatten([list(map(int, input().split())) for _ in range(N)])

    # 1차원 배열 상으로 방향별 킬존 탐색.
    # 0: 동, 1: 남, 2: 서, 3: 북
    zone = get_killzones()

    # 점수 초기화
    score = 0

    # 라운드 수만큼 반복
    for i in range(M):

        # TODO 1: 공격 방향, 공격 칸수 입력 받고 필드에서 해당칸 비우기 + 점수 합산
        attack_dirc, attack_dist = map(int, input().split())
        for j in range(attack_dist):
            loc = int(zone[attack_dirc][j])
            score += field[loc]
            field[loc] = 0

        # TODO 2: 빈공간을 채우며 4번 이상 중복되는 값 삭제, 점수 추가를 더 이상 뽑을 점수 없어지는 시점까지 반복
        #       이때, 페어에 대한 처리도 동시에 진행한다.
        #       종료 시점에 나오는 페어가 다음 필드로 대체된다.
        while True:
            field, pairs, new_score = dup_check(field)
            score += new_score
            if new_score == 0:
                break

        # TODO 3: 필드를 페어로 대체하고, 길이 맞춰주기
        if len(pairs) > pow(N, 2):
            field = pairs[:pow(N, 2)]
        elif len(pairs) < pow(N, 2):
            pad_length = pow(N, 2) - len(pairs)
            zeroes = [0] * pad_length
            field = pairs + zeroes
        else:
            field = pairs

    # 정답 출력
    print(score)
