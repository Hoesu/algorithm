# 경주로 건설
from heapq import heappush, heappop

def solution(board):
    n = len(board)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    heap = [[0, 0, 0, -1]]
    dajk = [[[int(1e9)] * 4 for _ in range(n)] for _ in range(n)]
    dajk[0][0] = [0, 0, 0, 0]

    while heap:
        cost, cr, cc, cd = heappop(heap)
        if cost > dajk[cr][cc][cd]:
            continue

        for nd in range(4):
            nr, nc = cr + dr[nd], cc + dc[nd]

            if not(0 <= nr < n and 0 <= nc < n):
                continue
            if board[nr][nc] == 1:
                continue

            if cd == -1:
                dajk[nr][nc][nd] = 100
                heappush(heap, [100, nr, nc, nd])
            else:
                if cd != nd:
                    if cost+600 <= dajk[nr][nc][nd]:
                        dajk[nr][nc][nd] = cost+600
                        heappush(heap, [cost+600, nr, nc, nd])
                else:
                    if cost+100 < dajk[nr][nc][nd]:
                        dajk[nr][nc][nd] = cost+100
                        heappush(heap, [cost+100, nr, nc, nd])
    return min(dajk[n-1][n-1])
