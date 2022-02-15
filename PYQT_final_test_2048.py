import sys
import random

import math
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QLabel)
from PyQt5.QtCore import Qt


class board:
    def __init__(self):

        self.init_val = [0, 0, 0, 0, 2, 2, 4]   #Стартовой вброс чисел, у 2 шанс 30%, у 4 15%, 0 55%
        self.x = 4
        self.value = [[random.choice(self.init_val) for i in range(self.x)] for j in range(self.x)]   #раскидываем рандомно по полю

        self.failure = self.check()[2]      #продолжение игры пока False
        self.score = self.score_cal()            # набираем до 2048

    def score_cal(self):                     # ищем в нашей матрице ячейку с максимальной величиной, до 2048
        maxim = self.value[0][0]
        for i in range(self.x):
            for j in range(self.x):
                if (self.value[i][j] > maxim):
                    maxim = self.value[i][j]

        return maxim

    def calculator(self, direc):                #изменение чисел после движения
        self.move(direc)
        if direc == 'l':
            for i in range(self.x):
                pos = self.x - 1
                while pos > 0:
                    if self.value[i][pos] == self.value[i][pos - 1] and self.value[i][pos] != 0:
                        self.value[i][pos - 1] = self.value[i][pos] * 2
                        self.value[i][pos] = 0
                        self.move(direc)
                        pos = self.x - 1
                    pos = pos - 1

        if direc == 'r':
            for i in range(self.x):
                pos = 0
                while pos < self.x - 1:
                    if self.value[i][pos] == self.value[i][pos + 1] and self.value[i][pos] != 0:
                        self.value[i][pos + 1] = self.value[i][pos] * 2
                        self.value[i][pos] = 0
                        self.move(direc)
                        pos = 0
                    pos = pos + 1
        if direc == 'u':
            for i in range(self.x):
                pos = self.x - 1
                while (pos > 0):
                    if (self.value[pos][i] == self.value[pos - 1][i] and self.value[pos][i] != 0):
                        self.value[pos - 1][i] = self.value[pos][i] * 2
                        self.value[pos][i] = 0
                        self.move(direc)
                        pos = self.x - 1
                    pos = pos - 1

        if (direc == 'd'):
            for i in range(self.x):
                pos = 0
                while (pos < self.x - 1):
                    if (self.value[pos][i] == self.value[pos + 1][i] and self.value[pos][i] != 0):
                        self.value[pos + 1][i] = self.value[pos][i] * 2
                        self.value[pos][i] = 0
                        self.move(direc)
                        pos = 0
                    pos = pos + 1

        self.score = self.score_cal()
        self.num_generator()

    def move(self, direc):                      #cмещение в завсимости от опорной точки
        if (direc == 'l'):
            for i in range(self.x):
                temp1 = 0
                for temp2 in range(self.x):
                    if (self.value[i][temp2] != 0):
                        self.value[i][temp1] = self.value[i][temp2]
                        temp1 = temp1 + 1
                while (temp1 < self.x):
                    self.value[i][temp1] = 0
                    temp1 = temp1 + 1

        if (direc == 'r'):
            for i in range(self.x):
                temp1 = self.x - 1
                for temp2 in range(self.x - 1, -1, -1):
                    if (self.value[i][temp2] != 0):
                        self.value[i][temp1] = self.value[i][temp2]
                        temp1 = temp1 - 1
                while (temp1 >= 0):
                    self.value[i][temp1] = 0
                    temp1 = temp1 - 1

        if (direc == 'u'):
            for i in range(self.x):
                temp1 = 0
                for temp2 in range(self.x):
                    if (self.value[temp2][i] != 0):
                        self.value[temp1][i] = self.value[temp2][i]
                        temp1 = temp1 + 1
                while (temp1 < self.x):
                    self.value[temp1][i] = 0
                    temp1 = temp1 + 1

        if (direc == 'd'):
            for i in range(self.x):
                temp1 = self.x - 1
                for temp2 in range(self.x - 1, -1, -1):
                    if (self.value[temp2][i] != 0):
                        self.value[temp1][i] = self.value[temp2][i]
                        temp1 = temp1 - 1
                while (temp1 >= 0):
                    self.value[temp1][i] = 0
                    temp1 = temp1 - 1

    def check(self):              #проверяем заполн. поля

        l1 = []
        l2 = []
        for i in range(self.x):
            for j in range(self.x):
                if (self.value[i][j] == 0):
                    l1.append(i)
                    l2.append(j)

        return l1, l2, len(l1) == 0

    def num_generator(self):

        l1, l2, full_or_not = self.check()
        if (full_or_not != True):

            index = random.sample(range(len(l1)), 1)               #случайная клетка на поле
            for i in index:
                self.value[l1[i]][l2[i]] = random.choice([2, 2, 2, 2, 2, 4, 4])     # вброс чисел на поле после хода

        else:
            self.failure = True   #проигрыш


class ui(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):



        self.resize(600, 600)

        self.height = self.height()
        self.width = self.width()



        QMessageBox.information(self, "Начало игры","Используйте стрелки на клавиатуре, чтобы набрать 2048 и выиграть!")

        self.setStyleSheet("QLabel{background-color:rgb(220,220,220);""border-style: outset;}" "QLabel{color:rgb(100,100,100,250);font-size:45px;font-weight:bold;font-family:Roman times;}""QLabel:hover{color:rgb(100,100,100,120);}")

        self.board = board()

        self.lb = self.label_generator()

        self.drawNum()                  #цвета чисел и доски
        self.color_map()

        self.setWindowTitle('Игра 2048')

        self.show()

    def label_generator(self):                                                      #визуализируем числа после перемещения

        lb = [[i for i in range(4)] for j in range(4)]

        self.lb_width = int((self.width - 45) / 4)
        self.lb_height = int((self.height - 45) / 4)

        for i in range(4):
            for j in range(4):
                lb[i][j] = QLabel(str(self.board.value[i][j]), self)
                lb[i][j].setGeometry(15 + (self.lb_width + 5) * j, 15 + (self.lb_height + 5) * i,self.lb_width, self.lb_height)
                lb[i][j].setAlignment(Qt.AlignmentFlag.AlignCenter)
        return lb



    def drawNum(self):                                                  #отоброжаем цифры на экране, если не 0
        for i in range(4):
            for j in range(4):
                if (self.board.value[i][j] == 0):
                    self.lb[i][j].setText('')
                else:
                    self.lb[i][j].setText(str(self.board.value[i][j]))

        return None



    def color_map(self):                            #раскраска

        color = ["#4682B4", "#00CED1", "#FF1493", "#FFA500", "#8B3626", "#8B0000", "#FF8247", "#FFA500", "#FF4500",
                 "#FF0000"]



        for i in range(4):
            for j in range(4):
                if (self.board.value[i][j] >= 2 and self.board.value[i][j] <= 1024):
                    self.lb[i][j].setStyleSheet("color:" + color[int(math.log(self.board.value[i][j], 2)) - 1] + ";")
                else:
                    self.lb[i][j].setStyleSheet("color:#323232;")

        return None



    def keyPressEvent(self, event):   #назначение стрелок

        key = event.key()
        if (key == Qt.Key.Key_Left):
            self.board.calculator('l')
        if (key == Qt.Key.Key_Right):
            self.board.calculator('r')
        if (key == Qt.Key.Key_Up):
            self.board.calculator('u')
        if (key == Qt.Key.Key_Down):
            self.board.calculator('d')

        self.drawNum()
        self.color_map()

        if (self.board.score == 2048):      #победили
            reply = QMessageBox.question(self,"Вы победили!","Сыграем еще раз?", QMessageBox.Yes | QMessageBox.No)
            if (reply == QMessageBox.Yes):

                self.board = board()
                self.drawNum()
                self.color_map()

            else:
                exit(app.exec_())

        elif (self.board.failure == True):   #проиграли
            reply = QMessageBox.question(self,"Проигрышь =(","Попробуем еще разок?", QMessageBox.Yes | QMessageBox.No)
            if (reply == QMessageBox.Yes):

                self.board = board()
                self.drawNum()
                self.color_map()

            else:
                exit(app.exec_())

        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)


    ex = ui()

    sys.exit(app.exec_())
