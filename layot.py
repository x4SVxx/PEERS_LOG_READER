from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
import parameters


def CreateLayot(self, x, y, width, height):
    layot = QLabel("", self)
    layot.setGeometry(x, y, width, height)
    layot.setFont(QFont(parameters.date_layot_font, parameters.date_layot_font_size))
    return layot