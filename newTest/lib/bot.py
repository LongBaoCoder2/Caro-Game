import json, random, time
from . import win_checker

# các bước giúp di chuyển tới ô kề
NB_MOVE = [
    (-1, -1), ( 0, -1), ( 1, -1),
    (-1,  0),           ( 1,  0),
    (-1,  1), ( 0,  1), ( 1,  1),
]

# kế thừa từ hàm WinChecker
class Bot(win_checker.WinChecker):

    def __init__(self):
        self.setting = json.load(open('data/setting.json'))
        self.SIZE_X  = self.setting['grid']['size_x']
        self.SIZE_Y  = self.setting['grid']['size_y']
        self.WIN_CNT = self.setting['game']['win_cnt']
        
        # khởi tạo bộ nhớ của bot
        self.memory = dict()
        self.cnt    = 0

        # self.file = open('history.txt', 'w')

        # khởi tạo hàm random
        random.seed(time.time())

    # hàm tìm những nước đi ứng cử viên
    def find_candidate_move(self, board, history):
        candidate_move = set()

        # for row in range(SIZE_X):
        #     for col in range(SIZE_Y):
        #         if (board[row][col] == -1):
        #             continue
        #         for move in NB_MOVE:
        #             nb_cell = (row + move[0], col + move[1])
        #             if self.in_board(nb_cell[0], nb_cell[1]) and board[nb_cell[0]][nb_cell[1]] == -1:
        #                 candidate_move.add(nb_cell)

        for (row, col) in history:
                for move in NB_MOVE:
                    nb_cell = (row + move[0], col + move[1])
                    if self.in_board(nb_cell[0], nb_cell[1]) and board[nb_cell[0]][nb_cell[1]] == -1:
                        candidate_move.add(nb_cell)

        if len(candidate_move) != 0:
            return list(candidate_move)

        candidate_move = list()

        for row in range(self.SIZE_X):
            for col in range(self.SIZE_Y):
                if (board[row][col] == -1):
                    candidate_move.append((row, col))

        return [random.choice(candidate_move)]

        # print('Candidate move: ', end=' ')
        # for move in candidate_move:
        #     print(move, end=' ')
        # print()

    # hàm tìm bước đi tốt nhất bằng thuật toán minimax_abp
    def minimax_abp(self, board, history, turn, alpha, beta, depth):

        # nếu bot đã từng giải quyết trạng thái này thì đưa ra đáp án từ bộ nhớ
        for dep in range(depth, depth + 1, 1):
            if str((board, turn, dep)) in self.memory.keys():
                # print('Aha!', str((board, turn)), self.memory[str((board, turn))])
                return self.memory[str((board, turn, dep))]

        # nếu tìm vượt quá độ sâu thì dừng lại
        if depth == 0:
            # print('Brain break!')
            # self.file.writelines('Brain break!')
            if turn == 1:
                return ((-1, -1), alpha)
            elif turn == 0:
                return ((-1, -1),  beta)

        # tìm các bước đi ứng cử
        candidate_move = self.find_candidate_move(board, history)
        # print(candidate_move, '\n')

        # nếu không có nước đi ứng cử nào thì dừng lại
        if len(candidate_move) == 0:
            # print('No candidate!')
            # self.file.write('No candidate!' + '\n')
            if turn == 1:
                return ((-1, -1), 0)
            elif turn == 0:
                return ((-1, -1), 0)

        # lưu lại bước tốt nhất
        alpha_move = (-1, -1)
        beta_move  = (-1, -1)

        # duyệt qua từng nước ứng cử
        for move in candidate_move:

            # kiểm tra xem nước đi có thắng luôn không
            board[move[0]][move[1]] = turn

            for cnt in range(self.WIN_CNT, self.WIN_CNT - 1, -1):

                # cắt tỉa
                if alpha >= beta:
                    break

                val = self.check_win(board, turn, move[0], move[1], cnt)

                # nếu thắng luôn
                if val == True:
                    if turn == 1:
                        if alpha < cnt:
                            alpha      = cnt
                            alpha_move = move
                            break
                            # return (alpha_move, alpha)
                    elif turn == 0:
                        if beta > -cnt:
                            beta      = -cnt
                            beta_move = move
                            break
                            # return ( beta_move,  beta)
            
            board[move[0]][move[1]] = -1

        # nếu không thắng luôn
        # duyệt qua từng nước ứng cử
        for move in candidate_move:

            # cắt tỉa
            if alpha >= beta:
                break

            # tiếp tục thuật toán
            board[move[0]][move[1]] = turn
            history.append(move)
            val = self.minimax_abp(board, history, 1 - turn, alpha, beta, depth - 1)
            history.pop()
            board[move[0]][move[1]] = -1
            
            if turn == 1:
                if alpha < val[1]:
                    alpha      = val[1]
                    alpha_move = move
            elif turn == 0:
                if beta > val[1]:
                    beta      = val[1]
                    beta_move = move

        if turn == 1:
            self.memory[str((board, turn, depth))] = (alpha_move, alpha)
        elif turn == 0:
            self.memory[str((board, turn, depth))] = (beta_move ,  beta)
        # self.cnt += 1
        # self.file.write(str(self.cnt) + ' Memoried ' + str((board, turn)) + ' ' + str(self.memory[str((board, turn))]) + '\n')
        return self.memory[str((board, turn, depth))]
    
    # hàm tìm nước đi tốt nhất
    def find_best_move(self, board, history):

        print(history, '\n')

        found = self.minimax_abp(board, history, turn = 1, alpha = -self.WIN_CNT, beta = self.WIN_CNT, depth = self.WIN_CNT)

        # nếu không tìm được nước đi thắng hay hoà
        if found[1] == -self.WIN_CNT:
            print('Cant find any!', found[1])

            # trả về ngẫu nhiên một nước đi trong các nước ứng cử
            return random.choice(self.find_candidate_move(board, history))

        elif found[1] == self.WIN_CNT:
            # nếu tìm ra nước đi dẫn tới chắc chắn chiến thắng
            print('Found best move!', found[1])
            return found[0]

        else:
            # trả về nước đi hoà
            print('Found good move!', found[1])
            return found[0]
