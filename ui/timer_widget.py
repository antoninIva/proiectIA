from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class TimerWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.human_time = 0
        self.computer_time = 0
        self.current_player = None

        self._setup_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)  

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        title = QLabel("Cronometru")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title.setFont(title_font)
        layout.addWidget(title)

        self.computer_label = QLabel("Calculator")
        self.computer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.computer_label)

        self.computer_time_label = QLabel("00:00")
        self.computer_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_font = QFont()
        time_font.setPointSize(18)
        time_font.setBold(True)
        self.computer_time_label.setFont(time_font)
        layout.addWidget(self.computer_time_label)

        separator = QLabel("─" * 20)
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(separator)

        self.human_label = QLabel("Jucator")
        self.human_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.human_label)

        self.human_time_label = QLabel("00:00")
        self.human_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.human_time_label.setFont(time_font)
        layout.addWidget(self.human_time_label)

        layout.addStretch()

        self.setLayout(layout)

    def _update_time(self):
        from GameClasses import PlayerType

        if self.current_player == PlayerType.Human:
            self.human_time += 1
            self._update_display()
        elif self.current_player == PlayerType.Computer:
            self.computer_time += 1
            self._update_display()

    def _update_display(self):
        self.human_time_label.setText(self._format_time(self.human_time))
        self.computer_time_label.setText(self._format_time(self.computer_time))

    def _format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def set_current_player(self, player):
        from GameClasses import PlayerType

        self.current_player = player

        if player == PlayerType.Human:
            self.human_label.setStyleSheet("color: #2196F3; font-weight: bold;")
            self.computer_label.setStyleSheet("color: #757575;")
        elif player == PlayerType.Computer:
            self.computer_label.setStyleSheet("color: #2196F3; font-weight: bold;")
            self.human_label.setStyleSheet("color: #757575;")
        else:
            self.human_label.setStyleSheet("color: #757575;")
            self.computer_label.setStyleSheet("color: #757575;")

    def reset(self):
        self.human_time = 0
        self.computer_time = 0
        self.current_player = None
        self._update_display()
        self.set_current_player(None)

    def pause(self):
        self.current_player = None
        self.set_current_player(None)
