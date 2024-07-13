import sys
from PySide6.QtWidgets import QApplication
from widgets2 import CSVViewer2


def main():
    app = QApplication(sys.argv)
    widget = CSVViewer2()
    widget.show()
    app.exec()

# def main():
#     app = QApplication(sys.argv)

#     # Show login dialog
#     login_dialog = LoginDialog()
#     if login_dialog.exec() == QDialog.Accepted:
#         username, password = login_dialog.get_credentials()
#         # Here you should check the credentials
#         if username == "admin" and password == "password":  # Dummy check
#             widget = CSVViewer2()
#             widget.show()
#             sys.exit(app.exec_())
#         else:
#             sys.exit()  # Exit if credentials are wrong
#     else:
#         sys.exit()  # Exit if login dialog is cancelled


if __name__ == "__main__":
    main()
