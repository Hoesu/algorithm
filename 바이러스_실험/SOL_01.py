"""바이러스 실험 / 20260828 / 체감 난이도: S2
소요 시간 54분 / 시도 2회 / 실행 시간 972ms (코드트리) / 메모리 25MB (코드트리)

[구상]
    - 17분 구상했는데, 아침부터 갑자기 배아픔 + 근데 또 아침이라 머리는 잘돌아가는 상태였다.
    - 화장실 너무 가고 싶었는데 일단 문제는 풀어야겠어서 열심히 했다..
    - 일단 문제는 굉장히 명확했고, 제시된 조건 중 구현이 까다로운 부분은 없었다.
    - 다만, 영양분 섭취, 분열, 그리고 마지막 전체 영양분 추가 과정에서 자칫하면 무진장 많은 중복 + 쓸데없는 연산이 발생할 수 있다는 것을 파악했다.
        - 섭취 과정에서 전체 배열 순회는 불가피하다. (물론 길이 0은 스킵 가능함.)
        - 분열 과정에선 5의 배수 나이를 가지는 바이러스 위치만 미리 알아두면 된다. (섭취 과정에서 별도로 기록 남기기)
        - 전체 영양분 추가도 따로 배열 순회할 필요 없고, 섭취 끝나면 해당 위치에 추가하면 된다.
    - 결론적으로 시간초과빔의 싸늘한 시선을 느낀 덕에 화장실에 갈 수 있었다.

[구현]
    - 별로 어려운 내용은 없어서 한방에 구현했다.
    - 원자충돌이 많이 생각나는 문제였다.

[디버깅]
    - 죄송합니다 화장실이 너무 급해서.. 한번 틀렸습니다.
    - 문제 다시 읽어봤는데, 죽은 바이러스 나이 // 2만큼 양분 추가하는 것을 깜빡했다.
    - 그리고 모든 바이러스가 영양분을 전부 흡수하고나서 죽은것 처리를 해주라고 하는데, 낚시인게 뻔했다.
        - 적어도 1*1 칸 내부 연산이 끝나고 나면 전체 영양분 보너스처럼 더해줘도 상관없다.

[후기]
    - 시간초과를 당해본자, 그 아픔과 허탈함을 이해할지니...
    - 사실 구상단계에서 위기감지 한 것은 정말 운이 좋았다고 생각한다.
    - 틀리지 않으면서 최소한의 최적화는 해야하는데 또 최적화는 나중에 생각해야 한다는 이중적인 생각을 자주 하게된다.
"""

if __name__ == '__main__':
    # 8방향 벡터
    dr = [-1, 1, 0, 0, 1, 1, -1, -1]
    dc = [0, 0, -1, 1, 1, -1, 1, -1]

    # 영양분 보너스 배열, 바이러스 저장할 3차원 리스트, 영양분 현황 저장할 2차원 리스트
    N, M, K = map(int, input().split())
    plus = [list(map(int, input().split())) for _ in range(N)]
    virus = [[[] for _ in range(N)] for _ in range(N)]
    nutrition = [[5] * N for _ in range(N)]

    # 초기 바이러스 삽입: 위치 무조건 다른 것이 보장된다.
    for _ in range(M):
        row, col, age = map(int, input().split())
        virus[row - 1][col - 1].append(age)

    for _ in range(K):
        # 재방문할 위치를 저장
        revisit = []

        # 바이러스야 밥 먹자~
        for r in range(N):
            for c in range(N):
                # 바이러스 없으면 영양분만 추가하고 무시
                if len(virus[r][c]) < 1:
                    nutrition[r][c] += plus[r][c]
                    continue
                # 바이러스 2개 이상이면 오름차순 정렬
                if len(virus[r][c]) > 1:
                    virus[r][c].sort()
                # 살아남은 바이러스만 임시 배열에 저장
                nxt_virus = []
                # 죽은 바이러스에 의한 추가 영양분 저장할 값
                dead_bonus = 0
                for v in range(len(virus[r][c])):
                    # 현재 위치 영양분이 바이러스의 나이보다 크거가 같으면 바이러스 유지.
                    if nutrition[r][c] >= virus[r][c][v]:
                        nutrition[r][c] -= virus[r][c][v]
                        # 살아남은 바이러스 나이+1이 5의 배수라면 재방문 리스트에 좌표 추가
                        if (virus[r][c][v] + 1) % 5 == 0:
                            revisit.append((r, c))
                        # 살아남은 바이러스 나이+1을 임시 리스트에 추가.
                        nxt_virus.append(virus[r][c][v] + 1)
                    # 바이러스 죽으면 해당 칸에 나이 절반만큼의 영양분 추가해줘야 한다.
                    else:
                        dead_bonus += virus[r][c][v] // 2
                # 리스트 대체
                virus[r][c] = nxt_virus
                # 해당 위치 연산 끝났으니 영양분 보너스 지금 더해줘도 상관 없음.
                nutrition[r][c] += (dead_bonus + plus[r][c])

        # 재방문 순회하며 8방향으로 바이러스 뿌리기
        for r, c in revisit:
            for i in range(8):
                nr, nc = r + dr[i], c + dc[i]
                if not (0 <= nr < N and 0 <= nc < N):
                    continue
                virus[nr][nc].append(1)

    # 3차원 배열 각 원소 길이 전부 합산하여 출력
    answer = sum([sum([len(lst) for lst in row]) for row in virus])
    print(answer)
