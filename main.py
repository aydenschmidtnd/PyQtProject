from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtCore import QSize, Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(QSize(1200,800))

        self.button_is_checked = True

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)
        # self.button.setCheckable(True)
        # self.button.released.connect(self.the_button_was_released)
        # self.button.setChecked(self.button_is_checked)

        self.setCentralWidget(self.button)

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print(self.button_is_checked)

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)

    def the_button_was_clicked(self):
        self.button.setText("You already clicked me")
        self.button.setEnabled(True)

        self.setWindowTitle("My OneShot App")

#Create application handler
#Pass in sys.argv, a python list containing command line arguments passed to application
#You only need one of these for an application to function
#QApplication holds the event loop of our application
app = QApplication(sys.argv)

window = MainWindow()
window.show()

#Starts event loop
app.exec()