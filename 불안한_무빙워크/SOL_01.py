""" 불안한_무빙워크 / 20260823 / 체감 난이도: B1
소요 시간 INF / 시도 INF / 실행 시간 106ms (코드트리) / 메모리 19MB (코드트리)

[구상]
    - 회수야 제발 문제 좀 잘 읽자!!!!
    - 첫 풀이 당시에 거의 30분을 구상에 할애했는데, 처음부터 문제를 잘못 읽은게 모든 일의 원흉이었다.
    - 무빙워크 회전 이후, 사람들이 무조건 "한칸"을 이동한다고 문제에 명확하게 나와있다.
        - 그런데 나는 n번째 칸에 도착하는 순간 무빙워크를 나가는 샘플 이미지를 보고 '아 끝까지 가는구나~' 하고 있었다.
        - 즉, 사람이 무빙워크에서 움직이기 시작하면 갈 수 있는 최대한 간다고 이해한 상태였다.
    - 주말에 갑자기 생각나서 문제를 풀려고 앉았는데, 문제를 읽자마자 내가 뭘 잘못 이해한건지 바로 알아챘다.
        - 억울분통맨이 되어 머리를 쥐어 뜯으며 고함을 내질렀다.

[구현]
    - 문제 제대로 이해하고 한 15분만에 푼 것 같다.
    - 첫 시도를 할 때도 무빙워크를 보고 바로 deque 모듈의 rotate 함수가 떠올랐다.
    - 회전, 이동, 사람 추가를 함수로 나누어 단계별로 구현했다.
    - 또한, 첫 구현처럼 주어진 칸을 불안정화 시키는 함수를 전역변수를 활용하여 만들었다.
        - 덕분에 칸의 안정도가 0이 되었는지 실행부에서 일일히 체크할 필요가 없어졌다. 굳!

[디버깅]
    - 디버깅은 따로 하지 않았다. 한방에 맞았기 때문에 더욱 더 원통하고 분했다.

[후기]
    - 문제를 잘 읽자! 문제를 잘 읽자! 문제를 잘 읽자!
"""
from collections import deque

def destabilize(loc):
    # 불안정한 타일 개수를 전역변수화
    # 안정도를 줄이려고 하는 타일의 현재 안정도가 1일때 0으로 만들고,
    # 불안정 카운트를 1 올린다.
    global unstable
    if conveyer[loc] == 1:
        unstable += 1
    conveyer[loc] -= 1

def rotate():
    # 나 돌아가유~
    # N-1번째 칸은 바로 탈출이라 항상 0으로 바꿔줘야 한다.
    conveyer.rotate()
    standing.rotate()
    standing[N-1] = 0

def forward(loc):
    # 주어진 위치에 있는 사람 한칸 앞으로 이동 시키기.
    if conveyer[loc+1] == 0:
        return
    if standing[loc+1] == 1:
        return
    # 마지막 칸이면 자동 탈출
    if loc+1 != N-1:
        standing[loc+1] = 1
    standing[loc] = 0
    destabilize(loc+1)

def add():
    # 0번째 칸에 사람을 추가한다.
    if conveyer[0] == 0:
        return
    if standing[0] == 1:
        return
    destabilize(0)
    standing[0] = 1


if __name__ == '__main__':
    N, K = map(int, input().split())

    # 반복 횟수, 불안정 카운트, 무빙워크 현황, 사람 현황
    # 알파벳 글자수가 딱 맞아 떨어져서 기분이 아주 좋다.
    repeated = 0
    unstable = 0
    conveyer = deque(map(int, input().split()))
    standing = deque([0] * N)

    # 불안정 카운트가 제한치보다 낮은 동안 반복
    while unstable < K:
        repeated += 1
        # 회전
        rotate()
        # 앞사람부터 이동
        for loc in range(N-1, -1, -1):
            if standing[loc] == 1:
                forward(loc)
        # 사람 추가
        add()
    # 정답 출력
    print(repeated)
