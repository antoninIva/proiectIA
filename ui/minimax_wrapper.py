
from GameClasses import Minimax, PlayerType, PieceType
from .action import generate_all_actions, ActionType


class MinimaxWithPlacement:


    @staticmethod
    def find_best_action(board, depth, player):
        all_actions = generate_all_actions(board, player)

        player_name = "Human" if player == PlayerType.Human else "Computer"
        print(f"\n[DEBUG AI] {player_name} find_best_action: {len(all_actions)} actiuni posibile")

        if not all_actions:
            print(f"[DEBUG AI] {player_name}: NU sunt actiuni disponibile!")
            return None

        best_action = None
        best_score = float('-inf') if player == PlayerType.Computer else float('inf')

        for action in all_actions:
            temp_board = action.apply_to_board(board)
            if temp_board is None:
                continue

            if depth > 1:
                result_board = Minimax.find_next_board(
                    temp_board,
                    depth - 1,
                    float('-inf'),
                    float('inf'),
                    player == PlayerType.Computer
                )
                score = result_board.evaluation_function()
            else:
                score = temp_board.evaluation_function()

            if player == PlayerType.Computer:
                if score > best_score:
                    best_score = score
                    best_action = action
            else:
                if score < best_score:
                    best_score = score
                    best_action = action

        if best_action:
            print(f"[DEBUG AI] {player_name} alege: {best_action} (score={best_score})")
        else:
            print(f"[DEBUG AI] {player_name}: Nu s-a gasit best_action, folosesc prima actiune")

        return best_action

    @staticmethod
    def find_best_board(board, depth, player=PlayerType.Computer):
       
        best_action = MinimaxWithPlacement.find_best_action(board, depth, player)

        if best_action is None:
            return board

        new_board = best_action.apply_to_board(board)
        return new_board if new_board is not None else board


class FastPlacementAI:

    @staticmethod
    def suggest_placement(board, player):

        if not board.has_pieces_available(player):
            return None

        priority_positions = [
            (1, 1), (2, 1), (1, 2), (2, 2),  # Centru
            (0, 1), (0, 2), (3, 1), (3, 2),  # Lateral
            (1, 0), (2, 0), (1, 3), (2, 3),  # Lateral vertical
            (0, 0), (0, 3), (3, 0), (3, 3)   # Colturi 
        ]

        for x, y in priority_positions:
            if board.is_position_empty(x, y):
                if board.available_pieces[player][PieceType.Flat] > 0:
                    return (x, y, PieceType.Flat)
                elif board.available_pieces[player][PieceType.Standing] > 0:
                    return (x, y, PieceType.Standing)

        for x in range(4):
            for y in range(4):
                if board.is_position_empty(x, y):
                    if board.available_pieces[player][PieceType.Flat] > 0:
                        return (x, y, PieceType.Flat)
                    elif board.available_pieces[player][PieceType.Standing] > 0:
                        return (x, y, PieceType.Standing)

        return None
