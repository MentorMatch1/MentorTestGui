from PySide6.QtCore import Qt, QAbstractTableModel, QVariantAnimation, QModelIndex
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QWidget,
    QLabel,
    QLineEdit,

)
import pandas as pd


class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mentor Matcher")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # figure out what to do with this
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        button_layout = QVBoxLayout()

        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_data)
        button_layout.addWidget(self.process_button)

        self.load_mentors_button = QPushButton("Load Mentors data")
        self.load_mentors_button.clicked.connect(self.load_mentors_csv)
        button_layout.addWidget(self.load_mentors_button)

        self.load_mentees_button = QPushButton("Load Mentees data")
        self.load_mentees_button.clicked.connect(self.load_mentees_csv)
        button_layout.addWidget(self.load_mentees_button)

        self.save_matched_button = QPushButton("Save Matched Mentees")
        self.save_matched_button.clicked.connect(self.save_matched_mentees_csv)
        button_layout.addWidget(self.save_matched_button)

        self.layout.addLayout(button_layout)

        self.mentors_df = None
        self.mentees_df = None

        self.status_label = QLabel()
        self.layout.addWidget(self.status_label)

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)"
        )
        if file_name:
            try:
                df = pd.read_csv(file_name, encoding="utf-8")
                return df
            except Exception as e:
                print("Error:", e)

    def load_mentors_csv(self):
        self.mentors_df = self.load_csv()

    def load_mentees_csv(self):
        self.mentees_df = self.load_csv()

    def process_data(self):
        '''post request to backend'''

        # process data here self.mentors_df / self.mentees_df
        # Implement your data processing logic here
        if self.mentors_df is None or self.mentees_df is None:
            self.status_label.setText(
                "Can not process without uploading both CSVs")

        # self.mentor_mentee_matrix

    def save_matched_mentees_csv(self):
        if hasattr(self, "matched_mentee_df") and self.matched_mentee_df is not None:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save CSV File", "", "CSV Files (*.csv)"
            )
            if file_name:
                try:
                    self.matched_mentee_df.to_csv(file_name, index=False)
                    self.status_label.setText(
                        f"Matched mentee data saved to {file_name}"
                    )
                except Exception as e:
                    self.status_label.setText(f"Error saving file: {e}")
        else:
            self.status_label.setText("No matched mentee data to save.")
