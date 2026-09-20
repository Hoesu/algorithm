""" 연산자 배치하기 / 20260919 / 체감 난이도: S1
소요 시간 17분 / 시도 2회 / 실행 시간 68ms (코드트리) / 메모리 18MB (코드트리)

백트래킹 너무 오랜만이라서 실수 한번 했다.
가지치기는 할 수 없어도 최소한의 시도를 할 수 있는 방법을 생각해야 했다.
"""


def backtrack(num, add_cnt=0, sub_cnt=0, mul_cnt=0, step=0):
    if add_cnt > add:
        return
    if sub_cnt > sub:
        return
    if mul_cnt > mul:
        return

    global minimum, maximum
    if step == N-1:
        if num < minimum:
            minimum = num
        if num > maximum:
            maximum = num
        return

    backtrack(num+numbers[step+1], add_cnt+1, sub_cnt, mul_cnt, step+1)
    backtrack(num-numbers[step+1], add_cnt, sub_cnt+1, mul_cnt, step+1)
    backtrack(num*numbers[step+1], add_cnt, sub_cnt, mul_cnt+1, step+1)


if __name__ == '__main__':
    N = int(input())
    numbers = list(map(int, input().split()))
    add, sub, mul = map(int, input().split())

    minimum = int(1e9)
    maximum = -int(1e9)
    backtrack(num=numbers[0])
    print(minimum, maximum)


""" 연산자 배치하기 / 20260822 / 체감 난이도: S1
소요 시간 ??? / 시도 2회 / 실행 시간 87ms (코드트리) / 메모리 19MB (코드트리)
"""


def backtrack(lst=[], step=0, np=0, nm=0, ng=0):
    # 종료 조건 1
    if np > n_plus or nm > n_minus or ng > n_mult:
        return

    # 종료 조건 2
    global max_value
    global min_value
    if step == N-1:
        result = calc(lst)
        if result > max_value:
            max_value = result
        if result < min_value:
            min_value = result
        return

    backtrack(lst+[0], step+1, np+1, nm, ng)
    backtrack(lst+[1], step+1, np, nm+1, ng)
    backtrack(lst+[2], step+1, np, nm, ng+1)


def calc(operator_lst):
    res = num_lst[0]
    for i in range(N-1):
        op = operator_lst[i]
        if op == 0:
            res += num_lst[i+1]
        elif op == 1:
            res -= num_lst[i+1]
        else:
            res *= num_lst[i+1]
    return res


if __name__ == '__main__':
    N = int(input())
    num_lst = list(map(int, input().split()))
    n_plus, n_minus, n_mult = map(int, input().split())

    min_value = 1000000000
    max_value = -1000000000
    backtrack()
    print(f'{min_value} {max_value}')
