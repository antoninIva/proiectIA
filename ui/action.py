
from GameClasses import PieceType, PlayerType


class ActionType:
    PLACEMENT = 0
    MOVEMENT = 1


class Action:

    def __init__(self, action_type, **kwargs):
        self.action_type = action_type

        if action_type == ActionType.PLACEMENT:
            self.x = kwargs['x']
            self.y = kwargs['y']
            self.player = kwargs['player']
            self.piece_type = kwargs['piece_type']
            self.move = None
        else:  # MOVEMENT
            self.move = kwargs['move']
            self.x = None
            self.y = None
            self.player = None
            self.piece_type = None

    def apply_to_board(self, board):
        if self.action_type == ActionType.PLACEMENT:
            return board.place_piece(self.x, self.y, self.player, self.piece_type)
        else:
            return board.make_move(self.move)

    def __str__(self):
        if self.action_type == ActionType.PLACEMENT:
            player_name = "Human" if self.player == PlayerType.Human else "Computer"
            piece_name = "Flat" if self.piece_type == PieceType.Flat else "Standing"
            return f"PLACEMENT: {player_name} {piece_name} at ({self.x},{self.y})"
        else:
            return f"MOVEMENT: piece {self.move.piece_id} to ({self.move.new_x},{self.move.new_y})"

    def __repr__(self):
        return self.__str__()


def generate_all_actions(board, player):
    actions = []

    if board.has_pieces_available(player):
        for x in range(board.size):
            for y in range(board.size):
                if board.is_position_empty(x, y):
                    for piece_type in [PieceType.Flat, PieceType.Standing]:
                        if board.available_pieces[player][piece_type] > 0:
                            actions.append(Action(
                                ActionType.PLACEMENT,
                                x=x,
                                y=y,
                                player=player,
                                piece_type=piece_type
                            ))

    for piece in board.pieces:
        if piece.player == player:
            for move in piece.valid_moves(board):
                actions.append(Action(ActionType.MOVEMENT, move=move))

    return actions


def count_actions_by_type(actions):
    placements = sum(1 for a in actions if a.action_type == ActionType.PLACEMENT)
    movements = sum(1 for a in actions if a.action_type == ActionType.MOVEMENT)
    return placements, movements
