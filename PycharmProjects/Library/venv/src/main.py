from PyQt5 import uic, QtWidgets
import sqlite3 as sq
import sys
import easygui
from datetime import date

Form, _ = uic.loadUiType("library.ui")

with sq.connect("library.db") as con:
    cur = con.cursor()
    cur.execute("SELECT Full_name FROM  students")
    result = cur.fetchall()
    students = [str(item) for sub in result for item in sub]

class Ui(QtWidgets.QDialog, Form):

    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.ButtonSelectStudent)
        self.comboBox_3.addItems(students)

    def ButtonSelectStudent(self):
        student = str(self.comboBox_3.currentText())
        cur.execute("SELECT Names FROM books WHERE Quantity > 0")
        result = cur.fetchall()
        books = [str(item) for sub in result for item in sub]
        cur.execute(f"SELECT Book FROM control WHERE (Student = '{student}') and (Data2 = '-')")
        result = cur.fetchall()
        books_for_return = [str(item) for sub in result for item in sub]
        self.comboBox.clear()
        self.comboBox.addItems(books)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(books_for_return)
        self.pushButton.clicked.connect(self.ButtonTakeBook)
        self.pushButton_2.clicked.connect(self.ButtonReturnBook)

    def ButtonTakeBook(self):
        flag = False
        student = str(self.comboBox_3.currentText())
        cur.execute(f"SELECT Book FROM control WHERE (Student = '{student}') and (Data2 = '-')")
        result = cur.fetchall()
        booksssss = [str(item) for sub in result for item in sub]
        book = str(self.comboBox.currentText())
        cur.execute("SELECT Names FROM books WHERE Quantity > 0")
        result = cur.fetchall()
        books = [str(item) for sub in result for item in sub]
        self.comboBox.clear()
        self.comboBox.addItems(books)
        day = date.today()
        for i in range(len(booksssss)):
               if book == booksssss[i]:
                   flag = True

        if flag == True:
            easygui.msgbox("Вы не можете взять две одинаковые книги!", title="Предупреждение!!!")
        else:
            cur.execute(f"INSERT INTO control VALUES ('{student}', '{book}', '{day}','{'-'}')")
            cur.execute(f'UPDATE books SET Quantity = Quantity-1 WHERE Names = "{book}"')
            con.commit()
            cur.execute(f"SELECT Book FROM control WHERE (Student = '{student}') and (Data2 = '-')")
            result = cur.fetchall()
            books_for_return = [str(item) for sub in result for item in sub]
            self.comboBox_2.clear()
            self.comboBox_2.addItems(books_for_return)

    def ButtonReturnBook(self):
        student = str(self.comboBox_3.currentText())
        book = str(self.comboBox_2.currentText())
        day = date.today()
        cur.execute(f'UPDATE books SET Quantity = Quantity+1 WHERE Names = "{book}"')
        cur.execute(f'UPDATE control SET Data2 = "{day}" WHERE (Book = "{book}") and (Student = "{student}")')
        con.commit()
        cur.execute(f"SELECT Book FROM control WHERE (Student = '{student}') and (Data2 = '-')")
        result = cur.fetchall()
        books_for_return = [str(item) for sub in result for item in sub]
        self.comboBox_2.clear()
        self.comboBox_2.addItems(books_for_return)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())