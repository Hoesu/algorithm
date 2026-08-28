"""보도블럭 / 20260827 / 체감 난이도: S1
소요 시간 1시간 34분 / 시도 1회 / 실행 시간 67ms (코드트리) / 메모리 17MB (코드트리)

[구상]
    - 구상을 27분 정도 길게 가져갔다. 그림 예제가 상당히 별로였고, 중간에 면담이 잡혀 있어서 집중이 너무 안됐다.
    - 결국 행/열 별로 조건을 제시된 조건을 위배하지 않는 경우의 수를 계산하는 문제였고, 두 가지가 가장 중요한 이슈였다.
        - 진행 중 값이 다른 경우가 등장하면, 어떤 방향으로 경사로를 설치해야 하는가?
        - 이미 경사로가 설치되어 있는 위치에 경사로를 중복으로 설치하지 않는 방법은?
    - 2번 질문에 대한 답은 방문 배열 사용으로 해결하기로 계획을 세웠고, 1번은 구현을 하면서 조금씩 다듬어 나갔다.

[구현]
    - 구현을 하면서 현재 값과 다음 값의 크기 차이에 의해서 경사로 방향이 결정된다는 것을 파악했다.
    - 에.. 사실은 미리 구상 단계에서 파악하고 들어갔어야 했지만, 오늘따라 너무 산만하고 집중이 안됐다. 반성하자.

[디버깅]
    - 최소, 최대 케이스 다 찍어서 돌려봤다.

[후기]
    - 문제가 좀 별로다.
"""


def scan(lst):
    # 조회하는 행, 열마다 길이 N 방문 리스트 초기화
    vst = [0] * N
    # 아무 문제 없이 루프 다 통과하면 통행 가능하다.
    # 단, 연산량이 적은 조건을 우선으로 본다.
    walkable = True

    # 현재 위치와 다음 위치 대조해야 해서 N-1번만 순회.
    for i in range(N-1):
        # 현재 값과 다음 값이 동일하면 넘어가기
        if lst[i] == lst[i+1]:
            continue

        # 현재 값이 다음 값보다 작으면 뒤로 보기, (i-L+1, i+1)
        elif lst[i] < lst[i+1]:
            s, e = i-L+1, i+1
            # 범위 벗어나면 실패!
            if s < 0:
                walkable = False
                break
            # 값 차이가 1 아니면 실패!
            if lst[i+1]-lst[i] != 1:
                walkable = False
                break
            # 경사로 설치할 땅이 고르지 않으면 실패!
            if len(set(lst[s: e])) > 1:
                walkable = False
                break
            # 이미 다른 경사로 들어와 있으면 실패!
            if sum(vst[s: e]) != 0:
                walkable = False
                break
            # 경사로 설치 가능하면 방문배열 체크 후 넘어가기
            for j in range(s, e):
                vst[j] = 1
        # 현재 값이 다음 값보다 크면 앞으로 보기, (i+1, i+L+1)
        else:
            s, e = i+1, i+L+1
            if e > N:
                walkable = False
                break
            if lst[i]-lst[i+1] != 1:
                walkable = False
                break
            if len(set(lst[s: e])) > 1:
                walkable = False
                break
            if sum(vst[s: e]) != 0:
                walkable = False
                break
            for j in range(s, e):
                vst[j] = 1
    return walkable


if __name__ == '__main__':
    N, L = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    answer = 0
    # 행 스캔
    for row in arr:
        if scan(row):
            answer += 1
    # 열 스캔
    for col in zip(*arr):
        if scan(col):
            answer += 1
    print(answer)
