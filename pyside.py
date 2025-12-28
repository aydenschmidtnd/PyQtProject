import sys
from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QMainWindow, QGridLayout, QWidget
from PySide6.QtCore import Slot, QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Cool App")
        #self.setFixedSize(QSize(1200, 800))

        buttons = {
            0:"RCL",
            1:"SIN",
            2:"ENTER",
            3:"SYMBOLS",
            4:"MODE",
            5:"CLEAR",
            6:"ON/OFF"
        }

        self.button = QPushButton("Click me")
        self.button2 = QPushButton("Button2")
        self.line_edit = QLineEdit()

        self.button.clicked.connect(self.say_hello)
        self.button.clicked.connect(self.line_edit.clear)

        layout = QGridLayout()
        layout.addWidget(self.button,    0, 0)
        layout.addWidget(self.button2,   1, 0)
        layout.addWidget(self.line_edit, 1, 1)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    @Slot()
    def say_hello(self):
        print("Button clicked, Hello!") 

# Create the Qt Application
app = QApplication(sys.argv)
# Create a button, connect it and show it

window = MainWindow()
window.show()
# Run the main Qt loop
app.exec()