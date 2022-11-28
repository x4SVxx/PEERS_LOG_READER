import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
import pyqtgraph as pg
import parameters
import time
from PIL import Image
import numpy as np
import button
import slider
import table
import layot
import load_log
from tag import Tag
import random

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.min_time_log = 10**100 # минимальное время лога СТАРТ (задается очень большой величиной т.к. потом сравнивается и изменяется до минимума)
        self.max_time_log = 0 # максимальное время лога ФИНИШ (задается 0 т.к. потом сравнивается и изменяется до максимума)
        self.filenames_mas =[]
        self.all_logs_mas = []
        self.log_times = []
        self.log = []
        self.tags = []
        self.count = 0
        self.tag_width_sliders = []
        self.enable_disable_checkboxes = []
        self.tag_path_checkboxes = []
        self.time_tag_path_sliders = []
        self.tag_tails_length_sliders = []
        self.buttons_delete_log_mas = []
        self.current_speed = parameters.current_speed
        self.slide_menu_bar_flag = False
        # self.max_beacon_number = 0
        # self.log_for_beacons_mas = []
        #
        # self.current_text_combo_box = ""

        self.MainWindowGeometry()
        self.CreateMenuBar()
        self.CreateGraph()
        self.CreateButtons()
        self.CreateSlider()
        self.CreateDateLayot()
        self.CreateTable()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.Draw())

        self.ButtonNormalSpeedLogic()

    def MainWindowGeometry(self):
        self.SCREEN_WIDTH = QApplication.desktop().width()
        self.SCREEN_HEIGHT = QApplication.desktop().height()
        self.window_width = int(self.SCREEN_WIDTH / 10 * 9)
        self.window_height = int(self.SCREEN_HEIGHT / 10 * 9)
        self.window_x = int(self.SCREEN_WIDTH / 2 - self.window_width / 2)
        self.window_y = int(self.SCREEN_HEIGHT / 2 - self.window_height / 2)
        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #F3F3F3")
        self.setWindowTitle("PEERS LOGS ANALYSIS")

    def CreateMenuBar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setGeometry(0, 0, self.window_width, parameters.menu_bar_height)
        self.menu_bar.setStyleSheet("QMenuBar { background-color: White }" "QMenuBar::item:selected { background-color: LightGrey }")

        self.log_menu = QtWidgets.QMenu("Лог", self)
        self.log_menu.setStyleSheet("QMenu { background-color: White }" "QMenu { color: Black }" "QMenu::item:selected { background-color: LightGrey }")
        self.menu_bar.addMenu(self.log_menu)

        self.load_log_action = QAction("Загрузить лог", self)
        self.log_menu.addAction(self.load_log_action)
        self.load_log_action.triggered.connect(lambda : load_log.LogLoad(self))

        self.map_menu = QtWidgets.QMenu("Карта", self)
        self.map_menu.setStyleSheet("QMenu { background-color: White }" "QMenu { color: Black }" "QMenu::item:selected { background-color: LightGrey }")
        self.menu_bar.addMenu(self.map_menu)

        self.load_map_action = QAction("Загрузить карту", self)
        self.map_menu.addAction(self.load_map_action)
        self.load_map_action.triggered.connect(lambda : self.MapLoad())

        self.delete_map_action = QAction("Удалить карту", self)
        self.map_menu.addAction(self.delete_map_action)
        self.delete_map_action.triggered.connect(lambda : self.MapDelete())

        self.mod_menu = QtWidgets.QMenu("Режим работы", self)
        self.mod_menu.setStyleSheet("QMenu { background-color: White }" "QMenu { color: Black }" "QMenu::item:selected { background-color: LightGrey }")
        self.menu_bar.addMenu(self.mod_menu)

        self.tags_action = QAction("Анализ работы меток", self)
        self.mod_menu.addAction(self.tags_action)
        self.tags_action.triggered.connect(lambda : self.TagsMod())

        self.anchors_action = QAction("Анализ работы маяков", self)
        self.mod_menu.addAction(self.anchors_action)
        self.anchors_action.triggered.connect(lambda : self.AnchorMod())

    def MapLoad(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "SELECT A MAP", ".", "Images files (*.png *.jpg *.jpeg)")
        if filename:
            self.img = pg.ImageItem(np.flipud(np.array(Image.open(filename))).transpose([1, 0, 2]), name="map")
            self.img.setRect(QRect(int(filename.split()[1]), int(filename.split()[2]), int(filename.split()[3]), int(filename.split()[4].split(".")[0])))
            self.img.setZValue(-100)
            self.graph_widget.addItem(self.img)

    def MapDelete(self):
        self.graph_widget.removeItem(self.img)

    def CreateGraph(self):
        self.graph_width = int(self.window_width / 100 * 88)
        self.graph_height = int(self.window_height - parameters.offset_top - parameters.offset_bot - parameters.button_display_height - parameters.offset_after_graph - parameters.date_layot_height - parameters.offset_before_and_after_date_layot * 2 - parameters.table_height- parameters.menu_bar_height)
        self.graph_widget = pg.PlotWidget(self)
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setBackground("White")
        self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.menu_bar_height, self.graph_width, self.graph_height))
        self.graph_widget.getAxis("bottom").setTickFont(QFont(parameters.axes_font, parameters.axes_font_size))
        self.graph_widget.getAxis("left").setTickFont(QFont(parameters.axes_font, parameters.axes_font_size))
        self.graph_widget.getAxis('bottom').setTextPen(pg.mkPen(color="Black", width=3))
        self.graph_widget.getAxis('left').setTextPen(pg.mkPen(color="Black", width=3))

    def CreateButtons(self):
        self.button_play = button.CreateButton(self, int(parameters.offset_left), int(self.window_height - parameters.offset_bot - parameters.button_display_height), int(parameters.button_display_width), int(parameters.button_display_height), 14, "►", self.ButtonPlayLogic)
        self.button_pause = button.CreateButton(self, int(parameters.offset_left + parameters.button_display_width + parameters.offset_between_buttons_display), int(self.window_height - parameters.offset_bot - parameters.button_display_height), int(parameters.button_display_width), int(parameters.button_display_height), 15, "l l", self.ButtonPauseLogic)
        self.button_stop = button.CreateButton(self, int(parameters.offset_left + parameters.button_display_width * 2 + parameters.offset_between_buttons_display * 2), int(self.window_height - parameters.offset_bot - parameters.button_display_height), int(parameters.button_display_width), int(parameters.button_display_height), 9, "⬛", self.ButtonStopLogic)
        self.button_max_speed = button.CreateButton(self, int(self.window_width - parameters.offset_right - parameters.button_speed_width), int(self.window_height - parameters.offset_bot - parameters.button_display_height), int(parameters.button_speed_width), int(parameters.button_speed_height), 8, "МАКС.", self.ButtonMaxSpeedLogic)
        self.button_average_speed = button.CreateButton(self, int(self.window_width - parameters.offset_right - parameters.button_speed_width * 2 - parameters.offset_between_buttons_display), int(self.window_height - parameters.offset_bot - parameters.button_display_height), int(parameters.button_speed_width), int(parameters.button_speed_height), 8, "СРЕД.", self.ButtonverageSpeedLogic)
        self.button_normal_speed = button.CreateButton(self, int(self.window_width - parameters.offset_right - parameters.button_speed_width * 3 - parameters.offset_between_buttons_display * 2), int(self.window_height - parameters.offset_bot - parameters.button_display_height), int(parameters.button_speed_width), int(parameters.button_speed_height), 8, "НОРМ.", self.ButtonNormalSpeedLogic)
        self.button_slide_tools = button.CreateButton(self, int(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table), int(parameters.offset_top + parameters.menu_bar_height), 15, int(self.graph_height), 9, "<", self.ButtonSlideMenuLogic)

    def ButtonNormalSpeedLogic(self):
        try: button.ButtonSpeedLogic(self, self.button_normal_speed, parameters.current_speed * 1)
        except: pass
    def ButtonverageSpeedLogic(self):
        try: button.ButtonSpeedLogic(self, self.button_average_speed, parameters.current_speed * 5)
        except: pass
    def ButtonMaxSpeedLogic(self):
        try: button.ButtonSpeedLogic(self, self.button_max_speed, parameters.current_speed * 100)
        except: pass

    # def ButtonTargetsLogic(self):
    #     try:
    #         self.button_targets.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
    #                                           "QPushButton { background-color: silver }"
    #                                           "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
    #                                           "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
    #                                           "QPushButton { border-radius: " + "1" + "px }")
    #         self.button_beacons.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
    #                                           "QPushButton { background-color: light grey }"
    #                                           "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
    #                                           "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
    #                                           "QPushButton { border-radius: " + "1" + "px }")
    #
    #         if self.slide_menu_bar:
    #             self.table.setGeometry(0, 0, 0, 0)
    #             self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.window_width - parameters.offset_left - parameters.offset_right - 15 - 5, self.graph_height))
    #             self.button_slide_tools.setGeometry(self.window_width - parameters.offset_right - 15,
    #                                                 parameters.offset_top + parameters.button_beacons_height,
    #                                                 15,
    #                                                 self.graph_height)
    #             self.button_slide_tools.setText("<")
    #         else:
    #             self.table.setGeometry(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table,
    #                                    parameters.offset_top + parameters.button_beacons_height,
    #                                    self.window_width - (parameters.offset_left + parameters.offset_right + parameters.offset_between_graph_and_table + self.graph_width),
    #                                    self.graph_height)
    #             self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.graph_width, self.graph_height))
    #             self.button_slide_tools.setGeometry(parameters.offset_left + self.graph_width + 11,
    #                                                 parameters.offset_top + parameters.button_beacons_height,
    #                                                 15,
    #                                                 self.graph_height)
    #             self.button_slide_tools.setText(">")
    #
    #         self.button_1x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 6 - parameters.offset_between_buttons_display * 5,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.button_2x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 5 - parameters.offset_between_buttons_display * 4,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.button_5x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 4 - parameters.offset_between_buttons_display * 3,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.button_10x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 3 - parameters.offset_between_buttons_display * 2,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.button_50x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width * 2 - parameters.offset_between_buttons_display,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.button_100x.setGeometry(self.window_width - parameters.offset_right - parameters.button_display_width,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.button_play.setGeometry(parameters.offset_left,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.button_pause.setGeometry(parameters.offset_left + parameters.button_display_width + parameters.offset_between_buttons_display,
    #                                       self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                       parameters.button_display_width,
    #                                       parameters.button_display_height)
    #         self.button_stop.setGeometry(parameters.offset_left + parameters.button_display_width * 2 + parameters.offset_between_buttons_display * 2,
    #                                      self.window_height - parameters.offset_bot - parameters.button_display_height,
    #                                      parameters.button_display_width,
    #                                      parameters.button_display_height)
    #         self.slider.setGeometry(int(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3),
    #                                 int(self.window_height - parameters.offset_bot - parameters.button_display_height + (parameters.button_display_height - parameters.slider_height) / 2),
    #                                 int(self.window_width - (parameters.offset_left + parameters.offset_right + parameters.button_display_width * 9 + parameters.offset_between_buttons_display * 9)),
    #                                 int(parameters.slider_height))
    #
    #         self.start_date_layot.setGeometry(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3,
    #                                             self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
    #                                             parameters.date_layot_width,
    #                                             parameters.date_layot_height)
    #
    #         self.current_date_layot.setGeometry(int((self.window_width - parameters.offset_right - parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3) / 2 - parameters.date_layot_width / 2),
    #                                             self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
    #                                             parameters.date_layot_width,
    #                                             parameters.date_layot_height)
    #
    #         self.finish_date_layot.setGeometry(self.window_width - parameters.offset_right - parameters.date_layot_width,
    #                                             self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot,
    #                                             parameters.date_layot_width,
    #                                             parameters.date_layot_height)
    #
    #         self.beacons_graph_widget.setGeometry(QtCore.QRect(0, 0, 0, 0))
    #         self.combo_box.setGeometry(0, 0, 0, 0)
    #         self.combo_box_beacons.setGeometry(0, 0, 0, 0)
    #     except: pass
    #
    # def ButtonBeaconsLogic(self):
    #     try:
    #         self.button_targets.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
    #                                           "QPushButton { background-color: light grey }"
    #                                           "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
    #                                           "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
    #                                           "QPushButton { border-radius: " + "1" + "px }")
    #         self.button_beacons.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
    #                                           "QPushButton { background-color: silver }"
    #                                           "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
    #                                           "QPushButton { border: " + "1" + "px solid " + "Black" + " }"
    #                                           "QPushButton { border-radius: " + "1" + "px }")
    #
    #         self.table.setGeometry(0, 0, 0, 0)
    #         self.graph_widget.setGeometry(QtCore.QRect(0, 0, 0, 0))
    #         self.button_slide_tools.setGeometry(0, 0, 0, 0)
    #         self.button_1x.setGeometry(0, 0, 0, 0)
    #         self.button_2x.setGeometry(0, 0, 0, 0)
    #         self.button_5x.setGeometry(0, 0, 0, 0)
    #         self.button_10x.setGeometry(0, 0, 0, 0)
    #         self.button_50x.setGeometry(0, 0, 0, 0)
    #         self.button_100x.setGeometry(0, 0, 0, 0)
    #         self.button_play.setGeometry(0, 0, 0, 0)
    #         self.button_pause.setGeometry(0, 0, 0, 0)
    #         self.button_stop.setGeometry(0, 0, 0, 0)
    #         self.slider.setGeometry(0, 0, 0, 0)
    #         self.start_date_layot.setGeometry(0, 0, 0, 0)
    #         self.current_date_layot.setGeometry(0, 0, 0, 0)
    #         self.finish_date_layot.setGeometry(0, 0, 0, 0)
    #
    #         self.beacons_graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.button_beacons_height, self.beacons_graph_width, self.beacons_graph_height))
    #         self.combo_box.setGeometry(parameters.offset_left + parameters.button_beacons_width + parameters.button_targets_width + 10, parameters.offset_top, parameters.target_select_menu_width, parameters.target_select_menu_height)
    #         self.combo_box_beacons.setGeometry(parameters.offset_left + parameters.button_beacons_width + parameters.button_targets_width + 10 + parameters.target_select_menu_width, parameters.offset_top, parameters.target_select_menu_width, parameters.target_select_menu_height)
    #     except: pass
    #
    def ButtonSlideMenuLogic(self):
        if not self.slide_menu_bar_flag:
            self.table_for_filenames.setGeometry(0, 0, 0, 0)
            self.table_long_for_filenames.setGeometry(int(parameters.offset_left + self.window_width / 100 * 60 + parameters.offset_between_graph_and_table + 15), parameters.offset_top + parameters.menu_bar_height, int(self.window_width - parameters.offset_left - parameters.offset_right - (self.window_width / 100 * 60) - parameters.offset_between_graph_and_table - 15), self.graph_height)
            self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.menu_bar_height, int(self.window_width / 100 * 60), self.graph_height))
            self.button_slide_tools.setGeometry(self.window_width - parameters.offset_right - int(self.window_width - parameters.offset_left - parameters.offset_right - (self.window_width / 100 * 60) - parameters.offset_between_graph_and_table - 15) - 15,
                                                parameters.offset_top + parameters.menu_bar_height,
                                                15,
                                                self.graph_height)
            self.button_slide_tools.setText(">")
            self.slide_menu_bar_flag = True
        else:
            self.table_long_for_filenames.setGeometry(0, 0, 0, 0)
            self.table_for_filenames.setGeometry(int(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table + 15), int(parameters.offset_top + parameters.menu_bar_height), int(self.window_width - parameters.offset_right - parameters.offset_left - self.graph_width - parameters.offset_between_graph_and_table - 15), int(self.graph_height))
            self.graph_widget.setGeometry(QtCore.QRect(parameters.offset_left, parameters.offset_top + parameters.menu_bar_height, self.graph_width, self.graph_height))
            self.button_slide_tools.setGeometry(int(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table), int(parameters.offset_top + parameters.menu_bar_height), 15, int(self.graph_height))
            self.button_slide_tools.setText("<")
            self.slide_menu_bar_flag = False

    def CreateSlider(self):
        self.slider = slider.CreateSlider(self, int(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3), int(self.window_height - parameters.offset_bot - parameters.button_display_height + (parameters.button_display_height - parameters.slider_height) / 2), int(self.window_width - (parameters.offset_left + parameters.offset_right + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 6 + parameters.button_speed_width * 3)), int(parameters.slider_height), self.SliderLogic)

    def CreateDateLayot(self):
        self.start_date_layot = layot.CreateLayot(self, int(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3), int(self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot), int(parameters.date_layot_width), int(parameters.date_layot_height))
        self.current_date_layot = layot.CreateLayot(self, int(int(parameters.offset_left + parameters.button_display_width * 3 + parameters.offset_between_buttons_display * 3) + int(self.window_width - (parameters.offset_left + parameters.offset_right + parameters.button_display_width * 9 + parameters.offset_between_buttons_display * 9)) / 2 - parameters.date_layot_width / 2), int(self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot), int(parameters.date_layot_width), int(parameters.date_layot_height))
        self.finish_date_layot = layot.CreateLayot(self, int(self.window_width - parameters.offset_right - parameters.date_layot_width - (parameters.button_speed_width * 3 + parameters.offset_between_buttons_display * 3)), int(self.window_height - parameters.offset_bot - parameters.button_display_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot), int(parameters.date_layot_width), int(parameters.date_layot_height))
        self.speed_layot = layot.CreateLayot(self, int(self.window_width - parameters.offset_right - parameters.button_speed_width * 1.5 - parameters.offset_between_buttons_display - 100/2), int(self.window_height - parameters.offset_bot - parameters.button_speed_height - parameters.date_layot_height - parameters.offset_before_and_after_date_layot), 100, 20)
        self.speed_layot.setText("СКОРОСТЬ")
    def CreateTable(self):
        self.table_for_tags = table.CreateTableForTags(self, int(parameters.offset_left), int(parameters.offset_top + self.graph_height + parameters.offset_between_graph_and_table + parameters.menu_bar_height), int(self.graph_width), int(parameters.table_height))
        self.table_for_filenames = table.CreateTableForLogs(self, int(parameters.offset_left + self.graph_width + parameters.offset_between_graph_and_table + 15), int(parameters.offset_top + parameters.menu_bar_height), int(self.window_width - parameters.offset_right - parameters.offset_left - self.graph_width - parameters.offset_between_graph_and_table - 15), int(self.graph_height))
        self.table_long_for_filenames = table.CreateLongTableForLogs(self)

    def SliderLogic(self, value):
        if self.slider.isSliderDown():
            self.count = int(len(self.log) * value / 1000)
            if self.count >= len(self.log): self.count = len(self.log) - 1
            self.Draw()

    def Filter(self):
        alpha = 0.9
        for tag in self.tags:
            if len(tag.mas_x) != 0:
                for i in range(1, len(tag.mas_x)):
                    if float(tag.mas_time[i]) - float(tag.mas_time[i - 1]) < 10:
                        tag.mas_x_f[i] = float(tag.mas_x_f[i - 1] * alpha + tag.mas_x[i] * (1 - alpha))
                        tag.mas_y_f[i] = float(tag.mas_y_f[i - 1] * alpha + tag.mas_y[i] * (1 - alpha))
                    else:
                        tag.mas_x_f[i] = tag.mas_x[i]
                        tag.mas_y_f[i] = tag.mas_y[i]



    def ButtonPlayLogic(self):
        button.ButtonDisplayPress(self.button_play, self.button_pause, self.button_stop)
        if len(self.log) != 0: self.timer.start(1)

    def Draw(self):
        if ((time.time() - self.help_time) * self.current_speed) > (float(self.log[self.count][0]) - float(self.log[self.count - 1][0])) or self.count == 0:
            self.current_time = float(self.log[self.count][0])
            """Удаление метки, если ее логов не было больше n-ого количества времени"""
            if self.slider.isSliderDown():
                for tag in self.tags:
                    if len(tag.mas_time) != 0:
                        current_delete_step = 0
                        for i in range(len(tag.mas_time)):
                            if float(self.log[self.count][0]) < float(tag.mas_time[i]):
                                current_delete_step = i - 1
                                break
                        tag.current_time = tag.mas_time[current_delete_step]
                        tag.x = tag.mas_x[current_delete_step]
                        tag.y = tag.mas_y[current_delete_step]
                        tag.z = tag.mas_z[current_delete_step]
            for tag in self.tags:
                if self.current_time - float(tag.current_time) > parameters.detele_tag_time:
                    for item in self.graph_widget.listDataItems():
                        if item.name() == tag.name: self.graph_widget.removeItem(item)
                        for i in range(tag.tail_length):
                            if item.name() == tag.name + "tail" + str(i): self.graph_widget.removeItem(item)

            """Обработка нового лога"""
            if self.log[self.count][1] == "CLE:" and self.log[self.count][2] == "TAG" and self.log[self.count][4] == "1":
                for tag in self.tags:
                    if self.log[self.count][3] == tag.name:
                        tag.x = self.log[self.count][5]
                        tag.y = self.log[self.count][6]
                        tag.z = self.log[self.count][7]
                        tag.current_time = self.log[self.count][0]

                        for item in self.graph_widget.listDataItems():
                            if item.name() == tag.name: self.graph_widget.removeItem(item)
                            for i in range(tag.tail_length):
                                if item.name() == tag.name + "tail" + str(i): self.graph_widget.removeItem(item)

                        current_step = 0
                        for i in range(len(tag.mas_time)):
                            if float(tag.current_time) == float(tag.mas_time[i]): current_step = i

                        for i in range(len(self.tags)):
                            if self.tags[i].name == tag.name:
                                self.table_for_tags.setItem(i, 2, QTableWidgetItem(str(round(self.tags[i].mas_x_f[current_step], 2))))
                                self.table_for_tags.setItem(i, 3, QTableWidgetItem(str(round(self.tags[i].mas_y_f[current_step], 2))))
                                self.table_for_tags.resizeColumnsToContents()

                        for i in range(len(self.tags)):
                            if self.tags[i] == tag:
                                if self.enable_disable_checkboxes[i].isChecked():
                                    self.graph_widget.addItem(pg.ScatterPlotItem([tag.mas_x_f[current_step]], [tag.mas_y_f[current_step]], pen=pg.mkPen(width=tag.width, color=tag.color), name=tag.name))

                                    if current_step > tag.tail_length:
                                        for j in range(tag.tail_length):
                                            if tag.width - (j + 1) <= 1: tail_width = 1
                                            else: tail_width = int(tag.width - (j + 1))
                                            self.graph_widget.addItem(pg.ScatterPlotItem([str(tag.mas_x_f[current_step - (j + 1)])], [str(tag.mas_y_f[current_step - (j + 1)])], pen=pg.mkPen(width=tail_width, color=tag.color), symbol='o', name=(tag.name + "tail" + str(j))))
                        break
            self.count += 1
            self.current_date_layot.setText(str(time.ctime(float(self.current_time))))
            if not self.slider.isSliderDown(): self.slider.setValue(int(self.count / len(self.log) * 1000))
            if self.count >= len(self.log): self.timer.stop()
            self.help_time = time.time()

    def ButtonPauseLogic(self):
        button.ButtonDisplayPress(self.button_pause, self.button_play, self.button_stop)
        self.timer.stop()

    def ButtonStopLogic(self):
        button.ButtonDisplayPress(self.button_stop, self.button_play, self.button_pause)
        self.timer.stop()
        self.count = 0
        self.current_time = self.min_time_log
        self.help_time = self.min_time_log
        self.slider.setValue(0)
        self.current_date_layot.setText(str(time.ctime(self.current_time)))
        for i in range(len(self.tags)):
            self.table_for_tags.setItem(i, 2, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 3, QTableWidgetItem(""))
        self.table_for_tags.resizeColumnsToContents()
        for tag in self.tags:
            for item in self.graph_widget.listDataItems():
                if item.name() == tag.name: self.graph_widget.removeItem(item)
            for i in range(tag.tail_length):
                for item in self.graph_widget.listDataItems():
                    if item.name() == tag.name + "tail" + str(i): self.graph_widget.removeItem(item)

    def TailLengthSliderLogic(self, value):
        for i in range(len(self.tag_tails_length_sliders)):
            if self.tag_tails_length_sliders[i].value() == value:
                for item in self.graph_widget.listDataItems():
                    for J in range(self.tags[i].tail_length):
                        if item.name() == self.tags[i].name + "tail" + str(J): self.graph_widget.removeItem(item)
                self.tags[i].tail_length = int(value / 10)
                if self.enable_disable_checkboxes[i].isChecked():
                    current_step = 0
                    for j in range(len(self.tags[i].mas_time)):
                        if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]): current_step = j
                    if current_step > self.tags[i].tail_length:
                        for j in range(self.tags[i].tail_length):
                            if self.tags[i].width - (j + 1) <= 1: tail_width = 1
                            else: tail_width = int(self.tags[i].width - (j + 1))
                            self.graph_widget.addItem(pg.ScatterPlotItem([str(self.tags[i].mas_x_f[current_step - (j + 1)])], [str(self.tags[i].mas_y_f[current_step - (j + 1)])], pen=pg.mkPen(width=tail_width, color=self.tags[i].color), symbol='o', name=(self.tags[i].name + "tail" + str(j))))

    def TimePathSliderLogic(self, value):
        for i in range(len(self.time_tag_path_sliders)):
            if self.time_tag_path_sliders[i].value() == value:
                current_step = 0
                for j in range(len(self.tags[i].mas_time)):
                    if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]): current_step = j
                left_path = int(current_step - (current_step / 100 * value))
                right_path = int(current_step + ((len(self.tags[i].mas_x_f) - current_step) / 100 * value))
                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name + "path":
                        item.setData(self.tags[i].mas_x_f[left_path:right_path], self.tags[i].mas_y_f[left_path:right_path], pen=pg.mkPen(width=1, color=self.tags[i].color), name=(self.tags[i].name + "path"))

    def PathCheckboxLogic(self):
        for i in range(len(self.tags)):
            if self.tag_path_checkboxes[i].isChecked():
                if len(self.tags[i].mas_time) != 0:
                    path = self.graph_widget.plot(self.tags[i].mas_x_f, self.tags[i].mas_y_f, pen=pg.mkPen(width=1, color=self.tags[i].color), name=(self.tags[i].name + "path"))
                    path.setZValue(-1)
            else:
                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name + "path": self.graph_widget.removeItem(item)

    def EnableDisableCheckboxLogic(self):
        for i in range(len(self.tags)):
            if self.enable_disable_checkboxes[i].isChecked():
                if len(self.tags[i].mas_time) != 0:
                    current_step = 0
                    for j in range(len(self.tags[i].mas_time)):
                        if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]):
                            current_step = j
                    self.graph_widget.addItem(pg.ScatterPlotItem([self.tags[i].mas_x_f[current_step]], [self.tags[i].mas_y_f[current_step]], pen=pg.mkPen(width=self.tags[i].width, color=self.tags[i].color), name=self.tags[i].name))
                    if current_step > self.tags[i].tail_length:
                        for j in range(self.tags[i].tail_length):
                            if self.tags[i].width - (j + 1) <= 1: tail_width = 1
                            else: tail_width = int(self.tags[i].width - (j + 1))
                            self.graph_widget.addItem(pg.ScatterPlotItem([str(self.tags[i].mas_x_f[current_step - (j + 1)])], [str(self.tags[i].mas_y_f[current_step - (j + 1)])],  pen=pg.mkPen(width=tail_width, color=self.tags[i].color), symbol='o', name=(self.tags[i].name + "tail" + str(j))))
            else:
                for item in self.graph_widget.listDataItems():
                    if item.name() == self.tags[i].name: self.graph_widget.removeItem(item)
                    for j in range(self.tags[i].tail_length):
                        if item.name() == self.tags[i].name + "tail" + str(j): self.graph_widget.removeItem(item)

    def TagWidthSliderLogic(self, value):
        for i in range(len(self.tag_width_sliders)):
            if self.tag_width_sliders[i].value() == value:
                self.tags[i].width = value / 10
                if self.enable_disable_checkboxes[i].isChecked():
                    if len(self.tags[i].mas_time) != 0:
                        for item in self.graph_widget.listDataItems():
                            if item.name() == self.tags[i].name: self.graph_widget.removeItem(item)
                            for j in range(self.tags[i].tail_length):
                                if item.name() == self.tags[i].name + "tail" + str(j): self.graph_widget.removeItem(item)
                        current_step = 0
                        for j in range(len(self.tags[i].mas_time)):
                            if float(self.tags[i].current_time) == float(self.tags[i].mas_time[j]): current_step = j
                        self.graph_widget.addItem(pg.ScatterPlotItem([self.tags[i].mas_x_f[current_step]], [self.tags[i].mas_y_f[current_step]], pen=pg.mkPen(width=self.tags[i].width, color=self.tags[i].color), name=self.tags[i].name))
                        if current_step > self.tags[i].tail_length:
                            for j in range(self.tags[i].tail_length):
                                if self.tags[i].width - (j + 1) <= 1: tail_width = 1
                                else: tail_width = int(self.tags[i].width - (j + 1))
                                self.graph_widget.addItem(pg.ScatterPlotItem([str(self.tags[i].mas_x_f[current_step - (j + 1)])], [str(self.tags[i].mas_y_f[current_step - (j + 1)])], pen=pg.mkPen(width=tail_width, color=self.tags[i].color), symbol='o', name=(self.tags[i].name + "tail" + str(j))))

    def ChangeTagColor(self):
        for item in self.table_for_tags.selectedItems():
            if item.column() == 1:
                for tag in self.tags:
                    if tag.name == self.tags[item.row()].name:
                        color = QColorDialog.getColor()
                        if color.isValid():
                            tag.color = color.name()
                            self.table_for_tags.setItem(item.row(), 1, QTableWidgetItem(color.name()))
                            for item1 in self.table_for_tags.selectedItems():
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
                                                                    item5.setData(self.tags[i].mas_x_f[left_path:right_path], self.tags[i].mas_y_f[left_path:right_path], pen=pg.mkPen(width=1, color=self.tags[i].color), name=(self.tags[i].name + "path"))
                                                if item2.name() == tag1.name:
                                                    current_step = 0
                                                    for j in range(len(tag1.mas_time)):
                                                        if float(tag1.current_time) == float(tag1.mas_time[j]):
                                                            current_step = j
                                                    item2.setData([tag1.mas_x_f[current_step]], [tag1.mas_y_f[current_step]], pen=pg.mkPen(width=tag1.width, color=tag1.color), symbol='o',  name=tag1.name)
                                                    if current_step > tag1.tail_length:
                                                        for j in range(tag1.tail_length):
                                                            for item_tail2 in self.graph_widget.listDataItems():
                                                                if item_tail2.name() == tag1.name + "tail" + str(j):
                                                                    if tag1.width - (j + 1) <= 1: tail_width = 1
                                                                    else: tail_width = int(tag1.width - (j + 1))
                                                                    item_tail2.setData([tag1.mas_x_f[current_step - (j + 1)]], [tag1.mas_y_f[current_step - (j + 1)]], pen=pg.mkPen(width=tail_width, color=tag1.color), symbol='o', name=tag1.name + "tail" + str(j))
                            break

    def DeleteLogLogic(self):
        self.all_logs_mas.pop(self.table_long_for_filenames.selectedIndexes()[0].row())
        self.filenames_mas.pop(self.table_long_for_filenames.selectedIndexes()[0].row())

        self.tag_width_sliders = []
        self.enable_disable_checkboxes = []
        self.tag_path_checkboxes = []
        self.time_tag_path_sliders = []
        self.tag_tails_length_sliders = []
        self.buttons_delete_log_mas = []
        self.slider.setValue(0)
        self.tags = []
        self.log = []
        self.count = 0

        self.timer.stop()
        for item in self.graph_widget.listDataItems(): self.graph_widget.removeItem(item)

        self.table_for_filenames.setRowCount(0)
        self.table_long_for_filenames.setRowCount(0)
        self.table_for_tags.setRowCount(0)


        for filename in self.filenames_mas:
            new_log = []
            file = open(filename.filename, 'r')
            while True:
                line = file.readline().split()
                if not line: break
                if line[0] == "Synchronized:" or line[0] == "Sync":
                    pass
                else:
                    new_log.append(line)
                    self.log_times.append(float(line[0]))

                    if float(line[0]) < self.min_time_log:
                        self.min_time_log = float(line[0])
                    if float(line[0]) > self.max_time_log:
                        self.max_time_log = float(line[0])

                    if line[1] == "CLE:" and line[2] == "TAG" and line[4] == "0":
                        """Добавление новых меток"""
                        flag_cross_tag_name = False
                        for tag in self.tags:
                            if line[3] == tag.name: flag_cross_tag_name = True
                        if not flag_cross_tag_name: self.tags.append(
                            Tag(line[3], random.choice(parameters.tag_color), parameters.tag_width, line[5], line[6], line[7]))
                        """Добавление данных к метке"""
                        for tag in self.tags:
                            if line[3] == tag.name: tag.mas_time_with_flag_0.append(float(line[0]))

                    elif line[1] == "CLE:" and line[2] == "TAG" and line[4] == "1":
                        """Добавление новых меток"""
                        flag_cross_tag_name = False
                        for tag in self.tags:
                            if line[3] == tag.name: flag_cross_tag_name = True
                        if not flag_cross_tag_name: self.tags.append(
                            Tag(line[3], random.choice(parameters.tag_color), parameters.tag_width, line[5], line[6], line[7]))
                        # """Добавление данных к метке"""
                        # for tag in self.tags:
                        #     if line[3] == tag.name:
                        #         tag.mas_x.append(float(line[5]))
                        #         tag.mas_y.append(float(line[6]))
                        #         tag.mas_z.append(float(line[7]))
                        #         tag.mas_time.append(float(line[0]))
            file.close()

        for log_mas in self.all_logs_mas:
            for log in log_mas: self.log.append(log)

        print("Загружено " + str(len(self.filenames_mas)) + " лог(-а)(-ов)")
        self.current_time = self.min_time_log
        self.help_time = self.min_time_log

        for log in self.log:
            if log[1] == "CLE:" and log[2] == "TAG" and log[4] == "1":
                for tag in self.tags:
                    if log[3] == tag.name:
                        tag.mas_x.append(float(log[5]))
                        tag.mas_y.append(float(log[6]))
                        tag.mas_z.append(float(log[7]))
                        tag.mas_time.append(float(log[0]))

        for tag in self.tags:
            if len(tag.mas_time) != 0:
                for i in range(len(tag.mas_x)):
                    tag.mas_x_f.append(0)
                    tag.mas_y_f.append(0)
                tag.mas_x_f[0] = tag.mas_x[0]
                tag.mas_y_f[0] = tag.mas_y[0]

        self.Filter()

        """Заполнение таблицы логов"""
        self.table_for_filenames.setRowCount(len(self.filenames_mas))
        for i in range(len(self.filenames_mas)):
            filename_split_slash = self.filenames_mas[i].filename.split('/')
            filename_split_dot = filename_split_slash[len(filename_split_slash) - 1].split('.')
            self.table_for_filenames.setItem(i, 0, QTableWidgetItem(str(filename_split_dot[0])))
        self.table_for_filenames.resizeColumnsToContents()
        self.table_for_filenames.resizeRowsToContents()
        """Заполнение расширинной таблицы логов"""
        self.table_long_for_filenames.setRowCount(len(self.filenames_mas))
        for i in range(len(self.filenames_mas)):
            filename_split_slash = self.filenames_mas[i].filename.split('/')
            filename_split_dot = filename_split_slash[len(filename_split_slash) - 1].split('.')
            self.table_long_for_filenames.setItem(i, 0, QTableWidgetItem(str(filename_split_dot[0])))
            self.table_long_for_filenames.setItem(i, 1, QTableWidgetItem(str(len(self.all_logs_mas[i]))))
            self.table_long_for_filenames.setItem(i, 2, QTableWidgetItem(
                time.ctime(self.filenames_mas[i].min_date) + " - " + time.ctime(self.filenames_mas[i].max_date)))

            button = QtWidgets.QPushButton(self)
            button.setStyleSheet("QPushButton { color: " + parameters.button_text_color + " }"
                                 "QPushButton { background-color: " + "Red" + " }"
                                 "QPushButton:pressed { background-color: " + parameters.button_press_background_color + " }"
                                 "QPushButton { border: " + parameters.button_border_width + "px solid " + parameters.button_border_color + " }"
                                 "QPushButton { border-radius: " + parameters.button_border_radius + "px }")
            button.setFont(QFont(parameters.button_font, 10))
            button.setText("DEL")
            button.clicked.connect(self.DeleteLogLogic)
            self.buttons_delete_log_mas.append(button)
            self.table_long_for_filenames.setCellWidget(i, 3, button)

        self.table_long_for_filenames.resizeColumnsToContents()
        self.table_long_for_filenames.resizeRowsToContents()

        """Заполнение таблицы меток"""
        self.table_for_tags.setRowCount(len(self.tags))
        for i in range(len(self.tags)):
            self.table_for_tags.setItem(i, 0, QTableWidgetItem(self.tags[i].name))
            self.table_for_tags.setItem(i, 1, QTableWidgetItem(self.tags[i].color))
            self.table_for_tags.item(i, 1).setBackground(QColor(self.tags[i].color))
            self.table_for_tags.setItem(i, 2, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 3, QTableWidgetItem(""))

            tag_width_slider = QSlider(Qt.Horizontal, self)
            tag_width_slider.setValue(int(self.tags[i].width * 10))
            tag_width_slider.valueChanged[int].connect(self.TagWidthSliderLogic)
            tag_width_slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}" "QSlider::handle:horizontal:pressed {background-color: black;}")
            self.tag_width_sliders.append(tag_width_slider)
            self.table_for_tags.setCellWidget(i, 4, tag_width_slider)

            enable_disable_checkbox = QCheckBox("", self)
            enable_disable_checkbox.setChecked(True)
            enable_disable_checkbox.stateChanged.connect(self.EnableDisableCheckboxLogic)
            self.enable_disable_checkboxes.append(enable_disable_checkbox)
            self.table_for_tags.setCellWidget(i, 5, enable_disable_checkbox)

            tag_check_checkbox = QCheckBox("", self)
            tag_check_checkbox.stateChanged.connect(self.PathCheckboxLogic)
            self.tag_path_checkboxes.append(tag_check_checkbox)
            self.table_for_tags.setCellWidget(i, 6, tag_check_checkbox)

            time_tag_path_slider = QSlider(Qt.Horizontal, self)
            time_tag_path_slider.setValue(100)
            time_tag_path_slider.valueChanged[int].connect(self.TimePathSliderLogic)
            time_tag_path_slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}" "QSlider::handle:horizontal:pressed {background-color: black;}")
            self.time_tag_path_sliders.append(time_tag_path_slider)
            self.table_for_tags.setCellWidget(i, 7, time_tag_path_slider)

            tag_tail_length_slider = QSlider(Qt.Horizontal, self)
            tag_tail_length_slider.setValue(int(self.tags[i].tail_length * 10))
            tag_tail_length_slider.valueChanged[int].connect(self.TailLengthSliderLogic)
            tag_tail_length_slider.setStyleSheet("QSlider::handle:horizontal {background-color: dimgrey;}" "QSlider::handle:horizontal:pressed {background-color: black;}")
            self.tag_tails_length_sliders.append(tag_tail_length_slider)
            self.table_for_tags.setCellWidget(i, 8, tag_tail_length_slider)

            self.table_for_tags.setItem(i, 9, QTableWidgetItem(str(len(self.tags[i].mas_time) + len(self.tags[i].mas_time_with_flag_0))))
            self.table_for_tags.setItem(i, 10, QTableWidgetItem(str((round(len(self.tags[i].mas_time) / (len(self.tags[i].mas_time) + len(self.tags[i].mas_time_with_flag_0)), 2) * 100)) + " %"))

            self.table_for_tags.resizeColumnsToContents()
            self.table_for_tags.resizeRowsToContents()

        if len(self.filenames_mas) != 0:
            self.start_date_layot.setText(str(time.ctime(float(self.min_time_log))))
            self.current_date_layot.setText(str(time.ctime(float(self.min_time_log))))
            self.finish_date_layot.setText(str(time.ctime(float(self.max_time_log))))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()