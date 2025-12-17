from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QSlider, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DifficultyDialog(QDialog):

    def __init__(self, current_depth=3, parent=None):
        super().__init__(parent)
        if current_depth > 5: current_depth = 5
        self.selected_depth = current_depth

        self.setWindowTitle("Setari Dificultate")
        self.setModal(True)
        self.setMinimumWidth(400)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Selecteaza Dificultatea")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "Nivelul de dificultate determina cat de mult gandeste calculatorul.\n"
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: #666;")
        layout.addWidget(description)

        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(10)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(4)

        slider_val = 2
        if self.selected_depth == 2:
            slider_val = 1
        elif self.selected_depth == 3:
            slider_val = 2
        elif self.selected_depth == 4:
            slider_val = 3
        elif self.selected_depth >= 5:
            slider_val = 4

        self.slider.setValue(slider_val)

        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._on_slider_changed)
        slider_layout.addWidget(self.slider)

        labels_layout = QHBoxLayout()
        labels = ["1", "2", "3", "4"]
        for label_text in labels:
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 10px; color: #999;")
            labels_layout.addWidget(label)
        slider_layout.addLayout(labels_layout)

        layout.addLayout(slider_layout)

        self.level_label = QLabel()
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        level_font = QFont()
        level_font.setPointSize(16)
        level_font.setBold(True)
        self.level_label.setFont(level_font)
        layout.addWidget(self.level_label)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("color: #555;")
        layout.addWidget(self.preview_label)

        self._on_slider_changed(slider_val)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_button = QPushButton("Anuleaza")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumHeight(35)
        button_layout.addWidget(cancel_button)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setMinimumHeight(35)
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _on_slider_changed(self, value):
        if value == 1:
            self.selected_depth = 2
            level_name = "Usor "
            level_color = "#4CAF50"
        elif value == 2:
            self.selected_depth = 3
            level_name = "Mediu "
            level_color = "#FF9800"
        elif value == 3:
            self.selected_depth = 4
            level_name = "Greu "
            level_color = "#F44336"
        else:
            self.selected_depth = 5
            level_name = "Expert "
            level_color = "#9C27B0"

        self.level_label.setText(level_name)
        self.level_label.setStyleSheet(f"color: {level_color};")

    def get_depth(self):
        return self.selected_depth