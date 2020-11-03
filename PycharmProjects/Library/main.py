from PyQt5 import uic, QtWidgets
import sqlite3 as sq
import sys
import easygui
from datetime import date

Form, _ = uic.loadUiType("library.ui")

with sq.connect("library.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS books (
    	Id INTEGER PRIMARY KEY,
    	Names TEXT NOT NULL,
    	Authors TEXT NOT NULL,
    	Publishers TEXT NOT NULL,
    	Year_of_publishing INTEGER NOT NULL,
    	Quantity INTEGER
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS control (
        Student	TEXT,
        Book	TEXT,
        Data1	DATE,
        Data2 DATE
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        Id	INTEGER NOT NULL PRIMARY KEY,
        Full_name	TEXT NOT NULL
    )""")


    cur.execute("SELECT Full_name FROM  students")
    result = cur.fetchall()
    students = [str(item) for sub in result for item in sub]

class Ui(QtWidgets.QDialog, Form):

    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.select_student.clicked.connect(self.ButtonSelectStudent)
        self.list_of_students.addItems(students)

    def ButtonSelectStudent(self):
        student = str(self.list_of_students.currentText())
        cur.execute("SELECT Names FROM books WHERE Quantity > 0")
        result = cur.fetchall()
        books = [str(item) for sub in result for item in sub]
        cur.execute(f"SELECT Book FROM control WHERE (Student = '{student}') and (Data2 = '-')")
        result = cur.fetchall()
        books_for_return = [str(item) for sub in result for item in sub]
        self.list_of_books.clear()
        self.list_of_books.addItems(books)
        self.list_of_books_to_give.clear()
        self.list_of_books_to_give.addItems(books_for_return)
        self.take_book.clicked.connect(self.ButtonTakeBook)
        self.give_book.clicked.connect(self.ButtonReturnBook)

    def ButtonTakeBook(self):
        flag = False
        student = str(self.list_of_students.currentText())
        cur.execute(f"SELECT Book FROM control WHERE (Student = '{student}') and (Data2 = '-')")
        result = cur.fetchall()
        book_check = [str(item) for sub in result for item in sub]
        book = str(self.list_of_books.currentText())
        cur.execute("SELECT Names FROM books WHERE Quantity > 0")
        result = cur.fetchall()
        books = [str(item) for sub in result for item in sub]
        self.list_of_books.clear()
        self.list_of_books.addItems(books)
        day = date.today()
        for i in range(len(book_check)):
               if book == book_check[i]:
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
            self.list_of_books_to_give.clear()
            self.list_of_books_to_give.addItems(books_for_return)

    def ButtonReturnBook(self):
        student = str(self.list_of_students.currentText())
        book = str(self.list_of_books_to_give.currentText())
        day = date.today()
        cur.execute(f'UPDATE books SET Quantity = Quantity+1 WHERE Names = "{book}"')
        cur.execute(f'UPDATE control SET Data2 = "{day}" WHERE (Book = "{book}") and (Student = "{student}")')
        con.commit()
        cur.execute(f"SELECT Book FROM control WHERE (Student = '{student}') and (Data2 = '-')")
        result = cur.fetchall()
        books_for_return = [str(item) for sub in result for item in sub]
        self.list_of_books_to_give.clear()
        self.list_of_books_to_give.addItems(books_for_return)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())