import random

class PlayerType:
    NoPlayer = 0
    Computer = 1
    Human = 2

class PieceType:
    Flat=0
    Standing = 1

class Move:
    def __init__(self, piece_id, new_x, new_y):
        self.piece_id = piece_id
        self.new_x = new_x
        self.new_y = new_y

class Piece:
    def __init__(self, x, y, piece_id, player, type):
        self.x = x
        self.y = y
        self.id = piece_id
        self.player = player
        self.type = type

    def valid_moves(self, current_board):
        moves_list=[]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_valid_move(current_board, Move(self.id, self.x + i, self.y + j)):
                    moves_list.append(Move(self.id, self.x + i, self.y + j))
        return moves_list

    def is_valid_move(self, current_board, move):
        piece=None
        for p in current_board.pieces:
            if p.id == move.piece_id:
                piece = p
        if piece is None:
            return False
        if piece.type == PieceType.Standing:
            return False
        if move.new_x != piece.x and move.new_y != piece.y:
            return False
        if move.new_x == piece.x and move.new_y == piece.y:
            return False
        if abs(move.new_x-piece.x)>1 or abs(move.new_y-piece.y)>1:
            return False
        for p in current_board.pieces:
            if p.x==move.new_x and p.y==move.new_y:
                return False
        return current_board.size > move.new_x >= 0 and  current_board.size > move.new_y >= 0

class Board:
    def __init__(self, board=None):
        if board is None:
            self.size = 4
            self.pieces = []
            for i in range(self.size):
                self.pieces.append(Piece(i, self.size - 1, i, PlayerType.Computer, PieceType.Flat))
            for i in range(self.size-2):
                self.pieces.append(Piece(i, 0, i + self.size, PlayerType.Human, PieceType.Flat))
            for i in range(self.size - 2, self.size):
                self.pieces.append(Piece(i, 0, i + self.size, PlayerType.Human, PieceType.Standing))
        else:
            self.size = board.size
            self.pieces = [Piece(p.x, p.y, p.id, p.player, p.type) for p in board.pieces]

    def pozitii_linie_scop(self, scop):
        s=0
        for p in self.pieces:
            if p.y == scop:
                s=s+1
        return s

    def evaluation_function(self):
        return 12-sum([p.y for p in self.pieces if p.player == PlayerType.Human])-sum([p.y for p in self.pieces if p.player == PlayerType.Computer])+self.pozitii_linie_scop(0)-self.pozitii_linie_scop(self.size-1)

    def make_move(self, move):
        next_board = Board(self)  # copy
        if move is not None:
            next_board.pieces[move.piece_id].x = move.new_x
            next_board.pieces[move.piece_id].y = move.new_y
        return next_board

    def check_finish(self):
        finished = False
        winner = PlayerType.NoPlayer
        humanpieces=[p for p in self.pieces if p.player == PlayerType.Human and p.type==PieceType.Flat]
        existingpiecesonmaindiagonal=0
        existingpiecesonseconddiagonal=0
        for p in humanpieces:
            if p.x==p.y:
                existingpiecesonmaindiagonal += 1
        if existingpiecesonmaindiagonal==self.size:
            finished = True
            winner = PlayerType.Human
            return finished, winner

        for p in humanpieces:
            if p.x+p.y==self.size-1:
                existingpiecesonseconddiagonal += 1
        if existingpiecesonseconddiagonal==self.size:
            finished = True
            winner = PlayerType.Human
            return finished, winner

        biggestammountofpiecesonaline=[0,0,0,0]
        for p in humanpieces:
            biggestammountofpiecesonaline[p.x]+=1
        if max(biggestammountofpiecesonaline)==self.size:
            finished = True
            winner = PlayerType.Human
            return finished, winner

        biggestammountofpiecesonacolumn = [0, 0, 0, 0]
        for p in humanpieces:
            biggestammountofpiecesonacolumn[p.y] += 1
        if max(biggestammountofpiecesonacolumn) == self.size:
            finished = True
            winner = PlayerType.Human
            return finished, winner

        computerpieces = [p for p in self.pieces if p.player == PlayerType.Computer and p.type==PieceType.Flat]
        existingpiecesonmaindiagonal = 0
        existingpiecesonseconddiagonal = 0
        for p in computerpieces:
            if p.x == p.y:
                existingpiecesonmaindiagonal += 1
        if existingpiecesonmaindiagonal == self.size:
            finished = True
            winner = PlayerType.Computer
            return finished, winner

        for p in computerpieces:
            if p.x + p.y == self.size-1:
                existingpiecesonseconddiagonal += 1
        if existingpiecesonseconddiagonal == self.size:
            finished = True
            winner = PlayerType.Computer
            return finished, winner

        biggestammountofpiecesonaline = [0, 0, 0, 0]
        for p in computerpieces:
            biggestammountofpiecesonaline[p.x] += 1
        if max(biggestammountofpiecesonaline) == self.size:
            finished = True
            winner = PlayerType.Computer
            return finished, winner

        biggestammountofpiecesonacolumn = [0, 0, 0, 0]
        for p in computerpieces:
            biggestammountofpiecesonacolumn[p.y] += 1
        if max(biggestammountofpiecesonacolumn) == self.size:
            finished = True
            winner = PlayerType.Computer
            return finished, winner

        return finished, winner

class Minimax:
    _rand = random.Random()
    @staticmethod
    def find_next_board(current_board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True):
        finished, winner = current_board.check_finish()
        if finished or depth == 0:
            return current_board
        best_move = None
        if maximizing:  # Computer
            max_eval = float('-inf')
            for piece in current_board.pieces:
                if piece.player == PlayerType.Computer:
                    for move in piece.valid_moves(current_board):
                        temp_board = current_board.make_move(move)
                        result_board = Minimax.find_next_board(
                            temp_board,
                            depth - 1,
                            alpha,
                            beta,
                            False
                        )
                        eval_score = result_board.evaluation_function()
                        if eval_score > max_eval:
                            max_eval = eval_score
                            best_move = move
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
            if best_move is not None:
                current_board = current_board.make_move(best_move)
            return current_board
        else:
            min_eval = float('inf')
            for piece in current_board.pieces:
                if piece.player == PlayerType.Human:
                    for move in piece.valid_moves(current_board):
                        temp_board = current_board.make_move(move)
                        result_board = Minimax.find_next_board(
                            temp_board,
                            depth - 1,
                            alpha,
                            beta,
                            True
                        )
                        eval_score = result_board.evaluation_function()
                        if eval_score < min_eval:
                            min_eval = eval_score
                            best_move = move
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            if best_move is not None:
                current_board = current_board.make_move(best_move)
            return current_board
