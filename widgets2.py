from PySide6.QtCore import Qt, QAbstractTableModel, QVariantAnimation, QModelIndex
from PySide6.QtWidgets import (
    QApplication,
    QTabWidget,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QWidget,
    QLabel,
    QLineEdit,
    QDialog,
)
import pandas as pd
import json
import requests


class Login(QDialog):
    def __init__(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.handle_login)


class CSVViewer2(QMainWindow):
    '''
    variables

    '''

    def __init__(self):
        super().__init__()

        # Matching Mentees Tab for Assigning Junior Mentors to Mentees

        self.mentors_df = None
        self.mentees_df = None

        self.setWindowTitle("Mentor Matcher")
        self.setGeometry(100, 100, 800, 600)

        tab_widget = QTabWidget(self)
        self.setCentralWidget(tab_widget)

        self.match_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.match_layout)

        # figure out what to do with this
        self.table_widget = QTableWidget()
        self.match_layout.addWidget(self.table_widget)

        match_button_layout = QVBoxLayout()

        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_data)
        match_button_layout.addWidget(self.process_button)

        self.load_mentors_button = QPushButton("Load Mentors data")
        self.load_mentors_button.clicked.connect(self.load_mentors_csv)
        match_button_layout.addWidget(self.load_mentors_button)

        self.load_mentees_button = QPushButton("Load Mentees data")
        self.load_mentees_button.clicked.connect(self.load_mentees_csv)
        match_button_layout.addWidget(self.load_mentees_button)

        self.save_matched_button = QPushButton("Save Matched Mentees")
        self.save_matched_button.clicked.connect(self.save_matched_mentees_csv)
        match_button_layout.addWidget(self.save_matched_button)

        self.match_layout.addLayout(match_button_layout)

        self.status_label = QLabel()
        self.match_layout.addWidget(self.status_label)

        # Cohort Model Tab for Processing Cohort Reccomendation

        self.cohort_widget = QWidget()

        cohort_button_layout = QVBoxLayout()

        self.cohort_table_widget = QTableWidget()
        cohort_button_layout.addWidget(self.cohort_table_widget)

        self.process_cohorts_button = QPushButton("Process Cohort")
        self.process_cohorts_button.clicked.connect(
            self.process_cohort_matching)
        cohort_button_layout.addWidget(self.process_cohorts_button)

        self.cohort_load_mentees = QPushButton("Load Mentees Data")
        self.cohort_load_mentees.clicked.connect(self.load_mentees_csv)
        cohort_button_layout.addWidget(self.cohort_load_mentees)

        self.save_cohort_reccomendations = QPushButton(
            "Save Reccomended Cohorts")
        self.save_cohort_reccomendations.clicked.connect(self.saveReccomended)
        cohort_button_layout.addWidget(self.save_cohort_reccomendations)

        self.status_label_cohorts = QLabel()
        cohort_button_layout.addWidget(self.status_label_cohorts)

        self.cohort_widget.setLayout(cohort_button_layout)

        # At the end adding all the widgets into their own seperate tabs

        tab_widget.addTab(self.central_widget, "Match Mentees")
        tab_widget.addTab(self.cohort_widget, "Cohort Matching")

        # Applying styles to the GUI

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222;
            }
            QTabWidget::pane {
                border: 1px solid #c4c4c3;
                background: #222;
                padding: 10px;
            }
            QTabBar::tab {
                background: #222;
                border: 1px solid #c4c4c3;
                border-radius: 10px;
                padding: 10px;
                margin-top: 10px;
            }
            QTabBar::tab:selected {
                background: #444;
                border-bottom-color: #222;
            }
            QTableWidget {
                gridline-color: #fff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #5a9bd4;
                color: white;
                font-size: 16px;
                padding: 8px;
                border: none;
                border-radius: 5px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #7db7e3;
            }
            QPushButton:pressed {
                background-color: #497aab;
            }
            QLabel {
                color: #fff;
                font-size: 14px;
                margin: 10px 0;
            }
        """)

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
        print("Mentors data loaded")

    def load_mentees_csv(self):
        self.mentees_df = self.load_csv()
        print("Mentees data loaded")

    def process_data(self):
        '''post request to backend'''

        if self.mentors_df is None or self.mentees_df is None:
            self.status_label.setText(
                "Can not process without uploading both CSVs")
            return

        self.status_label.setText("Data processing in progress...")

        # make a request to  /csv
        data = dict()
        mentor_data = self.convert_csv_to_json(self.mentors_df)
        mentee_data = self.convert_csv_to_json(self.mentees_df)
        data['mentor'] = mentor_data
        data['mentee'] = mentee_data

        # print(data)

        # current port 5001
        self.response = requests.post('http://0.0.0.0:5001/csv', json=data)

        print(type(self.response))
        print(self.response)

        if self.response.json() is not None:
            self.matched_mentee_df = pd.DataFrame(
                json.loads(self.response.json()['matches']))
            self.mentor_assigned_info = pd.DataFrame(
                json.loads(self.response.json()['info']))

            print("Successful creation of matched_mentee dataframe")
            self.status_label.setText(
                "Successful Creation of Dataframe, Able to save as CSV file")

        else:
            print("Dataframe creation not successful")

    def process_cohort_matching(self):

        if self.mentees_df is None:
            self.status_label_cohorts.setText(
                "Can not process without uploading the Mentors CSV File")
            return

        self.status_label_cohorts.setText("Data processing in progress...")

        data = dict()
        mentee_data = self.convert_csv_to_json(self.mentees_df)
        data['mentee'] = mentee_data

        # Should return data really to be put into a dataframe
        self.response = requests.post('http://0.0.0.0:5001/cohorts', json=data)

        if self.response.json() is not None:
            self.cohort_reccomended_df = pd.DataFrame(
                json.loads(self.response.json()['reccomended']))
            print("Successful creation of cohort Reccomendations")
            self.status_label_cohorts.setText(
                "Successful creation of Cohort Reccomendation Dataframe")

    def convert_csv_to_json(self, input_data):
        # convert the csv data to json format
        jsonified_dataframe = input_data.to_json()

        return jsonified_dataframe

    def save_matched_mentees_csv(self):
        if hasattr(self, "matched_mentee_df") and self.matched_mentee_df is not None:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save CSV File", "", "CSV Files (*.csv)"
            )
            if file_name:
                try:
                    self.matched_mentee_df.to_csv(file_name, index=True)
                    self.status_label.setText(
                        f"Matched mentee data saved to {file_name}")
                except Exception as e:
                    self.status_label.setText(f"Error saving file: {e}")
        else:
            self.status_label.setText("No matched mentee data to save.")

        if hasattr(self, "mentor_assigned_info") and self.mentor_assigned_info is not None:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save CSV File", "", "CSV Files (*.csv)")
            if file_name:
                try:
                    self.mentor_assigned_info.to_csv(file_name, index=False)
                except Exception as e:
                    self.status_label.setText(f"Error saving file: {e}")

        self.mentees_df = None
        self.mentors_df = None

    def saveReccomended(self):
        if hasattr(self, "cohort_reccomended_df") and self.cohort_reccomended_df is not None:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save CSV File", "", "CSV Files (*.csv)"
            )
            if file_name:
                try:
                    self.cohort_reccomended_df.to_csv(file_name, index=True)
                    self.status_label_cohorts.setText(
                        f"cohort Reccomendations csv saved to {file_name}"
                    )
                except Exception as e:
                    self.status_label_cohorts.setText(
                        f"Error saving file: {e}")
        else:
            self.status_label_cohorts.setText(
                "No matched mentee data to save.")
