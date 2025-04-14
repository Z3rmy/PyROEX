# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 19:05:04 2025

@author: 22185
"""
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QTabWidget, QWidget, QHBoxLayout, QPushButton, QTextEdit  
                             , QApplication,QFileDialog,QMessageBox,QDialog,QSizePolicy,QVBoxLayout,QLabel,QComboBox,
                             QGridLayout,QFormLayout,QLineEdit,QRadioButton, QButtonGroup,QCheckBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect,Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import read_A,read_I
from function import *
from functools import partial
import numpy as np
import os,webbrowser,sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.selected_options = {}  # 初始为空字典，动态生成选项卡内容时填充
        # self.tabs = None  # 初始化选项卡
        # self.A_or_I = 'none'
    def initUI(self):
        # 窗口设置
        self.setWindowTitle('PyROEX (National Space Science Center, CAS)')
        self.resize(800, 1000)

        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 设置中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 顶部控制栏
        top_layout = QHBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setFixedHeight(50)
        self.btn_browse = QPushButton("Input")
        self.btn_browse.setFixedHeight(50)

        top_layout.addWidget(self.textEdit)
        top_layout.addWidget(self.btn_browse)
        main_layout.addLayout(top_layout)

        # 选项卡系统
        self.tabs = QTabWidget()

        # 初始化选项卡
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        # self.tab5 = QWidget()

        self.tabs.addTab(self.tab1, "Data Monitoring")
        self.tabs.addTab(self.tab2, "Quality Checking")
        self.tabs.addTab(self.tab3, "File Editing")
        # self.tabs.addTab(self.tab4, "Figure Edit")
        self.tabs.addTab(self.tab4, "Help")
        
        # 初始化各选项卡内容
        self.init_tab1(self.tab1)
        self.init_tab2(self.tab2)
        self.init_tab3()
        

        main_layout.addWidget(self.tabs)
        self.btn_browse.clicked.connect(self.showDialog)
        
        for tab in [self.tab1, self.tab2, self.tab3, self.tab4]:
            layout = QVBoxLayout()
            tab.setLayout(layout)

        # 连接currentChanged信号到槽函数
        self.tabs.currentChanged.connect(self.tab_changed)
        
    def tab_changed(self, index):
        # 如果切换到Help选项卡（索引为3）
        if index == 3:
            self.open_help_documentation()

    def open_help_documentation(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        doc_path = os.path.join(parent_dir, "doc", "User Manual.pdf")  # 假设说明文件是HTML格式

        if os.path.exists(doc_path):
            # 使用默认浏览器打开说明文件
            webbrowser.open(doc_path)
        else:
            # 如果文件不存在，可以显示一个错误消息
            self.showWarning('Help documentation file not found!')
    
    def init_tab1(self, tab):
        main_layout = QVBoxLayout(tab)
        
        # 控制面板
        control_panel = QWidget()
        control_layout = QGridLayout(control_panel)  # 使用 QGridLayout
        
        file_type_label = QLabel("File Type")
        file_type_label.setAlignment(Qt.AlignCenter)  # 可以居中对齐标签文本
        
        # 创建 Combobox 并添加三个选项
        self.combo_box = QComboBox()
        self.combo_box.addItem(" ")
        self.combo_box.addItem("Atm")
        self.combo_box.addItem("Ion")
        self.combo_box.setMaximumWidth(150)  # 设置 Combobox 宽度
        
        
        SNR_LIM_CLO_TAB1 = QLabel("CLO SNR LIM ")
        SNR_LIM_CLO_TAB1.setAlignment(Qt.AlignCenter)  # 标签居中对齐
        self.SNR_LIM_CLO_TAB1 = QLineEdit()
        self.SNR_LIM_CLO_TAB1.setMaximumWidth(100)  # 缩短输入框的宽度
        self.SNR_LIM_CLO_TAB1.setText("40")
        
        
        SNR_LIM_OPE_TAB1 = QLabel("OPE SNR LIM")
        SNR_LIM_OPE_TAB1.setAlignment(Qt.AlignCenter)  # 标签居中对齐
        self.SNR_LIM_OPE_TAB1 = QLineEdit()
        self.SNR_LIM_OPE_TAB1.setMaximumWidth(100)  # 缩短输入框的宽度
        self.SNR_LIM_OPE_TAB1.setText("0.1")
        

        # 将标签和 Combobox 添加到布局
        control_layout.addWidget(file_type_label, 0, 0)  # 将文件类型标签放在第一行
        control_layout.addWidget(self.combo_box, 1, 0)  # 将 Combobox 放在第二行
        
        control_layout.addWidget(SNR_LIM_CLO_TAB1, 0, 3)  # 将 SNR 标签放在第一行第二列
        control_layout.addWidget(self.SNR_LIM_CLO_TAB1, 1, 3)  # 将输入框放在第二行第二列
        
        control_layout.addWidget(SNR_LIM_OPE_TAB1, 0, 6)  # 将 SNR 标签放在第一行第二列
        control_layout.addWidget(self.SNR_LIM_OPE_TAB1, 1, 6)  # 将输入框放在第二行第二列
        # 设置布局项居中对齐
        control_layout.setAlignment(Qt.AlignCenter)  # 设置整个布局居中对齐
        
        main_layout.addWidget(control_panel)
        
        

        '''
        
        =============
        '''
        # 创建 TabWidget
        self.tab_widget = QTabWidget()    
        self.combo_box.currentIndexChanged.connect(self.update_tab1)
        '''
        =============
        '''
        
        # 创建一个容器来放置动态生成的 Checkbox
        self.checkbox_container = QWidget()
        self.checkbox_layout = QHBoxLayout(self.checkbox_container)  # 使用 QVBoxLayout
        self.checkbox_layout.setSpacing(0)
        self.checkbox_layout.setContentsMargins(0, 0, 0, 0)
        
        # 将 Checkbox 容器添加到主布局
        main_layout.addWidget(self.checkbox_container)

        # 创建一个容器来放置动态生成的选项卡
        self.figure_container = QWidget()
        self.figure_layout = QVBoxLayout(self.figure_container)  # 使用 QVBoxLayout
        self.figure_layout.setSpacing(10)
        self.figure_layout.setContentsMargins(5, 5, 5, 5)
        

        # 将选项卡容器添加到主布局
        main_layout.addWidget(self.figure_container)
        
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        tab.figure = plt.figure()
        plt.close(tab.figure)
        tab.canvas = FigureCanvas(tab.figure)
        tab.toolbar = NavigationToolbar(tab.canvas, self)
        # plt.close(tab.figure)
            
        main_layout.addWidget(tab.toolbar)
        main_layout.addWidget(tab.canvas)

        
        # 确保控件的最小尺寸设置
        self.checkbox_container.setMaximumHeight(150)
        # self.tab_widget.setMaximumHeight(300)
        control_panel.setMaximumHeight(200)  # 控制面板的最小高度
        tab.canvas.setMinimumWidth(400)  # 绘图区域的最小宽度
        tab.canvas.setMinimumHeight(400)  # 绘图区域的最小高度

        self.update_tab1()

    def update_tab1(self):
        # 获取当前选择的 figure number
        num_tabs = 2
        # self.tab1.figure.clear()

        figsize = (12, 8)  # 宽度 10，高度 6
        aspect_ratio = 'auto'

        # 动态调整 figure 大小
        self.tab1.figure.set_size_inches(*figsize)
    
        # 创建子
        self.tab1.ax = self.tab1.figure.add_subplot(1, 1, 1)
        self.tab1.ax.set_aspect('auto')  # 设置宽高比
        self.tab1.ax.plot([], [])  # 绘制空白图
        
        # self.tab1.figure = 
        self.tab1.canvas.draw()
        # 清空现有的选项卡
        self.tab_widget.clear()
        
        current_text = self.combo_box.currentText()
        
        self.A_or_I = jug_A_or_I(self.textEdit.toPlainText())

        '''
        还应该设置一个clear选项，清空当前所有的
        '''
        
        if self.A_or_I == 'A' and current_text == 'Atm':
            # SNR = float(self.SNR_LIM_CLO_TAB1.text())
            # self.target_file.read_A_file(self.textEdit.toPlainText(),SNR)
            try:
                self.tab1.checkbox_labels_OCC_CLO = self.target_file.OCC_CLO
                self.tab1.checkbox_labels_REF_CLO = self.target_file.REF_CLO
                self.tab1.checkbox_labels_OCC_OPE = self.target_file.OCC_OPE
                self.tab1.checkbox_labels_REF_OPE = self.target_file.REF_OPE
                
                # 定义各行列内容
                row_labels = [
                    f"CLO_{self.target_file.sat1} :",
                    f"CLO_{self.target_file.sat2} :",
                    f"OPE_{self.target_file.sat1} :",
                    f"OPE_{self.target_file.sat2} :"
                ]
                groups = [
                    self.tab1.checkbox_labels_OCC_CLO,
                    self.tab1.checkbox_labels_REF_CLO,
                    self.tab1.checkbox_labels_OCC_OPE,
                    self.tab1.checkbox_labels_REF_OPE
                ]
                # groups = [self.target_file.OCC_CLO_MW , self.target_file.REF_CLO_MW ,self.target_file.OCC_OPE_MW ,self.target_file.REF_OPE_MW]
                tab_names = ["选项卡1", "选项卡2"]
                for i in range(num_tabs):
                    
                    tab_content = QWidget()
                    tab_layout = QGridLayout(tab_content)
                    checkboxes = []  # 用于存储当前选项卡的所有复选框
                    tab_layout.setSpacing(5)
                    tab_layout.setContentsMargins(0, 0, 0, 0)
                    
                    # 填充复选框

                    for row in range(len(groups)):
                        row_label = QLabel(row_labels[row])
                        row_label.setFixedWidth(100)
                        tab_layout.addWidget(row_label, row, 0)
                        
                        self.tab1.selected_options = {
                            f"选项卡{i+1}": {f"行{row+1}": [] for row in range(len(groups))}
                            for i in range(num_tabs)
                        }
                        self.tab1.checkbox_groups = {}
                        # print(self.selected_options)

                        # 添加空白列作为间距
                        tab_layout.addWidget(QLabel(), row, 1)
                        
                        for col, label in enumerate(groups[row]):
                            # print(str(label))
                            checkbox = QCheckBox(label)
                            checkbox.stateChanged.connect(partial(self.update_selected_options, tab_name=f"选项卡{i+1}", row=row, option_label=label))
                            tab_layout.addWidget(checkbox, row, col + 2)                
                            checkboxes.append(checkbox)
                    clear_button = QPushButton("CLEAR")
                    clear_button.clicked.connect(partial(self.clear_selected, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    clear_button = QPushButton("PLOT")
                    clear_button.clicked.connect(partial(self.PLOT_tab1_Atm, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    # 保存当前选项卡的复选框
                    self.tab1.checkbox_groups[tab_names[i]] = checkboxes
                    # 设置列宽
                    tab_layout.setColumnStretch(0, 0)
                    tab_layout.setColumnStretch(1, 0)
                    tab_layout.setColumnMinimumWidth(0, 100)
                    tab_layout.setColumnMinimumWidth(1, 10)
                
                # print(self.checked_OCC_CLO_OD , self.checked_REF_OPE_OD)
                # 将选项卡内容添加到选项卡小部件
                    if i==0:
                        self.tab_widget.addTab(tab_content, f"Original Data")
                    else:
                        self.tab_widget.addTab(tab_content, f"Data Changing Rate")
            except Exception as e:
                self.showWarning(f"Error generating checkboxes for 'Atm': {e}")
                
        elif self.A_or_I == "I" and current_text == "Ion":
            # SNR = float(self.SNR_LIM_CLO_TAB1.text())
            # self.target_file.read_I_file(self.textEdit.toPlainText(),SNR)
            # 处理 Ion 类型的逻辑
            try:
                self.tab1.checkbox_labels_OCC = self.target_file.OCC
                
                row_labels = [
                    f"{self.target_file.sat:} :"
                ]
                groups = [
                    self.tab1.checkbox_labels_OCC
                ]
                checkboxes = []
                # 创建每个选项卡及其内容
                tab_names = ["选项卡1", "选项卡2"]
                for i in range(num_tabs):
                    tab_content = QWidget()
                    tab_layout = QGridLayout(tab_content)
                    tab_layout.setSpacing(5)
                    tab_layout.setContentsMargins(0, 0, 0, 0)
                    self.tab1.checkbox_groups = {}
                    row_labels = [f"{self.target_file.sat} :"]
                    

                    for row in range(len(groups)):
                        row_label = QLabel(row_labels[row])
                        row_label.setFixedWidth(100)
                        tab_layout.addWidget(row_label, row, 0)
                        
                        self.tab1.selected_options = {
                            f"选项卡{i+1}": {f"行{row+1}": [] for row in range(len(groups))}
                            for i in range(num_tabs)
                        }
                        self.tab1.checkbox_groups = {}
                        # print(self.selected_options)

                        # 添加空白列作为间距
                        tab_layout.addWidget(QLabel(), row, 1)
                        
                        for col, label in enumerate(groups[row]):
                            # print(str(label))
                            checkbox = QCheckBox(label)
                            checkbox.stateChanged.connect(partial(self.update_selected_options, tab_name=f"选项卡{i+1}", row=row, option_label=label))
                            tab_layout.addWidget(checkbox, row, col + 2)                
                            checkboxes.append(checkbox)
                    clear_button = QPushButton("CLEAR")
                    clear_button.clicked.connect(partial(self.clear_selected, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    clear_button = QPushButton("PLOT")
                    clear_button.clicked.connect(partial(self.PLOT_tab1_Ion, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    if i==0:
                        self.tab_widget.addTab(tab_content, f"Original Data")
                    else:
                        self.tab_widget.addTab(tab_content, f"Data Changing Rate")
            except Exception as e:
                self.showWarning(f"Error generating checkboxes for 'Ion': {e}")
                
        # print(f"Checkbox '{sender.text()}' state changed to: {state}")
    def PLOT_tab1_Atm(self,tab_name, checkboxes):
        self.tab1.figure.clf()
        self.tab1.ax = self.tab1.figure.add_subplot(111)  # 添加一个新的Axes对象
        size = 5
        SNR_CLO = float(self.SNR_LIM_CLO_TAB1.text())
        SNR_OPE = float(self.SNR_LIM_OPE_TAB1.text())
        self.target_file.SNR_filter(SNR_CLO,SNR_OPE)
        if tab_name == '选项卡1':
            # print(self.checkbox_row)
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.CLO_time_list,self.target_file.OCC_CLO_filter[k],label = f"CLO_{self.target_file.sat1} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行2']:
                to_plot_list = self.tab1.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.CLO_time_list,self.target_file.REF_CLO[k] ,label = f"CLO_{self.target_file.sat2} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行3']:
                to_plot_list = self.tab1.selected_options[tab_name]['行3']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.OPE_time_list,self.target_file.OCC_OPE_filter[k]  ,label = f"OPE_{self.target_file.sat1} {k}",s=size)
            if self.tab1.selected_options[tab_name]['行4']:
                to_plot_list = self.tab1.selected_options[tab_name]['行4']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.OPE_time_list,self.target_file.REF_OPE[k]  ,label = f"OPE_{self.target_file.sat2} {k}",s=size)    
            

        else:
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.CLO_time_list[:-1],self.target_file.dOCC_CLO[k],label = f"CLO_{self.target_file.sat1} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行2']:
                to_plot_list = self.tab1.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.CLO_time_list[:-1],self.target_file.dREF_CLO[k] ,label = f"CLO_{self.target_file.sat2} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行3']:
                to_plot_list = self.tab1.selected_options[tab_name]['行3']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.OPE_time_list[:-1],self.target_file.dOCC_OPE[k]  ,label = f"OPE_{self.target_file.sat1} {k}",s=size)
            if self.tab1.selected_options[tab_name]['行4']:
                to_plot_list = self.tab1.selected_options[tab_name]['行4']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.OPE_time_list[:-1],self.target_file.dREF_OPE[k]  ,label = f"OPE_{self.target_file.sat2} {k}",s=size)    
        self.tab1.ax.set_title(f'{self.target_file.label_kb}')
        self.tab1.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)')  
        self.tab1.ax.grid(True,  which='both', linestyle='--', alpha=0.7, color='#757575')
        self.tab1.ax.legend()
        self.tab1.canvas.draw()
        
        
    def PLOT_tab1_Ion(self,tab_name, checkboxes):
        self.tab1.figure.clf()
        self.tab1.ax = self.tab1.figure.add_subplot(111)  # 添加一个新的Axes对象
        size = 5
        SRN = float(self.SNR_LIM_CLO_TAB1.text())
        self.target_file.SNR_filter(SRN)
        # print(self.checkbox_row)
        if tab_name == '选项卡1':
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.OCC_time_list,self.target_file.OCC_filter[k],label = f"{self.target_file.sat} {k}",s=size)
         
        else:
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    self.tab1.ax.scatter(self.target_file.OCC_time_list[:-1],self.target_file.dOCC[k],label = f"{self.target_file.sat} {k}",s=size)
        self.tab1.ax.set_title(f'{self.target_file.label_kb}') 
        self.tab1.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)')
        self.tab1.ax.grid(True,  which='both', linestyle='--', alpha=0.7, color='#757575')
        self.tab1.ax.legend()
        self.tab1.canvas.draw()
        
        
    def clear_selected(self, tab_name, checkboxes):
        # 清空当前选项卡的选中状态
        # self.tab1.figure.clf()
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        
        # 清空 selected_options 中对应的记录
        if hasattr(self, 'selected_options'):
            for row in self.tab1.selected_options.get(tab_name, {}):
                self.tab1.selected_options[tab_name][row].clear()


    def update_selected_options(self, state, tab_name, row, option_label):
        # 根据状态更新对应的列表
        if state == Qt.Checked:
            if option_label not in self.tab1.selected_options[tab_name][f"行{row+1}"]:
                self.tab1.selected_options[tab_name][f"行{row+1}"].append(option_label)
        else:
            if option_label in self.tab1.selected_options[tab_name][f"行{row+1}"]:
                self.tab1.selected_options[tab_name][f"行{row+1}"].remove(option_label)
        
        # 输出记录的信息
        # print(self.tab1.selected_options)
        # print(f"{tab_name} - 行{row+1} 选中的选项: {self.selected_options[tab_name][f'行{row+1}']}")

    def init_tab2(self, tab):
        main_layout = QVBoxLayout(tab)
        
        # 控制面板
        control_panel = QWidget()
        control_layout = QGridLayout(control_panel)  # 使用 QGridLayout
        
        file_type_label = QLabel("File Type")
        file_type_label.setAlignment(Qt.AlignCenter)  # 标签文本居中
        
        # 创建 Combobox 并添加三个选项
        self.combo_box_tab2 = QComboBox()
        self.combo_box_tab2.addItem(" ")
        self.combo_box_tab2.addItem("Atm")
        self.combo_box_tab2.addItem("Ion")
        self.combo_box_tab2.setMaximumWidth(150)  # 设置 Combobox 宽度
        
        # 将标签和 Combobox 添加到布局
        control_layout.addWidget(file_type_label, 0, 0)  # 将标签放在第一行
        control_layout.addWidget(self.combo_box_tab2, 1, 0)  # 将 Combobox 放在第二行
             
        SNR_LIM_CLO_TAB2 = QLabel("CLO SNR LIM ")
        SNR_LIM_CLO_TAB2.setAlignment(Qt.AlignCenter)  # 标签居中对齐
        self.SNR_LIM_CLO_TAB2 = QLineEdit()
        self.SNR_LIM_CLO_TAB2.setMaximumWidth(100)  # 缩短输入框的宽度
        self.SNR_LIM_CLO_TAB2.setText("40")
        
        
        SNR_LIM_OPE_TAB2 = QLabel("OPE SNR LIM")
        SNR_LIM_OPE_TAB2.setAlignment(Qt.AlignCenter)  # 标签居中对齐
        self.SNR_LIM_OPE_TAB2 = QLineEdit()
        self.SNR_LIM_OPE_TAB2.setMaximumWidth(100)  # 缩短输入框的宽度
        self.SNR_LIM_OPE_TAB2.setText("0.1")


        control_layout.addWidget(SNR_LIM_CLO_TAB2, 0, 1)  # 将 SNR 标签放在第一行第二列
        control_layout.addWidget(self.SNR_LIM_CLO_TAB2, 1, 1)  # 将输入框放在第二行第二列
        
        control_layout.addWidget(SNR_LIM_OPE_TAB2, 0, 2)  # 将 SNR 标签放在第一行第二列
        control_layout.addWidget(self.SNR_LIM_OPE_TAB2, 1, 2)  # 将输入框放在第二行第二列
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        DI_button = QPushButton("Data Integrity")
        DI_button.setFixedSize(200, 50)  # 设置按钮大小
        DI_button.clicked.connect(self.DI)
        
        # 将按钮添加到按钮布局中
        button_layout.addWidget(DI_button)

        # 将按钮布局添加到控制面板的主布局中(y , x)
        # control_layout.addWidget(comb_type_label, 0, 1)  # 将标签放在第一行
        # control_layout.addWidget(self.combo_box_tab2, 1, 1)  # 将 Combobox 放在第二行
        control_layout.addLayout(button_layout, 1, 3)  # 将按钮布局放在第三行
        
        # 将控制面板添加到主布局中
        main_layout.addWidget(control_panel)
        
        # 创建 TabWidget 并添加到主布局
        self.tab_widget_tab2 = QTabWidget()
        main_layout.addWidget(self.tab_widget_tab2)
        
        # 连接 ComboBox 信号到更新选项卡的槽函数
        self.combo_box_tab2.currentIndexChanged.connect(self.update_tabs2)
        
        # 初始化其他控件
        self.checkbox_container_tab2 = QWidget()
        self.checkbox_layout_tab2 = QVBoxLayout(self.checkbox_container_tab2)
        main_layout.addWidget(self.checkbox_container_tab2)
        
        self.figure_container_tab2 = QWidget()
        self.figure_layout_tab2 = QVBoxLayout(self.figure_container_tab2)
        main_layout.addWidget(self.figure_container_tab2)
        
        # Matplotlib 图形
        tab.figure = plt.figure()
        plt.close(tab.figure)
        tab.canvas = FigureCanvas(tab.figure)
        tab.toolbar = NavigationToolbar(tab.canvas, self)
        
        main_layout.addWidget(tab.toolbar)
        main_layout.addWidget(tab.canvas)
        
        # 设置控件大小
        control_panel.setMaximumHeight(200)
        tab.canvas.setMinimumSize(400, 400)
        tab.canvas.setMinimumWidth(400)  # 绘图区域的最小宽度
        tab.canvas.setMinimumHeight(600)  # 绘图区域的最小高度
        # 初始化选项卡
        self.update_tabs2()
        

    def update_tabs2(self):
        num_tabs = 3
        figsize = (12, 8)  # 宽度 10，高度 6
        aspect_ratio = 'auto'
        self.tab2.figure.clf()
        # 动态调整 figure 大小
        self.tab2.figure.set_size_inches(*figsize)
        plt.close(self.tab2.figure)
        self.tab2.ax = self.tab2.figure.add_subplot(1, 1, 1)
        self.tab2.ax.set_aspect(aspect_ratio)
        self.tab2.ax.plot([], [])
        self.tab2.canvas.draw()
        
        # 清空现有的选项卡
        self.tab_widget_tab2.clear()
        
        current_text = self.combo_box_tab2.currentText()
        self.A_or_I = jug_A_or_I(self.textEdit.toPlainText())
        
        
        if self.A_or_I == 'A' and current_text == 'Atm':
            self.target_file.SNR_filter()
            try:
                row_labels = [
                    f"CLO_{self.target_file.sat1}:",
                    f"CLO_{self.target_file.sat2}:",
                    f"OPE_{self.target_file.sat1}:",
                    f"OPE_{self.target_file.sat2}:"
                ]
                groups = [
                    [self.target_file.OCC_CLO_MW, self.target_file.REF_CLO_MW, self.target_file.OCC_OPE_MW, self.target_file.REF_OPE_MW],
                    [self.target_file.OCC_CLO_GF, self.target_file.REF_CLO_GF, self.target_file.OCC_OPE_GF, self.target_file.REF_OPE_GF],
                    [self.target_file.OCC_CLO_IF, self.target_file.REF_CLO_IF, self.target_file.OCC_OPE_IF, self.target_file.REF_OPE_IF],
                ]
                
                tab_names = ["MW", "GF", "IF"]
                for i in range(num_tabs):
                    tab_content = QWidget()
                    tab_layout = QGridLayout(tab_content)
                    checkboxes = []
                    # 填充复选框
                    for row in range(len(groups[i])):
                        row_label = QLabel(row_labels[row])
                        row_label.setFixedWidth(100)
                        tab_layout.addWidget(row_label, row, 0)
                        
                        # 添加空白列
                        tab_layout.addWidget(QLabel(), row, 1)
                        self.tab2.selected_options = {
                            f"{tab_names[i]}": {f"行{row+1}": [] for row in range(len(groups[i]))}
                            for i in range(num_tabs)
                        }
                        self.tab2.checkbox_groups = {}
                        tab_layout.addWidget(QLabel(), row, 1)
                        for col, label in enumerate(groups[i][row]):
                            checkbox = QCheckBox(label)
                            checkbox.stateChanged.connect(partial(self.tab2_update_selected_options, tab_name=tab_names[i], row=row, option_label=label))
                            tab_layout.addWidget(checkbox, row, col + 2)
                            checkboxes.append(checkbox)
                    # 添加按钮
                    clear_button = QPushButton("CLEAR")
                    clear_button.clicked.connect(partial(self.tab2_clear_selected, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button, len(groups[i]), 0, 1, 3)
                    
                    plot_button = QPushButton("PLOT")
                    plot_button.clicked.connect(partial(self.PLOT_tab2_Atm, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(plot_button, len(groups[i]) + 1, 0, 1, 3)
                    
                    # 添加选项卡到 self.tab_widget_tab2
                    self.tab_widget_tab2.addTab(tab_content, tab_names[i])
            
            except Exception as e:
                self.showWarning(f"{e}")
                
        if self.A_or_I == 'I' and current_text == 'Ion':
            self.target_file.SNR_filter()
            try:
                row_labels = [
                    f"{self.target_file.sat}:",
                ]
                groups = [
                    [self.target_file.OCC_MW], 
                    [self.target_file.OCC_GF], 
                    [self.target_file.OCC_IF]

                ]
                
                tab_names = ["MW", "GF", "IF"]
                for i in range(num_tabs):
                    tab_content = QWidget()
                    tab_layout = QGridLayout(tab_content)
                    checkboxes = []
                    # 填充复选框
                    for row in range(len(groups[i])):
                        row_label = QLabel(row_labels[row])
                        row_label.setFixedWidth(100)
                        tab_layout.addWidget(row_label, row, 0)
                        
                        # 添加空白列
                        tab_layout.addWidget(QLabel(), row, 1)
                        self.tab2.selected_options = {
                            f"{tab_names[i]}": {f"行{row+1}": [] for row in range(len(groups[i]))}
                            for i in range(num_tabs)
                        }
                        self.tab2.checkbox_groups = {}
                        tab_layout.addWidget(QLabel(), row, 1)
                        for col, label in enumerate(groups[i][row]):
                            checkbox = QCheckBox(label)
                            checkbox.stateChanged.connect(partial(self.tab2_update_selected_options, tab_name=tab_names[i], row=row, option_label=label))
                            tab_layout.addWidget(checkbox, row, col + 2)
                            checkboxes.append(checkbox)
                    # 添加按钮
                    clear_button = QPushButton("CLEAR")
                    clear_button.clicked.connect(partial(self.tab2_clear_selected, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button, len(groups[i]), 0, 1, 3)
                    
                    plot_button = QPushButton("PLOT")
                    plot_button.clicked.connect(partial(self.PLOT_tab2_Ion, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(plot_button, len(groups[i]) + 1, 0, 1, 3)
                    
                    # 添加选项卡到 self.tab_widget_tab2
                    self.tab_widget_tab2.addTab(tab_content, tab_names[i])
            
            except Exception as e:
                self.showWarning(f"{e}")
    def tab2_update_selected_options(self, state, tab_name, row, option_label):
        # 根据状态更新对应的列表
        if state == Qt.Checked:
            if option_label not in self.tab2.selected_options[tab_name][f"行{row+1}"]:
                self.tab2.selected_options[tab_name][f"行{row+1}"].append(option_label)
        else:
            if option_label in self.tab2.selected_options[tab_name][f"行{row+1}"]:
                self.tab2.selected_options[tab_name][f"行{row+1}"].remove(option_label)
        
    def tab2_clear_selected(self, tab_name, checkboxes):
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        
        # 清空 selected_options 中对应的记录
        if hasattr(self, 'selected_options'):
            for row in self.tab2.selected_options.get(tab_name, {}):
                self.tab2.selected_options[tab_name][row].clear()

        
    
    def PLOT_tab2_Atm(self,tab_name, checkboxes):
        self.tab2.figure.clf()
        self.tab2.ax = self.tab2.figure.add_subplot(111)  # 添加一个新的Axes对象
        size = 5
        SRN_CLO = float(self.SNR_LIM_CLO_TAB2.text())
        SRN_OPE = float(self.SNR_LIM_OPE_TAB2.text())
        self.target_file.SNR_filter(SRN_CLO,SRN_OPE)
        
        if tab_name == 'MW':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_CLO_MW[k])
                    self.tab2.ax.scatter(self.target_file.CLO_time_list[:l],self.target_file.OCC_CLO_MW[k],label = f"CLO_{self.target_file.sat1} MW {k}",s=size)
                    
            if self.tab2.selected_options[tab_name]['行2']:
                to_plot_list = self.tab2.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    l = len(self.target_file.REF_CLO_MW[k])
                    self.tab2.ax.scatter(self.target_file.CLO_time_list[:l],self.target_file.REF_CLO_MW[k] ,label = f"CLO_{self.target_file.sat2} MW {k}",s=size)
                    
            if self.tab2.selected_options[tab_name]['行3']:
                to_plot_list = self.tab2.selected_options[tab_name]['行3']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_OPE_MW[k])
                    self.tab2.ax.scatter(self.target_file.OPE_time_list[:l],self.target_file.OCC_OPE_MW[k]  ,label = f"OPE_{self.target_file.sat1} MW {k}",s=size)
            if self.tab2.selected_options[tab_name]['行4']:
                to_plot_list = self.tab2.selected_options[tab_name]['行4']
                for k in to_plot_list:
                    l = len(self.target_file.REF_OPE_MW[k])
                    self.tab2.ax.scatter(self.target_file.OPE_time_list[:l],self.target_file.REF_OPE_MW[k]  ,label = f"OPE_{self.target_file.sat2} MW {k}",s=size)    
            self.tab2.ax.set_ylabel('Cycle')
            
        if tab_name == 'GF':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_CLO_GF[k])
                    self.tab2.ax.scatter(self.target_file.CLO_time_list[:l],self.target_file.OCC_CLO_GF[k],label = f"CLO_{self.target_file.sat1} GF {k}",s=size)
                    
            if self.tab2.selected_options[tab_name]['行2']:
                to_plot_list = self.tab2.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    l = len(self.target_file.REF_CLO_GF[k])
                    self.tab2.ax.scatter(self.target_file.CLO_time_list[:l],self.target_file.REF_CLO_GF[k] ,label = f"CLO_{self.target_file.sat2} GF {k}",s=size)
                    
            if self.tab2.selected_options[tab_name]['行3']:
                to_plot_list = self.tab2.selected_options[tab_name]['行3']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_OPE_GF[k])
                    self.tab2.ax.scatter(self.target_file.OPE_time_list[:l],self.target_file.OCC_OPE_GF[k]  ,label = f"OPE_{self.target_file.sat1} GF {k}",s=size)
            if self.tab2.selected_options[tab_name]['行4']:
                to_plot_list = self.tab2.selected_options[tab_name]['行4']
                for k in to_plot_list:
                    l = len(self.target_file.REF_OPE_GF[k])
                    self.tab2.ax.scatter(self.target_file.OPE_time_list[:l],self.target_file.REF_OPE_GF[k]  ,label = f"OPE_{self.target_file.sat2} GF {k}",s=size)    
            self.tab2.ax.set_ylabel('m')   
            
        if tab_name == 'IF':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_CLO_IF[k])
                    self.tab2.ax.scatter(self.target_file.CLO_time_list[:l],self.target_file.OCC_CLO_IF[k],label = f"CLO_{self.target_file.sat1} IF {k}",s=size)
                    
            if self.tab2.selected_options[tab_name]['行2']:
                to_plot_list = self.tab2.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    l = len(self.target_file.REF_CLO_IF[k])
                    self.tab2.ax.scatter(self.target_file.CLO_time_list[:l],self.target_file.REF_CLO_IF[k] ,label = f"CLO_{self.target_file.sat2} IF {k}",s=size)
                    
            if self.tab2.selected_options[tab_name]['行3']:
                to_plot_list = self.tab2.selected_options[tab_name]['行3']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_OPE_IF[k])
                    self.tab2.ax.scatter(self.target_file.OPE_time_list[:l],self.target_file.OCC_OPE_IF[k]  ,label = f"OPE_{self.target_file.sat1} IF {k}",s=size)
            if self.tab2.selected_options[tab_name]['行4']:
                to_plot_list = self.tab2.selected_options[tab_name]['行4']
                for k in to_plot_list:
                    l = len(self.target_file.REF_OPE_IF[k])
                    self.tab2.ax.scatter(self.target_file.OPE_time_list[:l],self.target_file.REF_OPE_IF[k]  ,label = f"OPE_{self.target_file.sat2} IF {k}",s=size)    
            self.tab2.ax.set_ylabel('m') 
        self.tab2.ax.set_title(f'{self.target_file.label_kb}')
        self.tab2.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)')  
        self.tab2.ax.grid(True,  which='both', linestyle='--', alpha=0.7, color='#757575')
        self.tab2.ax.legend()
        self.tab2.canvas.draw()            
        pass
    
    def PLOT_tab2_Ion(self,tab_name, checkboxes):
        self.tab2.figure.clf()
        self.tab2.ax = self.tab2.figure.add_subplot(111)  # 添加一个新的Axes对象
        size = 5
        SRN = float(self.SNR_LIM_CLO_TAB2.text())
        self.target_file.SNR_filter(SRN)
        if tab_name == 'MW':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_MW[k])
                    self.tab2.ax.scatter(self.target_file.OCC_time_list[:l],self.target_file.OCC_MW[k],label = f"{self.target_file.sat} MW {k}",s=size)
            self.tab2.ax.set_ylabel('Cycle')
            
        if tab_name == 'GF':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_GF[k])
                    self.tab2.ax.scatter(self.target_file.OCC_time_list[:l],self.target_file.OCC_GF[k],label = f"{self.target_file.sat} GF {k}",s=size)
            self.tab2.ax.set_ylabel('m')      
            
        if tab_name == 'IF':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_IF[k])
                    self.tab2.ax.scatter(self.target_file.OCC_time_list[:l],self.target_file.OCC_IF[k],label = f"{self.target_file.sat} IF {k}",s=size)
            self.tab2.ax.set_ylabel('m')
            
        self.tab1.ax.set_title(f'{self.target_file.label_kb}')
        self.tab2.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)') 
        self.tab2.ax.grid(True,  which='both', linestyle='--', alpha=0.7, color='#757575')
        self.tab2.ax.legend()
        self.tab2.canvas.draw()           
    
    def DI(self):
        self.tab2.figure.clf()
        self.tab2.ax = self.tab2.figure.add_subplot(111)  # 添加一个新的Axes对象        
        SRN_CLO = float(self.SNR_LIM_CLO_TAB2.text())
        SRN_OPE = float(self.SNR_LIM_OPE_TAB2.text())
        self.target_file.SNR_filter(SRN_CLO,SRN_OPE)
        self.target_file.DI_CHECK()
        # size = 3
        if self.A_or_I == 'A':
            
            A = self.target_file.data_integrity_OCC_CLO*100
            B = self.target_file.data_integrity_REF_CLO*100
            C = self.target_file.data_integrity_OCC_OPE*100
            D = self.target_file.data_integrity_REF_OPE*100
            
            # 设置柱状图的位置
            bar_width = 0.35
            # index = np.arange(2)  # 只有两组（AB 和 CD）
            x_bar1 = [-0.175,  0.175] ; x_bar2=[0.825,1.175]
            bar1 = self.tab2.ax.bar(x_bar1, [A, B], bar_width, color='#E57373', label='CLO', edgecolor='black', linewidth=1.2)
            
            # 绘制CD组的柱状图（优雅的蓝色渐变）
            bar2 = self.tab2.ax.bar(x_bar2, [C, D], bar_width, color='#64B5F6', label='OPE', edgecolor='black', linewidth=1.2)
            for i, v in enumerate([A, B]):
                self.tab2.ax.text(x_bar1[i] , v + 2, f'{v:.2f}%', ha='center', va='bottom', color='#B71C1C', fontsize=12, fontweight='bold')
            
            for i, v in enumerate([C, D]):
                self.tab2.ax.text(x_bar2[i], v + 2, f'{v:.2f}%', ha='center', va='bottom', color='#0D47A1', fontsize=12, fontweight='bold')
            
            self.tab2.ax.set_ylabel('Data Integrity (%)', fontsize=14, fontweight='bold', color='#424242')

            # 优化刻度标签的字体和颜色
            self.tab2.ax.set_xticks([x_bar1[0] , x_bar1[1],x_bar2[0],x_bar2[1]])
            self.tab2.ax.set_xticklabels([f'{self.target_file.sat1}',f'{self.target_file.sat2}',f'{self.target_file.sat1}',f'{self.target_file.sat2}'], fontsize=12, fontweight='bold', color='#424242')
            self.tab2.ax.set_yticks(np.arange(0, 105, 10))
            self.tab2.ax.tick_params(axis='both', labelsize=12)
            
            self.tab2.ax.grid(True, axis='y', linestyle='--', alpha=0.7, color='#757575')

            # 添加图例
            self.tab2.ax.legend(fontsize=12, loc='best', frameon=False)

            # 设置背景色
            self.tab2.figure.patch.set_facecolor('#F5F5F5')
            self.tab2.ax.set_facecolor('#FAFAFA')
            self.tab2.canvas.draw()
            
            
            # print(self.target_file.data_integrity_OCC_CLO , self.target_file.data_integrity_REF_CLO,self.target_file.data_integrity_OCC_OPE,self.target_file.data_integrity_REF_OPE)
            # self.tab2.
            
        else:
            # self.target_file.DI_CHECK()
            A = self.target_file.data_integrity_OCC*100
            # A = 
            index = [-0.5 , 0 , 0.5]
            bar_width = 0.35
            bar1 = self.tab2.ax.bar(index, [0 , A , 0], bar_width, color='#E57373', edgecolor='black', linewidth=1.2)
            
            self.tab2.ax.text(index[1], A + 1, f'{A:.2f}%', ha='center', va='bottom', color='#E57373', fontsize=16, fontweight='bold')

            
            self.tab2.ax.set_ylabel('Data Integrity (%)', fontsize=14, fontweight='bold', color='#424242')
            
            self.tab2.ax.set_xticks(index)
            self.tab2.ax.set_xticklabels([f'',f'{self.target_file.sat}',f''], fontsize=12, fontweight='bold', color='#424242')
            self.tab2.ax.set_yticks(np.arange(0, 105, 10))
            self.tab2.ax.tick_params(axis='both', labelsize=12)
            
            
            self.tab2.ax.grid(True, axis='y', linestyle='--', alpha=0.7, color='#757575')
            self.tab2.figure.patch.set_facecolor('#F5F5F5')
            self.tab2.ax.set_facecolor('#FAFAFA')
            self.tab2.canvas.draw()
            # print( A )
            
            
        file_to_write = self.target_file.write_DI()
        Show_file(file_to_write) 
    
    
    def init_tab3(self):
        # 创建一个垂直布局作为选项卡的内容
        tab3_layout = QVBoxLayout()
        tab3_layout.setSpacing(10)  # 设置布局间距

        # 创建表单布局
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)  # 设置表单行间距
        
        # 添加 Atm File 文本
        atm_file_label = QLabel("Atm File ：")
        atm_file_label_layout = QHBoxLayout()
        atm_file_label_layout.addWidget(atm_file_label)
        form_layout.addRow(atm_file_label_layout)  # 将 Atm File 添加到表单布局
        
        # 存储所有 QLineEdit 对象的列表
        self.line_Atm_edits = []


        '''
        创建水平布局用于 Start Time 和 End Time  OPE
        '''
        time_range_CLO_layout = QHBoxLayout()

        # 添加 Start Time 字段
        start_time_CLO_label = QLabel("Start Time:")
        self.start_time_CLO_edit = QLineEdit()
        self.start_time_CLO_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        start_time_CLO_layout = QHBoxLayout()
        start_time_CLO_layout.addWidget(self.start_time_CLO_edit)
        start_time_CLO_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_CLO_layout.addLayout(start_time_CLO_layout)

        # 添加 End Time 字段
        end_time_CLO_label = QLabel("End Time:")
        self.end_time_CLO_edit = QLineEdit()
        self.end_time_CLO_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        end_time_CLO_layout = QHBoxLayout()
        end_time_CLO_layout.addWidget(self.end_time_CLO_edit)
        end_time_CLO_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_CLO_layout.addLayout(end_time_CLO_layout)

        # 将时间范围布局添加到表单布局
        form_layout.addRow("CLO Time Range :", time_range_CLO_layout)


        '''
        创建水平布局用于 Start Time 和 End Time  OPE
        '''
        
        
        '''
        创建水平布局用于 Start Time 和 End Time  CLO
        '''
        time_range_OPE_layout = QHBoxLayout()

        # 添加 Start Time 字段
        start_time_OPE_label = QLabel("Start Time:")
        self.start_time_OPE_edit = QLineEdit()
        self.start_time_OPE_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        start_time_OPE_layout = QHBoxLayout()
        start_time_OPE_layout.addWidget(self.start_time_OPE_edit)
        start_time_OPE_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_OPE_layout.addLayout(start_time_OPE_layout)

        # 添加 End Time 字段
        end_time_OPE_label = QLabel("End Time:")
        self.end_time_OPE_edit = QLineEdit()
        self.end_time_OPE_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        end_time_OPE_layout = QHBoxLayout()
        end_time_OPE_layout.addWidget(self.end_time_OPE_edit)
        end_time_OPE_layout.addWidget(QLabel("DD:HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_OPE_layout.addLayout(end_time_OPE_layout)

        # 将时间范围布局添加到表单布局
        form_layout.addRow("OPE Time Range :", time_range_OPE_layout)


        '''
        创建水平布局用于 Start Time 和 End Time  CLO
        '''
        
        '''
        添加 Output File 字段
        '''
        output_file_Atm_edit_label = QLabel("Output File:")
        self.output_file_Atm_edit = QLineEdit()
        self.output_file_Atm_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        output_file_Atm_edit_layout = QHBoxLayout()
        output_file_Atm_edit_layout.addWidget(self.output_file_Atm_edit)
        output_file_Atm_edit_layout.addWidget(QLabel("Current folder"), alignment=Qt.AlignLeft)
        form_layout.addRow(output_file_Atm_edit_label, output_file_Atm_edit_layout)

        self.line_Atm_edits.append(self.start_time_CLO_edit)
        self.line_Atm_edits.append(self.end_time_CLO_edit)

        
        self.line_Atm_edits.append(self.start_time_OPE_edit)
        self.line_Atm_edits.append(self.end_time_OPE_edit)

        self.line_Atm_edits.append(self.output_file_Atm_edit)

        '''
        添加 Output File 字段
        '''
        # 添加 Execute 和 Clear 按钮
        button_layout = QHBoxLayout()
        execute_button = QPushButton("Execute")
        execute_button.clicked.connect(self.on_execute_Atm_clicked)
        execute_button.setFixedSize(80, 30)  # 设置按钮大小

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.on_clear_Atm_clicked)
        clear_button.setFixedSize(80, 30)  # 设置按钮大小
        button_layout.addWidget(execute_button)
        button_layout.addWidget(clear_button)
        
        form_layout.addRow(button_layout)

        # 添加到主布局
        tab3_layout.addLayout(form_layout)
        
        '''
        ==============================
        Ion
        ==============================
        '''
        self.line_Ion_edits = []
        # 添加 Ion File 文本
        ion_file_label = QLabel("Ion File ：")
        ion_file_label_layout = QHBoxLayout()
        ion_file_label_layout.addWidget(ion_file_label)
        form_layout.addRow(ion_file_label_layout)  # 将 Ion File 添加到表单布局
        
        
        time_range_Ion_layout = QHBoxLayout()

        # 添加 Start Time 字段
        start_time_Ion_label = QLabel("Start Time:")
        self.start_time_Ion_edit = QLineEdit()
        self.start_time_Ion_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        start_time_Ion_layout = QHBoxLayout()
        start_time_Ion_layout.addWidget(self.start_time_Ion_edit)
        start_time_Ion_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_Ion_layout.addLayout(start_time_Ion_layout)

        # 添加 End Time 字段
        end_time_Ion_label = QLabel("End Time:")
        self.end_time_Ion_edit = QLineEdit()
        self.end_time_Ion_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        end_time_Ion_layout = QHBoxLayout()
        end_time_Ion_layout.addWidget(self.end_time_Ion_edit)
        end_time_Ion_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_Ion_layout.addLayout(end_time_Ion_layout)

        # 将时间范围布局添加到表单布局
        form_layout.addRow("Time Range :", time_range_Ion_layout)


        
        
        '''
        添加 Output File 字段
        '''
        output_file_Ion_edit_label = QLabel("Output File:")
        self.output_file_Ion_edit = QLineEdit()
        self.output_file_Ion_edit.setFixedWidth(300)  # 设置文本编辑框宽度

        output_file_Ion_edit_layout = QHBoxLayout()
        output_file_Ion_edit_layout.addWidget(self.output_file_Ion_edit)
        output_file_Ion_edit_layout.addWidget(QLabel("Current folder"), alignment=Qt.AlignLeft)
        form_layout.addRow(output_file_Ion_edit_label, output_file_Ion_edit_layout)
        
        
        self.line_Ion_edits.append(self.start_time_Ion_edit)
        self.line_Ion_edits.append(self.end_time_Ion_edit)    
        self.line_Ion_edits.append(self.output_file_Ion_edit)
        
        # 添加 Execute 和 Clear 按钮
        button_layout = QHBoxLayout()
        execute_Ion_button = QPushButton("Execute")
        execute_Ion_button.clicked.connect(self.on_execute_Ion_clicked)
        execute_Ion_button.setFixedSize(80, 30)  # 设置按钮大小

        clear_Ion_button = QPushButton("Clear")
        clear_Ion_button.clicked.connect(self.on_clear_Ion_clicked)
        clear_Ion_button.setFixedSize(80, 30)  # 设置按钮大小
        button_layout.addWidget(execute_Ion_button)
        button_layout.addWidget(clear_Ion_button)
        
        form_layout.addRow(button_layout)

        # 添加到主布局
        tab3_layout.addLayout(form_layout)
        # 设置选项卡的布局
        self.tab3.setLayout(tab3_layout)
    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            self.textEdit.setText(fname[0])
            

        input_filename = self.textEdit.toPlainText()
        self.A_or_I = jug_A_or_I(input_filename)
        if self.A_or_I =='none':
            self.showWarning('This is not a ROEX file')
        if self.A_or_I== 'A':
            self.target_file = read_A.Atm_File()
            self.target_file.read_file(input_filename)
        else:
            self.target_file = read_I.Ion_File()
            self.target_file.read_file(input_filename)
    
    def on_execute_Atm_clicked(self):

        
        start_time_CLO = self.start_time_CLO_edit.text()
        end_time_CLO   = self.end_time_CLO_edit.text()
       
        start_time_OPE = self.start_time_OPE_edit.text()
        end_time_OPE   = self.end_time_OPE_edit.text()
       
        output_filename = self.output_file_Atm_edit.text()
        jug =False
        warning ='plase check the information filled in'
        
        if output_filename[-4:]!='.ROX':
            output_filename = output_filename+'.ROX'
            
        if self.textEdit.toPlainText()=='':  #判断文件是否为空

            self.showWarning('you need select a ROEX file')
        else:
            input_filename = self.textEdit.toPlainText()
            A_or_I = jug_A_or_I(input_filename)
            
            if self.A_or_I =='none': #判断文件是否为ROEX类型（A or I）

                self.showWarning('This is not a ROEX file.')
       
            elif self.A_or_I =='I':
                self.showWarning('This is an Ion file.')
                
            else :
                
                try:
                    jug,warning = self.target_file.Edit_Atm(input_filename, start_time_CLO, end_time_CLO, start_time_OPE, end_time_OPE, output_filename)
                except Exception as e:
                    self.showWarning(f'An error occurred: {str(e)}')  # 打印具体的错误信息
                
            if jug == False:
                self.showWarning(warning)  # 打印具体的错误信息
            else:
                Show_file(output_filename)
        
    
    def on_clear_Atm_clicked(self):
        # Clear 按钮的点击事件处理
        for line_edit in self.line_Atm_edits:
            line_edit.clear()
        pass
    
    def on_execute_Ion_clicked(self):
        start_time_Ion = self.start_time_Ion_edit.text()
        end_time_Ion   = self.end_time_Ion_edit.text()
       
        start_time_OPE = self.start_time_OPE_edit.text()
        end_time_OPE   = self.end_time_OPE_edit.text()
       
        output_filename = self.output_file_Atm_edit.text()
        jug =False
        warning ='plase check the information filled in'
        
        if output_filename[-4:]!='.ROX':
            output_filename = output_filename+'.ROX'
            
        if self.textEdit.toPlainText()=='':  #判断文件是否为空消息框
            self.showWarning('you need select a ROEX file')
        else:
            input_filename = self.textEdit.toPlainText()
            A_or_I = jug_A_or_I(input_filename)
            
            if self.A_or_I =='none': #判断文件是否为ROEX类型（A or I）

                self.showWarning('This is not a ROEX file.')
       
            elif self.A_or_I =='A':
                self.showWarning('This is an Atm file.')
                
            else :
                
                try:
                    jug,warning = self.target_file.Edit_Ion(input_filename, start_time_Ion, end_time_Ion, output_filename)
                except Exception as e:
                    self.showWarning(f'An error occurred: {str(e)}')  # 打印具体的错误信息
                
            if jug == False:
                self.showWarning(warning)  # 打印具体的错误信息
            else:
                Show_file(output_filename)
    
    def on_clear_Ion_clicked(self):
        # Clear 按钮的点击事件处理
        for line_edit in self.line_Ion_edits:
            line_edit.clear()
        pass





        
    def showWarning(self,string):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)  # 设置消息框图标为警告图标
            msg.setText(string)  # 设置提示信息
            msg.setWindowTitle("Warning")  # 设置窗口标题
            msg.exec_()  # 显示消息框
    
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.__init__()
    # print(window.A_or_I)
    window.show()
    sys.exit(app.exec_())