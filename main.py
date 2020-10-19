import heapq
import copy
import requests
import json
import base64
import os
from PIL import Image
import math
import operator
from functools import reduce

BLOCK = []  # 给定状态
GOAL = []  # 目标状态
totalpath = ''  # 总路径

# 4个方向
direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]

openlist = []

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
        self.change = []
        self.fn = self.gn + self.hn
        self.child = []  # 孩子节点
        self.par = par  # 父节点
        self.state = state  # 局面状态
        self.hash_value = hash_value  # 哈希值

    def setchange(self, changenum):
        self.change = changenum

    def __lt__(self, other):  # 用于堆的比较，返回距离最小的
        return self.fn < other.fn

    def __eq__(self, other):  # 相等的判断
        return self.hash_value == other.hash_value

    def __ne__(self, other):  # 不等的判断
        return not self.__eq__(other)

def selfchange(now, aim):
    minhn = 100000000
    minstate = copy.deepcopy(now)
    mina = 10
    minb = 10
    for a in range(1, 10):
        for b in range(a, 10):
            # 对结点的数字序列进行复制，用于之后的移动测试
            # 因为最终的结果是对初始结点进行一次的交换，所以用副本进行尝试
            state = copy.deepcopy(now)
            x = int((a - 1) / 3)
            y = (a - 1) % 3
            i = int((b - 1) / 3)
            j = (b - 1) % 3
            state[i][j], state[x][y] = state[x][y], state[i][j]
            # 判断交换之后是否有解
            statestatus = getStatus(state)
            if statestatus % 2 == 0:
                # 如果有解，则进一步判断是否比当前的最小hn还小
                # 如果比当前的最小还小，则对最小记录进行刷新
                if minhn > manhattan_dis(state, aim) and state[i][j] != 0 and state[x][y] != 0:
                    minhn = manhattan_dis(state, aim)
                    minstate = copy.deepcopy(state)
                    mina = a
                    minb = b
    # 返回交换后的数字序列
    return minstate, [mina, minb]

def exchange(swap, start):
    # 将强制交换的序列转换成具体的索引
    a = swap[0]
    b = swap[1]
    x = int((a - 1) / 3)
    y = (a - 1) % 3
    i = int((b - 1) / 3)
    j = (b - 1) % 3
    start[i][j], start[x][y] = start[x][y], start[i][j]
    return start

def random_child(cur, hash_set, randomlist):
    num = len(cur.state)
    for i in range(0, num):
        for j in range(0, num):
            if cur.state[i][j] != 0:
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

                state = copy.deepcopy(cur.state)  # 复制父节点的状态
                state[i][j], state[x][y] = state[x][y], state[i][j]  # 交换位置
                h = hash(str(state))  # 哈希时要先转换成字符串
                if h in hash_set:  # 结点重复了
                    continue
                hash_set.add(h)  # 加入哈希表
                gn = cur.gn + 1  # 已经走的距离
                node = State(gn=gn, state=state, hash_value=h, par=cur, dir=dir)  # 新建节点
                cur.child.append(node)  # 加入到孩子队列
                heapq.heappush(randomlist, node)  # 加入到堆中

def getranpath(node):
    # 输出路径
    randompath = ''

    # 模拟栈
    pathlist = []
    # 当当前结点还有父节点时继续循环获取信息，直至根节点
    while node.par is not None:
        # 将当前结点的数字序列以及方向加入到栈中
        pathlist.append(node.dir)
        # 向父节点迭代
        node = node.par
    # 将节点的改变方向逐个从栈中弹出并加入到总路径中
    while len(pathlist) != 0:
        p = pathlist.pop()
        randompath += str(p)
    return randompath

def randomChange(start, changestep):
    randomlist = []
    #随机交换结果的字典，键为随机交换后的数字矩阵，值为交换序列
    randomresult = {}
    root = State(0, 0, start, hash(str(start)), None)  # 根节点

    randomlist.append(root)
    heapq.heapify(randomlist) #将列表转换为堆
    random_hash_set = set()  # 存储节点的哈希值
    random_hash_set.add(root.hash_value)

    while len(randomlist) != 0:
        # 删除并返回最小值结点
        top = heapq.heappop(randomlist)
        if top.gn == changestep:
            randomresult[getranpath(top)] = top.state
        if top.gn < changestep:
            #生成当前结点的子结点并加入堆中
            random_child(top, random_hash_set, randomlist)
    return randomresult

def manhattan_dis(cur_state, end_state):
    '''
    计算到目的状态的曼哈顿距离
    cur_state: 当前状态
    end_state: 目的状态
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

def generate_child(cur, end, hash_set, openlist, distance):
    '''
    生成子结点函数
    cur:  当前节点
    end:  最终状态节点
    hash_set:  哈希表，用于判重
    distance: 距离函数
    '''
    if cur == end:
        # 往堆中加入一个新的值
        heapq.heappush(openlist, end)
        return
    num = len(cur.state)
    for i in range(0, num):
        for j in range(0, num):
            if cur.state[i][j] != 0:
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

                state = copy.deepcopy(cur.state)  # 复制父节点的状态
                state[i][j], state[x][y] = state[x][y], state[i][j]  # 交换位置
                h = hash(str(state))  # 哈希时要先转换成字符串
                if h in hash_set:  # 结点重复了
                    continue
                hash_set.add(h)  # 加入哈希表
                gn = cur.gn + 1  # 已经走的距离
                hn = distance(cur.state, end.state)  # 启发的距离函数
                node = State(gn, hn, state, h, cur, dir)  # 新建节点
                cur.child.append(node)  # 加入到孩子队列
                heapq.heappush(openlist, node)  # 加入到堆中

def print_path(node, step):
    # 输出路径
    # node: 最终的节点
    changelist = []
    nomalpath = ''
    num = node.gn

    # 将变换过程中的每个节点的数字序列打印出来
    '''def show_block(block):
        print("---------------")
        for b in block:
            print(b)'''

    # 模拟栈
    pathlist = []
    stack = []
    # 当当前结点还有父节点时继续循环获取信息，直至根节点
    while node.par is not None:
        if node.change != []:
            changelist = node.change
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
        #show_block(t)
    # 将节点的改变方向逐个从栈中弹出并加入到总路径中
    while len(pathlist) != 0:
        p = pathlist.pop()
        nomalpath += str(p)
    # 返回交换路径的总长度和自选交换的序列
    return num, changelist, nomalpath

def AStar(start, end, distance_fn, generate_child_fn, swap, step, ischange):
    '''
    A*算法
    start: 起始状态
    end: 终止状态
    distance_fn: 距离函数
    generate_child_fn: 产生孩子节点的函数
    '''

    root = State(0, 0, start, hash(str(BLOCK)), None)  # 根节点
    end_state = State(0, 0, end, hash(str(GOAL)), None)  # 终止节点
    if root == end_state:
        return 0,[],''

    openlist.append(root)
    heapq.heapify(openlist) #将列表转换为堆
    node_hash_set = set()  # 存储节点的哈希值
    node_hash_set.add(root.hash_value)

    while len(openlist) != 0:
        # 删除并返回最小值结点
        top = heapq.heappop(openlist)

        # 如果获取节点为最后的节点，表示算法结束，获取输出路径
        # 同时将强制交换的步数传入print_path函数，用来获取自选交换的序列
        if top == end_state:
            return print_path(top, step)

        # 产生孩子节点，孩子节点加入openlist
        # 当进行到一定步数时进行强制交换，如果之前已经强制交换过，就不进行操作
        if top.gn == step and ischange == 0:
            top.state = exchange(swap, top.state)
            # 强制交换结束之后，判断当前是否有解，如果无解就进行自选交换
            status = getStatus(top.state)
            if status % 2 != 0:
                top.state, selfswap = selfchange(top.state, end)
                #将自选交换序列加入到当前结点的属性中
                top.setchange(selfswap)
        #生成当前结点的子结点并加入堆中
        generate_child_fn(cur=top, end=end_state, hash_set=node_hash_set,
                          openlist=openlist, distance=distance_fn)

# 图片对比
def compare(pic1, pic2):
    '''
    pic1: 图片1路径
    pic2: 图片2路径
    return: 返回对比的结果
    当返回结果为0时表示两张图片相同
    '''
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(
        reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))

    return differ

# 获取图片
def gethtml(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    html = r.text
    return html

def getproblem():
    #挑战赛题
    url = "http://47.102.118.1:8089/api/challenge/start/d33fbc6f-831b-4ecc-9372-982994da1a46"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Content-Type': 'application/json'
    }
    data_json = json.dumps({
        "teamid": 35,
        "token": "56f315e5-051d-493c-ab96-dc7bb87ea443"
    })
    r = requests.post(url, headers=headers, data=data_json)
    text = json.loads(r.text)
    img_base64 = text["data"]["img"]
    step = text["data"]["step"]
    swap = text["data"]["swap"]
    uuid = text["uuid"]
    chance = text["chanceleft"]
    print("chance = "+str(chance))
    img = base64.b64decode(img_base64)
    # 获取接口的图片并写入本地
    with open("E:/python/软工实践/结对编程/photo.jpg", "wb") as fp:
        fp.write(img)  # 900*900
    return step, swap, uuid

def postresult(uuid,totalpath,swap):
    #提交赛题答案
    url = "http://47.102.118.1:8089/api/challenge/submit"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Content-Type': 'application/json'
    }
    data_json = json.dumps({
    "uuid": uuid,
    "teamid": 35,
    "token": "56f315e5-051d-493c-ab96-dc7bb87ea443",
    "answer": {
        "operations": totalpath,
        "swap": swap
    }
    })
    r = requests.post(url, headers=headers, data=data_json)
    print(r.text)

# 将图片切割
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

# 将切割后的图片保存至本地
def save(path, image_list):
    if not os.path.exists(path):
        os.mkdir('picture')  # 在当前文件夹创建文件夹
    index = 1
    for image in image_list:
        image.save("E:/python/软工实践/结对编程/picture/_" + str(index) + '.jpg')
        index += 1

def createlist(path, cpath):
    train = os.listdir(cpath)
    test = os.listdir(path)
    # 识别获取的是哪,张图片
    pn = -1
    numofpic = {}
    # 确认空白格是哪个
    bleaknum = -1
    for path_ in test:
        if compare('E:/python/软工实践/结对编程/compare_img/white.jpg', 'E:/python/软工实践/结对编程/picture/' + path_) == 0:
            whitenum = str(path_.split('_')[1].split('.')[0])
            numofpic[whitenum] = 0
    for path_ in test:
        if compare('E:/python/软工实践/结对编程/compare_img/bleak.jpg', 'E:/python/软工实践/结对编程/picture/' + path_) == 0:
            bleaknum = str(path_.split('_')[1].split('.')[0])
    for path_ in test:
        if path_.split('_')[1].split('.')[0] == whitenum:
            continue
        if path_.split('_')[1].split('.')[0] == bleaknum:
            continue
        for path in train:
            if compare('E:/python/软工实践/结对编程/compare_img/' + path, 'E:/python/软工实践/结对编程/picture/' + path_) == 0:
                pn = int(path.split('_')[0])
                break
        if pn > 0:
            break
    print(pn)
    # 建立图片编号和应在位置的字典
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for path_ in test:
        for i in num:
            if compare('E:/python/软工实践/结对编程/compare_img/' + str(pn) + '_' + str(i) + '.jpg',
                       'E:/python/软工实践/结对编程/picture/' + path_) == 0:
                numofpic[str(path_.split('_')[1].split('.')[0])] = i
                num.remove(i)

    # 建立列表
    piclists = []
    for i in range(3):
        piclist = []
        for j in range(3):
            piclist.append(numofpic[str((j + 1) + i * 3)])
        piclists.append(piclist)

    # 生成目标列表
    aimlists = []
    for i in range(3):
        aimlist = []
        for j in range(3):
            if ((j + 1) + i * 3) != num[0]:
                aimlist.append((j + 1) + i * 3)
            else:
                aimlist.append(0)
        aimlists.append(aimlist)

    return piclists, aimlists

'''def getproblem():
    #接口测试获取题目
    url = "http://47.102.118.1:8089/api/challenge/start/4f198e1d-a7aa-4851-bfac-644597afb8fa"
    # 每次请求的结果都不一样，动态变化
    text = json.loads(gethtml(url))
    # print(text.keys())#dict_keys(['img', 'step', 'swap', 'uuid'])
    # text["img"] = "none" #{'img': 'none', 'step': 0, 'swap': [7, 7], 'uuid': '3bc827e5008d460b893e5cb28769e6bf'}
    img_base64 = text["img"]
    step = text["step"]
    swap = text["swap"]
    uuid = text["uuid"]
    img = base64.b64decode(img_base64)
    # 获取接口的图片并写入本地
    with open("E:/python/软工实践/结对编程/photo.jpg", "wb") as fp:
        fp.write(img)  # 900*900
    return step,swap,uuid'''

'''def postAnswer(uuid, opertions, swap):
    #接口测试提交
    url = "http://47.102.118.1:8089/api/answer"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Content-Type': 'application/json'
    }
    data_json = json.dumps({
        "uuid": uuid,
        "answer": {
            "operations": opertions,
            "swap": swap}
    })
    r = requests.post(url, headers=headers, data=data_json)
    print(r.text)'''

if __name__ == '__main__':

    # step,swap,uuid为从题目中获取的数据，即要进行强制交换的步数和交换序列，以及用户id
    step, swap, uuid = getproblem()

    # 打开从网页中下载到本地的图片
    img = Image.open('E:/python/软工实践/结对编程/photo.jpg')

    # 将图片进行切割，并保存到本地文件夹picture中
    save_path = "picture"
    save(save_path, cut_image(img))

    # 将图片转换为数字序列，startlists为获取图片的数字序列，aimlists为目标数字序列
    startlists, aimlists = createlist('E:/python/软工实践/结对编程/picture/', 'E:/python/软工实践/结对编程/compare_img/')

    ischange = 0
    BLOCK = startlists
    GOAL = aimlists
    length = 0
    selfswap = []

    # 打印初始结点
    print('初始结点：')
    print(BLOCK)

    #step等于0的情况
    if step == 0:
        BLOCK = exchange(swap, BLOCK)
        ischange = 1
        # 强制交换结束之后，判断当前是否有解，如果无解就进行自选交换
        status = getStatus(BLOCK)
        print(BLOCK)
        if status % 2 != 0:
            print('强制交换后，当前无解')
            BLOCK, selfswap = selfchange(BLOCK, GOAL)

    # 判断初始结点有没有解
    # startY为初始结点的逆序对个数，若为偶数则初始结点有解，奇数则无解
    startY = getStatus(BLOCK)
    if startY % 2 != 0:
        minhn = 100000000
        # 如果初始结点无解，进行一定步数的随机交换，只到达到了强制交换的步数
        print('初始结点无解')
        # BLOCK为随机交换之后的结点，randompath为随机交换的路径
        randomresult = randomChange(BLOCK, step)
        for randompath,BLOCK in randomresult.items():
            ranswap = []
            # 将随机交换后的节点进行强制交换，并设置ischange为强制交换时的步数
            BLOCK = exchange(swap, BLOCK)
            ischange = step
            # 强制交换结束之后，判断当前是否有解，如果无解就进行自选交换
            status = getStatus(BLOCK)
            if status % 2 != 0:
                BLOCK, ranswap = selfchange(BLOCK, GOAL)
            if minhn > manhattan_dis(BLOCK, GOAL):
                minhn = manhattan_dis(BLOCK, GOAL)
                minstate = copy.deepcopy(BLOCK)
                minranpath = randompath
                minswap = ranswap
        length, selfswap, nomalpath = AStar(minstate, GOAL, manhattan_dis, generate_child, swap, step, ischange)
        totalpath = minranpath + nomalpath
        selfswap = minswap

    else:
        # BLOCK为初始结点，GOAL目标结点，manhattan_dis为fn的计算函数
        # swap,step为强制交换的步数和交换序列，ischange用来控制是否已经进行过强制交换
        length, selfswap_, totalpath = AStar(BLOCK, GOAL, manhattan_dis, generate_child, swap, step, ischange)
        if selfswap == []:
            selfswap = selfswap_

    print("totalpath", totalpath)
    print("selfswap", selfswap)
    print("step = ", step)
    print("swap = ", swap)
    print("length = ", length)
    postresult(uuid, totalpath, selfswap)
    #测试
    #postAnswer(uuid, totalpath, selfswap)

