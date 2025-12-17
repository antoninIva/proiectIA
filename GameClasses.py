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
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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
        if abs(move.new_x - piece.x) + abs(move.new_y - piece.y) != 1:
            return False

        top_piece = current_board.get_top_piece(piece.x, piece.y)
        if top_piece is None or top_piece.id != piece.id:
            return False

        target_top_piece = current_board.get_top_piece(move.new_x, move.new_y)

        if target_top_piece is not None and target_top_piece.type == PieceType.Standing:
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

    def is_position_empty(self, x, y):
        return self.get_top_piece(x, y) is None

    def evaluation_function(self):
        fin, win = self.check_finish()
        if fin:
            if win == PlayerType.Computer:
                return 100000
            elif win == PlayerType.Human:
                return -100000

        score = 0

        computer_flats = 0
        human_flats = 0

        center_coords = [(1, 1), (1, 2), (2, 1), (2, 2)]

        for x in range(self.size):
            for y in range(self.size):
                p = self.get_top_piece(x, y)
                if p:
                    val = 10
                    if (x, y) in center_coords:
                        val += 5

                    if p.player == PlayerType.Computer:
                        if p.type == PieceType.Flat:
                            computer_flats += val
                    elif p.player == PlayerType.Human:
                        if p.type == PieceType.Flat:
                            human_flats += val

        score += (computer_flats - human_flats)

        computer_road = self.longest_road_length(PlayerType.Computer)
        human_road = self.longest_road_length(PlayerType.Human)

        score += (computer_road * 20) - (human_road * 20)

        return score

    def longest_road_length(self, player):
        player_top_flats = set()
        for x in range(self.size):
            for y in range(self.size):
                p = self.get_top_piece(x, y)
                if p is not None and p.player == player and p.type == PieceType.Flat:
                    player_top_flats.add((x, y))

        if not player_top_flats:
            return 0

        visited = set()
        max_len = 0

        for start_node in player_top_flats:
            if start_node not in visited:
                q = [start_node]
                local_visited = {start_node}
                count = 0
                while q:
                    cx, cy = q.pop(0)
                    count += 1
                    visited.add((cx, cy))

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in player_top_flats and (nx, ny) not in local_visited:
                            local_visited.add((nx, ny))
                            q.append((nx, ny))

                if count > max_len:
                    max_len = count

        return max_len

    def make_move(self, move):
        next_board = Board(self)
        if move is not None:
            mover = next((p for p in next_board.pieces if p.id == move.piece_id), None)

            if mover is not None:
                start_x, start_y = mover.x, mover.y
                target_x, target_y = move.new_x, move.new_y

                moving_stack = [p for p in next_board.pieces if p.x == start_x and p.y == start_y]
                moving_stack.sort(key=lambda p: p.id)

                target_stack = [p for p in next_board.pieces if p.x == target_x and p.y == target_y]

                max_dest_id = -1
                if target_stack:
                    max_dest_id = max(p.id for p in target_stack)

                base_new_id = max(max_dest_id, next_board.next_piece_id - 1) + 1

                for p in moving_stack:
                    p.x = target_x
                    p.y = target_y
                    p.id = base_new_id
                    base_new_id += 1

                next_board.next_piece_id = base_new_id

        return next_board

    def place_piece(self, x, y, player, piece_type):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return None
        if self.available_pieces[player][piece_type] <= 0:
            return None
        if not self.is_position_empty(x, y):
            return None

        new_board = Board(self)
        new_piece = Piece(x, y, new_board.next_piece_id, player, piece_type)
        new_board.pieces.append(new_piece)
        new_board.next_piece_id += 1
        new_board.available_pieces[player][piece_type] -= 1
        return new_board

    def has_pieces_available(self, player):
        return any(count > 0 for count in self.available_pieces[player].values())

    def has_road(self, player):
        size = self.size
        player_flats = set()

        for x in range(size):
            for y in range(size):
                p = self.get_top_piece(x, y)
                if p is not None and p.player == player and p.type == PieceType.Flat:
                    player_flats.add((x, y))

        if not player_flats:
            return False

        def check_connection(start_nodes, is_vertical):
            visited = set()
            queue = list(start_nodes)
            visited.update(start_nodes)

            while queue:
                cx, cy = queue.pop(0)

                if is_vertical:
                    if cy == size - 1: return True
                else:
                    if cx == size - 1: return True

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) in player_flats and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            return False

        start_vertical = [node for node in player_flats if node[1] == 0]
        if start_vertical and check_connection(start_vertical, is_vertical=True):
            return True

        start_horizontal = [node for node in player_flats if node[0] == 0]
        if start_horizontal and check_connection(start_horizontal, is_vertical=False):
            return True

        return False

    def check_finish(self):
        if self.has_road(PlayerType.Computer):
            return True, PlayerType.Computer
        if self.has_road(PlayerType.Human):
            return True, PlayerType.Human

        empty_spots = False
        for x in range(self.size):
            for y in range(self.size):
                if self.get_top_piece(x, y) is None:
                    empty_spots = True
                    break

        if not empty_spots:
            score = self.evaluation_function()
            return True, (PlayerType.Computer if score > 0 else PlayerType.Human)

        return False, PlayerType.NoPlayer

    def get_all_possible_next_boards(self, player):
        next_boards = []

        if self.has_pieces_available(player):
            for x in range(self.size):
                for y in range(self.size):
                    if self.is_position_empty(x, y):
                        if self.available_pieces[player][PieceType.Flat] > 0:
                            nb = self.place_piece(x, y, player, PieceType.Flat)
                            if nb: next_boards.append(nb)
                        if self.available_pieces[player][PieceType.Standing] > 0:
                            nb = self.place_piece(x, y, player, PieceType.Standing)
                            if nb: next_boards.append(nb)

        my_pieces = [p for p in self.pieces if p.player == player]
        for p in my_pieces:
            moves = p.valid_moves(self)
            for move in moves:
                nb = self.make_move(move)
                if nb: next_boards.append(nb)

        return next_boards


class Minimax:

    @staticmethod
    def find_next_board(current_board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True):
        finished, winner = current_board.check_finish()
        if finished or depth == 0:
            return current_board

        best_board = None

        if maximizing:
            max_eval = float('-inf')
            possible_boards = current_board.get_all_possible_next_boards(PlayerType.Computer)

            if not possible_boards:
                return current_board

            for next_board_state in possible_boards:
                result = Minimax.find_next_board(
                    next_board_state, depth - 1, alpha, beta, False
                )
                eval_score = result.evaluation_function()

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_board = next_board_state

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            return best_board if best_board else current_board

        else:
            min_eval = float('inf')
            possible_boards = current_board.get_all_possible_next_boards(PlayerType.Human)

            if not possible_boards:
                return current_board

            for next_board_state in possible_boards:
                result = Minimax.find_next_board(
                    next_board_state, depth - 1, alpha, beta, True
                )
                eval_score = result.evaluation_function()

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_board = next_board_state

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            return best_board if best_board else current_board