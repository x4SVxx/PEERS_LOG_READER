from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
import parameters


def CreateTableForTags(self, x, y, width, height):
    table = QTableWidget(self)
    table.setGeometry(x, y, width, height)
    table.setFont(QFont(parameters.table_font, parameters.table_font_size))
    table.itemSelectionChanged.connect(self.ChangeTagColor)
    table.setColumnCount(11)
    table.setHorizontalHeaderLabels(["   ИМЯ  ",
                                     "   ЦВЕТ   ",
                                     "   X   ",
                                     "   Y   ",
                                     "     РАЗМЕР     ",
                                     "   ОТОБРАЖЕНИЕ ВКЛ/ВЫКЛ   ",
                                     "   ТРАЕКТОРИЯ   ",
                                     "             ИНТЕРВАЛ ВРЕМЕНИ ТРАЕКТОРИИ             ",
                                     "   ДЛИНА ХВОСТА   ",
                                     "   ВСЕГО ЛОГОВ   ",
                                     "    СООТНОШЕНИЕ ЛОГОВ С ФЛАГОМ 1 и 0   "])
    for i in range(11): table.horizontalHeaderItem(i).setFont(QFont(parameters.table_font, parameters.table_header_font_size))
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    return table

def CreateTableForLogs(self, x, y, width, height):
    table = QTableWidget(self)
    table.setGeometry(x, y, width, height)
    table.setFont(QFont(parameters.table_font, parameters.table_font_size))
    table.setColumnCount(1)
    table.setHorizontalHeaderLabels(["             ФАЙЛЫ            "])
    for i in range(1): table.horizontalHeaderItem(i).setFont(QFont(parameters.table_font, parameters.table_header_font_size))
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    return table

def CreateLongTableForLogs(self):
    table = QTableWidget(self)
    table.setGeometry(0, 0, 0, 0)
    table.setFont(QFont(parameters.table_font, parameters.table_font_size))
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["             ФАЙЛЫ            ",
                                     "  КОЛ-ВО ЛОГОВ ",
                                     "    ДАТА    ",
                                     " УДАЛИТЬ "])
    for i in range(4): table.horizontalHeaderItem(i).setFont(QFont(parameters.table_font, parameters.table_header_font_size))
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    return table