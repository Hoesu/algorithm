""" 윷놀이 사기단 / 20260903 / 체감 난이도: G2
소요 시간 2시간 7분 / 시도 2회 / 실행 시간 444ms (코드트리) / 메모리 25MB (코드트리)

[구상]
    - 시작부터 엇나갔다. 좀 더 단순하게 생각했어야 하는데, 그냥 인덱스로 식별하면 될 것을 그래프로 만들어버렸다;;
        - 이거 문제 환경이 조금만 더 복잡했으면 절대 풀이 못했을것 같다.
        - 추상화 연습이 필요하다.
    - 아무튼 백트래킹 유형인 점은 너무나도 자명했고, 시뮬레이션 파트가 생각이 많이 필요한 문제였다.
        - 일단 그래프로 초점을 잡고 백트래킹 함수에 대한 계획표부터 짰다.
        - 역할, 인자, 종료 조건, 후보 조건, 재귀 호출, 조기 종료 항목으로 나눠서 계획표를 작성하고 수정했다.
    - 이번 구현에서 중추적인 역할을 수행하는 함수는 바로 4개의 말 중에서 이동시킬 후보 명단을 뽑는 함수였다.
        - 현재 칸에서 문제의 제약에 맞춰 이동했을 때 도달하는 칸을 정확히 집어낼 수 있어야 한다.
        - 또한, 이미 이동을 종료한 말과, 다른 말이 있는 곳으로 이동하려는 말을 정확히 걸러내야 했다.
        - find_destination 함수를 통해서 이를 해결해보려고 했다.

[구현]
    - 이동 함수 구현하다가 죽을뻔 했습니다. 인덱스로 할걸...
        - 이 부분은 track 그래프의 구조와 싱크를 잘 맞춰야했기 때문에, 양방향으로 체크하면서 구현을 진행했다.
        - 처음에는 4번 트랙을 따로 고려하지 않았는데, 구현 다 마치고 백트래킹으로 올라가서 실수를 깨달았다.
        - 다시 돌아가서 4번 트랙을 설정하고, 모든 값이 고유한 식별자를 지니게 되는 것을 꼼꼼히 체크했다.
        - 각 분기점 직후에 시작점을 찍고 루프 돌리면서 의도한 방향으로 잘 가는지 엄밀하게 체크했다.
        - 덕분에 첫번째 제출에 실패했을때 이 부분은 다시 돌려볼 필요가 없어서 좋긴 했다.
    - 백트래킹 구현은 쉽게 쉽게 했는데, 여기서 큰 실수를 하나 저질렀다.
        - 평소에 방문배열 원복하는 방식을 그렇게 애용하지 않았어서, 시작점도 지우고 복구해야 한다는 것을 놓쳤다.
        - 구상 단계에서 원복은 해야한다는 것을 잘 체크했지만, 구현 단계에서 디테일을 빠뜨린게 아쉬웠다.

[디버깅]
    - 오픈 테케는 한번에 다 맞았고, 제출하자마자 틀리는거 보고 디버깅 들어갔다.
    - 한 30분 정도 코드 째려보다가 방문 배열 실수한거 보여서 고치고 제출했다.

[후기]
    - 인덱스로 할걸...
"""


# TODO 1: 백트래킹 함수 작성
#   기능: 0~3(말 번호) 중에서 현재 턴에 이동시킬 수 있는 말에 대한 모든 경우의 수 탐색
#   인자: lst(각 말의 (트랙 번호, 칸 점수) 리스트), step(재귀 깊이), sm(현재 점수 합)
#   비고: 시작 칸은 0, 도착 칸은 -1로 표기하자.
def backtrack(lst, step=0, sm=0):
    # TODO 1.1 종료 조건
    #   step==10, 가능하면 최대 점수 업데이트하고 종료
    global max_score
    if step == 10:
        if sm > max_score:
            max_score = sm
        return

    # TODO 1.2 후보 조건
    #   이미 도착 칸에 도달할 말은 무시해야 한다.
    #   현재 턴에 이동하려는 위치에 다른 말이 없어야 한다. (도착점 제외)
    #       이동하면 도착하는 위치 뽑아서 방문 배열 체크하자.
    #   candidates: [(말 인덱스, 시작 트랙, 시작 점수, 도착 트랙, 도착 점수), (...), ...]
    candidates = []
    for idx in range(4):
        stt_id, stt_score = lst[idx]
        # 도착한 말 무시
        if stt_score == -1:
            continue
        # 다음 칸 위치와 점수 뽑기
        end_id, end_score = find_destination(stt_id, stt_score, moves[step])
        # 다음 칸이 최종칸이 아니고, 이미 방문한 위치라면 무시
        if end_score > 0 and visit[end_id][end_score] == 1:
            continue
        # 후보군에 추가
        candidates.append((idx, stt_id, stt_score, end_id, end_score))

    if candidates:
        # TODO 1.3 재귀 호출
        #   candidates 순회
        #       현재 리스트 복사본 만들기.
        #       움직일 말에 대한 정보를 업데이트 (트랙 넘버, 칸 점수)
        #       만약 최종칸에 도달했다면:
        #           방문 배열 출발 위치만 비우고 재귀, 다시 복원
        #       최종칸에 도달하지 못했다면:
        #           방문 배열 출발 위치 비우고 도착 위치 채우고 재귀
        #           방문 배열 원상복귀
        for idx, stt_id, stt_score, end_id, end_score in candidates:
            lst_copy = lst.copy()
            lst_copy[idx] = (end_id, end_score)
            # 최종 칸 도달.
            if end_score == -1:
                visit[stt_id][stt_score] = 0
                backtrack(lst_copy, step+1, sm)
                visit[stt_id][stt_score] = 1
            # 최종 칸 도달하지 못함.
            else:
                visit[stt_id][stt_score] = 0
                visit[end_id][end_score] = 1
                backtrack(lst_copy, step+1, sm+end_score)
                visit[stt_id][stt_score] = 1
                visit[end_id][end_score] = 0
    else:
        # TODO 1.4 조기 종료
        #   candidates 비어 있으면 다음 턴 시도??? 일단 종료해봐
        return


# TODO 2: 현재 트랙 넘버, 위치한 칸의 점수, 이동 거리 주어지면 도착 트랙과 점수 반환 (TEST 완료)
def find_destination(track_id, cur_score, distance):
    # 인덱스 찾는거 살짝 껄끄럽긴 하지만 리스트가 짧음.
    cur_idx = tracks[track_id].index(cur_score)
    # 도착 지점을 넘어선 곳으로 갈 수 없다.
    nxt_idx = min(cur_idx + distance, len(tracks[track_id]) - 1)
    # 1번, 2번, 3번 트랙은 전부 25번에서 합류한다.
    # 최대 이동 횟수가 5회이므로, 25를 넘어서 4번 트랙의 중간, 혹은 심지어 최종칸까지 도달 가능하다.
    # 이때를 대비하여 오프셋 수치를 미리 계산한다.
    offset = (cur_idx+distance) - len(tracks[track_id])

    # 한번에 도착 지점 도달
    if tracks[track_id][nxt_idx] == -1:
        return 0, -1

    # 0번 루트에서 발생 가능한 분기 처리
    if track_id == 0:
        # 일반 트랙에서 10번 루트로 이탈
        if tracks[track_id][nxt_idx] == 10:
            return 1, 10
        # 일반 트랙에서 20번 루트로 이탈
        elif tracks[track_id][nxt_idx] == 20:
            return 2, 20
        # 일반 트랙에서 30번 루트로 이탈
        elif tracks[track_id][nxt_idx] == 30:
            return 3, 30
        # 별다른 이슈 없이 기존 루트로 진행
        else:
            return track_id, tracks[track_id][nxt_idx]

    # 4번 루트에서 발생 가능한 분기 처리
    elif track_id == 4:
        # 40번은 유일하다. 중복 방지를 위해 전부 0번 트랙으로 처리한다.
        if tracks[track_id][nxt_idx] == 40:
            return 0, 40
        # 별다른 이슈 없이 기존 루트로 진행
        else:
            return track_id, tracks[track_id][nxt_idx]

    # 1, 2, 3 루트에서 발생 가능한 분기 처리
    else:
        # 오프셋이 4 이상이면 최종 위치에 도달한다.
        if offset >= 4:
            return 0, -1
        # 오프셋이 3이면 40번칸에 도달한다.
        elif offset == 3:
            return 0, 40
        # 오프셋이 0이상 4 미만이면 4번 트랙 위에서 정지한다.
        elif 0 <= offset < 4:
            return 4, tracks[4][offset]
        # 아니면 그냥 1, 2, 3 중 현재 트랙에 그대로 남아있는다.
        else:
            return track_id, tracks[track_id][nxt_idx]


if __name__ == '__main__':
    # 최대 점수
    max_score = 0
    # 턴별 이동 칸 수 받아오기
    moves = list(map(int, input().split()))

    # TODO 0: 트랙 정보 설정
    #   중복되는 점수가 있기 때문에 점수만으로 칸을 식별할 수 없다.
    #   0번: 한번도 분기하지 않고 검은색 화살표만 따라가는 루트
    #   1번: 0번 트랙의 10번 칸에서 분기하는 루트
    #   2번: 0번 트랙의 20번 칸에서 분기하는 루트
    #   3번: 0번 트랙의 30번 칸에서 분기하는 루트
    #   4번: 1, 2, 3 트랙이 합류하는 지점인 25번 칸에서 최종칸까지 이어지는 루트
    #   구현상 편의를 위해 4번 트랙도 최종 위치까지 이어지는 것으로 설정한다.
    #       단, 40번 칸은 유일하므로 중복 방지를 위해 고유 식별자는 (0, 40)으로 고정한다.
    tracks = [
        [0] + list(range(2, 42, 2)) + [-1],
        [10, 13, 16, 19],
        [20, 22, 24],
        [30, 28, 27, 26],
        [25, 30, 35, 40, -1]
    ]

    # 방문 배열 설정.
    # 총 5개의 트랙, 최대 40점의 점수가 있다.
    # 각 칸마다 고유한 식별자를 가지고 있으므로, 그냥 통 크게 5 * 41 배열로 설정한다.
    visit = [[0] * 41 for _ in range(5)]
    visit[0][0] = 1

    # 환경 초기화
    init = [(0, 0), (0, 0), (0, 0), (0, 0)]
    # 백트래킹 시작
    backtrack(lst=init)
    # 정답 출력
    print(max_score)
