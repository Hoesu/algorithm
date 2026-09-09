""" 팩맨 / 20260908 / 체감 난이도: G3
소요 시간 3시간 / 시도 INF / 실행 시간 54ms (코드트리) / 메모리 16MB (코드트리)

[구상]
    - 워, 워, 제출을 6번이나 했지만 절대 나쁜 의도가 있었던 것이 아닙니다요. 제 말을 좀 들어보시죠.
    - 절대 사후확신편향 같은게 아니라, 싹 다 아는 맛 조합이라 루틴만 지키면 무조건 풀 수 있는 문제였슴죠.
    - 그런데 문제를 처음 읽었을 때, 드디어 클래스를 활용한 풀이를 할 수 있겠다는 생각에 신이 나버렸지 뭡니까 허허.
        - 강사님이 클래스를 활용한 풀이가 한번쯤은 나타나기를 바라시는것 같아, 최근 묻어뒀던 클래스를 꺼내기만을 기다렸다.
        - 꼭 반에게 클래스의 아름다움을 보여주고야 말겠다는 다짐(자의식 과잉)으로 야심만만하게 시작했지만...
        - 최근 기본 자료구조, 최소한의 메서드, 딱 필요한 만큼의 함수화를 고집하다보니 내 안의 객체지향맨이 죽어있었다.
        - 신난 마음에 그만 죽어있던 애한테 급하게 산소호흡기 껴주고 클래스 구현부터 달려들었다. (대실패)
        - 결론은 클래스 구현에 문제가 있다기 보다, 클래스를 사용한 것 자체가 문제였다.
    - 일단 문제에서 중요한 부분을 몇가지 명시하고 지나가자면...
        - 8방향 탐색을 위한 벡터를 4방향으로 재활용할 수 있다.
        - 최대 3칸 뻗어나가는 팩맨의 이동 방식은 3중 루프로도, 백트래킹으로도 구현 가능하다.
        - 알은 몬스터 담은 자료구조와 똑같은 자료구조를 하나 생성해서, 동일한 위치에 박아뒀다가 꺼내서 몬스터 자료구조에 붙여주는 방식으로 '부화'를 구현 가능하다.
        - 시체의 지속 기간을 지속적으로 관리해줘야 하는 것처럼 포장하고 있는데, 나무박멸 제초제랑 똑같은 개념이다. 시간으로 관리 가능하다.

[구현]
    - 사실 구현 과정에서 (잘못은 했지만) 큰 어려움은 없어서.. 기록할만한 내용이 딱히 없다.
    - 그래서 왜 클래스를 쓰면 안됐는지에 대한 개인적인 고찰을 남긴다.
        - 알 만드는게 사실 인스턴스 복제를 만들어서 별도로 저장해뒀다가 나중에 쓰는거나 다름 없다.
        - 그래서 기존 구현에서는 copy 메서드 하나 만들어서, 행/열/방향 정보 똑같이 가진 새로운 인스턴스를 반환하게 했다.
        - 유령이 최대 100만 마리까지 가능하다는 것은 이미 확인해서 알고 있는 상태였는데, 인스턴스 복제가 그렇게 무거운 작업인지는 몰랐다.
        - 게다가 좌표 튜플을 키로 가지는 딕셔너리를 이미 사용하고 있는 상태에서, 좌표 정보를 또 가지고 있는 유령 인스턴스를 위치 별로 넣어주는것 만큼이나 멍청한 짓거리가 없다.
            - 그냥 유령 하나가 가지는 방향 인덱스를 각 포지션에 있는 리스트에 담아주면, 그게 추상적으로 유령을 표현하는 가장 효율적인 방법이다.
            - 암튼 억지 클래스 쓰려다가 된통 얻어맞은 격인데, 알고리즘 초반의 나로 회귀한 기분이었다.
            - 강사님이 해주신 극약처방으로 겨우 사람 흉내내기 시작했는데, 뭔가 반에 기여는 하고 싶고.. 욕심을 부렸다.

[디버깅]
    - 내가 진심으로 인정하는 잘못은 따로 있다.
        - 클래스 쓰면서 루틴 안 지켜지고 꼬인 것은 그렇다 치고, 유령 시체 만들때 빈칸이었던 칸에도 시체를 넣어버렸다.
        - 보통 테게 10번 이하라고 해도 안 열어보는데, 안하던 짓하면서 마음이 자꾸 조급해졌는지.. 3번 테케를 열어봤다.
        - 특히 이번 문제는 디버깅이 좀 어려운 편에 속해서.. 검증 더 부지런하게 해봐야 하는데 노력이 부족했다.
        - 이런 부분은 정말 100번 욕 먹어도 싸다.

[후기]
    - 그야말로 총체적 난국. 반에 기여하고 싶은 마음은 이해하는데, 니 앞가림부터 잘해라.
    - 항상 하던대로 루틴, 방식 지켜서 기출 제대로 다루고, 추후에 가능하면 클래스로 재풀이해서 소개하던가 하자.
    - 근데 다시 풀면 쉽게 풀긴 할 것 같다.
"""


def move(cr, cc, cd, pr, pc, time):
    for i in range(8):
        nd = (cd+i) % 8
        nr = cr+dr[nd]
        nc = cc+dc[nd]
        if not(0 <= nr < 4 and 0 <= nc < 4):
            continue
        if corpses[nr][nc] >= time:
            continue
        if nr == pr and nc == pc:
            continue
        cr = nr
        cc = nc
        cd = nd
        break
    return cr, cc, cd


def backtrack(cr, cc, lst=[], step=0, sm=0):
    global max_kills
    if step == 3:
        trials.append([sm, lst])
        if sm > max_kills:
            max_kills = sm
        return

    for i in range(4):
        nr, nc = cr+dr[i*2], cc+dc[i*2]
        if not (0 <= nr < 4 and 0 <= nc < 4):
            continue

        temp = cur_monsters[(nr, nc)]
        cur_monsters[(nr, nc)] = []
        backtrack(nr, nc, lst+[(nr, nc)], step+1, sm+len(temp))
        cur_monsters[(nr, nc)] = temp


if __name__ == '__main__':
    dr = [-1, -1, 0, 1, 1, 1, 0, -1]
    dc = [0, -1, -1, -1, 0, 1, 1, 1]

    M, T = map(int, input().split())
    pr, pc = map(int, input().split())
    pr, pc = pr-1, pc-1

    corpses = [[-1] * 4 for _ in range(4)]
    cur_monsters = dict()
    nxt_monsters = dict()
    eggs = dict()

    for r in range(4):
        for c in range(4):
            cur_monsters[(r, c)] = []
            nxt_monsters[(r, c)] = []
            eggs[(r, c)] = []

    for _ in range(M):
        r, c, d = map(int, input().split())
        cur_monsters[(r-1, c-1)].append(d-1)

    time = 0
    while time < T:

        # TODO 0: 임시 딕셔너리 비우기
        for loc in nxt_monsters:
            nxt_monsters[loc] = []

        # TODO 1: 복제 시도
        for loc, dir_list in cur_monsters.items():
            eggs[loc].extend(dir_list)

        # TODO 2: 몬스터 이동
        for loc, dir_list in cur_monsters.items():
            for dir_id in dir_list:
                gr, gc, gd = move(loc[0], loc[1], dir_id, pr, pc, time)
                nxt_monsters[(gr, gc)].append(gd)
            cur_monsters[loc] = []
        cur_monsters = nxt_monsters.copy()

        # TODO 3: 팩맨 이동 + 시체 위치 등록
        max_kills = 0
        trials = []
        backtrack(pr, pc)
        for kills, history in trials:
            if kills == max_kills:
                pr, pc = history[-1]
                for r, c in history:
                    if len(cur_monsters[(r, c)]) > 0:
                        cur_monsters[(r, c)] = []
                        corpses[r][c] = time+2
                break

        # TODO 4: 알 부화
        for key in cur_monsters:
            cur_monsters[key].extend(eggs[key])
            eggs[key] = []

        # TODO 5: 시간 증가
        time += 1

    # TODO 6: 정답 출력
    answer = 0
    for key, value in cur_monsters.items():
        answer += len(value)
    print(answer)
