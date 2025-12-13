from PyQt6.QtCore import QObject, QRunnable, pyqtSignal
from GameClasses import Minimax


class WorkerSignals(QObject):
    """Signals for MinimaxWorker to communicate with main thread"""
    finished = pyqtSignal(object)  # Emits the resulting board
    error = pyqtSignal(str)  # Emits error message if something goes wrong


class MinimaxWorker(QRunnable):
    """Worker thread for running Minimax algorithm without blocking UI"""

    def __init__(self, board, depth=3):
        super().__init__()
        self.board = board
        self.depth = depth
        self.signals = WorkerSignals()

    def run(self):
        """Execute Minimax algorithm in background thread"""
        try:
            result_board = Minimax.find_next_board(self.board, self.depth)
            self.signals.finished.emit(result_board)
        except Exception as e:
            self.signals.error.emit(str(e))
