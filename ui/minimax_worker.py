from PyQt6.QtCore import QObject, QRunnable, pyqtSignal
from GameClasses import Minimax, PlayerType
from .minimax_wrapper import MinimaxWithPlacement


class WorkerSignals(QObject):
    finished = pyqtSignal(object) 
    error = pyqtSignal(str)  


class MinimaxWorker(QRunnable):

    def __init__(self, board, depth=3):
        super().__init__()
        self.board = board
        self.depth = depth
        self.signals = WorkerSignals()

    def run(self):
        try:
            result_board = MinimaxWithPlacement.find_best_board(
                self.board,
                self.depth,
                PlayerType.Computer
            )
            self.signals.finished.emit(result_board)
        except Exception as e:
            self.signals.error.emit(str(e))
