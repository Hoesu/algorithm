""" 택배 하차 / 20260929 / 체감 난이도: G5
소요 시간 1시간 / 시도 1회 / 실행 시간 181ms (코드트리) / 메모리 23MB (코드트리)

[구상]
    - 몇기가 풀었던 문제인지 모르겠지만, 굉장히 꿀 빨았다고 할 수 있겠다. (선배로 인정 안하겠음 ㅋㅋ)
        - 미지의 공간 탈출, 메두사 등을 생각하며 이 문제를 보니까 살짝 현타가 왔다.
        - 결국 해당 분기에 뽑으려고 계획한 최종 인원 수가 우리의 운명을 좌우하는 것인가...
    - 단계별 절차만 잘 따르면 특별한 엣지가 존재할 수 없고, 기믹도 아주 기본적인 중력 밖에 없었다.
    - 심지어 격자 벗어나지 않는다는 조건도 보장해줬는데, 이게 맞나 싶다. 나는 평소 같은 진흙탕 싸움을 원한다고.
    - 풀이를 시작하기 전 스스로에게 던졌던 몇가지 질문들은 다음과 같다:
        - 클래스를 사용하면 인생이 쉬워지는가? => 진지하게 네.
        - 왼쪽, 오른쪽 비어있는 애들 찾을때 그냥 무식하게 순회하며 SET에 넣을까? => 최적화 자아 버려라. 네.
        - 택배 빼고 굳이 중력 적용해야 하나? 달라지는게 있나? => 이딴걸 질문이라고 하심? 네.
    - 결국 중력 적용 과정에서 인덱스 실수만 안하면 무조건 풀리는 문제라고 볼 수 있다.

[구현]
    - 그냥... 열심히 주석 설계하고 열심히 구현하니까 40분쯤 구현이 끝났다.
    - 딱 한가지 구상 단계에서 놓친 것이 있다면, 왼쪽, 오른쪽 비어있는 애들 스캔할 때 다른 택배에 막혀있는 애들을 상정하지 못했다.
        - 그래서 왼쪽, 오른쪽 노출된 택배에 대해 sum 체크하는 인스턴스 메서드로 해결했다.

[디버깅]
    - 커스텀 프린트로 찍어보기도 굉장히 쉬운 문제였다.
    - 격자 경계면에서 인덱스 안전 장치 잘 작동하는지 소형 테케 가지고 검증했다.

[후기]
    - 회전에선 항상 뚜드려 맞지만, 중력은 어떤 형태로 나오든 항상 풀긴 풀었다.
    - 심지어 어제 2차원 테트리스 N차 풀이해서 유독 빨리 풀이할 수 있었던 것 같다.
    - 자만은 하지 말자.
"""


def debug(msg):
    print()
    print(msg)
    for row in board:
        print(*row)
    print('-------')


class Box:
    def __init__(self, k, h, w, c):
        self.idx = k
        self.r = 0
        self.c = c
        self.h = h
        self.w = w

    def imprint(self):
        for cr in range(self.r, self.r + self.h):
            for cc in range(self.c, self.c + self.w):
                board[cr][cc] = self.idx

    def unprint(self):
        for cr in range(self.r, self.r + self.h):
            for cc in range(self.c, self.c + self.w):
                board[cr][cc] = 0

    def midair(self):
        if not(self.r + self.h < N):
            return False
        check = sum(board[self.r+self.h][self.c:self.c+self.w])
        if check == 0:
            return True
        return False

    def left_empty(self):
        if self.c == 0:
            return True
        check_sum = 0
        for cr in range(self.r, self.r+self.h):
            check_sum += sum(board[cr][:self.c])
        if check_sum > 0:
            return False
        return True

    def right_empty(self):
        if self.c + self.w == N:
            return True
        check_sum = 0
        for cr in range(self.r, self.r+self.h):
            check_sum += sum(board[cr][self.c+self.w:])
        if check_sum > 0:
            return False
        return True

    def gravitate(self):
        max_row = self.r + self.h
        all_col = list(range(self.c, self.c+self.w))
        while max_row < N and sum(board[max_row][x] for x in all_col) == 0:
            max_row += 1
        self.r = max_row - self.h


if __name__ == '__main__':
    DEBUG_MODE = False
    N, M = map(int, input().split())
    board = [[0] * N for _ in range(N)]

    answer = []
    boxes = dict()
    for _ in range(M):
        K, H, W, C = map(int, input().split())
        box = Box(K, H, W, C-1)
        box.gravitate()
        box.imprint()
        boxes[K] = box

    if DEBUG_MODE:
        debug(f'INITIAL STATE: ALL BOXES ARE PLACED.')

    candidates = set()
    while boxes:
        # TODO 1: 왼쪽 스캔
        candidates.clear()
        for r in range(N):
            for c in range(N):
                if board[r][c] > 0:
                    if board[r][c] in candidates:
                        break
                    if not boxes[board[r][c]].left_empty():
                        break
                    candidates.add(board[r][c])
                    break

        # TODO 2: 택배 ID 조회 후 가장 값이 작은 박스 추출
        #   추출한 택배 박스 ID는 정답 리스트에 추가
        to_remove = min(candidates)
        answer.append(to_remove)
        boxes[to_remove].unprint()
        boxes.pop(to_remove)

        # TODO 3: 모든 박스 중력 적용
        for key in boxes:
            if boxes[key].midair():
                boxes[key].unprint()
                boxes[key].gravitate()
                boxes[key].imprint()

        if DEBUG_MODE:
            print(to_remove)
            debug(f'LEFT.')

        # TODO 3: 오른쪽 스캔
        candidates.clear()
        for r in range(N):
            for c in range(N-1, -1, -1):
                if board[r][c] > 0:
                    if board[r][c] in candidates:
                        break
                    if not boxes[board[r][c]].right_empty():
                        break
                    candidates.add(board[r][c])
                    break

        # TODO 4: 택배 ID 조회 후 가장 값이 작은 박스 추출
        #   추출한 택배 박스 ID는 정답 리스트에 추가
        to_remove = min(candidates)
        answer.append(to_remove)
        boxes[to_remove].unprint()
        boxes.pop(to_remove)

        # TODO 5: 모든 박스 중력 적용
        for key in boxes:
            if boxes[key].midair():
                boxes[key].unprint()
                boxes[key].gravitate()
                boxes[key].imprint()

        if DEBUG_MODE:
            print(to_remove)
            debug(f'RIGHT.')

    # 정답 출력
    for num in answer:
        print(num)
