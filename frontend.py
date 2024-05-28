import sys
from PySide6.QtWidgets import QApplication
from widgets import CSVViewer


def main():

    app = QApplication(sys.argv)
    widget = CSVViewer()
    widget.show()
    app.exec()


if __name__ == "__main__":
    main()
