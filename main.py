from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, QLineEdit, \
    QPushButton, QWidget, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        # Sub Menu ( Actions )
        add_student_action = QAction("Add Student", self)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Calling load_data function here
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            # insert empty row
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                # add coordinates row , column and class
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            print(row_data)
        connection.close()


app = QApplication(sys.argv)
student_data = MainWindow()
student_data.show()
sys.exit(app.exec())