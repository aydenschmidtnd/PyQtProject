import sys
import serial
from time import sleep
from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QMainWindow, QGridLayout, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot, QSize, Qt

ROW_SIZE = 7
COLUMN_SIZE = 5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setFixedSize(QSize(500, 400))

        self.lcd_row1 = []
        self.lcd_row2 = []

        lcd_layout = QHBoxLayout()
        lcd_layout.setSpacing(0)
 
        for character_column in range(16):
            column = QVBoxLayout()
            character1 = QLineEdit()
            character2 = QLineEdit()
            character1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            character2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            character1.setReadOnly(True)
            character2.setReadOnly(True)
            self.lcd_row1.append(character1)
            self.lcd_row2.append(character2)

            column.addWidget(character1)
            column.addWidget(character2)
               
            lcd_layout.addLayout(column)

        self.button_names_noswitch = (("RCL","STACK DOWN","SWAP","<",">"),
                                      ("SIN","COS","TAN","X^Y","1/X"),
                                      ("ENTER","i","+/-","E","<--"),
                                      ("SYMBOLS","7","8","9","DIV"),
                                      ("SWITCH","4","5","6","x"),
                                      ("CLEAR","1","2","3","-"),
                                      ("ON/OFF","0",".","!","+"))
        
        self.button_names_switch = (("STORE","STACK UP","CONVERSIONS","",""),
                                    ("ASIN","ACOS","ATAN","SQRT(X)","LN(X)"),
                                    ("PI","PHASE","ABS","e^x","LOG(X)"),
                                    ("MODE","<-ENG","ENG->","X^2","FDISP"),
                                    ("SWITCH","DISPLAY","","",""),
                                    ("","","","",""),
                                    ("","","","",""))

        self.buttons = []

        self.switch_action = False

        button_matrix = QGridLayout()
        for row in range(ROW_SIZE):
            for column in range(COLUMN_SIZE):
                button_name = self.button_names_noswitch[row][column]
                button = QPushButton(f'{button_name}')

                self.buttons.append(button)
                if((row == 4) and (column == 0)):
                    self.buttons[row*COLUMN_SIZE].clicked.connect(self.switching_task)
                else:
                    self.buttons[row*COLUMN_SIZE + column].clicked.connect(lambda checked, Row=row, Col=column: self.button_task(Row,Col))

                button_matrix.addWidget(self.buttons[row*COLUMN_SIZE + column], row, column)

        main_layout = QVBoxLayout()
        main_layout.addLayout(lcd_layout)
        main_layout.addLayout(button_matrix)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def clear_lcd(self):
        for column in range(16):
            self.lcd_row1[column].setText('')
            self.lcd_row2[column].setText('')
    
    def text_to_lcd(self, line_number, text:str):
        if(len(text) > 16):
            print("text is out of bounds")
            return
        
        if(line_number == 1):
            for column in range(len(text)):
                self.lcd_row1[column].setText(f'{text[column]}')
        elif(line_number == 2):
            for column in range(len(text)):
                self.lcd_row2[column].setText(f'{text[column]}')
        else:
            print("line_number is invalid")
    
    def switch_button_names(self):
        if(self.switch_action):
            button_names = self.button_names_switch
        else:
            button_names = self.button_names_noswitch

        for row in range(ROW_SIZE):
            for column in range(COLUMN_SIZE):
                    button_name = button_names[row][column]
                    self.buttons[row*COLUMN_SIZE + column].setText(f'{button_name}')

    @Slot()
    def switching_task(self):
        self.switch_action = not self.switch_action
        self.switch_button_names()
        
    @Slot()
    def button_task(self, row, column):
        self.switch_action = False
        self.switch_button_names()

        if((row == 6) and (column == 1)):
            ser.write(b'\x00')
        elif((row == 5) and (column == 1)):
            ser.write(b'\x01')

        response = ser.readline()
        decoded_response = response.decode('utf-8')
        cleaned_response = decoded_response.strip()

        self.clear_lcd()
        self.text_to_lcd(1, cleaned_response)

if __name__ == "__main__":
    ser = serial.Serial(port='COM5',baudrate=115200,timeout=1)
    sleep(2)

    app = QApplication(sys.argv)
    app.setStyleSheet("QLineEdit {border: 1px solid gray; border-radius: 0px;}")
    
    window = MainWindow()
    window.show()
    
    app.exec()