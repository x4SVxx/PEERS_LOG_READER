from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
import parameters


def CreateButton(self, x, y, width, height, font_size, text, function):
    button = QtWidgets.QPushButton(self)
    button.setGeometry(x, y, width, height)
    button.setFont(QFont(parameters.button_font, font_size))
    button.setText(text)
    button.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                         "QPushButton { background-color: " + parameters.button_background_color + " }"
                         "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                         "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                         "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
    button.clicked.connect(lambda: function())
    return button

def ButtonSpeedLogic(self, button_press, speed):
    self.current_speed = speed

    self.button_normal_speed.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                 "QPushButton { background-color: " + parameters.button_background_color + " }"
                                 "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                 "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                 "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    self.button_average_speed.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                 "QPushButton { background-color: " + parameters.button_background_color + " }"
                                 "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                 "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                 "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    self.button_max_speed.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                 "QPushButton { background-color: " + parameters.button_background_color + " }"
                                 "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                 "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                 "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    button_press.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                               "QPushButton { background-color: " + parameters.button_press_background_color + " }"
                               "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                               "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                               "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

def ButtonDisplayPress(button_press, button_upress_1, button_upress_2):
    button_press.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                               "QPushButton { background-color: " + parameters.button_press_background_color + " }"
                               "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                               "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                               "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    button_upress_1.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                  "QPushButton { background-color: " + parameters.button_background_color + " }"
                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    button_upress_2.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                  "QPushButton { background-color: " + parameters.button_background_color + " }"
                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")