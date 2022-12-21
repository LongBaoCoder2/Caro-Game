import json, random
from . import win_checker

setting = json.load(open('data/setting.json'))
SIZE_X  = setting['grid']['size_x']
SIZE_Y  = setting['grid']['size_y']

# các bước giúp di chuyển tới ô kề
NB_MOVE = [
    (-1, -1), ( 0, -1), ( 1, -1),
    (-1,  0),           ( 1,  0),
    (-1,  1), ( 0,  1), ( 1,  1),
]

# kế thừa từ hàm WinChecker
class Bot(win_checker.WinChecker):

    def __init__(self):

        # khởi tạo bộ nhớ của bot
        self.memory = dict()

    # hàm tìm những nước đi ứng cử viên
    def find_candidate_move(self, board : list):
        candidate_move = set()
        for row in range(SIZE_X):
            for col in range(SIZE_Y):
                if (board[row][col] == -1):
                    continue
                for move in NB_MOVE:
                    nb_cell = (row + move[0], col + move[1])
                    if self.in_board(nb_cell[0], nb_cell[1]) and board[nb_cell[0]][nb_cell[1]] == -1:
                        candidate_move.add(nb_cell)

        # print('Candidate move: ', end=' ')
        # for move in candidate_move:
        #     print(move, end=' ')
        # print()

        return list(candidate_move)

    # hàm tìm bước đi tốt nhất bằng thuật toán minimax_abp
    def minimax_abp(self, board, turn, alpha, beta, depth):

        # nếu bot đã từng giải quyết trạng thái này thì đưa ra đáp án từ bộ nhớ
        if (str(board), turn) in self.memory:
            #print('Aha!')
            return self.memory[(str(board), turn)]

        # nếu tìm vượt quá độ sâu thì dừng lại (xem như hoà)
        if depth == 0:
            print('Brain break...')
            return ((-1, -1), -1)

        # tìm các bước đi ứng cử
        candidate_move = self.find_candidate_move(board)

        # nếu không có nước đi ứng cử nào thì trả về 0 (hoà)
        if len(candidate_move) == 0:
            return ((-1, -1), 0)

        alpha_move = (-1, -1)
        beta_move  = (-1, -1)

        # duyệt qua các bước trong các bước ứng cử
        for move in candidate_move:

            # kiểm tra xem nước đi có thắng luôn không
            board[move[0]][move[1]] = turn
            val = self.check_win(board, turn, move[0], move[1])
            board[move[0]][move[1]] = -1

            # nếu thắng luôn
            if val == True:
                if turn == 1:
                    self.memory[(str(board), turn)] = (move, 1)
                elif turn == 0:
                    self.memory[(str(board), turn)] = (move, -1)
                return self.memory[(str(board), turn)]

            # nếu không thắng luôn
            else:

                # tiếp tục thuật toán
                board[move[0]][move[1]] = turn
                val = self.minimax_abp(board, 1 - turn, alpha, beta, depth - 1)
                board[move[0]][move[1]] = -1
                
                if turn == 1:
                    if alpha < val:
                        alpha = val
                        alpha_move = move
                elif turn == 0:
                    if beta > val:
                        beta = val
                        beta_move = move
            
            # cắt tỉa
            if alpha >= beta:
                break

        if turn == 1:
            self.memory[(str(board), turn)] = (alpha_move, alpha)
        elif turn == 0:
            self.memory[(str(board), turn)] = (beta_move ,  beta)
        return self.memory[(str(board), turn)]
    
    # hàm tìm nước đi tốt nhất
    def find_best_move(self, board):

        found = self.minimax_abp(board, turn = 1, alpha = -1, beta = 1, depth = 10)

        # duyệt qua các bước trong các bước ứng cử
        for move in candidate_move:

            board[move[0]][move[1]] = 1
            val = self.minimax_abp(board, turn = 0, alpha = -1, beta = 1, depth = 10)
            board[move[0]][move[1]] = -1

            print(move, val)

            # nếu tìm ra nước đi dẫn tới chắc chắn chiến thắng
            if val == 1:
                print('Found best move!')
                return move

            # nếu tìm ra nước đi dẫn tới khả năng hoà
            elif val == 0:
                temp_candidate = move

        # nếu không tìm được nước đi thắng hay hoà
        if temp_candidate == (-1, -1):
            print('Cant find any!')

            # trả về ngẫu nhiên một nước đi trong các nước ứng cử
            return random.choice(candidate_move)

        else:
            # trả về nước đi hoà
            print('Found good move!')
            return temp_candidate
