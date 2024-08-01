from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # Window Size
        self.setMinimumSize(600, 400)

        # Menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        # Sub Menu ( Actions )
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        # noinspection PyUnresolvedReferences
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        # noinspection PyUnresolvedReferences
        search_action.triggered.connect(self.search)
        edit_menu.addAction(search_action)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create ToolBar and add Tools or ToolBar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create Status Bar and add Status Bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect click (selecting a row in table) and then display status bar elements
        self.table.cellClicked.connect(self.cell_clicked)


        # Calling load_data function here
        self.load_data()

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)


        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # To display status bar buttons only once instead of multiple when clicked to avoid duplicate buttons
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

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

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
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


# noinspection PyUnresolvedReferences
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Records")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # Get student name from selected row which user wants to edit
        index = student_data.table.currentRow()
        student_name = student_data.table.item(index, 1).text()

        # Get id from selected row
        self.student_id = student_data.table.item(index, 0).text()

        # Add Student name Widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name:")
        layout.addWidget(self.student_name)

        # Add Combo box of Courses
        course_name = student_data.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile = student_data.table.item(index, 3).text()
        self.student_mobile = QLineEdit(mobile)
        self.student_mobile.setPlaceholderText("Mobile Number:")
        layout.addWidget(self.student_mobile)

        # Add a submit button
        button = QPushButton("Update/Edit")
        button.clicked.connect(self.edit_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def edit_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.student_mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        # to refresh or load data automatically
        student_data.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        pass



app = QApplication(sys.argv)
student_data = MainWindow()
student_data.show()
sys.exit(app.exec())