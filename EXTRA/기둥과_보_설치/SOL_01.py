def check_garo(cr, cc, garo_arr, sero_arr, n):
    # 보는 한쪽 끝 부분이 기둥 위에 있거나, 또는 양쪽 끝 부분이 다른 보와 동시에 연결되어 있어야 합니다.
    if sero_arr[cr][cc] == 1:
        return True
    elif sero_arr[cr][cc+1] == 1:
        return True
    elif 0 < cc < n-1 and garo_arr[cr][cc-1] == 1 and garo_arr[cr][cc+1] == 1:
            return True
    return False


def check_sero(cr, cc, garo_arr, sero_arr, n):
    # 기둥은 바닥 위에 있거나 보의 한쪽 끝 부분 위에 있거나, 또는 다른 기둥 위에 있어야 합니다.
    if cr == n-1:
        return True
    elif cc > 0 and garo_arr[cr+1][cc-1] == 1:
        return True
    elif cc < n and garo_arr[cr+1][cc] == 1:
        return True
    elif sero_arr[cr+1][cc] == 1:
        return True
    return False


def solution(n, build_frame):
    sero = [[0] * (n+1) for _ in range(n)]
    garo = [[0] * n for _ in range(n+1)]

    for x, y, a, b in build_frame:
        # 좌표 변환 (0: 기둥, 1, 보)
        if a == 0:
            r, c = n-1-y, x
        else:
            r, c = n-y, x

        if b == 0:
            # 구조물 삭제
            possible = True
            if a == 0:
                sero[r][c] = 0
            else:
                garo[r][c] = 0

            for sr in range(len(sero)):
                for sc in range(len(sero[0])):
                    if sero[sr][sc] == 1:
                        if not check_sero(sr, sc, garo, sero, n):
                            possible = False
                            break

            for gr in range(len(garo)):
                for gc in range(len(garo[0])):
                    if garo[gr][gc] == 1:
                        if not check_garo(gr, gc, garo, sero, n):
                            possible = False
                            break

            if not possible:
                if a == 0:
                    sero[r][c] = 1
                else:
                    garo[r][c] = 1

        else:
            # 구조물 설치
            if a == 0:
                if check_sero(r, c, garo, sero, n):
                    sero[r][c] = 1
            else:
                if check_garo(r, c, garo, sero, n):
                    garo[r][c] = 1

    result = []
    for sr in range(len(sero)):
        for sc in range(len(sero[0])):
            if sero[sr][sc] == 1:
                result.append([sc, n-sr-1, 0])
    for gr in range(len(garo)):
        for gc in range(len(garo[0])):
            if garo[gr][gc] == 1:
                result.append([gc, n-gr, 1])
    result.sort(key=lambda z: [z[0], z[1], z[2]])
    return result