""" 2차원 테트리스 / 20260902 / 체감 난이도: G2
소요 시간 2시간 7분 / 시도 1회 / 실행 시간 434ms (코드트리) / 메모리 24MB (코드트리)

[구상]
    - 슬슬 문제 체급이 올라가는게 체감 된다. 이번 문제 힘들었다.
    - 쉽게 푸는 것을 가장 좋아하기 때문에 뭔가 좋은 수가 없나 생각하면서 문제를 읽었다.
        - 아무리 봐도 빡구현 말고는 대책이 떠오르지 않았다...
    - 일단 핵심 사안 위주로 체크했다.
        - 핵심 1) 테트리스 블럭이 내려올 때, 모래처럼 쌓이는 구조가 아니라 단위 블럭 형태를 유지해야 한다.
        - 핵심 2) 행/열 체크를 통해 꽉찬 줄을 매 턴마다 파악해서 삭제해줘야 한다.
        - 핵심 3) 연한 칸(buffer zone 역할)으로 블럭이 흘러넘치면 그만큼 슬라이딩을 해줘야 한다.
        - 핵심 4) 꽉찬 줄 제거를 통한 점수 계산이 항상 우선시 되어야 한다.
        - 핵심 5) 빨간 배열, 노란 배열이 각각 다르게 작동하기 때문에 연산 방향을 신경써야 한다.
        - 한 문제에 핵심이 이렇게 많아도 되는건가요? 허허
    - 이번 문제를 풀면서 키보드를 정말 빨리 잡았는데, 어제부터 시작한 TODO의 활용법을 여러 방면에서 테스트 해보고 싶었다.
        - 경험상 빡구현 문제들은 풀이 도중 필요에 의해 추가할 기능들이 발생한다.
        - 그렇기 때문에 손설계 단계를 오래 가져간다고 하더라도, 구현 도중에 계획을 바꾸는 일이 빈번했다.
        - 그렇다면 차라리 문제를 단계 별로 나눠서 오름차순으로 구현을 진행하고, 중간에 필요해지는 내용은 TODO로 별도로 기록하면 어떨까 싶었다.

[구현]
    - 풀이 끝나고 보니까 뭐.. 그냥 하드코딩 수준이다.
    - 가장 먼저 시작한 부분은 테트리스 블럭을 규칙에 맞게 쌓는 일이었다.
        - 줄 삭제 / 버퍼 비우기를 시도하기 전에, 일단 블럭부터 제대로 쌓이는지 체크하기 위함이었다.
        - 이 과정에서 블럭이 원 형태를 잘 유지하면서도 가장 아래로 떨어질 수 있는 위치를 찾는 함수를 구현하였다.
        - 열 방향 이동 시 3번, 행 방향 이동 시 2번 블럭의 케이스를 특별히 신경 썼다. (2칸 기준으로 체크 해야함)
        - 구현을 마친 뒤, 별도의 스크립트를 파서 단위 테스트를 진행했다. 실제로 테트리스 하는 기분이라 재밌었다.
        - 검증할 때는 각 블럭이 차지한 칸을 1, 2, 3으로 타입에 맞게 입력을 줘서 가시성을 높였다. 나중에 1로 롤백함.
    - 다음엔 꽉찬 행 체크, 버퍼 빌 때까지 배열 밀어내기를 함께 구현했다.
        - 사실 clear 함수 하나만 잘 구현하면 다 같은 원리로 작동한다.
        - 외부에서 빨간 배열, 노란 배열에서 제거할 열/행을 미리 찾아내서 클리어 함수에게는 자기 할일만 전달하도록 했다.
            - 꽉찬 배열 인덱스 리스트는 빼뒀다가 그 길이를 점수에 추가해줬다. (버림)
            - 유지할 배열 인덱스 리스트는 클리어 함수에 전달하여 배열을 재구성하게 만들었다.
            - 이때 그냥 shallow copy 써도 되지 않나 싶긴 했는데, 혹시 몰라 일단은 딥카피로 했다.

[디버깅]
    - 앞선 시간에 동은 프로가 한말에 전적으로 동의한다. 검증도 문제에 맞춰서 해야한다.
    - 이번 문제는 대단한 엣지 케이스가 존재하는 타입은 아니다.
    - 대신에 한 사이클이 정상적으로 작동하는지만 체크하면, 나머지는 믿고 맡기는 타입이라고 해야하나.
        - 이번 문제에서 한 사이클이란, 테트리스 블럭 설치, 꽉 찬 줄 제거, 그리고 버퍼 비우기까지라고 생각한다.
        - 오픈 테케 2번에서 이 모든 과정이 수행되므로, 정답이 제대로 나오는 것을 확인하고 안심했다.

[후기]
    - 구상 부분에서 언급한 TODO의 활용 방식에 대한 의견이 반반이다.
    - 실수를 줄여줘서 좋긴한데, 부족한 구상을 임기응변으로 채우니까 구현 과정이 길고 복잡해진다.
    - 결국 손설계와 주석 설계를 조화롭게 활용하는 스킬이 중요한 것 같다.
"""


# TODO 2: 정보 받아서 axis 주면 가장 마지막 빈칸 알려주는 함수
def find_space(points, axis):
    if axis == 0:
        best = 5
        for c in points:
            for r in range(6):
                if Y[r][c] != 0:
                    if r-1 < best:
                        best = r-1
                    break
    else:
        best = 5
        for r in points:
            for c in range(6):
                if R[r][c] != 0:
                    if c-1 < best:
                        best = c-1
                    break
    return best


# TODO 3: 꽉찬 칸 제거용 함수
def clear(lines, axis):
    global Y, R
    keep = []
    zero = []
    if axis == 0:
        for r in lines:
            keep.append(Y[r].copy())
        for _ in range(6 - len(lines)):
            zero.append([0] * 4)
        result = zero + keep
        Y = result
    else:
        for c in lines:
            keep.append([row[c] for row in R])
        for _ in range(6 - len(lines)):
            zero.append([0] * 4)
        result = zero + keep
        R = [list(col) for col in zip(*result)]


# TODO 4: 오버한 칸 제거용 함수
def push_by(step, axis):
    if step == 2:
        keep_lines = [0, 1, 2, 3]
        clear(keep_lines, axis)
    if step == 1:
        keep_lines = [0, 1, 2, 3, 4]
        clear(keep_lines, axis)


# TODO 1: 테트리스 블럭 입력 들어오면 쌓아주는 함수 구현
def add_block(x, y, t, axis=0):
    # TODO 1.0: 점수 전역 변수 선언
    global score

    # TODO 1.1
    #  axis=0 이면 행 방향 이동, 노란색
    #   타입 1, 3은 아래 행만 체크, 타입 2는 아래 행 두개 동시 체크
    #   체크한 내용에 맞춰서 알맞은 배열에 값 붙여넣기 (TEST 완료)
    if axis == 0 and t == 1:
        nx, ny = find_space([y], axis=0), y
        Y[nx][ny] = 1
    elif axis == 0 and t == 2:
        nx, ny = find_space([y, y+1], axis=0), y
        Y[nx][ny], Y[nx][ny+1] = 1, 1
    elif axis == 0 and t == 3:
        nx, ny = find_space([y], axis=0)-1, y
        Y[nx][ny], Y[nx+1][ny] = 1, 1

    # TODO 1.2
    #  axis=1 이면 열 방향 이동, 빨간색
    #   타입 1, 2는 오른쪽 열만 체크, 타입 3은 오른쪽 열 두개 동시 체크
    #   체크한 내용에 맞춰서 알맞은 배열에 값 붙여넣기 (TEST 완료)
    elif axis == 1 and t == 1:
        nx, ny = x, find_space([x], axis=1)
        R[nx][ny] = 1
    elif axis == 1 and t == 2:
        nx, ny = x, find_space([x], axis=1)-1
        R[nx][ny], R[nx][ny+1] = 1, 1
    else:
        nx, ny = x, find_space([x, x+1], axis=1)
        R[nx][ny], R[nx+1][ny] = 1, 1

    # TODO 1.3
    #  axis=0 꽉찬 행 체크 (테스트 완료)
    if axis == 0:
        skip_rows = []
        keep_rows = []
        for r in range(6):
            if sum(Y[r]) == 4:
                skip_rows.append(r)
            else:
                keep_rows.append(r)
        if keep_rows:
            clear(keep_rows, axis=0)
            score += len(skip_rows)

    # TODO 1.4
    #  axis=1 꽉찬 열 체크 (테스트 완료)
    else:
        skip_cols = []
        keep_cols = []
        for c in range(6):
            if sum([row[c] for row in R]) == 4:
                skip_cols.append(c)
            else:
                keep_cols.append(c)
        if skip_cols:
            clear(keep_cols, axis=1)
            score += len(skip_cols)

    # TODO 1.5
    #  axis=0 Y 0~1행 검사 (테스트 완료)
    if axis == 0:
        sum0 = sum(Y[0])
        sum1 = sum(Y[1])
        if sum0 > 0:
            push_by(2, axis=0)
        elif sum1 > 0:
            push_by(1, axis=0)

    # TODO 1.6
    #  axis=1 R 0~1열 검사 (테스트 완료)
    else:
        sum0 = sum([row[0] for row in R])
        sum1 = sum([row[1] for row in R])
        if sum0 > 0:
            push_by(2, axis=1)
        elif sum1 > 0:
            push_by(1, axis=1)


if __name__ == '__main__':
    score = 0
    K = int(input())
    R = [[0] * 6 for _ in range(4)]
    Y = [[0] * 4 for _ in range(6)]

    for asd in range(K):
        t, x, y = map(int, input().split())
        add_block(x, y, t, axis=0)
        add_block(x, y, t, axis=1)

    r_sum = sum(map(sum, R))
    y_sum = sum(map(sum, Y))

    print(score)
    print(r_sum + y_sum)
