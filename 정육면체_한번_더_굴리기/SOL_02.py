""" 정육면체 한번 더 굴리기 / 20260921 / 체감 난이도: S1
소요 시간 24분 / 시도 1회 / 실행 시간 57ms (코드트리) / 메모리 17MB (코드트리)

함수화 안하는 연습 해보기.
하드코딩은 여전히 싫다만, 주사위 굴릴 때는 이거만한게 없는것 같다.
이번엔 1번 인덱스부터 받아서 헷갈릴 여지를 아예 주지 않았다.
"""
from collections import deque

if __name__ == '__main__':
    N, M = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # 주사위 초기화 (X, 상, 남, 동, 서, 북, 하)
    dice = [0, 1, 2, 3, 4, 5, 6]

    # 주사위 초기 위치와 이동 방향 설정
    r, c, d = 0, 0, 0

    # 점수 초기화
    score = 0

    # M번 반복
    for _ in range(M):

        # TODO: 현재 이동 방향대로 이동했을 때, 격자 벗어난다면 이동 방향 반전
        if not(0 <= r + directions[d][0] < N and 0 <= c + directions[d][1] < N):
            d = (d + 2) % 4

        # TODO: 현재 방향대로 주사위 이동 (X, 상, 남, 동, 서, 북, 하)
        if d == 0:
            temp = [0, dice[4], dice[2], dice[1], dice[6], dice[5], dice[3]]
        elif d == 1:
            temp = [0, dice[5], dice[1], dice[3], dice[4], dice[6], dice[2]]
        elif d == 2:
            temp = [0, dice[3], dice[2], dice[6], dice[1], dice[5], dice[4]]
        else:
            temp = [0, dice[2], dice[6], dice[3], dice[4], dice[1], dice[5]]
        dice = temp

        # TODO: 주사위 굴린 후 위치 업데이트
        r += directions[d][0]
        c += directions[d][1]

        # TODO: 현재 주사위 놓인 칸에 있는 수와 상하좌우로 뻗어나가는 모든 동일 수의 합 구하기
        que = deque()
        que.append((r, c))

        vst = [[0] * N for _ in range(N)]
        vst[r][c] = 1

        val = board[r][c]
        score += val

        while que:
            cr, cc = que.popleft()
            for cd in range(4):
                nr = cr + directions[cd][0]
                nc = cc + directions[cd][1]
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if vst[nr][nc] != 0:
                    continue
                if board[nr][nc] != val:
                    continue
                score += val
                vst[nr][nc] = 1
                que.append((nr, nc))

        # TODO: 주사위 이동 방향 조정
        #   주사위의 아랫면 > 보드 숫자
        #       이동 방향 90도 시계방향 회전
        #   주사위의 아랫면 == 보드 숫자
        #       이동 방향 변동 없음
        #   주사위의 아랫면 < 보드 숫자
        #       이동 방향 90도 반시계방향 회전
        if dice[-1] > board[r][c]:
            d = (d + 1) % 4
        elif dice[-1] < board[r][c]:
            d = (d - 1) % 4

    # 정답 출력
    print(score)


"""정육면체 한번 더 굴리기 / 20260828 / 체감 난이도: S1
소요 시간 2시간 / 시도 2회 / 실행 시간 73ms (코드트리) / 메모리 16MB (코드트리)

[구상]
    - 드래곤 커브 후유증으로 문제 제대로 읽는데만 30분 넘게 썼다...
    - 주사위 회전은 예전에 비슷한 문제를 경험해봤기에, 구현 방안을 떠올리는건 어렵지 않았다.
    - 그리고 문제가 나름 착한게, 주사위 자체가 회전하는게 아니라 구르는 방향만 바뀌기 때문에 구현이 편리하다.
    - 주사위 굴렸을 때 눈이 변하는 과정은 함수화하여 구현하기로 했다.
    - 보드 값과 주사위 값에 따른 방향 전환은 실행부에서, 점수 계산은 BFS로 해야겠다고 생각했다.
    - 시작할 때 점수 측정하는지도 고민해봤는데, 이동 후에 점수를 계산한다고 명시되어 있어서 건너 뛰었다.

[구현]
    - 하지만 주사위 배열을 0~5로 길이에 딱 맞게 지정했던게 오히려 발목을 잡았다.
        - 0~7로 잡아서 주사위 눈과 배열 인덱스를 동일하게 맞춰주는게 헷갈리지 않고 편하다.
        - 회전할 때 인덱스 바뀌는 과정을 전부 손으로 그리고 들어가긴 했다만...
            - 집중 하나도 안되는 상태에서 억지로 참고 하다보니 실수가 들어갔다.
    - 그래도 한가지 잘한게 있다면 주사위 판을 벗어날 때에 대한 예외처리를 올바르게 한 것이다.
        - 문제상황에 맞춰 예외처리의 순서도 조정해줘야 한다는 것을 이제는 꽤 여러번 경험했다.
            - 이 사소한 디테일 차이로 큰 고민없이 정답을 내는 사람이 있는가하면,
            - 예외처리를 하긴 했는데 실행순서가 달라서 별도로 디버깅을 해줘야 하는 사람들이 있다. (나임)
        - 이번 문제에서 주사위는 항상 먼저 이동하고, 그 이후에 방향을 변경한다.
        - 따라서 "이동 전에" 예외처리를 단 한번만 해주면, 다른 곳에서 이게 문제가 될 일이 없는 것이다.

[디버깅]
    - 오픈 테케가 다 맞는걸 확인하고 제출했는데, 오답이 나왔다.
    - 그러면 회전 함수, 방향 변경 처리, 점수 계산 이 셋 중 하나에서 문제가 생겼다는 것이기에 순서대로 디버깅을 진행했다.
        - 제일 수상한 회전 함수부터 살펴봤는데, 일단 내가 오타를 내거나 실수를 했다면 주사위를 무한히 굴릴 때 중복 눈이 나올거라고 가정했다.
        - 그런데 하필 틀려도 교묘하게 틀려서 중복 눈이 안나왔고... 그래서 방향, 점수 계산 파트까지 다 보고 다시 돌아왔다.
        - 이번엔 손 필기로 구상한 파트를 돌아봤는데, 내 드래곤 커브 풀이를 곱씹으며 도파민에 절여진 채로 구상하다가 잘못 적은 내용을 발견했다.
        - 그래서 처음부터 다시 주사위 굴리는 파트의 손설계를 진행했고, 제대로 굴러가는걸 확인하고 제출했다.

[후기]
    - 원래라면 1시간 정도 걸려서 풀었을 문제를 무려 2시간을 잡고 있었다.
    - 기출 풀면서 이런저런 실패를 맛보면서 경험을 누적하는건 나도 좋다고 생각하는데, 살다 살다 문제를 잘 풀어서 실패하는 경험을 하게 될줄은 몰랐다.
    - 더 중요한건, 긴장을 끈을 놓으니 실수가 늘어나고, 실수가 늘어나니 디버깅하다가 체력까지 삭제되는 기이한 경험을 하게 되었다.
    - 실제 시험도 크게 다르지 않을거라는 생각이 들었다.
        - 각자 다른 난이도의 서브 태스크가 여러개 있는 상황에서, 오늘같이 하나 해결했다고 과하게 흥분했다면 어떤 결과가 나올까?
        - 아마 평소라면 쉽게 풀었을 파트에서 되려 실수하고, 체력까지 크게 소모하는 일이 발생할지도 모른다.
    - 나대지 말자.
"""
from collections import deque


def move(cr, cc, cd):
    # 현재 위치와 이동 방향을 받아서 주사위를 굴린 후 상태, 다음 위치 반환
    temp = dice.copy()
    dr, dc = directions[cd]
    if cd == 0:
        dice[4] = temp[0]
        dice[5] = temp[4]
        dice[1] = temp[5]
        dice[0] = temp[1]
    elif cd == 1:
        dice[2] = temp[0]
        dice[5] = temp[2]
        dice[3] = temp[5]
        dice[0] = temp[3]
    elif cd == 2:
        dice[1] = temp[0]
        dice[5] = temp[1]
        dice[4] = temp[5]
        dice[0] = temp[4]
    elif cd == 3:
        dice[0] = temp[2]
        dice[3] = temp[0]
        dice[5] = temp[3]
        dice[2] = temp[5]
    return cr+dr, cc+dc


def bfs(row, col):
    # 점수 계산용 BFS 함수
    vst = [[0] * N for _ in range(N)]
    vst[row][col] = 1
    que = deque()
    que.append((row, col))
    target = arr[row][col]
    # 현 위치 값도 생각해야 하기에
    # 카운트는 1부터 시작한다.
    count = 1

    while que:
        cr, cc = que.popleft()
        for dr, dc in directions:
            nr, nc = cr+dr, cc+dc
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if arr[nr][nc] != target:
                continue
            if vst[nr][nc] != 0:
                continue
            # 가보지 않은 위치에 타겟값이 발견되면
            # 카운트 1 증가 시키고 탐색 진행
            vst[nr][nc] = 1
            que.append((nr, nc))
            count += 1
    # 타겟값 * 카운트가 이번 점수다.
    return int(target * count)


if __name__ == '__main__':
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    # 상, 남, 동, 서, 북, 하
    dice = [1, 2, 3, 4, 5, 6]
    # 북, 동, 남, 서
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    # 현재 행/열 좌표
    cr, cc, cd = 0, 0, 1

    # 전체 점수
    total_score = 0
    # M번 반복
    for _ in range(M):
        # 격자 탈출 체크, 벗어난다면 방향 반전
        dr, dc = directions[cd]
        if not(0 <= cr+dr < N and 0 <= cc+dc < N):
            cd = (cd+2) % 4
        # 주사위 움직이고 현재 위치 업데이트
        cr, cc = move(cr, cc, cd)
        # 현재 위치에서 점수 계산
        total_score += bfs(cr, cc)
        # 아랫면 < 보드: 반시계
        if dice[5] < arr[cr][cc]:
            cd = (cd-1) % 4
        # 아랫면 > 보드: 시계
        elif dice[5] > arr[cr][cc]:
            cd = (cd+1) % 4
        else:
            continue
    print(total_score)
