from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QSlider,
                             QPushButton, QRadioButton, QButtonGroup,
                             QFrame, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class StartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tak Master - Configurare")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setMinimumWidth(450)

        self.selected_depth = 3
        self.computer_starts = True

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("Tak Master")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("mainTitle")
        layout.addWidget(title_label)

        subtitle = QLabel("Minimax cu retezare alfa-beta")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        diff_frame = QFrame()
        diff_frame.setObjectName("settingFrame")
        diff_layout = QVBoxLayout(diff_frame)

        diff_title = QLabel("Nivel Dificultate")
        diff_title.setObjectName("sectionTitle")
        diff_layout.addWidget(diff_title)


        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(4)
        self.slider.setValue(2)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._update_difficulty_label)
        diff_layout.addWidget(self.slider)

        self.diff_label = QLabel()
        self.diff_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.diff_label.setObjectName("statusLabel")
        diff_layout.addWidget(self.diff_label)


        self._update_difficulty_label(self.slider.value())

        layout.addWidget(diff_frame)


        player_frame = QFrame()
        player_frame.setObjectName("settingFrame")
        player_layout = QVBoxLayout(player_frame)

        player_title = QLabel("Cine incepe?")
        player_title.setObjectName("sectionTitle")
        player_layout.addWidget(player_title)

        radio_layout = QHBoxLayout()

        self.rb_computer = QRadioButton("Calculator (Rosu)")
        self.rb_computer.setChecked(True)
        self.rb_human = QRadioButton("Eu (Albastru)")

        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.rb_computer)
        self.btn_group.addButton(self.rb_human)

        radio_layout.addWidget(self.rb_computer)
        radio_layout.addWidget(self.rb_human)
        player_layout.addLayout(radio_layout)

        layout.addWidget(player_frame)

        layout.addStretch()

        self.start_btn = QPushButton("Start Joc")
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.clicked.connect(self.accept)
        self.start_btn.setMinimumHeight(50)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def _update_difficulty_label(self, value):
        if value == 1:
            self.selected_depth = 2
            text = "Usor (Adancime 2) - Instant"
            color = "#4CAF50"
        elif value == 2:
            self.selected_depth = 3
            text = "Mediu (Adancime 3) - Echilibrat"
            color = "#FF9800"
        elif value == 3:
            self.selected_depth = 4
            text = "Greu (Adancime 4) - Gandeste putin"
            color = "#F44336"
        else:
            self.selected_depth = 5
            text = "Expert (Adancime 5) - Lent & Precis"
            color = "#9C27B0"

        self.diff_label.setText(text)
        self.diff_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }

            QLabel#mainTitle {
                font-size: 28px;
                font-weight: bold;
                color: #2196F3;
                margin-bottom: 5px;
            }

            QLabel#subtitle {
                font-size: 14px;
                color: #757575;
                margin-bottom: 10px;
            }

            QFrame#settingFrame {
                background-color: #F5F5F5;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }

            QLabel#sectionTitle {
                font-size: 16px;
                font-weight: bold;
                color: #424242; 
            }

            QRadioButton {
                font-size: 14px;
                color: #333333; 
                padding: 5px;
            }

            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }

            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }

            QPushButton:hover {
                background-color: #1976D2;
            }

            QPushButton:pressed {
                background-color: #0D47A1;
            }

            /* Slider Styling */
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 10px;
                border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
                background: #2196F3;
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #2196F3;
                width: 24px;
                height: 24px;
                margin: -7px 0;
                border-radius: 12px;
            }
        """)

    def get_settings(self):
        return {
            'difficulty': self.selected_depth,
            'computer_starts': self.rb_computer.isChecked()
        }