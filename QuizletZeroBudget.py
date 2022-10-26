import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("search.ui", self)
        self.con = sqlite3.connect("cards.db")
        res = self.con.cursor().execute("SELECT * FROM decks").fetchall()    # вывод наборов на экран
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.id = None

        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(0, 0)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 251)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(4, 120)
        self.tableWidget.setColumnWidth(5, 0)
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Название"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Описание"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("№ определений"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Пользователь"))
        self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem("Цена"))

        self.conditions = [False, False, False, '']

        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.search_decks.clicked.connect(self.search)

        self.create.clicked.connect(self.open_create)

        self.select.clicked.connect(lambda x: self.open_select(self.id))

        self.update.clicked.connect(self.upd)

        self.tableWidget.cellClicked.connect(self.get_id)

        self.select.clicked.connect(self.learning)

        self.free.toggled.connect(self.show_only_free)

        self.premium.toggled.connect(self.show_only_premium)

        self.my_decks.toggled.connect(self.show_only_my_decks)

        self.both.toggled.connect(self.show_all_prices)

    def show_data(self):
        if self.conditions[0]:
            req = "SELECT * FROM decks WHERE price = 'Free' AND name LIKE ?"
            if self.conditions[2]:
                req = "SELECT * FROM decks WHERE price = 'Free' AND user = 'me' AND name LIKE ?"
        elif self.conditions[1]:
            req = "SELECT * FROM decks WHERE price = 'Premium' AND name LIKE ?"
            if self.conditions[2]:
                req = "SELECT * FROM decks WHERE price = 'Premium' AND user = 'me' AND name LIKE ?"
        elif self.conditions[2]:
            req = "SELECT * FROM decks WHERE user = 'me' AND name LIKE ?"
        else:
            req = "SELECT * FROM decks WHERE name LIKE ?"
        res = self.con.cursor().execute(req, ('%' + self.conditions[3] + '%', )).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def show_all_prices(self):
        if self.both.isChecked():
            self.conditions[0], self.conditions[1] = False, False
            self.show_data()
        else:
            self.show_data()

    def show_only_free(self):
        if self.free.isChecked():
            self.conditions[0], self.conditions[1] = True, False
            self.premium.setChecked(False)
            self.show_data()
        else:
            self.conditions[0] = False
            self.show_data()

    def show_only_premium(self):
        if self.premium.isChecked():
            self.conditions[1], self.conditions[0] = True, False
            self.free.setChecked(False)
            self.show_data()
        else:
            self.conditions[1] = False
            self.show_data()

    def show_only_my_decks(self):
        if self.my_decks.isChecked():
            self.conditions[2] = True
            self.show_data()
        else:
            self.conditions[2] = False
            self.show_data()

    def get_id(self, row, column):    # получение id выбранного набора слов для дальнейшего изучения
        dat = self.tableWidget.item(row, 1)
        data = dat.text()
        self.id = self.con.cursor().execute("SELECT id FROM decks where name = ?", (data, )).fetchone()

    def learning(self):
        if self.id is not None:
            self.open_select(self.id)    # открываем форму для изучения

    def open_create(self):    # открываем форму для создания наборов
        self.create_form = SecondForm(self.con)
        self.create_form.show()

    def open_select(self, id):    # открываем форму для изучения
        self.select_form = ThirdForm(id, self.con)
        self.select_form.show()

    def search(self):    # поиск наборов по названию
        request = self.lineEdit.text()
        self.conditions[3] = request
        self.show_data()

    def keyPressEvent(self, event):    # таким образом при нажатии на enter поиск будет производиться
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            request = self.lineEdit.text()
            self.conditions[3] = request
            self.show_data()

    def upd(self):    # обновление главного окна
        res = self.con.cursor().execute("SELECT * FROM decks").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.con.close()


class SecondForm(QWidget):    # форма для создания наборов
    def __init__(self, con):
        super().__init__()
        uic.loadUi("creating.ui", self)
        self.con = con

        self.setWindowTitle('Create')

        self.add_deck.clicked.connect(self.add)

        self.comboBox.addItems(['Free', 'Premium'])

    def add(self):    # добавление набора
        title = self.title.text()
        description = self.description.text()
        if bool(title) and bool(description):
            cur = self.con.cursor()
            cur.execute("""INSERT INTO decks(name, description, quantity, user, price) VALUES(?, ?, 0, 'me', ?)""",
                        (title, description, self.comboBox.currentText()))
            self.id = cur.execute("""SELECT id FROM decks WHERE name LIKE ?""", (title, )).fetchone()[0]
            self.quant = cur.execute("SELECT quantity FROM decks WHERE name LIKE ?", (title, )).fetchone()[0]
            self.added_successfully_2.setText('Набор успешно добавлен')

            self.add_button.clicked.connect(self.add_terms)
        else:
            self.added_successfully_2.setText('Заполните все поля')

    def add_terms(self):    # добавление определений
        cur = self.con.cursor()
        if bool(self.term.text()) and bool(self.definition.text()):
            self.quant += 1
            cur.execute("""UPDATE decks SET quantity = ? WHERE id = ?""", (self.quant, self.id,))
            cur.execute("INSERT INTO content(term, definition, deck_id) VALUES(?, ?, ?)",
                        (self.term.text(), self.definition.text(), self.id,))
            self.added_successfully.setText('Определение успешно добавлено')
        else:
            self.added_successfully.setText('Заполните все поля')


class ThirdForm(QWidget):     # форма для изучения
    def __init__(self, id, con):
        super().__init__()
        uic.loadUi("learning.ui", self)
        self.con = sqlite3.connect("cards.db")

        self.setWindowTitle('Learn')

        self.con = con
        self.id = id[0]

        cur = self.con.cursor()

        self.terms = cur.execute("SELECT term FROM content WHERE deck_id = ?", (self.id, )).fetchall()
        self.definitions = cur.execute("""SELECT definition FROM content WHERE deck_id = ?""", (self.id, )).fetchall()
        self.quantity = cur.execute("SELECT quantity FROM decks WHERE id = ?", (self.id, )).fetchone()[0]
        if self.quantity > 0:    # проверка на достаточное количество определений
            self.flag = True
        else:
            self.flag = False

        self.n = 0
        self.define = False
        self.left_arrow.setVisible(False)
        if self.quantity == 1:
            self.right_arrow.setVisible(False)
        if self.flag:

            self.word.setText(self.terms[self.n][0])

            self.word.clicked.connect(self.show_def)

            self.right_arrow.clicked.connect(self.next)

            self.left_arrow.clicked.connect(self.back)
        else:
            self.right_arrow.setVisible(False)
            self.word.setText('')

    def show_def(self):    # при нажатии на карточку термин меняется на его определение и наоборот
        if not self.define:
            defin = self.definitions[self.n][0]
            if len(defin) > 30:
                length = len(defin)
                i = length // 30 + 1
                x = 0
                lines = []
                for j in range(i):
                    if j != i - 1:
                        lines.append(defin[x:x + 30])
                        x += 30
                    else:
                        lines.append(defin[x:])
                lines = '\n'.join(lines)
                self.word.setText(lines)
                self.define = True
            else:
                self.word.setText(self.definitions[self.n][0])
                self.define = True
        else:
            self.word.setText(self.terms[self.n][0])
            self.define = False

    def next(self):    # функция для того, чтобы получить доступ к следующей карточке
        self.left_arrow.setVisible(True)
        self.define = False
        self.n += 1
        self.word.setText(self.terms[self.n][0])
        last = self.quantity - 1
        if self.n == last:
            self.right_arrow.setVisible(False)

    def back(self):    # функция для того, чтобы получить доступ к предыдущей карточке
        self.right_arrow.setVisible(True)
        self.define = False
        self.n -= 1
        self.word.setText(self.terms[self.n][0])
        first = 0
        if self.n == first:
            self.left_arrow.setVisible(False)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
