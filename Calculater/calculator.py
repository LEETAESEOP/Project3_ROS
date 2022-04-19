
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("LEE's Calculator")
        self.resize(800,500)
        self.center()
        
        
        

        


        btn = QPushButton('닫기', self)
        btn.move(300,200)
        print(btn.sizeHint())
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)
      


    

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
 



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    sys.exit(app.exec())



    




