
def rotate():
    arr_copy = [row.copy() for row in arr]
    for r in range(N):
        for c in range(N):
            arr_copy[N-1-c][r] = arr[r][c]
    return arr_copy


if __name__ == '__main__':
    N = 4
    arr = [[0] * N for _ in range(N)]

    step = 0
    for r in range(N):
        for c in range(N):
            arr[r][c] = step
            step += 1

    for row in arr:
        print(*row)


    arr = rotate()


    print()
    for row in arr:
        print(*row)