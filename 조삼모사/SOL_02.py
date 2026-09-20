""" 조삼모사 / 20260919 / 체감 난이도: S1
소요 시간 18분 / 시도 1회 / 실행 시간 993ms (코드트리) / 메모리 24MB (코드트리)

이번엔 셋 자료형을 써서 해봤다. 굳이 아침 저녁 구분할 필요도 없음.
"""


def get_diff(x: set):
    y = list(members-x)
    x = list(x)
    x_labor = 0
    for i in x:
        for j in x:
            if i == j:
                continue
            x_labor += table[i][j]
    y_labor = 0
    for i in y:
        for j in y:
            if i == j:
                continue
            y_labor += table[i][j]
    return abs(x_labor-y_labor)


def backtrack(group=set(), start=0, step=0):
    global answer
    if step==N//2:
        diff = get_diff(group)
        if diff < answer:
            answer = diff
        return

    for i in range(start, N):
        group.add(i)
        backtrack(group, i+1, step+1)
        group.discard(i)


if __name__ == '__main__':
    N = int(input())
    table = [list(map(int, input().split())) for _ in range(N)]
    members = set(list(range(N)))
    answer = int(1e9)
    backtrack()
    print(answer)


""" 조삼모사 / 20260822 / 체감 난이도: S1
소요 시간 ??? / 시도 2회 / 실행 시간 1664ms (코드트리) / 메모리 55MB (코드트리)
"""


def evening_backtrack(lst=[], start=0, step=0):
    global evening_cost
    if step == 2:
        evening_cost += arr[lst[0]][lst[1]]
        evening_cost += arr[lst[1]][lst[0]]
        return

    for i in range(start, len(evening)):
        evening_backtrack(lst+[evening[i]], i+1, step+1)

def morning_backtrack(lst=[], start=0, step=0):
    global morning_cost
    if step == 2:
        morning_cost += arr[lst[0]][lst[1]]
        morning_cost += arr[lst[1]][lst[0]]
        return

    for i in range(start, len(morning)):
        morning_backtrack(lst+[morning[i]], i+1, step+1)


def outer_backtrack(lst=[], start=0, step=0):
    if step == N//2:
        temp.append(lst.copy())
        return
    for i in range(start, N):
        outer_backtrack(lst+[i], i+1, step+1)


if __name__ == '__main__':
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]
    all = set(range(0, N))

    temp = []
    outer_backtrack()

    min_difficulty = int(1e9)
    for morning in temp:
        evening = list(all - set(morning))
        morning_cost = 0
        morning_backtrack()
        evening_cost = 0
        evening_backtrack()
        diff = abs(morning_cost - evening_cost)

        if diff < min_difficulty:
            min_difficulty = diff
    print(min_difficulty)
