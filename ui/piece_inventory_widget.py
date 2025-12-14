
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QPen, QFont
from GameClasses import PieceType, PlayerType


class PieceButton(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, piece_type, parent=None):
        super().__init__(parent)
        self.piece_type = piece_type
        self.count = 0
        self.selected = False
        self.setFixedSize(100, 100)
        self.setToolTip(self._get_tooltip())

    def _get_tooltip(self):
        type_name = "Flat" if self.piece_type == PieceType.Flat else "Standing"
        return f"{type_name} Piece\nClick to select for placement"

    def set_count(self, count):
        self.count = count
        self.update()

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def mousePressEvent(self, event):
        if self.count > 0:
            self.clicked.emit(self.piece_type)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.selected:
            painter.fillRect(self.rect(), QColor(33, 150, 243, 40))

        if self.selected:
            painter.setPen(QPen(QColor(33, 150, 243), 3))
            painter.drawRect(2, 2, self.width() - 4, self.height() - 4)

        center_x = self.width() // 2
        center_y = self.height() // 2 - 10

        if self.piece_type == PieceType.Flat:
            self._draw_flat_piece(painter, center_x, center_y)
        else:
            self._draw_standing_piece(painter, center_x, center_y)

        font = QFont("Arial", 14, QFont.Weight.Bold)
        painter.setFont(font)

        if self.count > 0:
            painter.setPen(QColor(0, 0, 0))
        else:
            painter.setPen(QColor(150, 150, 150))

        count_text = str(self.count)
        painter.drawText(0, self.height() - 20, self.width(), 20,
                        Qt.AlignmentFlag.AlignCenter, count_text)

        font_small = QFont("Arial", 10)
        painter.setFont(font_small)
        painter.setPen(QColor(100, 100, 100))
        type_name = "Flat" if self.piece_type == PieceType.Flat else "Standing"
        painter.drawText(0, 5, self.width(), 15,
                        Qt.AlignmentFlag.AlignCenter, type_name)

    def _draw_flat_piece(self, painter, x, y):
        radius = 20

        gradient = QRadialGradient(x, y, radius)
        if self.count > 0:
            gradient.setColorAt(0, QColor(33, 150, 243))
            gradient.setColorAt(1, QColor(21, 101, 192))
            painter.setPen(QPen(QColor(13, 71, 161), 2))
        else:
            gradient.setColorAt(0, QColor(200, 200, 200))
            gradient.setColorAt(1, QColor(150, 150, 150))
            painter.setPen(QPen(QColor(100, 100, 100), 2))

        painter.setBrush(gradient)
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    def _draw_standing_piece(self, painter, x, y):
        width = 30
        height = 40

        if self.count > 0:
            painter.setBrush(QColor(13, 71, 161))
            painter.setPen(QPen(QColor(0, 0, 0), 2))
        else:
            painter.setBrush(QColor(150, 150, 150))
            painter.setPen(QPen(QColor(100, 100, 100), 2))

        painter.drawRect(x - width // 2, y - height // 2, width, height)


class PieceInventoryWidget(QWidget):
    pieceTypeSelected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_piece_type = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel("Piese Disponibile")
        title_font = QFont("Arial", 12, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        pieces_layout = QHBoxLayout()
        pieces_layout.setSpacing(10)

        self.flat_button = PieceButton(PieceType.Flat)
        self.flat_button.clicked.connect(self._on_piece_clicked)
        pieces_layout.addWidget(self.flat_button)

        self.standing_button = PieceButton(PieceType.Standing)
        self.standing_button.clicked.connect(self._on_piece_clicked)
        pieces_layout.addWidget(self.standing_button)

        layout.addLayout(pieces_layout)

        self.info_label = QLabel("Selectati o piesa pentru plasare")
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(self.info_label)

        self.deselect_button = QPushButton("Anuleaza Selectia")
        self.deselect_button.clicked.connect(self._on_deselect)
        self.deselect_button.setEnabled(False)
        self.deselect_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #888;
            }
        """)
        layout.addWidget(self.deselect_button)

        layout.addStretch()
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border-radius: 5px;
            }
        """)

    def update_counts(self, available_pieces, player):
        if player not in available_pieces:
            return

        flat_count = available_pieces[player].get(PieceType.Flat, 0)
        standing_count = available_pieces[player].get(PieceType.Standing, 0)

        self.flat_button.set_count(flat_count)
        self.standing_button.set_count(standing_count)

        if self.selected_piece_type is not None:
            if self.selected_piece_type == PieceType.Flat and flat_count == 0:
                self.clear_selection()
            elif self.selected_piece_type == PieceType.Standing and standing_count == 0:
                self.clear_selection()

    def _on_piece_clicked(self, piece_type):
        if self.selected_piece_type == piece_type:
            self.clear_selection()
        else:
            self.selected_piece_type = piece_type
            self._update_selection_ui()
            self.deselect_button.setEnabled(True)
            self.pieceTypeSelected.emit(piece_type)

            type_name = "Flat" if piece_type == PieceType.Flat else "Standing"
            self.info_label.setText(f"Selectat: {type_name}\nClick pe board pentru plasare")

    def _on_deselect(self):
        self.clear_selection()

    def clear_selection(self):
        self.selected_piece_type = None
        self._update_selection_ui()
        self.deselect_button.setEnabled(False)
        self.info_label.setText("Selectati o piesa pentru plasare")
        self.pieceTypeSelected.emit(-1)  # -1 = no selection

    def _update_selection_ui(self):
        self.flat_button.set_selected(self.selected_piece_type == PieceType.Flat)
        self.standing_button.set_selected(self.selected_piece_type == PieceType.Standing)

    def get_selected_piece_type(self):
        return self.selected_piece_type

    def is_piece_selected(self):
        return self.selected_piece_type is not None
