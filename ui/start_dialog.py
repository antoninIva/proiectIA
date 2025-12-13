from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QSlider, QPushButton, QRadioButton, QButtonGroup,
                              QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class StartDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.difficulty_depth = 3
        self.computer_starts = True

        self.setWindowTitle("Tak Master")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(450)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Tak Master")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2196F3; margin-bottom: 10px;")
        layout.addWidget(title)

        subtitle = QLabel("Minimax cu retezare alfa-beta")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        diff_frame = self._create_difficulty_section()
        layout.addWidget(diff_frame)

        first_player_frame = self._create_first_player_section()
        layout.addWidget(first_player_frame)

        layout.addStretch()

        start_button = QPushButton("Start Joc")
        start_button.clicked.connect(self.accept)
        start_button.setMinimumHeight(50)
        start_button.setDefault(True)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def _create_difficulty_section(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        section_title = QLabel("Dificultate")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        section_title.setFont(title_font)
        layout.addWidget(section_title)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(8)
        self.slider.setValue(self.difficulty_depth)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._on_difficulty_changed)
        layout.addWidget(self.slider)

        labels_layout = QHBoxLayout()
        labels = ["1", "2", "3", "4", "5", "6", "7", "8"]
        for label_text in labels:
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 10px; color: #999;")
            labels_layout.addWidget(label)
        layout.addLayout(labels_layout)

        self.level_label = QLabel()
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        level_font = QFont()
        level_font.setPointSize(14)
        level_font.setBold(True)
        self.level_label.setFont(level_font)
        layout.addWidget(self.level_label)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("color: #555; font-size: 12px;")
        layout.addWidget(self.preview_label)

        self._on_difficulty_changed(self.difficulty_depth)

        frame.setLayout(layout)
        return frame

    def _create_first_player_section(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        section_title = QLabel("Cine incepe?")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        section_title.setFont(title_font)
        layout.addWidget(section_title)

        self.button_group = QButtonGroup()

        self.computer_radio = QRadioButton("🔴 Calculator ")
        self.computer_radio.setChecked(True)
        self.computer_radio.setStyleSheet("font-size: 13px; padding: 5px;")
        self.button_group.addButton(self.computer_radio)
        layout.addWidget(self.computer_radio)

        self.human_radio = QRadioButton("🔵 Eu ")
        self.human_radio.setStyleSheet("font-size: 13px; padding: 5px;")
        self.button_group.addButton(self.human_radio)
        layout.addWidget(self.human_radio)

        frame.setLayout(layout)
        return frame

    def _on_difficulty_changed(self, value):
        self.difficulty_depth = value

        if value <= 2:
            level_name = "Usor"
            level_color = "#4CAF50"
        elif value <= 4:
            level_name = "Mediu"
            level_color = "#FF9800"
        elif value <= 6:
            level_name = "Greu"
            level_color = "#F44336"
        else:
            level_name = "Expert"
            level_color = "#9C27B0"

        self.level_label.setText(level_name)
        self.level_label.setStyleSheet(f"color: {level_color};")

        if value == 1:
            preview = "Calculatorul va gandi 1 mutare inainte"
        else:
            preview = f"Calculatorul va gandi {value} mutari inainte"

        self.preview_label.setText(preview)

    def get_settings(self):
        return {
            'difficulty': self.difficulty_depth,
            'computer_starts': self.computer_radio.isChecked()
        }
