import os
import sys
import copy
import random
import heapq
from enum import IntEnum
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox, QTextEdit, QAction, QPushButton
from PyQt5.QtGui import QFont, QPalette, QPixmap, QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QTextEdit, QGridLayout, QWidget
from PyQt5.QtGui import QIcon

BLOCK = []  # 给定状态
GOAL = []  # 目标状态
totalpath = ''  # 总路径

# 4个方向
direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]

# OPEN表
OPEN = []

# 节点的总数
SUM_NODE_NUM = 0


# 计算是奇数列还是偶数列
def getStatus(array2d):
    y = 0
    list = []
    for i in range(0, 3):
        for j in range(0, 3):
            if array2d[i][j] != 0:
                list.append(array2d[i][j])
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            if list[i] > list[j]:
                y += 1
    return y


# 状态节点
class State(object):
    def __init__(self, gn=0, hn=0, state=None, hash_value=None, par=None, dir=None):
        '''
        初始化
        gn: gn是初始化到现在的距离
        hn: 启发距离
        state: 节点存储的状态
        hash_value: 哈希值，用于判重
        par: 父节点指针
        '''
        self.dir = dir
        self.gn = gn
        self.hn = hn
        self.fn = self.gn + self.hn
        self.child = []  # 孩子节点
        self.par = par  # 父节点
        self.state = state  # 局面状态
        self.hash_value = hash_value  # 哈希值

    def __lt__(self, other):  # 用于堆的比较，返回距离最小的
        return self.fn < other.fn

    def __eq__(self, other):  # 相等的判断
        return self.hash_value == other.hash_value

    def __ne__(self, other):  # 不等的判断
        return not self.__eq__(other)


def manhattan_dis(cur_state, end_state):
    '''
    计算曼哈顿距离
    :param cur_state: 当前状态
    :return: 到目的状态的曼哈顿距离
    '''
    dist = 0
    N = len(cur_state)
    for i in range(N):
        for j in range(N):
            if cur_state[i][j] == end_state[i][j]:
                continue
            num = cur_state[i][j]
            if num == 0:
                x = N - 1
                y = N - 1
            else:
                x = num / N  # 理论横坐标
                y = num - N * x - 1  # 理论的纵坐标
            dist += (abs(x - i) + abs(y - j))

    return dist


def generate_child(cur_node, end_node, hash_set, open_table, dis_fn):
    '''
    生成子节点函数
    :param cur_node:  当前节点
    :param end_node:  最终状态节点
    :param hash_set:  哈希表，用于判重
    :param open_table: OPEN表
    :param dis_fn: 距离函数
    :return: None
    '''
    if cur_node == end_node:
        # 往堆中加入一个新的值
        heapq.heappush(open_table, end_node)
        return
    num = len(cur_node.state)
    for i in range(0, num):
        for j in range(0, num):
            if cur_node.state[i][j] != 0:
                continue
            for d in direction:  # 四个偏移方向
                if d[0] == 0 and d[1] == 1:
                    dir = 'd'
                if d[0] == 0 and d[1] == -1:
                    dir = 'a'
                if d[0] == 1 and d[1] == 0:
                    dir = 's'
                if d[0] == -1 and d[1] == 0:
                    dir = 'w'
                x = i + d[0]
                y = j + d[1]
                if x < 0 or x >= num or y < 0 or y >= num:  # 越界了
                    continue
                # 记录扩展节点的个数
                global SUM_NODE_NUM
                SUM_NODE_NUM += 1

                state = copy.deepcopy(cur_node.state)  # 复制父节点的状态
                state[i][j], state[x][y] = state[x][y], state[i][j]  # 交换位置
                h = hash(str(state))  # 哈希时要先转换成字符串
                if h in hash_set:  # 重复了
                    continue
                hash_set.add(h)  # 加入哈希表
                gn = cur_node.gn + 1  # 已经走的距离函数
                hn = dis_fn(cur_node.state, end_node.state)  # 启发的距离函数
                node = State(gn, hn, state, h, cur_node, dir)  # 新建节点
                cur_node.child.append(node)  # 加入到孩子队列
                heapq.heappush(open_table, node)  # 加入到堆中


def print_path(node):
    # 输出路径
    # node: 最终的节点
    changelist = []
    global totalpath
    num = node.gn

    # 模拟栈
    pathlist = []
    stack = []
    # 当当前结点还有父节点时继续循环获取信息，直至根节点
    while node.par is not None:
        # 将当前结点的数字序列以及方向加入到栈中
        stack.append(node.state)
        pathlist.append(node.dir)
        # 向父节点迭代
        node = node.par
    # 迭代至根节点时，根节点无法进入循环，因此要单独获取数字序列
    stack.append(node.state)
    # 将节点的数字序列逐个从栈中弹出并打印
    while len(stack) != 0:
        t = stack.pop()
    # 将节点的改变方向逐个从栈中弹出并加入到总路径中
    while len(pathlist) != 0:
        p = pathlist.pop()
        totalpath += str(p)
    print('总路径：')
    print(totalpath)


def A_start(start, end, distance_fn, generate_child_fn):
    '''
    A*算法
    start: 起始状态
    end: 终止状态
    distance_fn: 距离函数，可以使用自定义的
    generate_child_fn: 产生孩子节点的函数
    time_limit: 时间限制，默认10秒
    '''

    root = State(0, 0, start, hash(str(BLOCK)), None)  # 根节点
    end_state = State(0, 0, end, hash(str(GOAL)), None)  # 最后的节点
    if root == end_state:
        print("start == end !")

    OPEN.append(root)
    heapq.heapify(OPEN)

    node_hash_set = set()  # 存储节点的哈希值
    node_hash_set.add(root.hash_value)
    while len(OPEN) != 0:
        # 获取OPEN表中第一个节点
        top = heapq.heappop(OPEN)

        # 如果获取节点为最后的节点，表示算法结束，获取输出路径
        # 同时将强制交换的步数传入print_path函数，用来获取自选交换的序列
        if top == end_state:
            print_path(top)
            return 0
        generate_child_fn(cur_node=top, end_node=end_state, hash_set=node_hash_set,
                          open_table=OPEN, dis_fn=distance_fn)

    print("No road !")  # 没有路径
    return -1


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
    blocks_start = []
    blocks_end = []

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
        self.blocks_end = copy.deepcopy(self.blocks)
        # 打乱数组
        for i in range(10):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        self.blocks_start = copy.deepcopy(self.blocks)
        self.updatePanel()

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_Up or key == Qt.Key_W):
            self.num_(Direction.UP)
            self.move(Direction.UP)
            self.change()
        if (key == Qt.Key_Down or key == Qt.Key_S):
            self.num_(Direction.DOWN)
            self.move(Direction.DOWN)
            self.change()
        if (key == Qt.Key_Left or key == Qt.Key_A):
            self.num_(Direction.LEFT)
            self.move(Direction.LEFT)
            self.change()
        if (key == Qt.Key_Right or key == Qt.Key_D):
            self.num_(Direction.RIGHT)
            self.move(Direction.RIGHT)
            self.change()

        if self.checkResult():
            self.final.append(self.num)
            if min(self.final) == 0:
                self.final[self.final.index(min(self.final))] = 999
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
        if (direction == Direction.UP):  # 下
            if self.zero_row != 0:
                self.num += 1
        if (direction == Direction.RIGHT):  # 左
            if self.zero_column != 2:
                self.num += 1
        if (direction == Direction.LEFT):  # 右
            if self.zero_column != 0:
                self.num += 1

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

    def sho(self):
        self.lab6.setVisible(True)

    def updatePanel(self):
        self.lab2 = QLabel()
        self.lab3 = QLabel()
        self.lab4 = QLabel()
        self.lab5 = QLabel()
        self.lab6 = QLabel()
        self.lab6.setText(totalpath)
        self.gltMain.addWidget(self.lab6,3,1,2,3)
        self.lab6.setVisible(False)

        self.btn = QPushButton('提示', self)
        self.gltMain.addWidget(self.btn, 2, 0, 1, 3)
        self.btn.clicked.connect(self.sho)
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
                    QPixmap(r'G:\TECENT(3)\origin desktop\software\2\outpic\%d.jpg' % self.blocks[row][column - 3]))
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
        image.save(r"G:\TECENT(3)\origin desktop\software\2\outpic/" + str(index) + '.jpg')
        index += 1




'''    def __init__(self):
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
        self.setWindowIcon(QIcon('num.png'))'''

if __name__ == '__main__':
    img = Image.open(r'G:\TECENT(3)\origin desktop\software\2\无框字符\无框字符\a_.jpg')
    save_path = r"picture"
    save(save_path, cut_image(img))
    app = QApplication(sys.argv)
    ax = start()
    ex = Example()
    BLOCK = ex.blocks_start
    GOAL = ex.blocks_end
    A_start(BLOCK, GOAL, manhattan_dis, generate_child)
    ax.show()
    ax.btn.clicked.connect(ax.closewin)
    ax.btn.clicked.connect(ex.show)
    sys.exit(app.exec_())
