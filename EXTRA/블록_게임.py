class Block:
    def __init__(self, idx, lst):
        lst.sort(key=lambda x: x[0])
        self.r = lst[0][0]
        self.h = lst[-1][0] - self.r + 1
        lst.sort(key=lambda x: x[1])
        self.c = lst[0][1]
        self.w = lst[-1][1] - self.c + 1
        self.lst = lst
        self.idx = idx

    def find_targets(self, arr):
        missing = []
        for cr in range(self.r, self.r + self.h):
            for cc in range(self.c, self.c + self.w):
                if arr[cr][cc] == 0:
                    missing.append((cr, cc))
                    continue
                if arr[cr][cc] != self.idx:
                    return 0, arr

        for cr, cc in missing:
            if sum([row[cc] for row in arr[:cr]]) != 0:
                return 0, arr

        for cr, cc in self.lst:
            arr[cr][cc] = 0
        return 1, arr


def solution(board):
    answer = 0
    blocks = dict()

    while True:
        blocks.clear()
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] > 0:
                    key = board[r][c]
                    if key in blocks:
                        blocks[key].append((r, c))
                    else:
                        blocks[key] = [(r, c)]

        for k, v in blocks.items():
            blocks[k] = Block(k, v)

        erase_cnt = 0
        for k in blocks:
            is_erased, board = blocks[k].find_targets(board)
            erase_cnt += is_erased
        answer += erase_cnt

        if erase_cnt == 0:
            return answer
