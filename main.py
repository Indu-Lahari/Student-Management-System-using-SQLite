from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QComboBox
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
        edit_menu = self.menuBar().addMenu("&Edit")

        # Sub Menu ( Actions )
        add_student_action = QAction("Add Student", self)
        # noinspection PyUnresolvedReferences
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        search_action = QAction("Search", self)
        # noinspection PyUnresolvedReferences
        search_action.triggered.connect(self.search)
        edit_menu.addAction(search_action)

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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Student name Widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name:")
        layout.addWidget(self.student_name)

        # Add Combo box of Courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile Number:")
        layout.addWidget(self.student_mobile)

        # Add a submit button
        button = QPushButton("Insert")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.student_mobile.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        # to refresh or load data automatically
        student_data.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # set window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name:")
        layout.addWidget(self.student_name)

        # Create Button
        button = QPushButton("Search")
        # noinspection PyUnresolvedReferences
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = student_data.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            student_data.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
student_data = MainWindow()
student_data.show()
sys.exit(app.exec())