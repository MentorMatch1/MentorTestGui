import sys
from PySide6.QtWidgets import QApplication
from widgets2 import CSVViewer2


def main():
    app = QApplication(sys.argv)
    widget = CSVViewer2()
    widget.show()
    app.exec()


if __name__ == "__main__":
    main()
