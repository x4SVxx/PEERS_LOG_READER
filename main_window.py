import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
import pyqtgraph as pg
import parameters
from tag import Tag
import time
from PIL import Image
import numpy as np

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.filenames_mas =[]
        self.all_logs_mas = []
        self.log = []
        self.zero_log = []
        self.tags = []
        self.count = 0
        self.current_time = 0
        self.tag_width_sliders = []
        self.enable_disable_checkboxes = []
        self.tag_path_checkboxes = []
        self.time_tag_path_sliders = []
        self.tag_tails_length_sliders = []
        self.more_log_flag = False
        self.input_start_flag = False
        self.slide_menu_bar = False
        self.max_beacon_number = 0
        self.log_for_beacons_mas = []
        self.mas_time_for_beacon = []
        self.current_text_combo_box = ""

        self.flag_x1 = True
        self.flag_x2 = False
        self.flag_x5 = False
        self.flag_x10 = False
        self.flag_x50 = False
        self.flag_x100 = False

        self.MainWindowGeometry()
        self.CreateMenuBar()
        self.CreateGraph()
        self.ComboBoxForTargets()
        self.CreateButtons()
        self.CreateSlider()
        self.CreateDateLayot()
        self.CreateTable()

    def MainWindowGeometry(self):
        self.SCREEN_WIDTH = QApplication.desktop().width()
        self.SCREEN_HEIGHT = QApplication.desktop().height()
        self.window_width = int(self.SCREEN_WIDTH / 10 * 9)
        self.window_height = int(self.SCREEN_HEIGHT / 10 * 9)
        self.window_x = int(self.SCREEN_WIDTH / 2 - self.window_width / 2)
        self.window_y = int(self.SCREEN_HEIGHT / 2 - self.window_height / 2)
        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #F3F3F3")
        # self.setWindowFlags(Qt.FramelessWindowHint)

    def CreateMenuBar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setGeometry(0, 0, self.window_width, parameters.menu_bar_height)
        self.menu_bar.setStyleSheet("QMenuBar { background-color: White }" "QMenuBar::item:selected { background-color: LightGrey }")

        self.log_menu = QtWidgets.QMenu("Log", self)
        self.log_menu.setStyleSheet("QMenu { background-color: White }" "QMenu { color: Black }" "QMenu::item:selected { background-color: LightGrey }")
        self.menu_bar.addMenu(self.log_menu)

        self.load_log_action = QAction("Load log", self)
        self.log_menu.addAction(self.load_log_action)
        self.load_log_action.triggered.connect(lambda : self.LogLoad())

        self.map_menu = QtWidgets.QMenu("Map", self)
        self.map_menu.setStyleSheet("QMenu { background-color: White }" "QMenu { color: Black }" "QMenu::item:selected { background-color: LightGrey }")
        self.menu_bar.addMenu(self.map_menu)

        self.load_map_action = QAction("Load map", self)
        self.map_menu.addAction(self.load_map_action)
        self.load_map_action.triggered.connect(lambda : self.MapLoad())

        self.delete_map_action = QAction("Delete map", self)
        self.map_menu.addAction(self.delete_map_action)
        self.delete_map_action.triggered.connect(lambda : self.MapDelete())

    def ComboBoxForTargets(self):
        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.setGeometry(0, 0, 0, 0)
        self.combo_box.activated[str].connect(self.ComboBoxActivated)

    def ComboBoxActivated(self):
        self.current_text_combo_box = str(self.combo_box.currentText())

        for tag in self.tags:
            for i in range(self.max_beacon_number + 1):
                for item in self.beacons_graph_widget.listDataItems():
                    if item.name() == "beacon" + str(i) + str(tag.name): item.hide()

        for tag in self.tags:
            if tag.name == self.current_text_combo_box:
                for i in range(self.max_beacon_number + 1):
                    for item in self.beacons_graph_widget.listDataItems():
                        if item.name() == "beacon" + str(i) + str(tag.name): item.show()

    def CreateGraph(self):
        self.graph_width = int(self.window_width / 100 * 57)
        self.graph_height = int(self.window_height - parameters.offset_top - parameters.offset_bot - parameters.button_display_height - parameters.offset_after_graph - parameters.date_layot_height - parameters.offset_before_and_after_date_layot * 2 - parameters.button_beacons_height)
        self.graph_widget = pg.PlotWidget(self)
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setBackground("White")
        self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.graph_width, self.graph_height))
        self.graph_widget.getAxis("bottom").setTickFont(QFont(parameters.axes_font, parameters.axes_font_size))
        self.graph_widget.getAxis("left").setTickFont(QFont(parameters.axes_font, parameters.axes_font_size))
        self.graph_widget.getAxis('bottom').setTextPen(pg.mkPen(color="Black", width=3))
        self.graph_widget.getAxis('left').setTextPen(pg.mkPen(color="Black", width=3))

        self.beacons_graph_width = int(self.window_width - parameters.offset_left - parameters.offset_right)
        self.beacons_graph_height = int(self.window_height - parameters.offset_bot - parameters.offset_top - parameters.button_beacons_height)
        self.beacons_graph_widget = pg.PlotWidget(self)
        self.beacons_graph_widget.showGrid(x=True, y=True)
        self.beacons_graph_widget.setBackground("White")
        self.beacons_graph_widget.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.beacons_graph_widget.getAxis("bottom").setTickFont(QFont(parameters.axes_font, parameters.axes_font_size))
        self.beacons_graph_widget.getAxis("left").setTickFont(QFont(parameters.axes_font, parameters.axes_font_size))
        self.beacons_graph_widget.getAxis('bottom').setTextPen(pg.mkPen(color="Black", width=3))
        self.beacons_graph_widget.getAxis('left').setTextPen(pg.mkPen(color="Black", width=3))

    def CreateButtons(self):
        self.button_play = QtWidgets.QPushButton(self)
        self.button_play.setGeometry(parameters.offset_left,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_play.setFont(QFont(parameters.button_font, 14))
        self.button_play.setText("►")
        self.button_play.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }"
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_play.clicked.connect(lambda: self.ButtonPlayLogic())
        """--------------------------------------------------------------------------------------------------------------------------------------------------"""
        self.button_pause = QtWidgets.QPushButton(self)
        self.button_pause.setGeometry(parameters.offset_left + parameters.button_display_width + parameters.offset_between_buttons_display,
                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
                                      parameters.button_display_width,
                                      parameters.button_display_height)
        self.button_pause.setFont(QFont(parameters.button_font, 15))
        self.button_pause.setText("l l")
        self.button_pause.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_pause.clicked.connect(lambda: self.ButtonPauseLogic())
        """--------------------------------------------------------------------------------------------------------------------------------------------------"""
        self.button_stop = QtWidgets.QPushButton(self)
        self.button_stop.setGeometry(parameters.offset_left + parameters.button_display_width * 2 + parameters.offset_between_buttons_display * 2,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_stop.setFont(QFont(parameters.button_font, 9))
        self.button_stop.setText("⬛")
        self.button_stop.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_stop.clicked.connect(lambda: self.ButtonStopLogic())

        """--------------------------------------------------------------------------------------------------------------------------------------------------"""
        self.button_100x = QtWidgets.QPushButton(self)
        self.button_100x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_100x.setFont(QFont(parameters.button_font, 7))
        self.button_100x.setText("100x")
        self.button_100x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_100x.clicked.connect(lambda: self.Button100xLogic())

        self.button_50x = QtWidgets.QPushButton(self)
        self.button_50x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 2 - parameters.offset_between_buttons_display,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_50x.setFont(QFont(parameters.button_font, 8))
        self.button_50x.setText("50x")
        self.button_50x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_50x.clicked.connect(lambda: self.Button50xLogic())

        self.button_10x = QtWidgets.QPushButton(self)
        self.button_10x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 3 - parameters.offset_between_buttons_display * 2,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_10x.setFont(QFont(parameters.button_font, 8))
        self.button_10x.setText("10x")
        self.button_10x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_10x.clicked.connect(lambda: self.Button10xLogic())

        self.button_5x = QtWidgets.QPushButton(self)
        self.button_5x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 4 - parameters.offset_between_buttons_display * 3,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_5x.setFont(QFont(parameters.button_font, 8))
        self.button_5x.setText("5x")
        self.button_5x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_5x.clicked.connect(lambda: self.Button5xLogic())

        self.button_2x = QtWidgets.QPushButton(self)
        self.button_2x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 5 - parameters.offset_between_buttons_display * 4,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_2x.setFont(QFont(parameters.button_font, 8))
        self.button_2x.setText("2x")
        self.button_2x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_2x.clicked.connect(lambda: self.Button2xLogic())

        self.button_1x = QtWidgets.QPushButton(self)
        self.button_1x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 6 - parameters.offset_between_buttons_display * 5,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_1x.setFont(QFont(parameters.button_font, 8))
        self.button_1x.setText("1x")
        self.button_1x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_1x.clicked.connect(lambda: self.Button1xLogic())

        """--------------------------------------------------------------------------------------------------------------------------------------------------"""
        self.button_slide_tools = QtWidgets.QPushButton(self)
        self.button_slide_tools.setGeometry(parameters.offset_left + self.graph_width + 11,
                                            parameters.offset_top + parameters.button_beacons_height,
                                            15,
                                            self.graph_height)
        self.button_slide_tools.setFont(QFont(parameters.button_font, 9))
        self.button_slide_tools.setText(">")
        self.button_slide_tools.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: #C0C0C0 }"
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
                                                  "QPushButton { border-radius: " + "1" + "px }")
        self.button_slide_tools.clicked.connect(lambda: self.ButtonSlideMenuLogic())

        """--------------------------------------------------------------------------------------------------------------------------------------------------"""
        self.button_targets = QtWidgets.QPushButton(self)
        self.button_targets.setGeometry(parameters.offset_left,
                                        parameters.offset_top, parameters.button_targets_width, parameters.button_tartgets_height)
        self.button_targets.setFont(QFont(parameters.button_font, 9))
        self.button_targets.setText("TARGETS")
        self.button_targets.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: silver }"
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
                                                  "QPushButton { border-radius: " + "1" + "px }")
        self.button_targets.clicked.connect(lambda: self.ButtonTargetsLogic())
        """--------------------------------------------------------------------------------------------------------------------------------------------------"""
        self.button_beacons = QtWidgets.QPushButton(self)
        self.button_beacons.setGeometry(parameters.offset_left + parameters.button_targets_width,
                                            parameters.offset_top,
                                            parameters.button_beacons_width,
                                            parameters.button_beacons_height)
        self.button_beacons.setFont(QFont(parameters.button_font, 9))
        self.button_beacons.setText("BEACONS")
        self.button_beacons.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: light grey }"
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
                                                  "QPushButton { border-radius: " + "1" + "px }")
        self.button_beacons.clicked.connect(lambda: self.ButtonBeaconsLogic())

    def ButtonTargetsLogic(self):
        self.button_targets.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                          "QPushButton { background-color: silver }"
                                          "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                          "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
                                          "QPushButton { border-radius: " + "1" + "px }")
        self.button_beacons.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                          "QPushButton { background-color: light grey }"
                                          "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                          "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
                                          "QPushButton { border-radius: " + "1" + "px }")

        if self.slide_menu_bar:
            self.table.setGeometry(0, 0, 0, 0)
            self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.window_width - parameters.offset_left - parameters.offset_right - 15 - 5, self.graph_height))
            self.button_slide_tools.setGeometry(self.window_width - parameters.offset_right - 15,
                                                parameters.offset_top + parameters.button_beacons_height,
                                                15,
                                                self.graph_height)
            self.button_slide_tools.setText("<")
        else:
            self.table.setGeometry(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table,
                                   parameters.offset_top + parameters.button_beacons_height,
                                   self.window_width - (parameters.offset_left + parameters.offset_right + parameters.offset_between_graph_and_table + self.graph_width),
                                   self.graph_height)
            self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.graph_width, self.graph_height))
            self.button_slide_tools.setGeometry(parameters.offset_left + self.graph_width + 11,
                                                parameters.offset_top + parameters.button_beacons_height,
                                                15,
                                                self.graph_height)
            self.button_slide_tools.setText(">")

        self.button_1x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 6 - parameters.offset_between_buttons_display * 5,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_2x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 5 - parameters.offset_between_buttons_display * 4,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_5x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 4 - parameters.offset_between_buttons_display * 3,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_10x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 3 - parameters.offset_between_buttons_display * 2,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_50x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 2 - parameters.offset_between_buttons_display,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_100x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_play.setGeometry(parameters.offset_left,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.button_pause.setGeometry(parameters.offset_left + parameters.button_display_width + parameters.offset_between_buttons_display,
                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
                                      parameters.button_display_width,
                                      parameters.button_display_height)
        self.button_stop.setGeometry(parameters.offset_left + parameters.button_display_width * 2 + parameters.offset_between_buttons_display * 2,
                                     self.window_height - parameters.offset_bot - parameters.button_display_height,
                                     parameters.button_display_width,
                                     parameters.button_display_height)
        self.slider.setGeometry(int(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3),
                                int(self.window_height - parameters.offset_bot - parameters.button_display_height + (parameters.button_display_height - parameters.slider_height) / 2),
                                int(self.window_width - (parameters.offset_left + parameters.offset_right + parameters.button_display_width * 9 + parameters.offset_between_buttons_display * 9)),
                                int(parameters.slider_height))

        self.start_date_layot.setGeometry(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3,
                                            self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
                                            parameters.date_layot_width,
                                            parameters.date_layot_height)

        self.current_date_layot.setGeometry(int((self.window_width - parameters.offset_right - parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3) / 2 - parameters.date_layot_width / 2),
                                            self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
                                            parameters.date_layot_width,
                                            parameters.date_layot_height)

        self.finish_date_layot.setGeometry(self.window_width - parameters.offset_right - parameters.date_layot_width,
                                            self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
                                            parameters.date_layot_width,
                                            parameters.date_layot_height)

        self.beacons_graph_widget.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.combo_box.setGeometry(0, 0, 0, 0)

    def ButtonBeaconsLogic(self):
        self.button_targets.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                          "QPushButton { background-color: light grey }"
                                          "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                          "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
                                          "QPushButton { border-radius: " + "1" + "px }")
        self.button_beacons.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                          "QPushButton { background-color: silver }"
                                          "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                          "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
                                          "QPushButton { border-radius: " + "1" + "px }")

        self.table.setGeometry(0, 0, 0, 0)
        self.graph_widget.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.button_slide_tools.setGeometry(0, 0, 0, 0)
        self.button_1x.setGeometry(0, 0, 0, 0)
        self.button_2x.setGeometry(0, 0, 0, 0)
        self.button_5x.setGeometry(0, 0, 0, 0)
        self.button_10x.setGeometry(0, 0, 0, 0)
        self.button_50x.setGeometry(0, 0, 0, 0)
        self.button_100x.setGeometry(0, 0, 0, 0)
        self.button_play.setGeometry(0, 0, 0, 0)
        self.button_pause.setGeometry(0, 0, 0, 0)
        self.button_stop.setGeometry(0, 0, 0, 0)
        self.slider.setGeometry(0, 0, 0, 0)
        self.start_date_layot.setGeometry(0, 0, 0, 0)
        self.current_date_layot.setGeometry(0, 0, 0, 0)
        self.finish_date_layot.setGeometry(0, 0, 0, 0)

        self.beacons_graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.beacons_graph_width, self.beacons_graph_height))
        self.combo_box.setGeometry(parameters.offset_left + parameters.button_beacons_width + parameters.button_targets_width + 10, parameters.offset_top, parameters.target_select_menu_width, parameters.target_select_menu_height)

    def Button1xLogic(self):
        self.flag_x1 = True
        self.flag_x2 = False
        self.flag_x5 = False
        self.flag_x10 = False
        self.flag_x50 = False
        self.flag_x100 = False
        self.button_1x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_press_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_2x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_5x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_10x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_50x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_100x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    def Button2xLogic(self):
        self.flag_x1 = False
        self.flag_x2 = True
        self.flag_x5 = False
        self.flag_x10 = False
        self.flag_x50 = False
        self.flag_x100 = False
        self.button_1x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_2x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_press_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_5x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_10x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_50x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_100x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
    def Button5xLogic(self):
        self.flag_x1 = False
        self.flag_x2 = False
        self.flag_x5 = True
        self.flag_x10 = False
        self.flag_x50 = False
        self.flag_x100 = False
        self.button_1x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_2x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_5x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_press_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_10x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_50x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_100x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    def Button10xLogic(self):
        self.flag_x1 = False
        self.flag_x2 = False
        self.flag_x5 = False
        self.flag_x10 = True
        self.flag_x50 = False
        self.flag_x100 = False
        self.button_1x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_2x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_5x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_10x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_press_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_50x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_100x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    def Button50xLogic(self):
        self.flag_x1 = False
        self.flag_x2 = False
        self.flag_x5 = False
        self.flag_x10 = False
        self.flag_x50 = True
        self.flag_x100 = False
        self.button_1x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_2x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_5x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_10x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_50x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_press_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_100x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    def Button100xLogic(self):
        self.flag_x1 = False
        self.flag_x2 = False
        self.flag_x5 = False
        self.flag_x10 = False
        self.flag_x50 = False
        self.flag_x100 = True
        self.button_1x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_2x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_5x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_10x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_50x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
        self.button_100x.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                                  "QPushButton { background-color: " + parameters.button_press_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                                  "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                                  "QPushButton { border-radius: " + parameters.button_border_radius + "px }")

    def ButtonSlideMenuLogic(self):
        if not self.slide_menu_bar:
            self.table.setGeometry(0, 0, 0, 0)
            self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.window_width - parameters.offset_left - parameters.offset_right - 15 - 5, self.graph_height))
            self.button_slide_tools.setGeometry(self.window_width - parameters.offset_right - 15,
                                                parameters.offset_top + parameters.button_beacons_height,
                                                15,
                                                self.graph_height)
            self.button_slide_tools.setText("<")
            self.slide_menu_bar = True
        else:
            self.table.setGeometry(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table,
                                   parameters.offset_top + parameters.button_beacons_height,
                                   self.window_width - (parameters.offset_left + parameters.offset_right + parameters.offset_between_graph_and_table + self.graph_width),
                                   self.graph_height)
            self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.graph_width, self.graph_height))
            self.button_slide_tools.setGeometry(parameters.offset_left + self.graph_width + 11,
                                                parameters.offset_top + parameters.button_beacons_height,
                                                15,
                                                self.graph_height)
            self.button_slide_tools.setText(">")
            self.slide_menu_bar = False

    def CreateSlider(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setGeometry(int(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3),
                                int(self.window_height - parameters.offset_bot - parameters.button_display_height + (parameters.button_display_height - parameters.slider_height) / 2),
                                int(self.window_width - (parameters.offset_left + parameters.offset_right + parameters.button_display_width * 9 + parameters.offset_between_buttons_display * 9)),
                                int(parameters.slider_height))
        self.slider.valueChanged[int].connect(self.SliderLogic)
        self.slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}"
                                  "QSlider::handle:horizontal:pressed {background-color: black;}")
        self.slider.setMaximum(1000)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)

    def CreateDateLayot(self):
        self.start_date_layot = QLabel("", self)
        self.start_date_layot.setGeometry(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3,
                                            self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
                                            parameters.date_layot_width,
                                            parameters.date_layot_height)
        self.start_date_layot.setFont(QFont(parameters.date_layot_font, parameters.date_layot_font_size))

        self.current_date_layot = QLabel("", self)
        self.current_date_layot.setGeometry(int((self.window_width - parameters.offset_right - parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3) / 2 - parameters.date_layot_width / 2),
                                            self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
                                            parameters.date_layot_width,
                                            parameters.date_layot_height)
        self.current_date_layot.setFont(QFont(parameters.date_layot_font, parameters.date_layot_font_size))

        self.finish_date_layot = QLabel("", self)
        self.finish_date_layot.setGeometry(self.window_width - parameters.offset_right - parameters.date_layot_width,
                                            self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
                                            parameters.date_layot_width,
                                            parameters.date_layot_height)
        self.finish_date_layot.setFont(QFont(parameters.date_layot_font, parameters.date_layot_font_size))

    def CreateTable(self):
        self.table = QTableWidget(self)
        self.table.setGeometry(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table,
                               parameters.offset_top + parameters.button_beacons_height,
                               self.window_width - (parameters.offset_left + parameters.offset_right + parameters.offset_between_graph_and_table + self.graph_width),
                               self.graph_height)
        self.table.setFont(QFont(parameters.table_font, parameters.table_font_size))
        self.table.itemSelectionChanged.connect(self.ChangeTagColor)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.verticalHeader().destroy()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(["NAME", "COLOR", "X", "Y", "WIDTH", "E/D", "PATH", "              PATH TIME              ", "TAIL", "LOGS", "%1/0"])
        for i in range (11): self.table.horizontalHeaderItem(i).setFont(QFont(parameters.table_font, parameters.table_header_font_size))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def SliderLogic(self, value):
        if int(len(self.log) / 1000 * value) >= len(self.log): self.count = len(self.log) - 1
        else: self.count = int(len(self.log) / 1000 * value)
        self.current_time = float(self.log[self.count][0])
        self.Draw()

    def Filter(self):
        alpha = 0.9
        for tag in self.tags:
            if len(tag.mas_x) != 0:
                for i in range(1, len(tag.mas_x)):
                    tag.mas_x_f[i] = float(tag.mas_x_f[i - 1] * alpha + tag.mas_x[i] * (1 - alpha))
                    tag.mas_y_f[i] = float(tag.mas_y_f[i - 1] * alpha + tag.mas_y[i] * (1 - alpha))

    def LogLoad(self):
        filenames, filetype = QFileDialog.getOpenFileNames(self, "SELECT A LOG", ".", "Text files (*.txt *.log)")
        for filename in filenames:
            if filename:

                filename_cross_flag = False
                for filen in self.filenames_mas:
                    if filen == filename: filename_cross_flag = True

                if not filename_cross_flag:
                    self.filenames_mas.append(filename)

                    file = open(filename, 'r')
                    while True:
                        try:
                            line = file.readline().split()
                            if not line: break
                            if line[1] == "CLE:" and line[2] == "TAG" and line[4] == "0": self.zero_log.append(line)
                        except: pass
                    file.close()

                    file = open(filename, 'r')
                    new_log = []
                    while True:
                        try:
                            line = file.readline().split()
                            if not line: break
                            if line[1] == "CLE:" and line[2] == "TAG" and line[4] == "1": new_log.append(line)
                        except: pass
                    file.close()

                    if len(new_log) !=0:
                        if len(self.all_logs_mas) == 0:
                            self.all_logs_mas.append(new_log)
                        else:
                            write_log_flag = False
                            for i in range(len(self.all_logs_mas)):
                                if float(new_log[0][0]) < float(self.all_logs_mas[i][0][0]):
                                    self.all_logs_mas.insert(i, new_log)
                                    write_log_flag = True
                            if not write_log_flag:
                                self.all_logs_mas.append(new_log)

                    self.log = []
                    for log in self.all_logs_mas:
                        for i in range(len(log)):
                            self.log.append(log[i])

                    self.tag_width_sliders = []
                    self.enable_disable_checkboxes = []
                    self.tag_path_checkboxes = []
                    self.time_tag_path_sliders = []
                    self.tag_tails_length_sliders = []
                    self.tags = []
                    self.count = 0
                    self.slider.setValue(0)

                    for log in self.log:
                        flag_cross_tag_name = False
                        for tag in self.tags:
                            if log[3] == tag.name: flag_cross_tag_name = True
                        if not flag_cross_tag_name:
                            new_tag = Tag(log[3], parameters.tag_color, parameters.tag_width, log[5], log[6], log[7])
                            self.tags.append(new_tag)

                            add_item_flag = False
                            for item in self.graph_widget.listDataItems():
                                if item.name() == new_tag.name:
                                    add_item_flag = True
                                    item.setData([new_tag.x], [new_tag.y], pen=pg.mkPen(width=new_tag.width, color=new_tag.color), symbol='o', name=new_tag.name)
                            if not add_item_flag:
                                self.graph_widget.addItem(pg.ScatterPlotItem([new_tag.x], [new_tag.y], pen=pg.mkPen(width=new_tag.width, color=new_tag.color), symbol='o', name=new_tag.name))

                    for log in self.zero_log:
                        flag_cross_tag_name = False
                        for tag in self.tags:
                            if log[3] == tag.name: flag_cross_tag_name = True
                        if not flag_cross_tag_name:
                            new_tag = Tag(log[3], parameters.tag_color, parameters.tag_width, log[5], log[6], log[7])
                            self.tags.append(new_tag)

                    for log in self.log:
                        for tag in self.tags:
                            if log[3] == tag.name:
                                tag.mas_x.append(float(log[5]))
                                tag.mas_y.append(float(log[6]))
                                tag.mas_z.append(float(log[7]))
                                tag.mas_time.append(float(log[0]))

                    for tag in self.tags:
                        self.combo_box.addItem(str(tag.name))
                        if len(tag.mas_x) != 0:
                            for i in range(len(tag.mas_x)):
                                tag.mas_x_f.append(0)
                                tag.mas_y_f.append(0)
                                tag.mas_x_f[0] = tag.mas_x[0]
                                tag.mas_y_f[0] = tag.mas_y[0]

                    for log in self.zero_log:
                        for tag in self.tags:
                            if log[3] == tag.name:
                                tag.mas_false_time.append(float(log[0]))

                    self.Filter()

                    for tag in self.tags:
                        if len(tag.mas_time) != 0:

                            add_item_flag = False
                            for item in self.graph_widget.listDataItems():
                                if item.name() == tag.name + "path":
                                    item.setData(tag.mas_x_f, tag.mas_y_f, pen=pg.mkPen(width=1, color=tag.color), name=(tag.name + "path"))
                                    add_item_flag = True
                            if not add_item_flag:
                                path = self.graph_widget.plot(tag.mas_x_f, tag.mas_y_f, pen=pg.mkPen(width=1, color=tag.color), name=(tag.name + "path"))
                                path.setZValue(-1)
                                path.hide()

                            for i in range(10):
                                add_item_flag = False
                                for item in self.graph_widget.listDataItems():
                                    if item.name() == tag.name + "tail" + str(i):
                                        item.setData([tag.x], [tag.y], pen=pg.mkPen(width=1, color=tag.color), name=(tag.name + "tail" + str(i)))
                                        add_item_flag = True
                                if not add_item_flag:
                                    tail = pg.ScatterPlotItem([tag.x], [tag.y], pen=pg.mkPen(width=1, color=tag.color), name=(tag.name + "tail" + str(i)))
                                    tail.hide()
                                    self.graph_widget.addItem(tail)
                            for i in range(tag.tail_length):
                                for item in self.graph_widget.listDataItems():
                                    if item.name() == tag.name + "tail" + str(i): item.show()

                    if len(self.log) != 0:
                        self.current_time = float(self.log[0][0])

                    for log in self.log:
                        self.mas_time_for_beacon.append(float(log[0]))

                    """-------------------------------------------------------------------------------------"""
                    for log in self.log:
                        for i in range(int(log[8])):
                            if i % 2 != 0:
                                if int(log[8 + i]) > self.max_beacon_number:
                                    self.max_beacon_number = int(log[8 + i])

                    for tag in self.tags:
                        for i in range(self.max_beacon_number + 1):
                            tag.log_for_beacons_mas.append([])

                    count_log_for_beacon = 0
                    for log in self.log:
                        for tag in self.tags:
                            if str(log[3]) == str(tag.name):
                                for i in range(len(tag.log_for_beacons_mas)): tag.log_for_beacons_mas[i].append(float(0))
                                for i in range(int(log[8])):
                                    if i % 2 != 0:
                                        for j in range(len(tag.log_for_beacons_mas)):
                                            if j == int(log[8 + i]): tag.log_for_beacons_mas[j][count_log_for_beacon] = j
                            else:
                                for i in range(len(tag.log_for_beacons_mas)): tag.log_for_beacons_mas[i].append(float(0))
                        count_log_for_beacon += 1

                    for tag in self.tags:
                        for i in range(self.max_beacon_number + 1):
                            self.beacons_graph_widget.plot(self.mas_time_for_beacon, tag.log_for_beacons_mas[i], pen=pg.mkPen(width=0.5, color="White"), symbol="o",name=("beacon" + str(i) + str(tag.name)))
                            for item in self.beacons_graph_widget.listDataItems():
                                    if item.name() == "beacon" + str(i) + str(tag.name): item.hide()

                    for tag in self.tags:
                        if tag.name == self.combo_box.currentText():
                            for i in range(self.max_beacon_number + 1):
                                for item in self.beacons_graph_widget.listDataItems():
                                    if item.name() == "beacon" + str(i) + str(tag.name): item.show()

                    """-------------------------------------------------------------------------------------"""

                    self.max_x = 0
                    self.max_y = 0
                    self.min_x = 0
                    self.min_y = 0
                    for log in self.log:
                        if float(log[5]) > self.max_x: self.max_x = float(log[5])
                        if float(log[6]) > self.max_y: self.max_y = float(log[6])
                        if float(log[5]) < self.min_x: self.min_x = float(log[5])
                        if float(log[5]) < self.min_y: self.min_y = float(log[5])
                    self.graph_widget.setXRange(self.min_x, self.max_x)
                    self.graph_widget.setYRange(self.min_y, self.max_y)

                    self.table.setRowCount(len(self.tags))
                    for i in range(len(self.tags)):
                        self.table.setItem(i, 0, QTableWidgetItem(self.tags[i].name))
                        self.table.setItem(i, 1, QTableWidgetItem(self.tags[i].color))
                        self.table.item(i, 1).setBackground(QColor(self.tags[i].color))
                        self.table.setItem(i, 2, QTableWidgetItem(self.tags[i].x))
                        self.table.setItem(i, 3, QTableWidgetItem(self.tags[i].y))

                        tag_width_slider = QSlider(Qt.Horizontal, self)
                        tag_width_slider.valueChanged[int].connect(self.TagWidthSliderLogic)
                        tag_width_slider.setValue(int(self.tags[i].width * 10))
                        tag_width_slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}" "QSlider::handle:horizontal:pressed {background-color: black;}")
                        self.tag_width_sliders.append(tag_width_slider)
                        self.table.setCellWidget(i, 4, tag_width_slider)

                        enable_disable_checkbox = QCheckBox("", self)
                        enable_disable_checkbox.setChecked(True)
                        enable_disable_checkbox.stateChanged.connect(self.EnableDisableCheckboxLogic)
                        self.enable_disable_checkboxes.append(enable_disable_checkbox)
                        self.table.setCellWidget(i, 5, enable_disable_checkbox)

                        tag_check_checkbox = QCheckBox("", self)
                        tag_check_checkbox.stateChanged.connect(self.PathCheckboxLogic)
                        self.tag_path_checkboxes.append(tag_check_checkbox)
                        self.table.setCellWidget(i, 6, tag_check_checkbox)

                        time_tag_path_slider = QSlider(Qt.Horizontal, self)
                        time_tag_path_slider.valueChanged[int].connect(self.TimePathSliderLogic)
                        time_tag_path_slider.setValue(100)
                        time_tag_path_slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}" "QSlider::handle:horizontal:pressed {background-color: black;}")
                        self.time_tag_path_sliders.append(time_tag_path_slider)
                        self.table.setCellWidget(i, 7, time_tag_path_slider)

                        tag_tail_length_slider = QSlider(Qt.Horizontal, self)
                        tag_tail_length_slider.valueChanged[int].connect(self.TailLengthSliderLogic)
                        tag_tail_length_slider.setValue(50)
                        tag_tail_length_slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}" "QSlider::handle:horizontal:pressed {background-color: black;}")
                        self.tag_tails_length_sliders.append(tag_tail_length_slider)
                        self.table.setCellWidget(i, 8, tag_tail_length_slider)

                        self.table.setItem(i, 9, QTableWidgetItem(str(len(self.tags[i].mas_time) + len(self.tags[i].mas_false_time))))
                        self.table.setItem(i, 10, QTableWidgetItem(str((round(len(self.tags[i].mas_time) / (len(self.tags[i].mas_time) + len(self.tags[i].mas_false_time)), 2) * 100)) + " %"))

                        self.table.resizeColumnsToContents()
                        self.table.resizeRowsToContents()

                    if len(self.log) != 0:
                        self.start_date_layot.setText(str(time.ctime(float(self.log[0][0]))))
                        self.current_date_layot.setText(str(time.ctime(float(self.log[0][0]))))
                        self.finish_date_layot.setText(str(time.ctime(float(self.log[len(self.log) - 1][0]))))

    def TailLengthSliderLogic(self, value):
        for i in range(len(self.tag_tails_length_sliders)):
            if self.tag_tails_length_sliders[i].value() == value:
                self.tags[i].tail_length = int(value / 10)

                current_step = 0
                for j in range(len(self.tags[i].mas_time)):
                    if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]):
                        current_step = j

                if current_step > self.tags[i].tail_length:
                    for j in range(10):
                        for item in self.graph_widget.listDataItems():
                            if item.name() == self.tags[i].name + "tail" + str(j): item.hide()

                    for j in range(self.tags[i].tail_length):
                        for item in self.graph_widget.listDataItems():
                            if item.name() == self.tags[i].name + "tail" + str(j):
                                if self.enable_disable_checkboxes[i].isChecked(): item.show()
                                if self.tags[i].width - (j + 1) <= 1: tail_width = 1
                                else: tail_width = int(self.tags[i].width - (j + 1))
                                item.setData([self.tags[i].mas_x_f[current_step - (j + 1)]], [self.tags[i].mas_y_f[current_step - (j + 1)]],
                                             pen=pg.mkPen(width=tail_width, color=self.tags[i].color), symbol='o', name=self.tags[i].name + "tail" + str(j))

    def TimePathSliderLogic(self, value):
        for i in range(len(self.time_tag_path_sliders)):
            if self.time_tag_path_sliders[i].value() == value:
                current_step = 0
                for j in range(len(self.tags[i].mas_time)):
                    if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]):
                        current_step = j

                left_path = int(current_step - (current_step / 100 * value))
                right_path = int(current_step + ((len(self.tags[i].mas_x_f) - current_step) / 100 * value))

                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name + "path":
                        item.setData(self.tags[i].mas_x_f[left_path:right_path], self.tags[i].mas_y_f[left_path:right_path], pen=pg.mkPen(width=1, color=self.tags[i].color), name=(self.tags[i].name + "path"))


    def PathCheckboxLogic(self):
        for i in range(len(self.tags)):
            if self.tag_path_checkboxes[i].isChecked():
                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name + "path":
                        item.show()
            else:
                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name + "path": item.hide()

    def EnableDisableCheckboxLogic(self):
        for i in range(len(self.tags)):
            if self.enable_disable_checkboxes[i].isChecked():
                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name: item.show()

                    for j in range(self.tags[i].tail_length):
                        for item_tail in self.graph_widget.listDataItems():
                            if item_tail.name() == self.tags[i].name + "tail" + str(j): item_tail.show()

            else:
                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name: item.hide()

                    for j in range(10):
                        for item_tail in self.graph_widget.listDataItems():
                            if item_tail.name() == self.tags[i].name + "tail" + str(j): item_tail.hide()

    def TagWidthSliderLogic(self, value):
        for i in range(len(self.tag_width_sliders)):
            if self.tag_width_sliders[i].value() == value:
                self.tags[i].width = value / 10
                for tag in self.tags:
                    current_step = 0
                    for j in range(len(self.tags[i].mas_time)):
                        if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]):
                            current_step = j

                    for item in self.graph_widget.listDataItems():
                        if item.name() == tag.name: item.setData([tag.mas_x_f[current_step]], [tag.mas_y_f[current_step]], pen=pg.mkPen(width=tag.width, color=tag.color), symbol='o', name=tag.name)


                    if current_step > self.tags[i].tail_length:
                        for j in range(self.tags[i].tail_length):
                            for item in self.graph_widget.listDataItems():
                                if item.name() == self.tags[i].name + "tail" + str(j):
                                    if self.tags[i].width - (j + 1) <= 1: tail_width = 1
                                    else: tail_width = int(self.tags[i].width - (j + 1))
                                    item.setData([self.tags[i].mas_x_f[current_step - (j + 1)]], [self.tags[i].mas_y_f[current_step - (j + 1)]],
                                                 pen=pg.mkPen(width=tail_width, color=self.tags[i].color), symbol='o',
                                                 name=self.tags[i].name + "tail" + str(j))

    def MapLoad(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "SELECT A MAP", ".", "Images files (*.png *.jpg *.jpeg)")
        if filename:
            self.img = pg.ImageItem(np.flipud(np.array(Image.open(filename))).transpose([1, 0, 2]), name="map")
            self.img.setRect(QRect(int(filename.split()[1]), int(filename.split()[2]), int(filename.split()[3]), int(filename.split()[4].split(".")[0])))
            self.img.setZValue(-100)
            self.graph_widget.addItem(self.img)

    def MapDelete(self):
        self.graph_widget.removeItem(self.img)

    def ButtonPlayLogic(self):
        if len(self.log) != 0:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.Draw())
            self.timer.start(1)

    def Draw(self):
        if self.current_time >= float(self.log[self.count][0]):
            for tag in self.tags:
                if self.log[self.count][3] == tag.name:
                    tag.x = self.log[self.count][5]
                    tag.y = self.log[self.count][6]
                    tag.z = self.log[self.count][7]
                    tag.current_time = self.log[self.count][0]

                    current_step = 0
                    for i in range(len(tag.mas_time)):
                        if float(self.log[self.count][0]) == float(tag.mas_time[i]):
                            current_step = i

                    for i in range(len(self.tags)):
                        if self.tags[i].name == tag.name:
                            self.table.setItem(i, 2, QTableWidgetItem(str(round(self.tags[i].mas_x_f[current_step], 2))))
                            self.table.setItem(i, 3, QTableWidgetItem(str(round(self.tags[i].mas_y_f[current_step], 2))))
                            self.table.resizeColumnsToContents()
                    for item in self.graph_widget.listDataItems():
                        if item.name() == tag.name: item.setData([str(tag.mas_x_f[current_step])], [str(tag.mas_y_f[current_step])], pen=pg.mkPen(width=tag.width, color=tag.color), symbol='o', name=tag.name)

                    if current_step > tag.tail_length:
                        for i in range(tag.tail_length):
                            for item in self.graph_widget.listDataItems():
                                if item.name() == tag.name + "tail" + str(i):
                                    if tag.width - (i + 1) <= 1: tail_width = 1
                                    else: tail_width = int(tag.width - (i + 1))
                                    item.setData([str(tag.mas_x_f[current_step - (i + 1)])], [str(tag.mas_y_f[current_step - (i + 1)])], pen=pg.mkPen(width=tail_width, color=tag.color), symbol='o', name=(tag.name + "tail" + str(i)))
                    self.count += 1
                    self.slider.setValue(int(self.count / len(self.log) * 1000))
                    if self.count >= len(self.log): self.ButtonStopLogic()
                    break

        if self.flag_x1: self.current_time += 0.001
        elif self.flag_x2: self.current_time += 0.001 * 2
        elif self.flag_x5: self.current_time += 0.001 * 5
        elif self.flag_x10: self.current_time += 0.001 * 10
        elif self.flag_x50: self.current_time += 0.001 * 50
        elif self.flag_x100: self.current_time += 0.001 * 100
        self.current_date_layot.setText(str(time.ctime(float(self.current_time))))

    def ButtonPauseLogic(self):
        if len(self.log) != 0:
            self.timer.stop()

    def ButtonStopLogic(self):
        if len(self.log) != 0:
            self.timer.stop()
            self.count = 0
            self.current_time = float(self.log[0][0])
            self.slider.setValue(0)
            self.current_date_layot.setText(str(time.ctime(float(self.log[0][0]))))
            for tag in self.tags:
                tag.x = tag.start_x
                tag.y = tag.start_y
                tag.z = tag.start_z
                for i in range(len(self.tags)):
                    if self.tags[i].name == tag.name:
                        self.table.setItem(i + 1, 2, QTableWidgetItem(self.tags[i].x))
                        self.table.setItem(i + 1, 3, QTableWidgetItem(self.tags[i].y))
                        self.table.resizeColumnsToContents()
                for item in self.graph_widget.listDataItems():
                    if item.name() == tag.name:
                        item.setData([tag.x], [tag.y],
                                     pen=pg.mkPen(width=tag.width, color=tag.color),
                                     symbol='h',
                                     name=tag.name)
                for i in range(tag.tail_length):
                    for item in self.graph_widget.listDataItems():
                        if item.name() == tag.name + "tail" + str(i):
                            if tag.width - (i + 1) <= 1: tail_width = 1
                            else: tail_width = int(tag.width - (i + 1))
                            item.setData([tag.x], [tag.y],
                                         pen=pg.mkPen(width=tail_width, color=tag.color), symbol='o', name=(tag.name + "tail" + str(i)))

    def ChangeTagColor(self):
        for item in self.table.selectedItems():
            if item.column() == 1:
                for tag in self.tags:
                    if tag.name == self.tags[item.row()].name:
                        color = QColorDialog.getColor()
                        if color.isValid():
                            tag.color = color.name()
                            self.table.setItem(item.row(), 1, QTableWidgetItem(color.name()))
                            for item1 in self.table.selectedItems():
                                if item1.column() == 1:
                                    for tag1 in self.tags:
                                        if tag1.name == self.tags[item1.row()].name:
                                            item1.setBackground(QColor(color.name()))
                                            for item2 in self.graph_widget.listDataItems():

                                                if item2.name() == tag1.name + "path":
                                                    for i in range(len(self.tags)):
                                                        if self.tags[i].name == tag1.name:
                                                            current_step = 0
                                                            for j in range(len(self.tags[i].mas_time)):
                                                                if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]):
                                                                    current_step = j

                                                            left_path = int(current_step - (current_step / 100 * self.time_tag_path_sliders[i].value()))
                                                            right_path = int(current_step + ((len(self.tags[i].mas_x_f) - current_step) / 100 * self.time_tag_path_sliders[i].value()))

                                                            for item5 in self.graph_widget.listDataItems():
                                                                if item5.name() == self.tags[i].name + "path":
                                                                    item5.setData(self.tags[i].mas_x_f[left_path:right_path], self.tags[i].mas_y_f[left_path:right_path],
                                                                                 pen=pg.mkPen(width=1, color=self.tags[i].color), name=(self.tags[i].name + "path"))

                                                if item2.name() == tag1.name:
                                                    current_step = 0
                                                    for j in range(len(tag1.mas_time)):
                                                        if float(tag1.current_time) == float(tag1.mas_time[j]):
                                                            current_step = j

                                                    item2.setData([tag1.mas_x_f[current_step]], [tag1.mas_y_f[current_step]],
                                                                 pen=pg.mkPen(width=tag1.width, color=tag1.color),
                                                                 symbol='o',
                                                                 name=tag1.name)

                                                    if current_step > tag1.tail_length:
                                                        for j in range(tag1.tail_length):
                                                            for item_tail2 in self.graph_widget.listDataItems():
                                                                if item_tail2.name() == tag1.name + "tail" + str(j):
                                                                    if tag1.width - (j + 1) <= 1: tail_width = 1
                                                                    else: tail_width = int(tag1.width - (j + 1))
                                                                    item_tail2.setData([tag1.mas_x_f[current_step - (j + 1)]],
                                                                                 [tag1.mas_y_f[current_step - (j + 1)]],
                                                                                 pen=pg.mkPen(width=tail_width, color=tag1.color), symbol='o',
                                                                                 name=tag1.name + "tail" + str(j))

                            break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()