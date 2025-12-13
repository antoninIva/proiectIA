import sys
from PyQt6.QtWidgets import QApplication
from ui.game_window import TakGameWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TakGameWindow()
    window.show()
    sys.exit(app.exec())
