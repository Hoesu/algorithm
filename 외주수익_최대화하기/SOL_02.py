""" 외주 수익 최대화하기 / 20260919 / 체감 난이도: S1
소요 시간 21분 / 시도 1회 / 실행 시간 81ms (코드트리) / 메모리 19MB (코드트리)

아 이건 예전 버전이 훨 나은데.. 깍두기 문제들 빨리 치우고 딴거 풀고 싶어서 방만하게 코드 짜버렸다.
이러지 맙시다.
"""


def backtrack(time=0, wage=0, step=0):
    global max_earning
    if step == N:
        if wage > max_earning:
            max_earning = wage
        return

    time = max(0, time-1)
    if time == 0 and step+jobs[step][0] <= N:
        backtrack(time+jobs[step][0], wage+jobs[step][1], step+1)
    backtrack(time, wage, step+1)


if __name__ == '__main__':
    N = int(input())
    jobs = [list(map(int, input().split())) for _ in range(N)]
    max_earning = 0
    backtrack()
    print(max_earning)


""" 외주 수익 최대화하기 / 20260823 / 체감 난이도: S1
소요 시간 ??? / 시도 2회 / 실행 시간 82ms (코드트리) / 메모리 19MB (코드트리)
"""


def backtrack(step=0, day=0, pay=0):
    # 종료 조건 1
    if day > N:
        return

    # 종료 조건 2
    global max_pay
    if step == N:
        if pay > max_pay:
            max_pay = pay
        return

    job_day = jobs[step][0]
    job_pay = jobs[step][1]

    if day > step:
        backtrack(step+1, day, pay)
    else:
        backtrack(step+1, day+1, pay)
        backtrack(step+1, day+job_day, pay+job_pay)


if __name__ == '__main__':
    N = int(input())
    jobs = []
    for _ in range(N):
        T, P = map(int, input().split())
        jobs.append((T, P))

    max_pay = 0
    backtrack()
    print(max_pay)
