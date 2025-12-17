from PyQt6.QtCore import QObject, QRunnable, pyqtSignal
from GameClasses import Minimax, PlayerType

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
            result_board = Minimax.find_next_board(
                self.board,
                self.depth,
                float('-inf'),
                float('inf'),
                True
            )
            self.signals.finished.emit(result_board)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.signals.error.emit(str(e))