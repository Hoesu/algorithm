""" 미생물 연구 / 20260928 / 체감 난이도: G3
소요 시간 3시간 5분 / 시도 3회 / 실행 시간 337ms (코드트리) / 메모리 25MB (코드트리)

[구상]
    - 쓸데없이 어렵게 풀었고, 그렇다고 내 풀이가 대단히 효율적이지도 않다.
    - 배열 덮어쓰기, BFS로 조건 만족하는 영역 탐색, 우선 순위 정렬, 인접 그룹 계산 등 전부 익숙한 업무들이 주어졌다.
    - 그냥 시키는대로 열심히 구현하는 문제인데, 배열을 순회할 일이 굉장히 많아서 방만하게 코딩하기 두려운 문제였다.
        - 그래서 나름의 최적화를 시도해보겠다며 모든 미생물 그룹의 정보를 들고 다니면서 관리하려고 했다.
        - 덕분에 그룹 크기 구할 때마다 매번 순회한다던가, 좌하단 좌표를 꾸준히 업데이트 한다던가 하는 괴랄한 길로 빠져들게 되었다.
    - 새로운 미생물 정보로 배열 덮어쓰고, 그냥 BFS로 그룹 구하고, 정렬하고, 값 옮기면 그만인데 나는 무슨 바람이 들었던걸까?
        - 굳이 컨디션 탓을 하기는 싫고, 그냥 구상이 부족해서 구현 단계에서 피를 본 것이라고 해두겠다.
    - 그나마 잘한거 한가지 뽑자면, 굳이 좌표 변환하지 않고, 디버깅 할때만 반시계 90도 회전시켜서 봤다.

[구현]
    - 그나마 루틴은 철저하게(구상 제외) 지켜서 풀 수 있었던 것이라고 생각한다.
    - 복잡하게 생각한 탓에 구현도 복잡하거나, 앞에서 똥 싼 부분들을 감당하기 위해 겉잡을 수 없이 길어졌다.
    - 특히 미생물 클래스 쓴 건 정말 지금 생각해도 어이가 없다 ㅋㅋㅋ
    - 구현 과정이 길긴 했지만, 특별히 힘들다거나 그런 부분은 없었다.

[디버깅]
    - 첫번째 제출: 풀이 시간 2시간 진입 시점에 주어지는 강제 이동 시간에 버저비터 한번 던지고 튀었다.
        - 인접 덩어리 측정하는 코드에서 사소한 오류가 있어서 바로 수정했다.
    - 두번째 제출: 이때 걸린 7번 테케가 하필이면 초대형 케이스였다.
        - 어차피 패닉해봐야 별 도움도 안되니 정답 대조를 해봤는데, 딱 2군데에서 답이 달랐다.
        - 그래서 전반적인 접근은 맞게 들어갔는데, 특정 케이스에서 내 가정이 빗나가고 있구나, 하는 생각이 들었다.
        - 19번째 루프에서 커스텀 프린트를 단계적으로 출력했고, 새로운 격자로 이동하는 과정이 이상하다는 것을 발견할 수 있었다.
        - 미생물 덩어리 하나가 다른 덩어리에 의해 덮어씌워지는 시점과, 영역을 측정하여 미생물 덩어리의 범위를 업데이트하는 시점의 서순이 잘못되었다.
        - 그래서 업데이트 시점을 바로 잡아주니 두 지점에서 발생했던 오류가 바로 올바르게 수정되는 것을 확인할 수 있었다.

[후기]
    - 일단 단순하게 생각하고 문제를 꼼꼼히 봐라. 시간복잡도 감이 떨어져서 이런 일이 발생한 것이다.
    - 시작부터 최적화 시도하지 마라.
"""
from collections import deque


def debug(msg, arr):
    print()
    print(msg)
    arr_rtt = [col for col in zip(*arr)][::-1]
    for row in arr_rtt:
        print(*row)
    print('------')


class Microbe:
    DR = [-1, 1, 0, 0]
    DC = [0, 0, -1, 1]

    def __init__(self, x1, y1, x2, y2, idx):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.idx = idx

    def imprint(self, arr):
        for cx in range(self.x1, self.x2):
            for cy in range(self.y1, self.y2):
                arr[cx][cy] = self.idx
        return arr

    def unprint(self, arr):
        for cx in range(self.x1, self.x2):
            for cy in range(self.y1, self.y2):
                if arr[cx][cy] == self.idx:
                    arr[cx][cy] = 0
        return arr

    def count_pieces(self, arr):
        call_count = 0
        vst = [[0] * N for _ in range(N)]
        for sx in range(self.x1, self.x2):
            for sy in range(self.y1, self.y2):
                if arr[sx][sy] == self.idx and vst[sx][sy] == 0:
                    call_count += 1
                    que = deque()
                    que.append((sx, sy))
                    vst[sx][sy] = 1

                    while que:
                        cx, cy = que.popleft()
                        for i in range(4):
                            nx = cx + Microbe.DR[i]
                            ny = cy + Microbe.DC[i]
                            if not(self.x1 <= nx < self.x2):
                                continue
                            if not(self.y1 <= ny < self.y2):
                                continue
                            if vst[nx][ny] != 0:
                                continue
                            if arr[nx][ny] != self.idx:
                                continue
                            que.append((nx, ny))
                            vst[nx][ny] = 1
        # BFS 횟수가 0일 때는 완전 덮어 씌워진 것.
        return call_count if call_count > 0 else 2

    def get_area(self, arr):
        area = 0
        for cx in range(self.x1, self.x2):
            for cy in range(self.y1, self.y2):
                if arr[cx][cy] == self.idx:
                    area += 1
        return area

    def get_coordinates(self, arr):
        coords = []
        min_found = False
        std_x, std_y = None, None
        for cx in range(self.x1, self.x2):
            for cy in range(self.y1, self.y2):
                if arr[cx][cy] == self.idx:
                    if not min_found:
                        std_x, std_y = cx, cy
                        min_found = True
                    coords.append([cx-std_x, cy-std_y])
        return coords

    def adjust(self, coords):
        x_val = [z[0] for z in coords]
        y_val = [z[1] for z in coords]
        self.x1 = min(x_val)
        self.x2 = max(x_val) + 1
        self.y1 = min(y_val)
        self.y2 = max(y_val) + 1

    @staticmethod
    def find_settlement(arr, coords):
        spots = []
        for cx in range(N):
            for cy in range(N):
                cell_check = True
                for dx, dy in coords:
                    nx, ny = cx+dx, cy+dy
                    if not(0 <= nx < N and 0 <= ny < N):
                        cell_check = False
                        break
                    if arr[nx][ny] != 0:
                        cell_check = False
                        break
                if cell_check:
                    spots.append((cx, cy))

        if not spots:
            return None, None
        else:
            spots.sort(key=lambda z: [z[0], z[1]])
            return spots[0]


def calc_adjacent(arr):
    adjacent = set()
    for cx in range(N):
        for cy in range(N):
            for dx, dy in [(0, 1), (1, 0)]:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < N and 0 <= ny < N):
                    continue
                if arr[cx][cy] == 0:
                    continue
                if arr[nx][ny] == 0:
                    continue
                if arr[cx][cy] == arr[nx][ny]:
                    continue
                if arr[cx][cy] > arr[nx][ny]:
                    adjacent.add((arr[nx][ny], arr[cx][cy]))
                else:
                    adjacent.add((arr[cx][cy], arr[nx][ny]))
    return adjacent


if __name__ == '__main__':
    DEBUG_MODE = False
    N, Q = map(int, input().split())
    cur_batch = [[0] * N for _ in range(N)]
    microbes = dict()

    for time in range(1, Q+1):
        r1, c1, r2, c2 = map(int, input().split())
        microbe = Microbe(r1, c1, r2, c2, time)
        microbes[time] = microbe

        # TODO 1: 미생물 투입
        #   주어진 영역을 순회하며 배치에 미생물 고유 ID를 덮어쓰기
        #   딕셔너리 키 순회하며 각 미생물 별로 주어진 영역 내에서 BFS로 덩어리 개수 세기
        #       만약에 덩어리 개수가 1보다 크다면 해당 미생물 ID 전부 지우고 딕셔너리에서 POP.
        cur_batch = microbe.imprint(cur_batch)
        for key in list(microbes.keys()):
            if microbes[key].count_pieces(cur_batch) > 1:
                cur_batch = microbes[key].unprint(cur_batch)
                microbes.pop(key)

        if DEBUG_MODE:
            debug(f'time = {time}, after placement:', cur_batch)

        # TODO 2: 배양 용기 이동
        #   딕셔너리 키 순회하며 (영역 넓이, 고유 ID) 추출하여 (-, +) 람다 정렬
        #   우선순위에 맞춰 딕셔너리 키 다시 순회
        #       주어진 미생물의 스캔 범위에서 배치 내 값이 자신의 고유 ID와 동일한 모든 칸의 상대좌표 추출
        #       다음 배치 배열을 행, 열 우선 순회하며 모든 상대좌표가 범위 내 빈칸이면 바로 삽입 후 브레이크
        #       만약 끝까지 삽입하지 못했다면 해당 미생물은 딕셔너리에서 POP.
        candidates = []
        for key in microbes:
            candidates.append([microbes[key].get_area(cur_batch), key])
        candidates.sort(key=lambda x: [-x[0], x[1]])
        nxt_batch = [[0] * N for _ in range(N)]

        for _, key in candidates:
            coordinates = microbes[key].get_coordinates(cur_batch)
            sr, sc = Microbe.find_settlement(nxt_batch, coordinates)

            if sr is None and sc is None:
                microbes.pop(key)
                continue

            for i in range(len(coordinates)):
                dr, dc = coordinates[i]
                nxt_batch[sr+dr][sc+dc] = key
                coordinates[i][0] += sr
                coordinates[i][1] += sc
            microbes[key].adjust(coordinates)
        cur_batch = nxt_batch

        if DEBUG_MODE:
            debug(f'time = {time}, after replacement:', cur_batch)

        # TODO 3: 실험 결과 기록
        #   다음 배치에 BFS 돌려서 모든 인접 무리 쌍 추출하기
        adj_sum = 0
        adj = calc_adjacent(cur_batch)

        if not adj:
            print(adj_sum)
        else:
            for this, other in adj:
                this_area = microbes[this].get_area(cur_batch)
                other_area = microbes[other].get_area(cur_batch)
                adj_sum += (this_area * other_area)
            print(adj_sum)
