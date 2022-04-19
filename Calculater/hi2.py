import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QPlainTextEdit, QLabel)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.str =''
        self.label =QLabel();
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i,j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '' : continue
            btn = QPushButton(name)
            btn.clicked.connect(self.func_a)
            grid.addWidget(btn, *position)
        grid.addWidget(self.label)
        self.move(300,150)
        self.setWindowTitle('Calculator')
        self.show()
        self.str=""

    def func_a(self,x) -> None:
        sender = self.sender()  # 어떤 콤포넌트 또는 위젯에서 어떤 signal이 발생했는가?
        self.str = self.str + sender.text()

        self.label.setText(self.str)
        result=[]
        first_operand = 0

        if 'C' in self.str: #비우기
            self.label.clear()
            self.str = '' #문자열 내용 비우기

        for i in list(self.str):
            result_str = ''.join(result)
            if i == '=': # =일 경우 계산 결과를 label에 적용
                print("결과는 =",i, 'result :', result)
                print('결과는 ',result_str)
                print('비어있나', first_operand)
                print('계산 결과는', int(result_str)+first_operand)
                if '+' in self.str:
                    self.label.setText(str(int(result_str) + first_operand))
                if '-' in self.str:
                    self.label.setText(str(first_operand - int(result_str)))
                if '*' in self.str:
                    self.label.setText(str(first_operand * int(result_str)))
                if '/' in self.str:
                    self.label.setText(str(first_operand / int(result_str)))

            elif i in ['+','-','*','/']:
                first_operand += int(result_str)
                print('덧셈 누르면',result_str)
                print(i)
                result=[]

            else:
                result.append(i)
                print(i, '결과 : ',result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())