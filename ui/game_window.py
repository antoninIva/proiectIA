from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                              QMessageBox, QMenuBar, QStatusBar)
from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtGui import QAction
from GameClasses import Board, PlayerType, Move, PieceType
from .board_widget import BoardWidget
from .timer_widget import TimerWidget
from .difficulty_dialog import DifficultyDialog
from .start_dialog import StartDialog
from .minimax_worker import MinimaxWorker
from .piece_inventory_widget import PieceInventoryWidget


class TakGameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.board = Board()
        self.current_player = PlayerType.Human
        self.difficulty_depth = 3
        self.computer_starts = True
        self.thread_pool = QThreadPool()

        self._setup_ui()
        self._apply_stylesheet()

        self._show_start_dialog()

        self.new_game()

    def _setup_ui(self):
        self.setWindowTitle("Tak Master")
        self.setMinimumSize(900, 700)

        self._create_menu_bar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.board_widget = BoardWidget(self.board)
        self.board_widget.pieceClicked.connect(self._on_piece_clicked)
        self.board_widget.moveRequested.connect(self._on_move_requested)
        self.board_widget.placementRequested.connect(self._on_placement_requested)
        main_layout.addWidget(self.board_widget)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(20)

        self.timer_widget = TimerWidget()
        right_panel.addWidget(self.timer_widget)

        self.inventory_widget = PieceInventoryWidget()
        self.inventory_widget.pieceTypeSelected.connect(self._on_piece_type_selected)
        right_panel.addWidget(self.inventory_widget)

        right_panel.addStretch()

        main_layout.addLayout(right_panel)

        central_widget.setLayout(main_layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status_bar()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        game_menu = menu_bar.addMenu("Joc")

        new_game_action = QAction("Joc Nou", self)
        new_game_action.triggered.connect(self.new_game)
        game_menu.addAction(new_game_action)

        difficulty_action = QAction("Dificultate...", self)
        difficulty_action.triggered.connect(self._show_difficulty_dialog)
        game_menu.addAction(difficulty_action)

        game_menu.addSeparator()

        exit_action = QAction("Iesire", self)
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Ajutor")

        about_action = QAction("Despre...", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _apply_stylesheet(self):
        stylesheet = """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #f5f5f5, stop:1 #e0e0e0);
            }

            QMenuBar {
                background-color: #2196F3;
                color: white;
                padding: 5px;
                font-size: 13px;
            }

            QMenuBar::item {
                background-color: transparent;
                padding: 5px 12px;
                border-radius: 4px;
            }

            QMenuBar::item:selected {
                background-color: rgba(255, 255, 255, 0.2);
            }

            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                padding: 5px;
            }

            QMenu::item {
                padding: 8px 25px;
                border-radius: 4px;
            }

            QMenu::item:selected {
                background-color: #E3F2FD;
                color: #2196F3;
            }

            QStatusBar {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 5px;
            }

            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1976D2;
            }

            QPushButton:pressed {
                background-color: #0D47A1;
            }

            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #1976D2;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background: #1976D2;
            }

            QDialog {
                background-color: white;
            }
        """
        self.setStyleSheet(stylesheet)

    def _update_status_bar(self):
        if self.current_player == PlayerType.Human:
            self.status_bar.showMessage("Randul tau")
        elif self.current_player == PlayerType.Computer:
            self.status_bar.showMessage("Calculatorul gandeste...")
        else:
            self.status_bar.showMessage("Joc terminat")

    def _show_start_dialog(self):
        dialog = StartDialog(self)
        result = dialog.exec()

        if not result:
            import sys
            sys.exit(0)

        settings = dialog.get_settings()
        self.difficulty_depth = settings['difficulty']
        self.computer_starts = settings['computer_starts']

    def new_game(self):
        self.board = Board()
        self.board_widget.set_board(self.board)
        self.board_widget.clear_selection()
        self.board_widget.set_placement_mode(None)
        self.inventory_widget.clear_selection()
        self.inventory_widget.update_counts(self.board.available_pieces, PlayerType.Human)
        self.timer_widget.reset()

        if self.computer_starts:
            self.current_player = PlayerType.Computer
            self.timer_widget.set_current_player(self.current_player)
            self._update_status_bar()
            self._make_computer_move()
        else:
            self.current_player = PlayerType.Human
            self.timer_widget.set_current_player(self.current_player)
            self._update_status_bar()

    def _show_difficulty_dialog(self):
        dialog = DifficultyDialog(self.difficulty_depth, self)
        if dialog.exec():
            self.difficulty_depth = dialog.get_depth()
            QMessageBox.information(
                self,
                "Dificultate Actualizata",
                "Schimbarea va fi aplicata în urmatorul joc."
            )

    def _show_about(self):
        QMessageBox.about(
            self,
            "Despre Tak Master",
            "Implementare Algoritmului Minimax cu retezare alfa-beta\n"
            "sub forma jocului Tak\n\n"
            "IA - Proiect"
        )

    def _on_piece_type_selected(self, piece_type):
        if piece_type == -1:
            self.board_widget.set_placement_mode(None)
        else:
            self.board_widget.set_placement_mode(piece_type)

    def _on_placement_requested(self, x, y, piece_type):
        if self.current_player != PlayerType.Human:
            return

        new_board = self.board.place_piece(x, y, PlayerType.Human, piece_type)
        if new_board is None:
            return

        self.board = new_board
        self.board_widget.set_board(self.board)
        self.board_widget.set_placement_mode(None)
        self.inventory_widget.clear_selection()
        self.inventory_widget.update_counts(self.board.available_pieces, PlayerType.Human)

        finished, winner = self.board.check_finish()
        if finished:
            self._handle_game_over(winner)
            return

        self.current_player = PlayerType.Computer
        self.timer_widget.set_current_player(self.current_player)
        self._update_status_bar()
        self._make_computer_move()

    def _on_piece_clicked(self, piece_id):
        if self.current_player != PlayerType.Human:
            return

        piece = None
        for p in self.board.pieces:
            if p.id == piece_id:
                piece = p
                break

        if not piece:
            return

        if piece.player == PlayerType.Human:
            self.board_widget.set_selected_piece(piece_id)
            self.inventory_widget.clear_selection()
        else:
            self.board_widget.clear_selection()

    def _on_move_requested(self, move):
        if self.current_player != PlayerType.Human:
            return

        piece = None
        for p in self.board.pieces:
            if p.id == move.piece_id:
                piece = p
                break

        if not piece or piece.player != PlayerType.Human:
            return

        if not piece.is_valid_move(self.board, move):
            return

        def after_animation():
            self.board = self.board.make_move(move)
            self.board_widget.set_board(self.board)
            self.inventory_widget.update_counts(self.board.available_pieces, PlayerType.Human)

            finished, winner = self.board.check_finish()
            if finished:
                self._handle_game_over(winner)
                return

            self.current_player = PlayerType.Computer
            self.timer_widget.set_current_player(self.current_player)
            self._update_status_bar()
            self._make_computer_move()

        self.board_widget.animate_move(move, after_animation)

    def _make_computer_move(self):
        worker = MinimaxWorker(self.board, self.difficulty_depth)
        worker.signals.finished.connect(self._on_computer_move_finished)
        worker.signals.error.connect(self._on_computer_move_error)
        self.thread_pool.start(worker)

    def _on_computer_move_finished(self, result_board):
        move = self._find_move_difference(self.board, result_board)

        if move:
            def after_animation():
                self.board = result_board
                self.board_widget.set_board(self.board)
                self.inventory_widget.update_counts(self.board.available_pieces, PlayerType.Human)

                finished, winner = self.board.check_finish()
                if finished:
                    self._handle_game_over(winner)
                    return

                self.current_player = PlayerType.Human
                self.timer_widget.set_current_player(self.current_player)
                self._update_status_bar()

            self.board_widget.animate_move(move, after_animation)
        else:
            self.board = result_board
            self.board_widget.set_board(self.board)
            self.inventory_widget.update_counts(self.board.available_pieces, PlayerType.Human)

            finished, winner = self.board.check_finish()
            if finished:
                self._handle_game_over(winner)
                return

            self.current_player = PlayerType.Human
            self.timer_widget.set_current_player(self.current_player)
            self._update_status_bar()

    def _on_computer_move_error(self, error_msg):
        QMessageBox.critical(
            self,
            "Eroare",
            f"Eroare in calculul mutarii: {error_msg}"
        )

    def _find_move_difference(self, old_board, new_board):
        for old_piece, new_piece in zip(old_board.pieces, new_board.pieces):
            if old_piece.x != new_piece.x or old_piece.y != new_piece.y:
                return Move(old_piece.id, new_piece.x, new_piece.y)
        return None

    def _handle_game_over(self, winner):
        self.current_player = PlayerType.NoPlayer
        self.timer_widget.pause()
        self._update_status_bar()

        if winner == PlayerType.Human:
            message = "Felicitari! Ai castigat!"
            title = "Victorie!"
        elif winner == PlayerType.Computer:
            message = "Calculatorul a castigat!"
            title = "Infrangere"
        else:
            message = "Joc terminat!"
            title = "Remiza"

        reply = QMessageBox.question(
            self,
            title,
            f"{message}\n\nVrei sa incepi un joc nou?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.new_game()
