import os
import sys
import random
from enum import IntEnum
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox, QTextEdit, QAction, QPushButton
from PyQt5.QtGui import QFont, QPalette, QPixmap, QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QTextEdit, QGridLayout, QWidget
from PyQt5.QtGui import QIcon


# 用枚举类表示方向
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class start(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def closewin(self):
        self.close()

    def initUI(self):
        self.btn = QPushButton("开始游戏", self)
        self.label = QLabel()
        self.btn.setGeometry(328, 325, 135, 135)
        self.btn.setStyleSheet('''QPushButton
                     {text-align : center;
                     background-color :brown ;}''')

        self.btn.setToolTip('开始游戏')
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(192, 253, 123))  # 设置背景颜色
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('num.png')))  # 设置背景图片
        self.setPalette(palette1)
        self.setGeometry(710, 250, 500, 500)
        self.setWindowIcon(QIcon('num.png'))
        self.setWindowTitle('华容道')
        self.show()


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.blocks = []
        self.wid_gltMain = QWidget()
        self.gltMain = QGridLayout()
        self.setLayout(self.gltMain)
        self.initUI()
        self.num = 0
        self.final = [0]

    def initUI(self):
        self.gltMain.setSpacing(5)
        self.final = [0]
        self.onInit()
        # 设置布局

        # 设置宽和高

        self.setFixedSize(500, 500)
        self.setWindowTitle('字母华容道')
        # 设置背景颜色

        self.setStyleSheet("background-color:grey;")
        self.setWindowIcon(QIcon('num.png'))

    def onInit(self):
        # 产生顺序数组
        self.num = 0
        self.numbers = list(range(1, 10))
        self.a = random.randint(0, 8)
        self.numbers[self.a] = 0
        self.blocks.clear()
        # 将数字添加到二维数组
        for row in range(3):
            self.blocks.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]

                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)
                print(self.blocks)

        # 打乱数组
        for i in range(10):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        self.updatePanel()

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_Up or key == Qt.Key_W):
            self.num_(Direction.UP)
            self.move(Direction.UP)
            self.change()
            print(self.blocks)
        if (key == Qt.Key_Down or key == Qt.Key_S):
            self.num_(Direction.DOWN)
            self.move(Direction.DOWN)
            self.change()
            print(self.blocks)
        if (key == Qt.Key_Left or key == Qt.Key_A):
            self.num_(Direction.LEFT)
            self.move(Direction.LEFT)
            self.change()
            print(self.blocks)
        if (key == Qt.Key_Right or key == Qt.Key_D):
            self.num_(Direction.RIGHT)
            self.move(Direction.RIGHT)
            self.change()
            print(self.blocks)

        if self.checkResult():
            self.final.append(self.num)
            if min(self.final) == 0:
                self.final[self.final.index(min(self.final))] = 999
            print(self.final)
            reply = QMessageBox.information(self, '结果', '成功复原，是否继续？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.onInit()
            else:
                self.close()

    # 方块移动算法
    def num_(self, direction):
        if direction == Direction.DOWN:
            if self.zero_row != 2:
                self.num += 1
                print(self.num)
        if (direction == Direction.UP):  # 下
            if self.zero_row != 0:
                self.num += 1
                print(self.num)
        if (direction == Direction.RIGHT):  # 左
            if self.zero_column != 2:
                self.num += 1
                print(self.num)
        if (direction == Direction.LEFT):  # 右
            if self.zero_column != 0:
                self.num += 1
                print(self.num)

    def move(self, direction):
        if (direction == Direction.DOWN):  # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1

        if (direction == Direction.UP):  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if (direction == Direction.RIGHT):  # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1

        if (direction == Direction.LEFT):  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1
        self.updatePanel()

    def updatePanel(self):
        self.lab2 = QLabel()
        self.lab3 = QLabel()
        self.lab4 = QLabel()
        self.lab5 = QLabel()
        self.btn = QPushButton('提示', self)
        self.gltMain.addWidget(self.btn, 2, 0, 1, 3)
        self.lab2.setText(str((self.num)))
        self.lab3.setText('当前步数  : ')
        self.lab4.setText('最好成绩  : ')
        self.lab5.setText(str(min(self.final)))
        self.gltMain.addWidget(self.lab4, 1, 0, 1, 2)
        self.gltMain.addWidget(self.lab2, 0, 2, 1, 1)
        self.gltMain.addWidget(self.lab3, 0, 0, 1, 2)
        self.gltMain.addWidget(self.lab5, 1, 2, 1, 1)
        for row in range(3):
            for column in range(3, 6):
                self.lab1 = QLabel()
                self.lab1.setPixmap(
                    QPixmap(r'C:\Users\Administrator\Desktop\software\2\outpic\%d.jpg' % self.blocks[row][column - 3]))
                self.lab1.setScaledContents(True)
                self.gltMain.addWidget(self.lab1, row, column, 1, 1)
        self.setLayout(self.gltMain)

    def change(self):
        if self.num == 10:
            row_random_1 = 1
            column_random_1 = 1
            row_random_2 = 2
            column_random_2 = 2
            if self.zero_row == 1 and self.zero_column == 1:
                self.zero_row += 1
                self.zero_column += 1
            elif self.zero_row == 2 and self.zero_column == 2:
                self.zero_row -= 1
                self.zero_column -= 1
            flag = self.blocks[row_random_1][column_random_1]
            self.blocks[row_random_1][column_random_1] = self.blocks[row_random_2][column_random_2]
            self.blocks[row_random_2][column_random_2] = flag
            self.updatePanel()
        else:
            pass

    # 检测是否完成
    def checkResult(self):
        # 先检测最右下角是否为0
        print(self.final)
        if self.blocks[self.a // 3][self.a % 3] != 0:
            return False

        for row in range(3):
            for column in range(3):
                # 运行到此处说名最右下角已经为0，pass即可
                if row == self.a // 3 and column == self.a % 3:
                    pass
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

        return True

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', '确定要退出吗', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def cut_image(image):
    width, hight = image.size
    cut_size = int(width / 3)
    box_list = []
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j * cut_size, i * cut_size, (j + 1) * cut_size, (i + 1) * cut_size)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list


def save(path, image_list):
    if not os.path.exists(path):
        os.mkdir('picture')  # 在当前文件夹创建文件夹
    index = 1
    for image in image_list:
        image.save(r"C:\Users\Administrator\Desktop\software\2\outpic/" + str(index) + '.jpg')
        index += 1


if __name__ == '__main__':
    img = Image.open(r'C:\Users\Administrator\Desktop\software\2\无框字符\无框字符\a_.jpg')
    save_path = r"picture"
    save(save_path, cut_image(img))
    app = QApplication(sys.argv)
    ax = start()
    ex = Example()
    ax.show()
    ax.btn.clicked.connect(ax.closewin)
    ax.btn.clicked.connect(ex.show)
    sys.exit(app.exec_())
