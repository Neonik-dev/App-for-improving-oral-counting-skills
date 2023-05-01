import sys
import random
import sqlite3

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QColorDialog
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QMessageBox, QLCDNumber
from PyQt5.QtGui import QPixmap

NAME_USER = "NoName"
AUTH_OR_REG = 0
COUNT_TRIES_EQUATIONS = 0
COUNT_TRUES_EQUATIONS = 0
COUNT_TRIES_ANGLES = 0
COUNT_TRUES_ANGLES = 0
TIMER = 0
TIME_COUNT = 0
COUNT_ARRAY = 0

global begin, array


class Enter_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(400, 200, 600, 400)
        self.setWindowTitle('Проверка знаний по математике')

        self.enter_btn = QPushButton('ВХОД', self)
        self.enter_btn.resize(120, 50)
        self.enter_btn.move(240, 135)
        self.f_r.seek(7)
        self.enter_btn.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.reg_btn = QPushButton('РЕГИСТРАЦИЯ', self)
        self.reg_btn.resize(120, 50)
        self.reg_btn.move(240, 195)
        self.f_r.seek(7)
        self.reg_btn.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.enter_btn.clicked.connect(self.open_login_form)
        self.reg_btn.clicked.connect(self.open_login_form)
        self.f_r.close()

    def open_login_form(self):
        global AUTH_OR_REG
        if self.sender().text() == 'ВХОД':
            AUTH_OR_REG = 0
        else:
            AUTH_OR_REG = 1
        self.login_form = Login_Window()
        self.login_form.show()
        self.close()


class Login_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global AUTH_OR_REG

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(550, 270, 370, 300)
        if AUTH_OR_REG == 0:
            self.setWindowTitle('Авторизация')
        else:
            self.setWindowTitle('Регистрация')

        self.name_label = QLabel(self)
        self.name_label.setText("Введите имя: ")
        self.name_label.move(35, 50)
        self.name_input = QLineEdit(self)
        self.name_input.move(180, 43)
        self.f_r.seek(14)
        self.name_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.surname_label = QLabel(self)
        self.surname_label.setText("Введите фамилию: ")
        self.surname_label.move(35, 100)
        self.surname_input = QLineEdit(self)
        self.surname_input.move(180, 93)
        self.f_r.seek(14)
        self.surname_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.password_label = QLabel(self)
        self.password_label.setText("Введите пароль: ")
        self.password_label.move(35, 150)
        self.password_input = QLineEdit(self)
        self.password_input.move(180, 143)
        self.f_r.seek(14)
        self.password_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.cancel_btn = QPushButton("← Назад", self)
        self.cancel_btn.resize(90, 30)
        self.cancel_btn.move(10, 260)
        self.cancel_btn.clicked.connect(self.back)
        self.f_r.seek(7)
        self.cancel_btn.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        if AUTH_OR_REG == 0:
            self.exit_btn = QPushButton('Авторизоваться', self)
            self.exit_btn.resize(140, 50)
            self.exit_btn.move(115, 200)
        else:
            self.exit_btn = QPushButton('Зарегистрироваться', self)
            self.exit_btn.resize(160, 50)
            self.exit_btn.move(105, 200)
        self.f_r.seek(7)
        self.exit_btn.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        if AUTH_OR_REG == 0:
            self.exit_btn.clicked.connect(self.input)
        else:
            self.exit_btn.clicked.connect(self.input)

    def back(self):
        self.back_form = Enter_Window()
        self.back_form.show()
        self.close()

    def input(self):
        global NAME_USER

        if self.name_input.text() and self.surname_input.text() and self.password_input.text():
            con = sqlite3.connect("name_users.db")
            cur = con.cursor()
            result1 = cur.execute("""SELECT * FROM Name_users
                            WHERE name = ? and surname = ? and password = ?""", (self.name_input.text(),
                                                                                 self.surname_input.text(),
                                                                                 self.password_input.text())).fetchone()
            if result1 == None and self.sender().text() == 'Авторизоваться':
                QMessageBox.critical(self, "Ошибка ", "К сожалению, такого пользователя не существует,"
                                                                            " попробуйте снова", QMessageBox.Ok)
            elif result1 != None and self.sender().text() == "Зарегистрироваться":
                QMessageBox.critical(self, "Ошибка ", "К сожалению, такой пользователь уже существует,"
                                                      " попробуйте снова", QMessageBox.Ok)
            else:
                if self.sender().text() == "Зарегистрироваться":
                    cur.execute("""INSERT INTO Name_users VALUES(?,?,?)""",
                                (self.name_input.text(), self.surname_input.text(),
                                 self.password_input.text()))
                    con.commit()
                NAME_USER = self.name_input.text()
                self.main_menu = MainMenu()
                self.main_menu.show()
                self.close()
                con.close()


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global NAME_USER

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(400, 200, 500, 380)
        self.setWindowTitle('Главное меню')

        hello_name = f"Привет, {NAME_USER}"
        self.hello_name_label = QLabel(hello_name, self)
        self.hello_name_label.setFont(QtGui.QFont("Currently only TrueType fonts", 12))
        self.hello_name_label.resize(200, 50)
        self.hello_name_label.move(160, 30)
        self.f_r.seek(14)
        self.hello_name_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.start_btn = QPushButton('Начать', self)
        self.start_btn.resize(180, 60)
        self.start_btn.move(160, 80)
        self.f_r.seek(7)
        self.start_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.info_btn = QPushButton('Прочти меня!', self)
        self.info_btn.resize(180, 60)
        self.info_btn.move(160, 150)
        self.f_r.seek(7)
        self.info_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, '#340B90'))

        font = QtGui.QFont()
        font.setPointSize(14)
        self.info_btn.setFont(font)

        self.settings_btn = QPushButton("Настройки", self)
        self.settings_btn.resize(180, 60)
        self.settings_btn.move(160, 220)
        self.f_r.seek(7)
        self.settings_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.exit_btn = QPushButton('Выход', self)
        self.exit_btn.resize(180, 60)
        self.exit_btn.move(160, 290)
        self.f_r.seek(7)
        self.exit_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        self.start_btn.clicked.connect(self.input)
        self.info_btn.clicked.connect(self.input)
        self.exit_btn.clicked.connect(self.input)
        self.settings_btn.clicked.connect(self.input)

    def input(self):
        if self.sender().text() == 'Начать':
            self.cont = Chose_Window()
        elif self.sender().text() == 'Прочти меня!':
            self.cont = Information_Window()
        elif self.sender().text() == 'Выход':
            self.cont = Question_Window()
        else:
            self.cont = Settings_Windows()
        self.cont.show()
        self.close()


class Settings_Windows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(400, 200, 400, 350)
        self.setWindowTitle('Настройки')

        self.label = QLabel(self)
        self.label.resize(400, 20)
        self.label.setText("Здесь ты можешь поменять цвет")
        self.label.setFont(QtGui.QFont("TrueType font collections", 12))
        self.label.move(60, 15)
        self.f_r.seek(14)
        self.label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.fon_btn = QPushButton('Фон', self)
        self.fon_btn.resize(150, 50)
        self.fon_btn.move(125, 70)
        self.f_r.seek(7)
        self.fon_btn.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.btns = QPushButton('Кнопки', self)
        self.btns.resize(150, 50)
        self.btns.move(125, 150)
        self.f_r.seek(7)
        self.btns.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.label_btn = QPushButton('Текст', self)
        self.label_btn.resize(150, 50)
        self.label_btn.move(125, 230)
        self.f_r.seek(7)
        self.label_btn.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.back_to_main_btn = QPushButton('← Назад', self)
        self.back_to_main_btn.resize(90, 30)
        self.back_to_main_btn.move(20, 300)
        self.f_r.seek(7)
        self.back_to_main_btn.setStyleSheet("QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        self.back_to_main_btn.clicked.connect(self.back)
        self.fon_btn.clicked.connect(self.fon_Dialog)
        self.btns.clicked.connect(self.btns_Dialog)
        self.label_btn.clicked.connect(self.label_Dialog)

    def back(self):
        self.back_form = MainMenu()
        self.back_form.show()
        self.close()

    def fon_Dialog(self):
        self.f_w = open("info", mode='r+')
        col = QColorDialog.getColor()
        if col.isValid():
            self.f_w.seek(0)
            self.f_w.write(col.name())
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.f_w.close()

    def btns_Dialog(self):
        with open('info', mode='r+') as self.f_w:
            col = QColorDialog.getColor()
            if col.isValid():
                self.f_w.seek(7)
                self.f_w.write(col.name())
                self.f_w.seek(14)
                self.btns.setStyleSheet(
                    "QPushButton { background-color: %s; border: %s; color: %s}" % (col.name(), None, self.f_w.read(7)))
                self.f_w.seek(14)
                self.back_to_main_btn.setStyleSheet(
                    "QPushButton { background-color: %s; border: %s; color: %s}" % (col.name(), None, self.f_w.read(7)))
                self.f_w.seek(14)
                self.label_btn.setStyleSheet(
                    "QPushButton { background-color: %s; border: %s; color: %s}" % (col.name(), None, self.f_w.read(7)))
                self.f_w.seek(14)
                self.fon_btn.setStyleSheet(
                    "QPushButton { background-color: %s; border: %s; color: %s}" % (col.name(), None, self.f_w.read(7)))
            self.f_w.close()

    def label_Dialog(self):
        self.f_w = open("info", mode='r+')
        col = QColorDialog.getColor()
        if col.isValid():
            self.f_w.seek(14)
            self.f_w.write(col.name())
            self.f_w.seek(7)
            self.btns.setStyleSheet(
                "QPushButton { color: %s; border: %s; background-color: %s}" % (col.name(), None, self.f_w.read(7)))
            self.f_w.seek(7)
            self.back_to_main_btn.setStyleSheet(
                "QPushButton { color: %s; border: %s; background-color: %s}" % (col.name(), None, self.f_w.read(7)))
            self.f_w.seek(7)
            self.label_btn.setStyleSheet(
                "QPushButton { color: %s; border: %s; background-color: %s}" % (col.name(), None, self.f_w.read(7)))
            self.f_w.seek(7)
            self.fon_btn.setStyleSheet(
                "QPushButton { color: %s; border: %s; background-color: %s}" % (col.name(), None, self.f_w.read(7)))
            self.label.setStyleSheet("QLabel {color: %s;}" % col.name())
        self.f_w.close()


class Chose_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(550, 300, 275, 290)
        self.setWindowTitle('Выбор темы')

        self.label = QLabel(self)
        self.label.resize(200, 15)
        self.label.setText("Выберите тему:")
        self.label.setFont(QtGui.QFont("Currently only TrueType fonts", 12))
        self.label.move(75, 15)
        self.f_r.seek(14)
        self.label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.normal_btn = QPushButton('Решение\nуравнений', self)
        self.normal_btn.resize(237, 50)
        self.normal_btn.move(20, 50)
        self.f_r.seek(7)
        self.normal_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.formula_btn = QPushButton('Формулы\nприведения', self)
        self.formula_btn.resize(237, 50)
        self.formula_btn.move(20, 170)
        self.f_r.seek(7)
        self.formula_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.angles_btn = QPushButton('Нахождение\n  углов', self)
        self.angles_btn.resize(237, 50)
        self.angles_btn.move(20, 110)
        self.f_r.seek(7)
        self.angles_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.cancel_btn = QPushButton('Отмена', self)
        self.cancel_btn.resize(237, 30)
        self.cancel_btn.move(20, 250)
        self.f_r.seek(7)
        self.cancel_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        self.cancel_btn.clicked.connect(self.cancel)
        self.normal_btn.clicked.connect(self.normal_begin)
        self.angles_btn.clicked.connect(self.angles)
        self.formula_btn.clicked.connect(self.formula)

    def cancel(self):
        self.cancel_form = MainMenu()
        self.cancel_form.show()
        self.close()

    def normal_begin(self):
        self.norm_play_form = Play_Window()
        self.norm_play_form.show()
        self.close()

    def angles(self):
        self.angles_play_form = Angles_Windows()
        self.angles_play_form.show()
        self.close()

    def formula(self):
        self.formula_play_form = Trigan_Window()
        self.formula_play_form.show()
        self.close()


class Play_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global TIMER, array
        global TIME_COUNT, COUNT_ARRAY

        TIMER = 1

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(400, 200, 600, 400)
        self.setWindowTitle('Решение уравнений')

        con = sqlite3.connect("name_users.db")
        cur = con.cursor()

        self.name_label = QLabel(self)
        self.name_label.setText("Решите уравнение:")
        self.name_label.resize(600, 30)
        self.name_label.move(15, 8)
        self.f_r.seek(14)
        self.name_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.answer_name_label = QLabel(self)
        self.answer_name_label.setText("Введите ваш ответ: ")
        self.answer_name_label.resize(250, 50)
        self.answer_name_label.move(15, 305)
        self.f_r.seek(14)
        self.answer_name_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))


        self.rec_btn = QPushButton('Следующее', self)
        self.rec_btn.resize(560, 170)
        self.rec_btn.move(20, 120)
        self.f_r.seek(7)
        self.rec_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        font = QtGui.QFont()
        font.setPointSize(17)
        self.rec_btn.setFont(font)

        self.rec_btn.clicked.connect(self.recursion)

        result = cur.execute("""SELECT * FROM Equations
                                                            WHERE way like '%'""").fetchall()
        if COUNT_ARRAY == 0:
            array = list(result)
            random.shuffle(array)

        self.true_answers = []
        self.player_answers = []

        self.way = array[COUNT_ARRAY]
        self.true_answers.append(self.way[1])

        self.pixmap = QPixmap(self.way[0])
        self.image = QLabel(self)
        self.image.move(0, 45)
        self.image.resize(600, 50)
        self.image.setPixmap(self.pixmap)

        self.answer_input = QLineEdit(self)
        self.answer_input.resize(150, 25)
        self.answer_input.move(180, 320)

        self.player_answers.append(self.answer_input.text())

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(0, 0, 80, 35))
        self.lcdNumber.move(500, 10)
        self.lcdNumber.setNumDigits(5)
        self.str1 = "{:0>2d}:{:0>2d}".format(begin // 60, begin % 60)
        self.lcdNumber.display(self.str1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        con.commit()
        con.close()

    def recursion(self):
        global COUNT_TRIES_EQUATIONS, begin
        global COUNT_TRUES_EQUATIONS, COUNT_ARRAY

        self.timer.stop()

        if str(self.answer_input.text()) == str(self.true_answers[-1]):
            COUNT_TRUES_EQUATIONS += 1

        COUNT_TRIES_EQUATIONS += 1
        COUNT_ARRAY += 1

        if COUNT_TRIES_EQUATIONS < 20:
            self.rec_form = Play_Window()
            self.rec_form.show()
            self.close()
        else:
            COUNT_ARRAY = 0
            self.res_form = Result_Window()
            self.res_form.show()
            self.close()

    def showTime(self):
        global begin
        begin = begin + 1
        self.str1 = "{:0>2d}:{:0>2d}:{:0>2d}".format(begin // 3600, (begin % 3600) // 60, begin % 60)
        self.lcdNumber.display(self.str1)


class Result_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global COUNT_TRUES_EQUATIONS, begin
        global COUNT_TRIES_EQUATIONS

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(500, 300, 400, 200)
        self.setWindowTitle('Результаты работы')

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(0, 0, 80, 35))
        self.lcdNumber.move(300, 10)
        self.lcdNumber.setNumDigits(5)
        self.str1 = "{:0>2d}:{:0>2d}".format(begin // 60, begin % 60)
        self.lcdNumber.display(self.str1)

        self.result_label = QLabel(self)
        self.result_label.setText(f"Ваш результат: {COUNT_TRUES_EQUATIONS} из {COUNT_TRIES_EQUATIONS}")
        self.result_label.setFont(QtGui.QFont("Currently only TrueType fonts", 14))
        self.result_label.resize(300, 50)
        self.result_label.move(80, 70)
        self.f_r.seek(14)
        self.result_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))
        COUNT_TRIES_EQUATIONS = 0
        COUNT_TRUES_EQUATIONS = 0

        begin = 0

        self.back_btn = QPushButton('← Меню', self)
        self.back_btn.resize(90, 30)
        self.back_btn.move(10, 160)
        self.f_r.seek(7)
        self.back_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.qu_btn = QPushButton('↺ Заново', self)
        self.qu_btn.resize(90, 30)
        self.qu_btn.move(110, 160)
        self.f_r.seek(7)
        self.qu_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()


        self.back_btn.clicked.connect(self.back)
        self.qu_btn.clicked.connect(self.ques)

    def back(self):
        self.back_form = MainMenu()
        self.back_form.show()
        self.close()

    def ques(self):
        self.ques_form = Play_Window()
        self.ques_form.show()
        self.close()


class Angles_Windows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global begin, COUNT_ARRAY, array
        global TIME_COUNT, TIMER

        TIMER = 1

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(400, 200, 500, 370)
        self.setWindowTitle('Нахождение углов')

        con = sqlite3.connect("name_users.db")
        cur = con.cursor()

        self.answer_name_label = QLabel(self)
        self.answer_name_label.setText("Введите ваши ответы: ")
        self.answer_name_label.resize(250, 50)
        self.answer_name_label.move(15, 305)
        self.f_r.seek(14)
        self.answer_name_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.rec_btn = QPushButton('Следующий', self)
        self.rec_btn.resize(215, 260)
        self.rec_btn.move(270, 45)
        self.f_r.seek(7)
        self.rec_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        font = QtGui.QFont()
        font.setPointSize(16)
        self.rec_btn.setFont(font)

        result = cur.execute("""SELECT * FROM Angles
                                                                    WHERE way like '%'""")
        if COUNT_ARRAY == 0:
            array = list(result)
            random.shuffle(array)

        self.true_answers = []
        self.player_answers = []

        self.way = array[COUNT_ARRAY]
        self.true_answers.append(self.way[1])

        self.pixmap = QPixmap(self.way[0])
        self.image = QLabel(self)
        self.image.move(30, 45)
        self.image.resize(215, 235)
        self.image.setPixmap(self.pixmap)

        self.answer_input = QLineEdit(self)
        self.answer_input.resize(150, 25)
        self.answer_input.move(180, 320)

        self.player_answers.append(self.answer_input.text())

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(0, 0, 80, 35))
        self.lcdNumber.move(405, 320)
        self.lcdNumber.setNumDigits(5)
        self.str1 = "{:0>2d}:{:0>2d}".format(begin // 60, begin % 60)
        self.lcdNumber.display(self.str1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        con.commit()
        con.close()
        self.rec_btn.clicked.connect(self.recursion)

    def recursion(self):
        global COUNT_TRIES_ANGLES, array, COUNT_ARRAY
        global COUNT_TRUES_ANGLES, begin

        self.timer.stop()

        if str(self.answer_input.text()) == str(self.true_answers[-1]):
            COUNT_TRUES_ANGLES += 1

        COUNT_TRIES_ANGLES += 1
        COUNT_ARRAY += 1

        if COUNT_TRIES_ANGLES < 34:
            self.rec_form = Angles_Windows()
            self.rec_form.show()
            self.close()
        else:
            COUNT_ARRAY = 0
            self.res_form = Result_Angles_Window()
            self.res_form.show()
            self.close()

    def showTime(self):
        global begin
        begin = begin + 1
        self.str1 = "{:0>2d}:{:0>2d}:{:0>2d}".format(begin // 3600, (begin % 3600) // 60, begin % 60)
        self.lcdNumber.display(self.str1)


class Result_Angles_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global COUNT_TRUES_ANGLES
        global COUNT_TRIES_ANGLES, begin

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(500, 300, 400, 200)
        self.setWindowTitle('Результаты работы')

        self.result_label = QLabel(self)
        self.result_label.setText(f"Ваш результат: {COUNT_TRUES_ANGLES} из 34")
        self.result_label.setFont(QtGui.QFont("Currently only TrueType fonts", 14))
        self.result_label.resize(300, 50)
        self.result_label.move(70, 70)
        self.f_r.seek(14)
        self.result_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))
        COUNT_TRIES_ANGLES = 0
        COUNT_TRUES_ANGLES = 0

        self.back_btn = QPushButton('← Меню', self)
        self.back_btn.resize(90, 30)
        self.back_btn.move(10, 160)
        self.f_r.seek(7)
        self.back_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.qu_btn = QPushButton('↺ Заново', self)
        self.qu_btn.resize(90, 30)
        self.qu_btn.move(110, 160)
        self.f_r.seek(7)
        self.qu_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(0, 0, 80, 35))
        self.lcdNumber.move(300, 10)
        self.lcdNumber.setNumDigits(5)
        self.str1 = "{:0>2d}:{:0>2d}".format(begin // 60, begin % 60)
        self.lcdNumber.display(self.str1)

        begin = 0

        self.back_btn.clicked.connect(self.back)
        self.qu_btn.clicked.connect(self.ques)

    def back(self):
        self.back_form = MainMenu()
        self.back_form.show()
        self.close()

    def ques(self):
        self.ques_form = Angles_Windows()
        self.ques_form.show()
        self.close()


class Trigan_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global TIMER, COUNT_ARRAY
        global TIME_COUNT, array

        TIMER = 1

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(400, 200, 500, 450)
        self.setWindowTitle('Формулы приведения')

        con = sqlite3.connect("name_users.db")
        cur = con.cursor()

        self.answer_name_label = QLabel(self)
        self.answer_name_label.setText("Введите ваш ответ: ")
        self.answer_name_label.resize(250, 50)
        self.answer_name_label.move(0, 380)
        self.f_r.seek(14)
        self.answer_name_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.rec_btn = QPushButton('Следующий', self)
        self.rec_btn.resize(480, 170)
        self.rec_btn.move(10, 200)
        self.f_r.seek(7)
        self.rec_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        font = QtGui.QFont()
        font.setPointSize(17)
        self.rec_btn.setFont(font)

        self.rec_btn.clicked.connect(self.recursion)

        result = cur.execute("""SELECT * FROM Trigonometry WHERE Way like '%'""")
        if COUNT_ARRAY == 0:
            array = list(result)
            random.shuffle(array)

        self.true_answers = []
        self.player_answers = []

        self.way = array[COUNT_ARRAY]
        self.true_answers.append(self.way[1])

        self.pixmap = QPixmap(self.way[0])
        self.image = QLabel(self)
        self.image.move(85, 10)
        self.image.resize(330, 160)
        self.image.setPixmap(self.pixmap)

        self.answer_input = QLineEdit(self)
        self.answer_input.resize(150, 30)
        self.answer_input.move(160, 390)

        self.player_answers.append(self.answer_input.text())

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(0, 0, 80, 35))
        self.lcdNumber.move(400, 390)
        self.lcdNumber.setNumDigits(5)
        self.str1 = "{:0>2d}:{:0>2d}".format(begin // 60, begin % 60)
        self.lcdNumber.display(self.str1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        con.commit()
        con.close()

    def recursion(self):
        global COUNT_TRIES_EQUATIONS, begin
        global COUNT_TRUES_EQUATIONS, COUNT_ARRAY

        self.timer.stop()

        if str(self.answer_input.text()) == str(self.true_answers[-1]):
            COUNT_TRUES_EQUATIONS += 1

        COUNT_TRIES_EQUATIONS += 1
        COUNT_ARRAY += 1

        if COUNT_TRIES_EQUATIONS < 32:
            self.rec_form = Trigan_Window()
            self.rec_form.show()
            self.close()
        else:
            COUNT_ARRAY = 0
            self.res_form = Trigan_Result_Window()
            self.res_form.show()
            self.close()

    def showTime(self):
        global begin
        begin = begin + 1
        self.str1 = "{:0>2d}:{:0>2d}:{:0>2d}".format(begin // 3600, (begin % 3600) // 60, begin % 60)
        self.lcdNumber.display(self.str1)


class Trigan_Result_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global COUNT_TRUES_EQUATIONS, begin
        global COUNT_TRIES_EQUATIONS

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(500, 300, 400, 200)
        self.setWindowTitle('Результаты работы')

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setGeometry(QtCore.QRect(0, 0, 80, 35))
        self.lcdNumber.move(300, 10)
        self.lcdNumber.setNumDigits(5)
        self.str1 = "{:0>2d}:{:0>2d}".format(begin // 60, begin % 60)
        self.lcdNumber.display(self.str1)

        self.result_label = QLabel(self)
        self.result_label.setText(f"Ваш результат: {COUNT_TRUES_EQUATIONS} из {COUNT_TRIES_EQUATIONS}")
        self.result_label.setFont(QtGui.QFont("Currently only TrueType fonts", 14))
        self.result_label.resize(300, 50)
        self.result_label.move(70, 70)
        self.f_r.seek(14)
        self.result_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))
        COUNT_TRIES_EQUATIONS = 0
        COUNT_TRUES_EQUATIONS = 0

        begin = 0

        self.back_btn = QPushButton('← Меню', self)
        self.back_btn.resize(90, 30)
        self.back_btn.move(10, 160)
        self.f_r.seek(7)
        self.back_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.qu_btn = QPushButton('↺ Заново', self)
        self.qu_btn.resize(90, 30)
        self.qu_btn.move(110, 160)
        self.f_r.seek(7)
        self.qu_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()


        self.back_btn.clicked.connect(self.back)
        self.qu_btn.clicked.connect(self.ques)

    def back(self):
        self.back_form = MainMenu()
        self.back_form.show()
        self.close()

    def ques(self):
        self.ques_form = Trigan_Window()
        self.ques_form.show()
        self.close()


class Information_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global NAME_USER

        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(400, 200, 500, 400)
        self.setWindowTitle('Информация')

        self.info_print_label = QLabel(self)
        self.info_print_label.setText(f"        Приветствую, {NAME_USER}! Перед тем,"
                                      f" как приступить к тренеровке, \nпрочитай правила!")
        self.info_print_label.resize(600, 40)
        self.info_print_label.move(10, 20)
        self.f_r.seek(14)
        self.info_print_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.equations_label = QLabel(self)
        self.equations_label.setText(f"<b>Решение уравнений</b>")
        self.equations_label.resize(150, 40)
        self.equations_label.move(170, 70)
        self.f_r.seek(14)
        self.equations_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.pravilo1_label = QLabel(self)
        self.pravilo1_label.setText(f"1.  Если ответ десятичный, то используй '.' \n"
                                    f"2.  Если число имеет сотую или тысячную часть, то ответ записывай\n"
                                    f"ввиде дроби, используя знак '/'\n"
                                    f"3.  Ответы записывай по возрастанию")
        self.pravilo1_label.resize(600, 80)
        self.pravilo1_label.move(10, 100)
        self.f_r.seek(14)
        self.pravilo1_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.angles_label = QLabel(self)
        self.angles_label.setText(f"<b>Формулы приведения</b>")
        self.angles_label.resize(160, 40)
        self.angles_label.move(165, 180)
        self.f_r.seek(14)
        self.angles_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.pravilo2_label = QLabel(self)
        self.pravilo2_label.setText(f"1.  Альфа пиши буквой 'a'\n"
                                    f"2.  Не отделяй альфа от тригонометрических функций пробелом,\nпиши все слитно,"
                                    f" вот так: 'cosa'\n"
                                    f"3.  Знак минус пиши слитно с тригонометрическими функциями,\nвот так: '-sina'")
        self.pravilo2_label.resize(600, 90)
        self.pravilo2_label.move(10, 220)
        self.f_r.seek(14)
        self.pravilo2_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.hello_name_label = QLabel(self)
        self.hello_name_label.setText(f"<b>Удачи, {NAME_USER}!</b>")
        self.hello_name_label.resize(150, 50)
        self.hello_name_label.move(190, 300)
        self.f_r.seek(14)
        self.hello_name_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.angles_label = QLabel(self)
        self.angles_label.setText(f"Разработчик: <b>Neonik</b>")
        self.angles_label.resize(160, 40)
        self.angles_label.move(330, 350)
        self.f_r.seek(14)
        self.angles_label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.back_to_main_btn = QPushButton('← Назад', self)
        self.back_to_main_btn.resize(90, 30)
        self.back_to_main_btn.move(20, 350)
        self.f_r.seek(7)
        self.back_to_main_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        self.back_to_main_btn.clicked.connect(self.back)

    def back(self):
        self.back_form = MainMenu()
        self.back_form.show()
        self.close()


class Question_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.f_r = open("info", mode='r')
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % self.f_r.read(7))
        self.frm.setGeometry(0, 0, 2000, 1000)

        self.setGeometry(550, 300, 275, 100)
        self.setWindowTitle('Подтверждение действия')

        self.label = QLabel(self)
        self.label.resize(215, 15)
        self.label.setText("Вы уверены, что хотите выйти?")
        self.label.move(30, 15)
        self.f_r.seek(14)
        self.label.setStyleSheet("QLabel {color: %s;}" % self.f_r.read(7))

        self.yes_btn = QPushButton('ДА', self)
        self.yes_btn.resize(90, 30)
        self.yes_btn.move(20, 50)
        self.f_r.seek(7)
        self.yes_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))

        self.no_btn = QPushButton('НЕТ', self)
        self.no_btn.resize(90, 30)
        self.no_btn.move(170, 50)
        self.f_r.seek(7)
        self.no_btn.setStyleSheet(
            "QPushButton { background-color: %s; border: %s; color: %s}" % (self.f_r.read(7), None, self.f_r.read(7)))
        self.f_r.close()

        self.yes_btn.clicked.connect(self.exit)
        self.no_btn.clicked.connect(self.not_exit)

    def exit(self):
        self.enter_form = Enter_Window()
        self.enter_form.show()
        self.close()

    def not_exit(self):
        self.main_menu = MainMenu()
        self.main_menu.show()
        self.close()


if __name__ == '__main__':
    begin = 0
    app = QApplication(sys.argv)
    ex = Enter_Window()
    ex.show()
    sys.exit(app.exec())
