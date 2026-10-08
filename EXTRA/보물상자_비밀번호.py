""" 보물상자 비밀번호 / 20261008 / 체감 난이도: S1
소요 시간 24분 / 시도 1회 / 실행 시간 97ms (코드트리) / 메모리 60,032KB (코드트리)

파이썬이 압도적으로 유리한 문제. 무지성 정렬로 해결 가능하다.
"""
if __name__ == '__main__':
    table = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    TEST_CASE = int(input())
    for TC in range(1, TEST_CASE+1):
        print(f'#{TC}', end=' ')

        N, K = map(int, input().split())
        lst = list(input().strip())

        passwords = set()
        for i in range(N//4):
            for j in range(i, i+N, N//4):
                string = ''
                for k in range(N//4):
                    string += (lst[(j+k) % N])
                passwords.add(string)

        passwords = list(passwords)
        passwords.sort(reverse=True)
        password = passwords[K-1]

        answer = 0
        for i, j in enumerate(range(len(password)-1, -1, -1)):
            if ord(password[j]) >= ord('A'):
                answer += (16 ** i) * table[password[j]]
            else:
                answer += (16 ** i) * int(password[j])
        print(answer)
