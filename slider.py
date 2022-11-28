from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
import parameters


def CreateSlider(self, x, y, width, height, function):
    slider = QSlider(Qt.Horizontal, self)
    slider.setFocusPolicy(Qt.NoFocus)
    slider.setGeometry(x, y, width, height)
    slider.valueChanged[int].connect(function)
    slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}"
                         "QSlider::handle:horizontal:pressed {background-color: black;}")
    slider.setMaximum(1000)
    slider.setTickInterval(1)
    slider.setSingleStep(1)
    return slider