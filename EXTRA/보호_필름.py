""" 보호 필름 / 20261007 / 체감 난이도: G5
소요 시간 28분 / 시도 1회 / 실행 시간 2,879ms (SWEA) / 메모리 93,808KB (SWEA)

엥? 백트래킹? 암튼 그냥 저냥 할만한 문제다.
"""


def check(arr):
    for cc in range(C):
        count = 0
        buffer = []
        for cr in range(R):
            if not buffer:
                buffer.append(arr[cr][cc])
                count = max(count, len(buffer))
                continue
            if arr[cr][cc] == buffer[-1]:
                buffer.append(arr[cr][cc])
                count = max(count, len(buffer))
            else:
                buffer = [arr[cr][cc]]
        if count < K:
            return False
    return True


def backtrack(arr, start=0, step=0):
    global answer
    if step >= answer:
        return

    if step == K:
        if step < answer:
            answer = step
        return

    if check(arr):
        if step < answer:
            answer = step

    for i in range(start, R):
        temp = [x[:] for x in arr]
        temp[i] = [0] * C
        backtrack(temp, i+1, step+1)
        temp[i] = [1] * C
        backtrack(temp, i+1, step+1)


if __name__ == '__main__':
    TEST_CASE = int(input())
    for TC in range(1, TEST_CASE+1):
        print(f'#{TC}', end=' ')

        R, C, K = map(int, input().split())
        film = [list(map(int, input().split())) for _ in range(R)]

        answer = int(1e9)
        backtrack(film)
        print(answer)
