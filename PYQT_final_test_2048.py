import sys
import random
from typing import List, Any
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QLabel)
from PyQt5.QtCore import Qt


class board:

    """Отвечает за логику игры

        Методы:

        score_cal -проходится по матрице значений и возвращает текущее максимальное количество очков.
        calculator - складывает соседние ячейки с одинаковыми значениями
        move - определяет опорную ячейку, и перемещает все ячейки к ней по направлению просмотра матрицы
        check - проходится по матрице значений в поиске пустой ячейки
        num_generator - заполняет пустые ячейки матрицы случайными значениями

        """

    def __init__(self):

        """Формирует матрицу 4х4 ( игровое поле), случайно заполняет некоторые ячейки числами
        """

        self.init_val = [0, 0, 0, 0, 2, 2, 4]   #Стартовой набор чисел, у 2 шанс 30%, у 4 - 15%, 0 - 55%

        self.x = 4          #Сторона матрицы(игрового поля). Матрица квадратная 4х4

        self.value = [[random.choice(self.init_val) for i in range(self.x)] for j in range(self.x)]   #Матрица значений, случайно заполненная числами из init_val

        self.failure = self.check()[2]      #показатель заполненности ячеек матрицы числами(отличных от 0)типа Boolean. При полном заполнении = True и игра проиграна

        self.score = self.score_cal()            # текущее максимальное количество очков, значение из метода score_cal. При достижении 2048 игра выиграна.



    def score_cal(self) -> int:

        """Метод проходится по матрице значений и возвращает текущее максимальное количество очков.

            :return: максимальное количество очков (максимальное значение среди всех ячеек матрицы).
            """

        maxim = self.value[0][0]                # текущее максимальное количество очков

        for i in range(self.x):                 # Прохождение по всем ячейкам матрицы в поисках нового макс. значения
            for j in range(self.x):
                if (self.value[i][j] > maxim):
                    maxim = self.value[i][j]       # новое максимальное количество очков

        return maxim



    def calculator(self, direc : str) -> None:

        """Метод складывает соседние ячейки с одинаковыми значениями.

            :param direc: Направление движения - одно из : "r", "l", "u", "d"- в зависимости от команды игрока из
            медота keyPressEvent класса ui.

            """
        self.move(direc)        #вызываем метод move, чтобы сместить все ячейки и начать складывать

        if direc == 'l':
            for i in range(self.x):                 #pos опорная грань(строка или столбец)
                pos = self.x - 1
                while pos > 0:                  #сравниваем два соседних элемента, в случае их равенства выбираем ближнию к опорной точке и умножаем на 2
                    if self.value[i][pos] == self.value[i][pos - 1] and self.value[i][pos] != 0:
                        self.value[i][pos - 1] = self.value[i][pos] * 2
                        self.value[i][pos] = 0
                        self.move(direc)                #вызываем метод move, чтобы cнова сместить все ячейки и продолжить сравнивать
                        pos = self.x - 1
                    pos = pos - 1

        if direc == 'r':                                 #Реализация алгоритма для остальных 3 направлений почти аналогична,за изменением "пути" итерации
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

        self.score = self.score_cal()           # в конце вызываются методы score_call и num_generator для определения текущего статуса игры,
        self.num_generator()



    def move(self, direc) -> None :

        """Метод определяет опорную ячейку, и перемещает все ячейки к ней по направлению просмотра матрицы

            :param direc : направление движения - одно из : "r", "l", "u", "d"- в зависимости от команды игрока из
            медота keyPressEvent класса ui.

            """


        if (direc == 'l'):
            for i in range(self.x):
                temp1 = 0                                   #просматривается вся матрица значений, отталкиваясь от опорной точки с индексами temp1 и temp2
                                                            # опорная точка, которая представляет собой первую ячейку столбца/строки
                for temp2 in range(self.x):                 #является противоположным заданному направлению из медота keyPressEvent класса ui.
                    if (self.value[i][temp2] != 0):
                        self.value[i][temp1] = self.value[i][temp2]             #Если в просматриваемой ячейке находится значение, то смещаем значение к опорной точке
                        temp1 = temp1 + 1
                while (temp1 < self.x):                 #очищаем от содержимого ячейки матрицы, откуда происходило копирование элементов
                    self.value[i][temp1] = 0            #цикл выполняется до тех пор, пока не будут заполнены все пустые значения в пределах опорной грани
                    temp1 = temp1 + 1

        if (direc == 'r'):                              #Реализация алгоритма для остальных 3 направлений почти аналогична,за изменением "пути" итерации
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



    def check(self) -> [str, bool] :
        """Метод проходится по матрице значений в поиске пустой ячейки

        :return: индексы пустых ячеек и показатель заполненности массива
        """


        l1 = []     #Список с вертикальными индексами пустых ячеек
        l2 = []     #Список с горизонтальными индексами пустых ячеек

        for i in range(self.x):
            for j in range(self.x):
                if (self.value[i][j] == 0):          #пустой ячейка считается, если ее значение равно 0
                    l1.append(i)
                    l2.append(j)

        return l1, l2, len(l1) == 0    #формируем одновременно два списка с вертикальными и горизонтальными индексами, а также проверяем остались ли пустые ячейки.




    def num_generator(self) -> None:
        """Метод заполняет пустые ячейки матрицы случайными значениями
            """


        l1, l2, full_or_not = self.check()
        if (full_or_not != True):                   #условие, что есть пустые ячейки

            index = random.sample(range(len(l1)), 1)    #выбираем 1 случайный индекс в зависимости от длины списка с пустыми ячейками
            i = index[0]  #тк index это список с длинной всегда 1, создаем переменную со значением этого элемента для посл. упрощения

            self.value[l1[i]][l2[i]] = random.choice([2, 2, 2, 2, 2, 4, 4])     # заполняем случайную ячейку, выбранную выше 1 случ. числом (2 или 4). у 2 шансов больше

        else:
            self.failure = True   #При полном заполнении игра проиграна, failure = True



class ui(QWidget):
    """Отвечает за графический интерфейс

            Методы:

            initUI - показывает подсказку перед игрой, а также формирует графику начального игрового поля
            label_generator - устанавливает графическое отоброжение ячеек
            drawNum - Изменяет отображение внутри ячеек в соответствии с их значеним.
            color_map - Изменяет цвет значения ячеек в соответствии с их значеним
            keyPressEvent - Производит графические изменения в зависимости от нажатой клавиши, а также
            выводит предложение сыграть заного в случае победы или поражения

            """


    def __init__(self):

        """наследование от класа QWidget
                """
        super().__init__()

        self.initUI()


    def initUI(self) -> None:

        """Метод показывает подсказку перед игрой, а также формирует графику начального игрового поля
            """


        self.resize(600, 600)           #устанавливаем размер игрового окна

        self.height = self.height()             #ширина и высота игрового окна
        self.width = self.width()



        QMessageBox.information(self, "Начало игры","Используйте стрелки на клавиатуре, чтобы набрать 2048 и выиграть!")    #Вызываем окно с подсказской перед игрой

        self.setStyleSheet("QLabel{background-color:rgb(220,220,220);""border-style: outset;}" "QLabel{color:rgb(100,100,100,250);font-size:45px;font-weight:bold;font-family:Roman times;}""QLabel:hover{color:rgb(100,100,100,120);}")
        #Настраиваем цвета переднего плана и фона


        self.board = board()
        self.lb = self.label_generator()

        self.drawNum()                  #формируем значение ячеек и их цвета
        self.color_map()

        self.setWindowTitle('Игра 2048')   #Название окна
        self.show()

    def label_generator(self) -> List:

        """Метод устанавливает графическое отоброжение ячеек
            """

        lb = [[i for i in range(4)] for j in range(4)]              # создаем доп. матрицу для графического отоброжения
                                                                  #устанавливаем размеры каждой ячейки на доске
        self.lb_width = int((self.width - 45) / 4)
        self.lb_height = int((self.height - 45) / 4)

        for i in range(4):
            for j in range(4):
                lb[i][j] = QLabel(str(self.board.value[i][j]), self)                                        #Графическое отоброжение ячеек cостоит из QLabel в кол-ве равным кол-ву ячеек матрицы
                lb[i][j].setGeometry(15 + (self.lb_width + 5) * j, 15 + (self.lb_height + 5) * i,self.lb_width, self.lb_height)         #устанавливаем положение ячеек на доске
                lb[i][j].setAlignment(Qt.AlignmentFlag.AlignCenter)         #устанавливаем отоброжение значений в центре ячейки
        return lb



    def drawNum(self) -> None :

        """Изменяет отображение содержимого ячеек в соответствии с их значеним.
            """

        for i in range(4):
            for j in range(4):
                if (self.board.value[i][j] == 0):               #При значении 0 - ячейка считается пустой, соответственно ничего не отоброжаем
                    self.lb[i][j].setText('')
                else:
                    self.lb[i][j].setText(str(self.board.value[i][j]))          #отоброжаем значение ячейки




    def color_map(self) -> None :
        """Изменяет цвет значения ячеек в соответствии с их значеним
            """

        color = ["#4682B4", "#00CED1", "#FF1493", "#FFA500", "#8B3626", "#8B0000", "#FF8247", "#FFA500", "#FF4500",
                 "#FF0000"]

        for i in range(4):
            for j in range(4):
                if (self.board.value[i][j] >= 2 and self.board.value[i][j] <= 1024):                        #изменяем цвет каждой ячейки кроме от 2 и 1024
                    self.lb[i][j].setStyleSheet("color:" + color[int(math.log(self.board.value[i][j], 2)) - 1])
                else:
                    self.lb[i][j].setStyleSheet("color:#323232;")





    def keyPressEvent(self, event) -> None:

        """Производит графические изменения в зависимости от нажатой клавиши, а также
            выводит предложение сыграть заного в случае победы или поражения
            :param event: одна из 4х клавиш со стрелками
            """
        key = event.key()                               #Определение смещение матрицы, а также сложение возможных ячеек в зависимости от нажатой клавиши
        if (key == Qt.Key.Key_Left):
            self.board.calculator('l')
        if (key == Qt.Key.Key_Right):
            self.board.calculator('r')
        if (key == Qt.Key.Key_Up):
            self.board.calculator('u')
        if (key == Qt.Key.Key_Down):
            self.board.calculator('d')

        self.drawNum()                               #Методы  drawNum и color_map вызываются для графического обновления в связи с изменением матрицы
        self.color_map()

        if (self.board.score == 2048):      #победа
            reply = QMessageBox.question(self,"Вы победили!","Сыграем еще раз?", QMessageBox.Yes | QMessageBox.No)  #Окно с предложением сыграть снова
            if (reply == QMessageBox.Yes):
                                            #запускаем игру заного
                self.board = board()
                self.drawNum()
                self.color_map()

            else:
                exit(app.exec_())       #закрываем игру

        elif (self.board.failure == True):   #Аналогично, только сообщение о проигрыше
            reply = QMessageBox.question(self,"Проигрышь =(","Попробуем еще разок?", QMessageBox.Yes | QMessageBox.No)
            if (reply == QMessageBox.Yes):

                self.board = board()
                self.drawNum()
                self.color_map()

            else:
                exit(app.exec_())




if __name__ == '__main__':
    app = QApplication(sys.argv)


    ex = ui()

    sys.exit(app.exec_())
