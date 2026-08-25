"""격자 숫자 놀이 / 20260825 / 체감 난이도: S1
소요 시간 1시간 13분 / 시도 3회 / 실행 시간 101ms (코드트리) / 메모리 19MB (코드트리)

[구상]
    - 27분 정도 오래 생각했다. 조건 나름 빡세게 체크했고, 일단 행 연산 케이스부터 pseudo code를 적고 들어갔다.
    - 가장 먼저 한줄에 들어있는 유니크 값을 뽑고, 중복 체크, 우선 순위에 맞춰 분류하는 태스크를 딕셔너리를 사용해 해결하기로 했다.
        - 정확히 어떤 수가 배열에 들어있을지 예측하기 어려운 상황에서, 키 값을 O(1)으로 대조하고, 카운트 증가, 다시 키로 접근하기에 가장 좋은 선택지라고 생각했다.
        - 여태까지 heapq 광신도로 살았기에, 새로운 마음가짐으로 돌아선 나에게 딕셔너리 키, 밸류 정렬은 살짝 어색한 감이 있었다.
            - 그래서 구상 단계에서 테스트 딕셔너리 만들고, 이리저리 가지고 놀면서 람다 함수로 정렬하는 법을 확실하게 하고 들어갔다.
    - 행이 열보다 짧을때 수행해야 하는 연산이 2중 리스트 구조에 알맞지 않다는 생각을 했다.
        - 그런데 문제를 읽다 보니까 행에 대한 연산 하나만 구현해놓고 경우에 따라 행렬을 전치시키면 되겠다는 생각이 들었다.
        - 아이디어는 나쁘지 않은데, 전치에 대한 시간 복잡도가 감이 잡히지 않았다.
        - 그래서 일단 행 연산 구현, 전치 방법 시도 후 시간 터지면 열도 따로 구현하기로 했다.
        - 또한 행렬을 전치하면 C행 R열 값을 참조해야 겠다는 생각을 했다. (디버깅 단계에서 원복해야 한다는 것을 깨달음)

[구현]
    - 0 무시, 길이 100 제한, 시간 100 제한, 딕셔너리 정렬 등 적어뒀던 조건들과 대조하며 천천히 코드를 작성했다.
    - 막 특별한 이슈는 없었다.

[디버깅]
    - 배열이 변화하는 과정을 눈으로 충분히 따라갈만한 수준이어서, 오픈 테케를 가지고 1초부터 100초까지 전부 프린트 찍어서 확인해봤다.
        - R, C가 1부터 시작하는데 입력 받을때 실수한 것을 잡아냈다.
        - 전치해서 열 연산 돌렸으면 다시 전치시켜서 원복시켜야 R행 C열을 제대로 조회 가능한 것을 확인했다.
        - 솔직히 배열 길이 100 넘어가는 경우가 있긴한지 의심스러웠음.
    - 첫번째 제출 실패: 아 시작 체크 제발 까먹지 말자...
    - 두번째 제출 실패: 인덱스 체크하고 초기값 검사해야 하는데 맘 급해서 바로 제출했다가 실수했슴다..

[후기]
    - 요즘 루틴 개발 중인데, 자주하는 실수 리스트도 만들어서 이번 실수 기록했습니다..
    - 문제 풀이마다 위에 주석으로 적어놓고 자기 암시 걸어보기.
    - 종협 프로 코드에서 한가지 배운점: 딕셔너리 매번 새롭게 만들지 말고 clear()로 비워서 재활용하기!
"""


def transpose():
    # 전치 행렬 구하기
    arr_t = []
    for col in zip(*arr):
        arr_t.append(col)
    return arr_t


def process():
    # 행 최대 길이
    max_length = 0
    # 행별 유니크 카운트 저장할 딕셔너리
    table = dict()

    # 행별로 순회
    for r in range(len(arr)):
        # 룩업 테이블 비워주고
        table.clear()

        # 값별로 순회
        for val in arr[r]:
            # 0은 무시합니다.
            if val == 0:
                continue
            # 새로운 수 들어오면 키 생성 후 카운트 +1
            elif val not in table.keys():
                table[val] = 1
            # 기존에 있는 수 들어오면 카운트만 +1
            else:
                table[val] += 1

        # 현재 행 최대 길이 저장
        cur_length = 0
        # 대체할 새로운 행 임시 저장
        new_row = []
        # 딕셔너리 키, 밸류 들고와서 밸류, 키 순으로 정렬합니다.
        for k, v in sorted(table.items(), key=lambda x: (x[1], x[0])):
            new_row.append(k)
            new_row.append(v)
            # 2개씩 더하니까 길이도 2씩 증가
            cur_length += 2

        # 행 길이 100 초과하면 잘라주기
        if len(new_row) > 100:
            new_row = new_row[:100]
        # 최대 행 길이도 100을 넘지 못하게 제어
        if max_length < min(cur_length, 100):
            max_length = min(cur_length, 100)
        # 새롭게 만든 행으로 기존 행 대체
        arr[r] = new_row

    # 최대 행 길이보다 짧은 행들 0으로 패딩 박아주기
    for r in range(len(arr)):
        zeroes = [0] * (max_length - len(arr[r]))
        arr[r] = arr[r] + zeroes


if __name__ == '__main__':
    R, C, K = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(3)]

    # 아 문제야 좌표로 낚시하지 말라고;
    Tr, Tc = R-1, C-1
    is_answer = False
    step = 0

    # 아 회수야 시작 조건 체크 좀 하라고;
    if 0 <= Tr < len(arr) and 0 <= Tc < len(arr[0]):
        if arr[Tr][Tc] == K:
            is_answer = True

    # 해당 위치에 원하는 값 나올때까지
    while not is_answer:
        # 물론 최대 100번만 시도
        step += 1
        if step > 100:
            break

        # 행이 열보다 짧으면 전치하고 행 연산, 다시 전치해서 원복시킨다. (개꿀)
        if len(arr) < len(arr[0]):
            arr = transpose()
            process()
            arr = transpose()
        # 행이 열보다 길거나 같으면 그냥 그대로 연산
        else:
            process()

        # 연산 후에 조건 만족하는지 계속 체크
        if 0 <= Tr < len(arr) and 0 <= Tc < len(arr[0]):
            if arr[Tr][Tc] == K:
                is_answer = True
                break

    # 답 나왔으면 스텝 출력
    if is_answer:
        print(step)
    # 답 없으면 -1 출력
    else:
        print(-1)
