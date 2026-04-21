import signal
import sys
import warnings

warnings.filterwarnings("ignore", message="Selected binding.*could not be found")
import qdarkstyle

from PySide6.QtWidgets import QApplication
from ui.windows.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    
    # Enable ctrl + c to close the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # Set the theme
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()