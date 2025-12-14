import random


class PlayerType:
    NoPlayer = 0
    Computer = 1
    Human = 2


class PieceType:
    Flat = 0
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
        moves_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_valid_move(current_board, Move(self.id, self.x + i, self.y + j)):
                    moves_list.append(Move(self.id, self.x + i, self.y + j))
        return moves_list

    def is_valid_move(self, current_board, move):
        piece = None
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
        if abs(move.new_x - piece.x) > 1 or abs(move.new_y - piece.y) > 1:
            return False
        top_piece = current_board.get_top_piece(move.new_x, move.new_y)
        if top_piece is not None and top_piece.type == PieceType.Standing:
            return False

        return current_board.size > move.new_x >= 0 and current_board.size > move.new_y >= 0


class Board:
    def __init__(self, board=None):
        if board is None:
            self.size = 4
            self.pieces = []
            self.next_piece_id = 0
            self.available_pieces = {
                PlayerType.Human: {PieceType.Flat: 13, PieceType.Standing: 2},
                PlayerType.Computer: {PieceType.Flat: 13, PieceType.Standing: 2}
            }
        else:
            self.size = board.size
            self.pieces = [Piece(p.x, p.y, p.id, p.player, p.type) for p in board.pieces]
            self.next_piece_id = board.next_piece_id
            self.available_pieces = {
                PlayerType.Human: dict(board.available_pieces[PlayerType.Human]),
                PlayerType.Computer: dict(board.available_pieces[PlayerType.Computer])
            }

    def get_top_piece(self, x, y):
        top_piece = None
        max_id = -1
        for p in self.pieces:
            if p.x == x and p.y == y and p.id > max_id:
                max_id = p.id
                top_piece = p
        return top_piece

    def longest_road_length(self, player):
        player_top_flats = {}
        for x in range(self.size):
            for y in range(self.size):
                p = self.get_top_piece(x, y)
                if p is not None and p.player == player and p.type == PieceType.Flat:
                    player_top_flats[(x, y)] = p

        max_length = 0

        def dfs_max_path(x, y, current_visited_path):
            nonlocal max_length

            current_path_length = len(current_visited_path)
            max_length = max(max_length, current_path_length)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nx, ny = x + dx, y + dy
                next_coord = (nx, ny)

                if next_coord in player_top_flats and next_coord not in current_visited_path:
                    new_visited_path = current_visited_path.copy()
                    new_visited_path.add(next_coord)

                    dfs_max_path(nx, ny, new_visited_path)

        for start_coord in player_top_flats.keys():
            dfs_max_path(start_coord[0], start_coord[1], {start_coord})

        return max_length

    def evaluation_function(self):
        human_score = self.longest_road_length(PlayerType.Human)
        computer_score = self.longest_road_length(PlayerType.Computer)
        return computer_score - human_score

    def make_move(self, move):
        next_board = Board(self)
        if move is not None:
            mover = next((p for p in next_board.pieces if p.id == move.piece_id), None)
            if mover is not None:
                start_x, start_y = mover.x, mover.y
                target_x, target_y = move.new_x, move.new_y
                pieces_in_stack = [p for p in next_board.pieces if p.x == start_x and p.y == start_y]
                for piece in pieces_in_stack:
                    piece.x = target_x
                    piece.y = target_y
                mover.id = next_board.next_piece_id
                next_board.next_piece_id += 1
        return next_board

    def place_piece(self, x, y, player, piece_type):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return None
        if self.available_pieces[player][piece_type] <= 0:
            return None
        top_piece = self.get_top_piece(x, y)
        if top_piece is not None:
            return None
        new_board = Board(self)
        new_piece = Piece(x, y, new_board.next_piece_id, player, piece_type)
        new_board.pieces.append(new_piece)
        new_board.next_piece_id += 1
        new_board.available_pieces[player][piece_type] -= 1
        return new_board

    def is_position_empty(self, x, y):
        return self.get_top_piece(x, y) is None

    def has_pieces_available(self, player):
        return any(count > 0 for count in self.available_pieces[player].values())

    def has_road(self, player):
        size = self.size
        player_top_flats = {}
        for x_coord in range(size):
            for y_coord in range(size):
                p = self.get_top_piece(x_coord, y_coord)
                if p is not None and p.player == player and p.type == PieceType.Flat:
                    player_top_flats[(x_coord, y_coord)] = p
        visited_y = set()
        queue_y = []
        for coord, p in player_top_flats.items():
            if p.y == 0:
                queue_y.append(coord)
        while queue_y:
            x, y = queue_y.pop(0)
            if (x, y) in visited_y:
                continue
            visited_y.add((x, y))
            if y == size - 1:
                return True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nx, ny = x + dx, y + dy
                next_coord = (nx, ny)
                if next_coord in player_top_flats and next_coord not in visited_y:
                    queue_y.append(next_coord)
        visited_x = set()
        queue_x = []

        for coord, p in player_top_flats.items():
            if p.x == 0:
                queue_x.append(coord)
        while queue_x:
            x, y = queue_x.pop(0)
            if (x, y) in visited_x:
                continue
            visited_x.add((x, y))
            if x == size - 1:
                return True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nx, ny = x + dx, y + dy
                next_coord = (nx, ny)
                if next_coord in player_top_flats and next_coord not in visited_x:
                    queue_x.append(next_coord)

        return False

    def check_finish(self):
        finished = False
        winner = PlayerType.NoPlayer
        if self.has_road(PlayerType.Human):
            finished = True
            winner = PlayerType.Human
            return finished, winner
        if self.has_road(PlayerType.Computer):
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
        if maximizing:
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