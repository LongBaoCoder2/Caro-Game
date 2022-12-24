# Notes:
# Check 4 o chi dung trong truong hop danh voi may (AI)
import json

class WinChecker:
    def __init__(self) -> None:
        self.setting = json.load(open('data/setting.json'))
        self.SIZE_X  = self.setting['grid']['size_x']
        self.SIZE_Y  = self.setting['grid']['size_y']
        self.WIN_CNT = self.setting['game']['win_cnt']
    
    def in_board(self, posX : int, posY : int) -> bool:
        return posX >= 0 and posX < self.SIZE_X and posY >= 0 and posY < self.SIZE_Y

    def check_cell(self, board: list, user: int, posX: int, posY: int) -> int:
        # nếu ô đó có đúng ký tự của user đó thì return 1
        if self.in_board(posX, posY) and (board[posX][posY] == user):
            #print(user)
            #print(board[posX][posY])
            return 1
        # gặp ký tự của đối thủ thì ăn penalty
        elif self.in_board(posX, posY) and (board[posX][posY] == 1 - user):
            # print(board[posX][posY])
            # print(user)
            return -100
        return 0

    def horizontal_check(self, board: list, user: int, posX: int, posY: int, pieces_to_win: int):
        # print()
        # print(board)
        for i in range(-pieces_to_win + 1, 1):
            startX = posX + i
            # count lưu giá trị max liên tiếp
            countH, curCountH = 0, 0
            for j in range(0, pieces_to_win):
                curX, curY = startX + j, posY
                point = self.check_cell(board, user, curX, curY)
                if point == 0:
                    if curCountH:
                        countH = max(curCountH, countH)
                        curCountH = 0
                else:
                    curCountH += point
            countH = max(curCountH, countH)
            opponent = 1 - user
            leftX = startX - 1
            l = self.check_cell(board, opponent, leftX, posY) == 1
            rightX = startX + pieces_to_win
            r = self.check_cell(board, opponent, rightX, posY) == 1
            #print("LeftX = %d, LeftY = %d" % (leftX, rightX))
            #print("User %d has %d max horizontal continous steps. This was check at (%d, %d)" % (user, countH, startX, posY))
            #print("User %d has %d max vertical continous steps. This was check at (%d, %d)" % (user, countV, posX, startY))
            # Chỉ dùng check 4 cho AI
            # if countH == 4 and not (l or r):
            #     # print("l is %s and r is %s" % (l, r))
            #     return True
            if countH == pieces_to_win and not (l and r):
                return True
        return False
    
    def vertical_check(self, board: list, user: int, posX: int, posY: int, pieces_to_win: int):
        # print()
        # print(board)
        for i in range(-pieces_to_win + 1, 1):
            startY = posY + i
            # count lưu giá trị max liên tiếp
            countV, curCountV = 0, 0
            for j in range(0, pieces_to_win):
                curX, curY = posX, startY + j
                point = self.check_cell(board, user, curX, curY)
                if point == 0:
                    if curCountV:
                        countV = max(curCountV, countV)
                        curCountV = 0
                else:
                    curCountV += point
            countV = max(curCountV, countV)
            opponent = 1 - user
            topY = startY - 1
            t = self.check_cell(board, opponent, posX, topY) == 1
            bottomY = startY + pieces_to_win
            b = self.check_cell(board, opponent, posX, bottomY) == 1
            #print("LeftX = %d, LeftY = %d" % (leftX, rightX))
            #print("User %d has %d max horizontal continous steps. This was check at (%d, %d)" % (user, countH, startX, posY))
            #print("User %d has %d max vertical continous steps. This was check at (%d, %d)" % (user, countV, posX, startY))
            # Chỉ dùng check 4 cho AI
            # if countV == 4 and not (t or b):
            #     return True
            if countV == pieces_to_win and not (t and b):
                return True
        return False

    def main_diag_check(self, board: list, user: int, posX: int, posY: int, pieces_to_win):
        # print()
        for i in range(-pieces_to_win + 1, 1):
            startX = posX + i
            startY = posY + i
            # count lưu giá trị max liên tiếp
            countM, curCountM = 0, 0
            for j in range(0, pieces_to_win):
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
            bottomrightX, bottomrightY = startX + pieces_to_win, startY + pieces_to_win
            br = self.check_cell(board, opponent, bottomrightX, bottomrightY) == 1
            # if countM == 4 and not (tl or br):
            #     return True
            if countM == pieces_to_win and not (tl and br):
                return True
        return False

    def anti_diag_check(self, board: list, user: int, posX: int, posY: int, pieces_to_win):
        # print()
        for i in range(-pieces_to_win + 1, 1):
            startX = posX + i
            startY = posY - i
            # count lưu giá trị max liên tiếp
            countA, curCountA = 0, 0
            for j in range(0, pieces_to_win):
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
            toprightX, toprightY = startX + pieces_to_win, startY - pieces_to_win
            tr = self.check_cell(board, opponent, toprightX, toprightY) == 1
            bottomleftX, bottomleftY = startX - 1, startY + 1
            bl = self.check_cell(board, opponent, bottomleftX, bottomleftY) == 1
            # print("LeftX = %d, LeftY = %d" % (leftX, rightX))
            # print("User %d has %d max continous steps. This was check at (%d, %d)" % (user, countA, startX, startY))
            # print("User %d has %d max vertical continous steps. This was check at (%d, %d)" % (user, countV, posX, startY))
            # if countA == 4 and not (tr or bl):
            #     # print(self.check_cell(opponent, toprightX, toprightY))
            #     # print(tr, toprightX, toprightY)
            #     return True
            if countA == pieces_to_win and not (tr and bl):
                return True
        return False

    def check_win(self, board: list, user: int, posX: int, posY: int, pieces_to_win: int = 5):
        # if self.hv_check(board, user, posX, posY):
        #     print("User %d wins horizontal or vertical" % (user))
        # if self.main_diag_check(board, user, posX, posY):
        #     print("User %d wins main diag" % (user))
        # if self.anti_diag_check(board, user, posX, posY):
        #     print("User %d wins anti diag" % (user))
        pieces_to_win = self.WIN_CNT
        return (
            self.horizontal_check(board, user, posX, posY, pieces_to_win)
            or self.vertical_check(board, user, posX, posY, pieces_to_win)
            or self.main_diag_check(board, user, posX, posY, pieces_to_win)
            or self.anti_diag_check(board, user, posX, posY, pieces_to_win)
        )
