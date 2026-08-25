""" 원자 충돌 / 20260821 / 체감 난이도: G5
소요 시간 INF / 시도 3회 / 실행 시간 221ms (코드트리) / 메모리 29MB (코드트리)

[구상]
    - 구상 시간은 약 17분. 굉장히 자신있는 유형의 문제였다.
    - 그냥 시키는대로만 성실히 구현하면 되는 문제였고, '원자'를 클래스로 구현하여 현재 위치, 질량, 속도, 방향을 속성값으로 지정해주고자 했다.

[구현]
    - 전체 구현 시간은 40분 가량 걸렸다.
    - 직접 배열을 생성해서 특정 위치에 값을 저장하는 구조로 하면 시간이나 메모리 제한에 걸릴 것이 자명했다.
        - 따라서 딕셔너리를 활용하여 좌표 튜플을 키로 잡고, 해당 칸에 원자 카운트와 원자 인스턴스 리스트를 저장하기로 헀다.
        - 해당 부분은 클래스가 아니라 그 인스턴스를 활용하는 실행부 코드였고, 구현 중간에 즉석으로 떠올린 방법이었다.
        - 결정적으로 여기서 시간 초과가 발생했는데, 아이디어의 문제가 아니라, 그것을 구현하는 과정에서 불필요한 중복 연산이 너무 많았다.
            - 분열로 인해서 제거되는 원자들을 그냥 다음 루프로 넘겨주지 않으면 그만이었다.
            - 하지만 제거할 원자들의 인덱스들을 따로 저장하고, 임시 리스트에 제거할 인덱스에 포함되지 않는 원본 리스트의 값들을 넘겨주었다.
            - 여기서 in 연산을 쓸데없이 많이 반복하게 되었고, 시간 초과가 발생했다.

[디버깅]
    - 오픈 테스트 케이스, 커스텀 테스트 케이스 모두 정답이 잘 나왔기 때문에 미치고 펄쩍 뛸 노릇이었다.
    - 시뮬레이션 문제는 시키는대로만 하면 항상 답이 잘 나왔었는데, "쓸데없는 구현 없이 시키는대로" 하는 연습이 부족했던 것 같다.
    - 본능적으로 메인 함수에 문제가 있다는 것은 알았지만, 정확히 어디서 병목이 발생하는지 코드를 다시 봐도 알기 어려웠다.
    - 최대 사이즈의 테케를 만들고, time 모듈을 활용하고 난 뒤에야 어디서 시간이 가장 오래 걸리는지 알 수 있었는데,
    - 시험 시간이 끝나는 바람에 시간 내에 제출하지 못했다.

[후기]
    - 사실상 다 푼 문제였기에 하루 이틀은 억울분통 모드긴 했지만... 시간이 지나서 돌아보니 지금이라도 이런 실수를 경험해본 것에 감사하다.
    - 클래스로 풀 수 있는 문제가 나왔다고 신나서 달려들기 전에, 실행부에 대한 고민도 제대로 하고 들어가자.
"""


class Atom:
    def __init__(self, xx, yy, ms, sp, dr):
        # x좌표, y좌표, 질량, 속도, 방향
        self.x = xx
        self.y = yy
        self.ms = ms
        self.sp = sp
        self._set_direction(dr)

    def _set_direction(self, dir_num):
        # 방향 번호를 받아서 벡터로 변환한다.
        # 대각/직선 방향 체크하여 불리언 값으로 저장한다.
        dx = [-1, -1, 0, 1, 1, 1, 0, -1]
        dy = [0, 1, 1, 1, 0, -1, -1, -1]
        self.dx = dx[dir_num]
        self.dy = dy[dir_num]
        if dir_num % 2 == 0:
            self.is_diag = 0
        else:
            self.is_diag = 1

    def move(self):
        # 모듈로 이동 함수. 끝과 끝 연결.
        self.x = (self.x + self.sp * self.dx) % N
        self.y = (self.y + self.sp * self.dy) % N
        return self.x, self.y

    def get_speed(self):
        # 속도 반환
        return self.sp

    def get_mass(self):
        # 질량 반환
        return self.ms

    def get_type(self):
        # 대각 타입 여부 반환
        return self.is_diag


def divide(x, y, atoms):
    # (x, y)에 있는 원자들을 4개의 원자로 분열시키는 함수
    sum_mass = 0
    sum_speed = 0
    sum_type = 0
    for at in atoms:
        sum_mass += at.get_mass()
        sum_speed += at.get_speed()
        sum_type += at.get_type()
    nmass = sum_mass // 5
    nspeed = sum_speed // len(atoms)
    # 분열한 원자들의 질량이 0이면, 빈 리스트를 반환한다.
    # 실행부에서 사용하는 방식을 살펴보면, 사실상 원자들을 버리는거나 마찬가지.
    if nmass == 0:
        return []
    # 타입 불리언 값의 합이 0 혹은 4라면, 모두 같은 방향이라는 뜻.
    # 수평 수직 방향으로 분할.
    elif sum_type == 0 or sum_type == len(atoms):
        return[
            Atom(x, y, nmass, nspeed, 0),
            Atom(x, y, nmass, nspeed, 2),
            Atom(x, y, nmass, nspeed, 4),
            Atom(x, y, nmass, nspeed, 6)
        ]
    # 0이나 4가 아니면 타입이 섞여있으므로 대각방향으로 분할.
    else:
        return[
            Atom(x, y, nmass, nspeed, 1),
            Atom(x, y, nmass, nspeed, 3),
            Atom(x, y, nmass, nspeed, 5),
            Atom(x, y, nmass, nspeed, 7)
        ]


if __name__ == '__main__':
    N, M, K = map(int, input().split())
    # 초기 원자 정보 받아서 리스트에 저장.
    atoms = []
    for _ in range(M):
        x, y, m, s, d = map(int, input().split())
        atoms.append(Atom(x, y, m, s, d))

    for _ in range(K):
        # 위치별로 원자들이 몇개씩 분포해 있는지 체크하기 위한 임시 딕셔너리.
        counter = dict()
        for atom in atoms:
            # 모듈로 이동 후 좌표 계산
            nx, ny = atom.move()
            # 튜플로 키를 만들어서 원자 정보 삽입 혹은 업데이트
            if (nx, ny) not in counter.keys():
                counter[(nx, ny)] = [1, [atom]]
            else:
                counter[(nx, ny)][0] += 1
                counter[(nx, ny)][1].append(atom)

        # 다음 라운드에 사용할 원자 리스트
        nxt_atoms = []
        for key, value in counter.items():
            # 주어진 위치에 원자가 2개 미만일 경우: 그대로 리스트에 추가
            if value[0] < 2:
                nxt_atoms.extend(value[1])
            # 주어진 위치에 원자가 2개 이상일 경우: Divide 호출하여 분할
            else:
                new_atoms = divide(key[0], key[1], value[1])
                nxt_atoms.extend(new_atoms)
        # 원자 리스트 업데이트. 다시 처음으로.
        atoms = nxt_atoms

    # 정답 출력
    answer = 0
    for at in atoms:
        answer += at.get_mass()
    print(answer)
