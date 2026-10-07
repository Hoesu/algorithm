from collections import deque

def in_range(x, y, n):
    return 0 <= x < n and 0 <= y < n

def get_next(lcr, lcc, rcr, rcc, arr):
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    n = len(arr)
    candidates = []

    for i in range(4):
        lnr, lnc = lcr + dr[i], lcc + dc[i]
        rnr, rnc = rcr + dr[i], rcc + dc[i]
        if not in_range(lnr, lnc, n):
            continue
        if not in_range(rnr, rnc, n):
            continue
        if arr[lnr][lnc] == 1:
            continue
        if arr[rnr][rnc] == 1:
            continue
        candidates.append((lnr, lnc, rnr, rnc))

    for delta_r, delta_c in ([lcc-rcc, rcr-lcr], [rcc-lcc, lcr-rcr]):
        if not in_range(lcr+delta_r, lcc+delta_c, n):
            continue
        if not in_range(rcr+delta_r, rcc+delta_c, n):
            continue
        if arr[lcr+delta_r][lcc+delta_c] == 1:
            continue
        if arr[rcr+delta_r][rcc+delta_c] == 1:
            continue
        candidates.append([lcr, lcc, lcr+delta_r, lcc+delta_c])

    for delta_r, delta_c in ([rcc-lcc, lcr-rcr], [lcc-rcc, rcr-lcr]):
        if not in_range(lcr+delta_r, lcc+delta_c, n):
            continue
        if not in_range(rcr+delta_r, rcc+delta_c, n):
            continue
        if arr[lcr+delta_r][lcc+delta_c] == 1:
            continue
        if arr[rcr+delta_r][rcc+delta_c] == 1:
            continue
        candidates.append([rcr+delta_r, rcc+delta_c, rcr, rcc])
    return candidates


def solution(board):
    n = len(board)

    vst = {(0, 0, 0, 1): 0}
    que = deque([(0, 0, 0, 1)])

    while que:
        lcr, lcc, rcr, rcc = que.popleft()
        dist = vst[(lcr, lcc, rcr, rcc)]

        for lnr, lnc, rnr, rnc in get_next(lcr, lcc, rcr, rcc, board):
            if (lnr, lnc) == (n - 1, n - 1) or (rnr, rnc) == (n - 1, n - 1):
                return dist + 1

            state = (lnr, lnc, rnr, rnc)

            if state in vst:
                continue

            vst[state] = dist + 1
            que.append(state)