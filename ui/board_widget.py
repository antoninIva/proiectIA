from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF, QPropertyAnimation, QEasingCurve, QObject, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient
from GameClasses import Board, PlayerType, PieceType, Move


class AnimatedPiece(QObject):
    def __init__(self, piece_id, x, y):
        super().__init__()
        self.piece_id = piece_id
        self._x = x
        self._y = y

    @pyqtProperty(float)
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @pyqtProperty(float)
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class BoardWidget(QWidget):
    pieceClicked = pyqtSignal(int)
    moveRequested = pyqtSignal(object)

    BOARD_SIZE = 600
    CELL_SIZE = BOARD_SIZE // 4
    PIECE_MARGIN = 10

    def __init__(self, board=None):
        super().__init__()
        self.board = board if board else Board()
        self.selected_piece_id = None
        self.valid_moves = []
        self.animated_pieces = {}
        self.animation_running = False

        self.setMinimumSize(self.BOARD_SIZE, self.BOARD_SIZE)
        self.setMaximumSize(self.BOARD_SIZE, self.BOARD_SIZE)

    def set_board(self, board):
        self.board = board
        self.selected_piece_id = None
        self.valid_moves = []
        self.update()

    def set_selected_piece(self, piece_id):
        self.selected_piece_id = piece_id

        if piece_id is not None:
            piece = None
            for p in self.board.pieces:
                if p.id == piece_id:
                    piece = p
                    break

            if piece:
                self.valid_moves = piece.valid_moves(self.board)
            else:
                self.valid_moves = []
        else:
            self.valid_moves = []

        self.update()

    def clear_selection(self):
        self.selected_piece_id = None
        self.valid_moves = []
        self.update()

    def animate_move(self, move, callback=None):
        self.animation_running = True

        piece = None
        for p in self.board.pieces:
            if p.id == move.piece_id:
                piece = p
                break

        if not piece:
            self.animation_running = False
            if callback:
                callback()
            return

        animated = AnimatedPiece(piece.id, piece.x, piece.y)
        self.animated_pieces[piece.id] = animated

        animation = QPropertyAnimation(animated, b"x")
        animation.setDuration(300)
        animation.setStartValue(float(piece.x))
        animation.setEndValue(float(move.new_x))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        animation_y = QPropertyAnimation(animated, b"y")
        animation_y.setDuration(300)
        animation_y.setStartValue(float(piece.y))
        animation_y.setEndValue(float(move.new_y))
        animation_y.setEasingCurve(QEasingCurve.Type.OutCubic)

        def on_finished():
            self.animated_pieces.pop(piece.id, None)
            self.animation_running = False
            if callback:
                callback()
            self.update()

        animation.finished.connect(on_finished)
        animation.valueChanged.connect(lambda: self.update())
        animation_y.valueChanged.connect(lambda: self.update())

        animation.start()
        animation_y.start()

        self._current_animation = animation
        self._current_animation_y = animation_y

    def mousePressEvent(self, event):
        if self.animation_running:
            return

        x = event.pos().x() // self.CELL_SIZE
        y = 3 - (event.pos().y() // self.CELL_SIZE)

        # verifica daca mutarea e valida
        if self.selected_piece_id is not None:
            for move in self.valid_moves:
                if move.new_x == x and move.new_y == y:
                    self.moveRequested.emit(move)
                    return

        # verifica daca a apasat pe o piesca
        for piece in self.board.pieces:
            if piece.x == x and piece.y == y:
                self.pieceClicked.emit(piece.id)
                return

        # daca a apasat pe un spatiu nepermis dispare selectia
        self.clear_selection()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._draw_board(painter)

        self._draw_valid_move_indicators(painter)

        self._draw_pieces(painter)

    def _draw_board(self, painter):
        for row in range(4):
            for col in range(4):
                if (row + col) % 2 == 0:
                    color = QColor("#FFFFFF")
                else:
                    color = QColor("#E3F2FD")

                painter.fillRect(
                    col * self.CELL_SIZE,
                    row * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                    color
                )

        pen = QPen(QColor("#BDBDBD"), 2)
        painter.setPen(pen)

        for i in range(5):
            painter.drawLine(
                i * self.CELL_SIZE, 0,
                i * self.CELL_SIZE, self.BOARD_SIZE
            )
            painter.drawLine(
                0, i * self.CELL_SIZE,
                self.BOARD_SIZE, i * self.CELL_SIZE
            )

    def _draw_valid_move_indicators(self, painter):
        if not self.valid_moves:
            return

        for move in self.valid_moves:
            center_x = move.new_x * self.CELL_SIZE + self.CELL_SIZE // 2
            center_y = (3 - move.new_y) * self.CELL_SIZE + self.CELL_SIZE // 2

            color = QColor("#4CAF50")
            color.setAlpha(100)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)

            radius = 20
            painter.drawEllipse(
                QPointF(center_x, center_y),
                radius, radius
            )

    def _draw_pieces(self, painter):
        for piece in self.board.pieces:
            if piece.id in self.animated_pieces:
                animated = self.animated_pieces[piece.id]
                draw_x = animated.x
                draw_y = animated.y
            else:
                draw_x = piece.x
                draw_y = piece.y

            pixel_x = int(draw_x * self.CELL_SIZE + self.PIECE_MARGIN)
            pixel_y = int((3 - draw_y) * self.CELL_SIZE + self.PIECE_MARGIN)
            pixel_width = self.CELL_SIZE - 2 * self.PIECE_MARGIN

            if piece.type == PieceType.Flat:
                pixel_height = pixel_width  
            else:  
                pixel_height = pixel_width // 2  

            if piece.player == PlayerType.Computer:
                gradient = QLinearGradient(pixel_x, pixel_y, pixel_x, pixel_y + pixel_height)
                gradient.setColorAt(0, QColor("#E53935"))  # rosu deschis
                gradient.setColorAt(1, QColor("#C62828"))  # rosu inchis
                brush = QBrush(gradient)
                border_color = QColor("#B71C1C")
            else: 
                gradient = QLinearGradient(pixel_x, pixel_y, pixel_x, pixel_y + pixel_height)
                gradient.setColorAt(0, QColor("#2196F3"))  # albastru deschis
                gradient.setColorAt(1, QColor("#1565C0"))  # albastru inchis
                brush = QBrush(gradient)
                border_color = QColor("#0D47A1")

            if piece.id == self.selected_piece_id:
                border_color = QColor("#FFC107")
                border_width = 4
            else:
                border_width = 2

            painter.setPen(QPen(border_color, border_width))
            painter.setBrush(brush)
            painter.drawRoundedRect(
                pixel_x, pixel_y,
                pixel_width, pixel_height,
                8, 8  
            )
