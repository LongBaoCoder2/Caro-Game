import json

setting = json.load(open('data/setting.json'))
SIZE_X = setting['grid']['size_x']
SIZE_Y = setting['grid']['size_y']

class WinChecker:

    def in_board(self, posX : int, posY : int) -> bool:
        return posX >= 0 and posX < SIZE_X and posY >= 0 and posY < SIZE_Y

    def check_cell(self, board: list, user: int, posX: int, posY: int) -> int:
        # nếu ô đó có đúng ký tự của user đó thì return 1
        if self.in_board(posX, posY) and (board[posX][posY] == user):
            return 1
        # gặp ký tự của đối thủ thì ăn penalty
        elif self.in_board(posX, posY) and (board[posX][posY] == 1 - user):
            return -100
        return 0

    def hv_check(self, board: list, user: int, posX: int, posY: int):
        # print()
        for i in range(-4, 1):
            startX = posX + i
            startY = posY + i
            # count lưu giá trị max liên tiếp
            countH, countV, curCountH, curCountV = 0, 0, 0, 0
            for j in range(0, 5):
                curX, curY = startX + j, posY
                point = self.check_cell(board, user, curX, curY)
                if point == 0:
                    if curCountH:
                        countH = max(curCountH, countH)
                        curCountH = 0
                else:
                    curCountH += point

                curX, curY = posX, startY + j
                point = self.check_cell(board, user, curX, curY)
                if point == 0:
                    if curCountV:
                        countV = max(curCountV, countV)
                        curCountV = 0
                else:
                    curCountV += point
            countH = max(curCountH, countH)
            countV = max(curCountV, countV)
            opponent = 1 - user
            leftX = startX - 1
            l = self.check_cell(board, opponent, leftX, posY) == 1
            rightX = startX + 5
            r = self.check_cell(board, opponent, rightX, posY) == 1
            topY = startY - 1
            t = self.check_cell(board, opponent, posX, topY) == 1
            bottomY = startY + 5
            b = self.check_cell(board, opponent, posX, bottomY) == 1
            # print("LeftX = %d, LeftY = %d" % (leftX, rightX))
            # print("User %d has %d max horizontal continous steps. This was check at (%d, %d)" % (user, countH, startX, posY))
            # print("User %d has %d max vertical continous steps. This was check at (%d, %d)" % (user, countV, posX, startY))
            if countH == 4 and not (l or r):
                # print("l is %s and r is %s" % (l, r))
                return True
            if countH == 5 and not (l and r):
                return True
            if countV == 4 and not (t or b):
                return True
            if countV == 5 and not (t and b):
                return True
        return False

    def main_diag_check(self, board: list, user: int, posX: int, posY: int):
        # print()
        for i in range(-4, 1):
            startX = posX + i
            startY = posY + i
            # count lưu giá trị max liên tiếp
            countM, curCountM = 0, 0
            for j in range(0, 5):
                curX, curY = startX + j, startY + j
                point = self.check_cell(board, user, curX, curY)
                if point == 0:
                    if curCountM:
                        countM = max(curCountM, countM)
                        curCountM = 0
                else:
                    curCountM += point
            countM = max(curCountM, countM)
            opponent = 1 - user
            topleftX, topleftY = startX - 1, startY - 1
            tl = self.check_cell(board, opponent, topleftX, topleftY) == 1
            bottomrightX, bottomrightY = startX + 5, startY + 5
            br = self.check_cell(board, opponent, bottomrightX, bottomrightY) == 1
            if countM == 4 and not (tl or br):
                return True
            if countM == 5 and not (tl and br):
                return True
        return False

    def anti_diag_check(self, board: list, user: int, posX: int, posY: int):
        # print()
        for i in range(-4, 1):
            startX = posX + i
            startY = posY - i
            # count lưu giá trị max liên tiếp
            countA, curCountA = 0, 0
            for j in range(0, 5):
                curX, curY = startX + j, startY - j
                point = self.check_cell(board, user, curX, curY)
                if point == 0:
                    if curCountA:
                        countA = max(curCountA, countA)
                        curCountA = 0
                else:
                    curCountA += point
            countA = max(curCountA, countA)
            opponent = 1 - user
            toprightX, toprightY = startX + 5, startY - 5
            tr = self.check_cell(board, opponent, toprightX, toprightY) == 1
            bottomleftX, bottomleftY = startX - 1, startY + 1
            bl = self.check_cell(board, opponent, bottomleftX, bottomleftY) == 1
            # print("LeftX = %d, LeftY = %d" % (leftX, rightX))
            # print("User %d has %d max continous steps. This was check at (%d, %d)" % (user, countA, startX, startY))
            # print("User %d has %d max vertical continous steps. This was check at (%d, %d)" % (user, countV, posX, startY))
            if countA == 4 and not (tr or bl):
                # print(self.check_cell(opponent, toprightX, toprightY))
                # print(tr, toprightX, toprightY)
                return True
            if countA == 5 and not (tr and bl):
                return True
        return False

    def check_win(self, board: list, user: int, posX: int, posY: int):
        if self.hv_check(board, user, posX, posY):
            print("User %d wins horizontal or vertical" % (user))
        if self.main_diag_check(board, user, posX, posY):
            print("User %d wins main diag" % (user))
        if self.anti_diag_check(board, user, posX, posY):
            print("User %d wins anti diag" % (user))
        return (
            self.hv_check(board, user, posX, posY)
            or self.main_diag_check(board, user, posX, posY)
            or self.anti_diag_check(board, user, posX, posY)
        )
