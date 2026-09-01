"""2048 게임 / 20260831 / 체감 난이도: G4
소요 시간 55분 / 시도 1회 / 실행 시간 346ms (코드트리) / 메모리 24MB (코드트리)

[구상]
    - 19분 정도 구상하고 들어갔다. 평소보다 짧은 이유는 이 게임을 엄청 많이 해봤기 때문에 문제 이해가 쉬웠기 때문.
    - 보자마자 백트래킹 문제인건 눈치를 챘고... 중력 구현에 대해서 꽤 고민하는 시간을 가졌다.
        - 결국 핵심은 중력 방향에 따라서 부딪히는 벽과 가까운 순서로 처리를 해주는 것이다.
        - 따라서 기존 배열에서 값을 빼와서 임시 배열에서 알맞은 처리를 해주는 방식을 떠올렸다.
    - 시간복잡도에 대해서도 생각을 해봤는데, 꽤 여유롭다는 의견이다.
        - 백트래킹 4^5, 중력 적용할 때마다 대충 N^2이라 치면 최대 4 * 10^5 정도 된다.
        - 그래서 시간을 좀 더 잡아먹더라도, 복잡한 구현 없이 편하게 갈 수 있는 방법에 대해 고민했다.
        - 중력 방향에 따라서 처리를 다르게 해줘야 하는 부분들을 행렬 전치와 열/행 순서 반전으로 해결하기로 했다.

[구현]
    - 갑자기 든 생각에 따라서 백트래킹 함수를 미뤄두고 중력 적용 함수부터 구현했다.
        - 일단 이게 제대로 작동해야 백트래킹을 하던 말던 하기 때문에...
        - pseudo code를 짜두고 들어갔기 때문에 별다른 어려움 없이 구현을 마쳤다.
        - 모든 방향을 기준으로 검증하는 시간을 가졌는데, 첫 시도부터 잘나와서 좀 당혹스러웠다.
        - 대신에 행렬 전치(zip), 행/열 반전 과정에서 튜플이 나오거나, 제로 패딩 방향이 틀린 부분은 수정해줬다.
    - 나머지는 그냥 맨날 먹던 맛이라 백트래킹 구현하고 끝냈다.
    - 총 구현 시간은 대략 26분 정도 걸렸다.

[디버깅]
    - 남은 10분은 검증하는데 썼는데, 이것 저것 엣지 만들어서 돌려봤다.
        - N이 1인 이상한 케이스도 가능하긴 해서.. 돌려봤다.
        - 시간 초과 살짝 쫄려서 20*20으로 돌려봤는데 초스피드로 나오길래 시간은 됐구나 했다.

[후기]
    - 개인적으로 종협 프로의 풀이가 정말 인상 깊었다.
    - 배열만 매번 다르게 회전시켜주면 중력을 항상 아래로 향하게 해도 문제를 풀 수 있다!
"""


# 행렬 전치 함수
def transpose(origin: list):
    result = []
    for col in zip(*origin):
        result.append(col)
    return result


# 배열에 주어진 방향대로 중력 적용하는 함수
def gravitate(array: list, direction: int):
    use_reverse = False
    # 중력이 상, 하로 작용하면 열 연산을 수행해야 하므로 행렬 전치.
    if direction == 0 or direction == 2:
        array = transpose(array)
    # 중력이 상, 좌로 작용하면 거꾸로 연산해야 하므로 플래그 활성화.
    if direction == 0 or direction == 3:
        use_reverse = True

    # 행/열별로 연산 수행
    for r in range(N):
        # 임시 버퍼 초기화
        buffer = []
        # 리스트로 캐스팅하여 튜플 에러 방지
        if use_reverse:
            row = list(array[r][::-1])
        else:
            row = list(array[r])

        # 병합 플래그. 현재 버퍼에 들어가 있는 최신값이 이미 합쳐진 값인지 체크.
        merge_flag = True
        for _ in range(N):
            # 값 뽑고...
            val = row.pop()
            # 0이면 무시
            if val == 0:
                continue
            # 버퍼에 값이 있고, 첫번째 값이 방금 뽑은 값과 동일하며, 병합이 가능한 경우
            if buffer and val == buffer[0] and merge_flag:
                # 버퍼 첫번째 값 2 곱해주고, 병합 플래그 반전. 뽑은 값은 버려도 무관.
                buffer[0] *= 2
                merge_flag = False
            else:
                # 아니면 그냐 버퍼에 넣어주고, 병합 플래그 반전.
                buffer = [val] + buffer
                merge_flag = True

        # 제로 패딩 설정
        zeroes = [0] * (N - len(buffer))
        # 상, 좌의 경우 패딩을 반전 시킨 버퍼 뒤에 붙여줘야함.
        if use_reverse:
            buffer = list(buffer[::-1]) + zeroes
        # 하, 우의 경우 패딩을 앞에 붙여줘야함.
        else:
            buffer = zeroes + buffer
        # 연산 대상이 되는 행을 버퍼로 교체.
        array[r] = buffer
    # 앞에서 전치시켰으면 다시 전치시켜주기.
    if direction == 0 or direction == 2:
        array = transpose(array)
    return array


# 0~3까지 방향 인덱스를 가지고 길이가 5인 중복있는 순열 생성하는 백트래커 함수
def backtrack(lst=[], step=0):
    global answer
    if step == 5:
        # 그대로 가져다 쓰면 대참사 벌어짐.
        temp = [row.copy() for row in arr]
        for i in range(5):
            temp = gravitate(temp, lst[i])
        maximum = max([max(row) for row in temp])
        if maximum > answer:
            answer = maximum
        return

    for i in range(4):
        backtrack(lst+[i], step+1)


if __name__ == '__main__':
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]
    answer = 0
    backtrack()
    print(answer)
