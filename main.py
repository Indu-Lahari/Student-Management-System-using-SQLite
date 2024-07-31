from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, QLineEdit, QMenu, \
    QPushButton, QWidget, QMainWindow
from PyQt6.QtGui import QAction
import sys


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


app = QApplication(sys.argv)
student_data = MainWindow()
student_data.show()
sys.exit(app.exec())