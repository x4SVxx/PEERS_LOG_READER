from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import *
from tag import Tag
import random
import parameters
import time
import file_class


def LogLoad(self):
    filenames, filetype = QFileDialog.getOpenFileNames(self, "SELECT A LOG", ".", "Text files (*.txt *.log)")

    file_flag = False
    for filename in filenames:
        if filename:
            file_flag = True

    if file_flag:
        self.tag_width_sliders = []
        self.enable_disable_checkboxes = []
        self.tag_path_checkboxes = []
        self.time_tag_path_sliders = []
        self.tag_tails_length_sliders = []
        self.buttons_delete_log_mas = []
        self.slider.setValue(0)
        # self.tags = []
        for tag in self.tags:
            tag.mas_time = []
            tag.mas_x = []
            tag.mas_y = []
            tag.mas_z = []
            tag.mas_x_f = []
            tag.mas_y_f = []
        self.log = []
        self.count = 0

        self.timer.stop()
        for item in self.graph_widget.listDataItems(): self.graph_widget.removeItem(item)

        self.table_for_filenames.setRowCount(0)
        self.table_for_tags.setRowCount(0)

        for i in range(len(self.filenames_mas)):
            self.table_for_filenames.setItem(i, 0, QTableWidgetItem(""))

        for i in range(len(self.filenames_mas)):
            self.table_long_for_filenames.setItem(i, 0, QTableWidgetItem(""))
            self.table_long_for_filenames.setItem(i, 1, QTableWidgetItem(""))
            self.table_long_for_filenames.setItem(i, 2, QTableWidgetItem(""))
            self.table_long_for_filenames.setItem(i, 3, QTableWidgetItem(""))


        for i in range(len(self.tags)):
            self.table_for_tags.setItem(i, 0, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 1, QTableWidgetItem(""))
            self.table_for_tags.item(i, 1).setBackground(QColor("White"))
            self.table_for_tags.setItem(i, 2, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 3, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 4, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 5, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 6, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 7, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 8, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 9, QTableWidgetItem(""))
            self.table_for_tags.setItem(i, 10, QTableWidgetItem(""))
            self.table_for_tags.resizeColumnsToContents()
            self.table_for_tags.resizeRowsToContents()

        for filename in filenames:
            if not filename:
                print("Пустой лог")
            else:
                filename_cross_flag = False
                for filename_obj in self.filenames_mas:
                    if filename_obj.filename == filename: filename_cross_flag = True
                if filename_cross_flag:
                    print("Пересечение логов")
                else:
                    filename_object = file_class.File(filename)
                    new_log = []
                    file = open(filename, 'r')
                    while True:
                        line = file.readline().split()
                        if not line: break
                        if line[0] == "Synchronized:" or line[0] == "Sync":
                            pass
                        else:
                            new_log.append(line)
                            self.log_times.append(float(line[0]))
                            """Поиск максимального и минимального времен лога (глобальное(по всем логам))"""
                            if float(line[0]) < filename_object.min_date:
                                filename_object.min_date = float(line[0])
                            if float(line[0]) > filename_object.max_date:
                                filename_object.max_date = float(line[0])

                            if float(line[0]) < self.min_time_log:
                                self.min_time_log = float(line[0])
                            if float(line[0]) > self.max_time_log:
                                self.max_time_log = float(line[0])

                            if line[1] == "CLE:" and line[2] == "TAG" and line[4] == "0":
                                """Добавление новых меток"""
                                flag_cross_tag_name = False
                                for tag in self.tags:
                                    if line[3] == tag.name: flag_cross_tag_name = True
                                if not flag_cross_tag_name: self.tags.append(Tag(line[3], random.choice(parameters.tag_color), parameters.tag_width, line[5], line[6], line[7]))
                                """Добавление данных к метке"""
                                for tag in self.tags:
                                    if line[3] == tag.name: tag.mas_time_with_flag_0.append(float(line[0]))

                            elif line[1] == "CLE:" and line[2] == "TAG" and line[4] == "1":
                                """Добавление новых меток"""
                                flag_cross_tag_name = False
                                for tag in self.tags:
                                    if line[3] == tag.name: flag_cross_tag_name = True
                                if not flag_cross_tag_name: self.tags.append(Tag(line[3], random.choice(parameters.tag_color), parameters.tag_width, line[5], line[6], line[7]))
                                # """Добавление данных к метке"""
                                # for tag in self.tags:
                                #     if line[3] == tag.name:
                                #         tag.mas_x.append(float(line[5]))
                                #         tag.mas_y.append(float(line[6]))
                                #         tag.mas_z.append(float(line[7]))
                                #         tag.mas_time.append(float(line[0]))
                    file.close()

                    if len(new_log) != 0:
                        if len(self.all_logs_mas) == 0:
                            self.all_logs_mas.append(new_log)
                            self.filenames_mas.append(filename_object)
                        else:
                            write_log_flag = False
                            for i in range(len(self.all_logs_mas)):
                                if float(new_log[0][0]) < float(self.all_logs_mas[i][0][0]):
                                    self.all_logs_mas.insert(i, new_log)
                                    self.filenames_mas.insert(i, filename_object)
                                    write_log_flag = True
                                    break
                            if not write_log_flag:
                                self.all_logs_mas.append(new_log)
                                self.filenames_mas.append(filename_object)

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
            self.table_long_for_filenames.setItem(i, 2, QTableWidgetItem(time.ctime(self.filenames_mas[i].min_date) + " - " + time.ctime(self.filenames_mas[i].max_date)))

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