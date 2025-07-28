# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 09:33:18 2025

@author: zhangmingyi24
"""

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QTabWidget, QWidget, QHBoxLayout, QPushButton, QTextEdit, 
                             QApplication, QFileDialog, QMessageBox, QDialog, QSizePolicy, QLabel, QComboBox,
                             QGridLayout, QFormLayout, QLineEdit, QRadioButton, QButtonGroup, QCheckBox, 
                             QGroupBox, QStackedWidget)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import read_A, read_I
from function import *
from functools import partial
import numpy as np
import os, webbrowser, sys

font = {'family': 'Arial', 'color': 'black', 'weight': 'bold', 'size': 8, 'style': 'normal'}
font_small = {'family': 'Arial', 'color': 'black', 'weight': 'bold', 'size': 5, 'style': 'normal'}
watermark_props = {
    'fontsize': 8,
    'alpha': 0.7,
    'color': 'gray',
    'ha': 'left',
    'va': 'top'
}
DEFAULT_FONT_SIZE = 9
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_options = {}
        self.tabs = None
        self.A_or_I = 'none'

    def initUI(self):
        # 设置默认字体为Arial
        default_font = QtGui.QFont("Arial", DEFAULT_FONT_SIZE)
        self.setFont(default_font)
        
        # 窗口设置
        self.setWindowTitle('PyROEX (National Space Science Center, CAS)')
        self.resize(800, 900)
    
        # 中央控件
        central_widget = QWidget()
        central_widget.setFont(default_font)  # 应用字体
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
    
        # 顶部文件选择区域
        file_group = QGroupBox("File Selection")
        file_group.setFont(default_font)  # 应用字体
        file_layout = QGridLayout(file_group)
        
        self.textEdit = QTextEdit()
        self.textEdit.setFont(default_font)  # 应用字体
        self.textEdit.setFixedHeight(30)
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.setFont(default_font)  # 应用字体
        self.btn_browse.setFixedHeight(30)
        self.btn_browse.setFixedWidth(80)
        
        # 为标签应用字体
        file_path_label = QLabel("File Path:")
        file_path_label.setFont(default_font)
        file_layout.addWidget(file_path_label, 0, 0)
        file_layout.addWidget(self.textEdit, 0, 1)
        file_layout.addWidget(self.btn_browse, 0, 2)
        
        main_layout.addWidget(file_group)
    
        # 配置区域
        config_group = QGroupBox("Configuration")
        config_group.setFont(default_font)  # 应用字体
        config_layout = QGridLayout(config_group)
        
        # 文件类型选择
        file_type_label = QLabel("File Type:")
        file_type_label.setFont(default_font)  # 应用字体
        config_layout.addWidget(file_type_label, 0, 0)
        self.combo_box_filetype = QComboBox()
        self.combo_box_filetype.setFont(default_font)  # 应用字体
        self.combo_box_filetype.addItem(" ")
        self.combo_box_filetype.addItem("Atm")
        self.combo_box_filetype.addItem("Ion")
        self.combo_box_filetype.setFixedWidth(150)
        config_layout.addWidget(self.combo_box_filetype, 0, 1)
        
        # Atm配置
        atm_layout = QHBoxLayout()
        # 减少控件之间的间距
        atm_layout.setSpacing(8)
        
        atm_label1 = QLabel("CLO SNR LIM:")
        atm_label1.setFont(default_font)
        atm_layout.addWidget(atm_label1)
        self.SNR_LIM_CLO = QLineEdit()
        self.SNR_LIM_CLO.setFont(default_font)
        self.SNR_LIM_CLO.setText("40")
        self.SNR_LIM_CLO.setFixedWidth(60)
        atm_layout.addWidget(self.SNR_LIM_CLO)
        
        atm_label2 = QLabel("OPE SNR LIM:")
        atm_label2.setFont(default_font)
        atm_layout.addWidget(atm_label2)
        self.SNR_LIM_OPE = QLineEdit()
        self.SNR_LIM_OPE.setFont(default_font)
        self.SNR_LIM_OPE.setText("40")
        self.SNR_LIM_OPE.setFixedWidth(60)
        atm_layout.addWidget(self.SNR_LIM_OPE)
        
        atm_label3 = QLabel("Window_CLO:")
        atm_label3.setFont(default_font)
        atm_layout.addWidget(atm_label3)
        self.window_CLO = QLineEdit()
        self.window_CLO.setFont(default_font)
        self.window_CLO.setText("30")
        self.window_CLO.setFixedWidth(60)
        atm_layout.addWidget(self.window_CLO)
        
        atm_label4 = QLabel("Window_OPE:")
        atm_label4.setFont(default_font)
        atm_layout.addWidget(atm_label4)
        self.window_OPE = QLineEdit()
        self.window_OPE.setFont(default_font)
        self.window_OPE.setText("60")
        self.window_OPE.setFixedWidth(60)
        atm_layout.addWidget(self.window_OPE)
        
        # Ion配置 - 更紧凑的布局
        ion_layout = QHBoxLayout()
        # 减小间距使布局更紧凑
        ion_layout.setSpacing(15)
        # 去除边缘空白
        ion_layout.setContentsMargins(0, 0, 0, 0)
        
        ion_label1 = QLabel("SNR LIM:")
        ion_label1.setFont(default_font)
        ion_layout.addWidget(ion_label1)
        self.SNR_LIM = QLineEdit()
        self.SNR_LIM.setFont(default_font)
        self.SNR_LIM.setText("40")
        self.SNR_LIM.setFixedWidth(60)
        ion_layout.addWidget(self.SNR_LIM)
        
        # 添加一个小的间隔
        ion_layout.addSpacing(20)
        
        ion_label2 = QLabel("Window:")
        ion_label2.setFont(default_font)
        ion_layout.addWidget(ion_label2)
        self.window = QLineEdit()
        self.window.setFont(default_font)
        self.window.setText("60")
        self.window.setFixedWidth(60)
        ion_layout.addWidget(self.window)
        
        # 配置堆叠
        self.config_stack = QStackedWidget()
        atm_widget = QWidget()
        atm_widget.setLayout(atm_layout)
        ion_widget = QWidget()
        ion_widget.setLayout(ion_layout)
        self.config_stack.addWidget(atm_widget)
        self.config_stack.addWidget(ion_widget)
        self.config_stack.setCurrentIndex(0)  # 默认显示Atm配置
        
        settings_label = QLabel("Settings:")
        settings_label.setFont(default_font)  # 应用字体
        config_layout.addWidget(settings_label, 1, 0)
        config_layout.addWidget(self.config_stack, 1, 1, 1, 2)
        
        # 连接文件类型选择信号
        self.combo_box_filetype.currentIndexChanged.connect(self.update_config_display)
        
        main_layout.addWidget(config_group)
    
        # 选项卡系统
        self.tabs = QTabWidget()
        self.tabs.setFont(default_font)  # 应用字体
        self.tab1 = QWidget()
        self.tab1.setFont(default_font)  # 应用字体
        self.tab2 = QWidget()
        self.tab2.setFont(default_font)  # 应用字体
        self.tab3 = QWidget()
        self.tab3.setFont(default_font)  # 应用字体
        self.tab4 = QWidget()
        self.tab4.setFont(default_font)  # 应用字体
        self.tab5 = QWidget()
        self.tab5.setFont(default_font)  # 应用字体
    
        self.tabs.addTab(self.tab1, "Data Monitoring")
        self.tabs.addTab(self.tab2, "Data Combination")
        self.tabs.addTab(self.tab3, "Data Integrity")
        self.tabs.addTab(self.tab4, "File Clipping")
        self.tabs.addTab(self.tab5, "Help")
        
        # 初始化各选项卡内容
        self.init_tab1()
        self.init_tab2()
        self.init_tab3()
        self.init_tab4()
        self.init_tab5()
    
        main_layout.addWidget(self.tabs)
        self.btn_browse.clicked.connect(self.showDialog)
        self.tabs.currentChanged.connect(self.tab_changed)


    def update_config_display(self):
        """根据选择的文件类型显示不同的配置"""
        file_type = self.combo_box_filetype.currentText()
        if file_type == "Atm":
            self.config_stack.setCurrentIndex(0)
        elif file_type == "Ion":
            self.config_stack.setCurrentIndex(1)
        else:
            self.config_stack.setCurrentIndex(0)

    def init_tab1(self):
        tab = self.tab1
        main_layout = QVBoxLayout(tab)
        
        # 创建TabWidget
        self.tab_widget = QTabWidget()    
        self.combo_box_filetype.currentIndexChanged.connect(self.update_tab1)
        
        # 创建一个容器来放置动态生成的Checkbox
        self.checkbox_container = QWidget()
        self.checkbox_layout = QHBoxLayout(self.checkbox_container)
        self.checkbox_layout.setSpacing(0)
        self.checkbox_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.checkbox_container)

        # 创建一个容器来放置动态生成的选项卡
        main_layout.addWidget(self.tab_widget)
        
        tab.figure = plt.figure()
        plt.close(tab.figure)
        tab.canvas = FigureCanvas(tab.figure)
        tab.toolbar = NavigationToolbar(tab.canvas, self)
            
        main_layout.addWidget(tab.toolbar)
        main_layout.addWidget(tab.canvas)

        self.checkbox_container.setMaximumHeight(150)
        tab.canvas.setMinimumHeight(400)
        self.update_tab1()

    def update_tab1(self):
        # 获取当前选择的 figure number
        num_tabs = 2
        # self.tab1.figure.clear()

        figsize = (8, 6)  # 宽度 10，高度 6
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
        
        current_text = self.combo_box_filetype.currentText()
        
        self.A_or_I = jug_A_or_I(self.textEdit.toPlainText())

        '''
        还应该设置一个clear选项，清空当前所有的
        '''
        
        if self.A_or_I == 'A' and current_text == 'Atm':
            # 使用顶部配置区域的设置值            
            try:
                self.target_file.read_file(self.textEdit.toPlainText())
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
            # 使用顶部配置区域的设置值
            
            try:
                self.target_file.read_file(self.textEdit.toPlainText())
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
        SNR_CLO = float(self.SNR_LIM_CLO.text())
        SNR_OPE = float(self.SNR_LIM_OPE.text())
        window_CLO = int(self.window_CLO.text())
        window_OPE = int(self.window_OPE.text())
        self.target_file.SNR_filter(SNR_CLO,SNR_OPE,window_CLO,window_OPE)
        ylabel = []
        if tab_name == '选项卡1':
            # print(self.checkbox_row)
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.CLO_time_list,self.target_file.OCC_CLO_filter[k],label = f"CLO_{self.target_file.sat1} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行2']:
                to_plot_list = self.tab1.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.CLO_time_list,self.target_file.REF_CLO[k] ,label = f"CLO_{self.target_file.sat2} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行3']:
                to_plot_list = self.tab1.selected_options[tab_name]['行3']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.OPE_time_list,self.target_file.OCC_OPE_filter[k]  ,label = f"OPE_{self.target_file.sat1} {k}",s=size)
            if self.tab1.selected_options[tab_name]['行4']:
                to_plot_list = self.tab1.selected_options[tab_name]['行4']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.OPE_time_list,self.target_file.REF_OPE[k]  ,label = f"OPE_{self.target_file.sat2} {k}",s=size)    
            
            y_units = set()  # 用集合去重单位类型
            for label in ylabel:
                if label.startswith('S'):
                    y_units.add('SNR (dB)')
                elif label.startswith('L'):
                    y_units.add('Carrier Phase (Cycle)')
                elif label.startswith('C'):
                    y_units.add('Pseudorange (m)')
                elif label.startswith('O'):
                    y_units.add('Mode Phase (Cycle)')
                elif label.startswith('I'):
                    y_units.add('Channel I')
                elif label.startswith('Q'):
                    y_units.add('Channel Q')


        else:
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.CLO_time_list[:-1],self.target_file.dOCC_CLO[k],label = f"CLO_{self.target_file.sat1} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行2']:
                to_plot_list = self.tab1.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.CLO_time_list[:-1],self.target_file.dREF_CLO[k] ,label = f"CLO_{self.target_file.sat2} {k}",s=size)
                    
            if self.tab1.selected_options[tab_name]['行3']:
                to_plot_list = self.tab1.selected_options[tab_name]['行3']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.OPE_time_list[:-1],self.target_file.dOCC_OPE[k]  ,label = f"OPE_{self.target_file.sat1} {k}",s=size)
            if self.tab1.selected_options[tab_name]['行4']:
                to_plot_list = self.tab1.selected_options[tab_name]['行4']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.OPE_time_list[:-1],self.target_file.dREF_OPE[k]  ,label = f"OPE_{self.target_file.sat2} {k}",s=size)    
                    
            y_units = set()  # 用集合去重单位类型
            for label in ylabel:
                if label.startswith('S'):
                    y_units.add('SNR CR (dB/s)')
                elif label.startswith('L'):
                    y_units.add('Carrier Phase CR (Cycle/S)')
                elif label.startswith('C'):
                    y_units.add('Pseudorange CR (m/S)')
                elif label.startswith('O'):
                    y_units.add('Mode Phase CR (Cycle/S)')

            
            # 组合单位文本（多个单位用逗号分隔）
        if y_units:
            if len(y_units) > 3:
                # 保留原x轴标签文本，只调整字体大小
                self.tab1.ax.set_ylabel(', '.join(y_units), fontdict=font_small)
            else:
                self.tab1.ax.set_ylabel(', '.join(y_units), fontdict=font)
        else:
            self.tab1.ax.set_ylabel('')  # 默认标签
        
        
        
        self.text_time_atm(self.tab1)
        self.fig_xlabel_time(self.tab1)
        self.tab1.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)',fontdict=font)  
        self.tab1.ax.grid(True,  which='both', linestyle='--', alpha=0.7, color='#757575')
        self.tab1.ax.legend()
        self.tab1.canvas.draw()
        
        
    def PLOT_tab1_Ion(self,tab_name, checkboxes):
        self.tab1.figure.clf()
        self.tab1.ax = self.tab1.figure.add_subplot(111)  # 添加一个新的Axes对象
        size = 5
        SNR = float(self.SNR_LIM.text())
        window = int(self.window.text())
        
        self.target_file.SNR_filter(SNR,window)
        ylabel=[]
        # print(self.checkbox_row)
        if tab_name == '选项卡1':
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.OCC_time_list,self.target_file.OCC_filter[k],label = f"{self.target_file.sat} {k}",s=size)
            
            y_units = set()  # 用集合去重单位类型
            for label in ylabel:
                if label.startswith('S'):
                    y_units.add('SNR (dB)')
                elif label.startswith('L'):
                    y_units.add('Carrier Phase (Cycle)')
                elif label.startswith('C'):
                    y_units.add('Pseudorange (m)')
        else:
            if self.tab1.selected_options[tab_name]['行1']:
                to_plot_list = self.tab1.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    ylabel.append(k)
                    self.tab1.ax.scatter(self.target_file.OCC_time_list[:-1],self.target_file.dOCC[k],label = f"{self.target_file.sat} {k}",s=size)
            
            y_units = set()  # 用集合去重单位类型
            for label in ylabel:
                if label.startswith('S'):
                    y_units.add('SNR CR (dB/s)')
                elif label.startswith('L'):
                    y_units.add('Carrier Phase CR (Cycle/S)')
                elif label.startswith('C'):
                    y_units.add('Pseudorange CR (m/S)')

            
            # 组合单位文本（多个单位用逗号分隔）
        if y_units:
            self.tab1.ax.set_ylabel(', '.join(y_units),fontdict=font)
        else:
            self.tab1.ax.set_ylabel('')  # 默认标签
        
 
        self.text_time_ion(self.tab1)
        self.fig_xlabel_time(self.tab1)
        self.tab1.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)',fontdict=font)
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

    def init_tab2(self):
        tab = self.tab2
        main_layout = QVBoxLayout(tab)
        
        # 创建 TabWidget 并添加到主布局
        self.tab_widget_tab2 = QTabWidget()
        main_layout.addWidget(self.tab_widget_tab2)
         
        # 连接 ComboBox 信号到更新选项卡的槽函数
        self.combo_box_filetype.currentIndexChanged.connect(self.update_tabs2)
         
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
        tab.canvas.setMinimumSize(300, 300)
        tab.canvas.setMinimumWidth(300)  # 绘图区域的最小宽度
        tab.canvas.setMinimumHeight(400)  # 绘图区域的最小高度
         # 初始化选项卡
        self.update_tabs2()
        
    def update_tabs2(self):
        # num_tabs = 4
        figsize = (8, 6)  # 宽度 10，高度 6
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
        
        current_text = self.combo_box_filetype.currentText()
        self.A_or_I = jug_A_or_I(self.textEdit.toPlainText())
        
        
        if self.A_or_I == 'A' and current_text == 'Atm':
            # 使用顶部配置区域的设置值
            SNR_CLO = float(self.SNR_LIM_CLO.text())
            SNR_OPE = float(self.SNR_LIM_OPE.text())
            window_CLO = int(self.window_CLO.text())
            window_OPE = int(self.window_OPE.text())
            
            self.target_file.SNR_filter(SNR_CLO,SNR_OPE)
            try:
                row_labels = [
                    f"CLO_{self.target_file.sat1}:",
                    f"CLO_{self.target_file.sat2}:",
                    f"OPE_{self.target_file.sat1}:",
                    f"OPE_{self.target_file.sat2}:"
                ]
                row_labels_dif = [f"CLO_{self.target_file.sat1}:",
                                 f"OPE_{self.target_file.sat1}:"
                    ]
                groups = [
                    [self.target_file.OCC_CLO_MW, self.target_file.REF_CLO_MW, self.target_file.OCC_OPE_MW, self.target_file.REF_OPE_MW],
                    [self.target_file.OCC_CLO_GF, self.target_file.REF_CLO_GF, self.target_file.OCC_OPE_GF, self.target_file.REF_OPE_GF],
                    [self.target_file.OCC_CLO_IF, self.target_file.REF_CLO_IF, self.target_file.OCC_OPE_IF, self.target_file.REF_OPE_IF],
                    [self.target_file.OCC_CLO_DIF,self.target_file.OCC_OPE_DIF]
                ]
                
                tab_names = ["MW", "GF", "IF","DIF"]
                num_tabs = len(tab_names)
                for i in range(num_tabs):
                    tab_content = QWidget()
                    tab_layout = QGridLayout(tab_content)
                    checkboxes = []
                    # 填充复选框
                    if tab_names[i] == "DIF":
                            # DIF选项卡使用简化标签（2行）
                            current_row_labels = row_labels_dif
                    else:
                            # 其他选项卡使用完整标签（4行）
                            current_row_labels = row_labels
                        
                        # 填充复选框（循环次数由当前选项卡的groups[i]长度决定）
                    for row in range(len(groups[i])):
                            # 使用当前选项卡对应的行标签（避免标签数量超过行数）
                        row_label = QLabel(current_row_labels[row])
                        row_label.setFixedWidth(100)
                        tab_layout.addWidget(row_label, row, 0)
                        
                        # 添加空白列作为间距
                        tab_layout.addWidget(QLabel(), row, 1)
                        
                        # 初始化当前选项卡的选中状态存储（移到循环外更合理）
                        if i == 0:  # 只初始化一次，避免重复覆盖
                            self.tab2.selected_options = {
                                tab_name: {f"行{row+1}": [] for row in range(len(groups[tab_idx]))}
                                for tab_idx, tab_name in enumerate(tab_names)
                            }
                            self.tab2.checkbox_groups = {}
                        
                        # 添加当前行的复选框
                        for col, label in enumerate(groups[i][row]):
                            checkbox = QCheckBox(label)
                            checkbox.stateChanged.connect(
                                partial(self.tab2_update_selected_options, 
                                        tab_name=tab_names[i], row=row, option_label=label)
                            )
                            tab_layout.addWidget(checkbox, row, col + 2)
                            checkboxes.append(checkbox)
                    # 添加按钮
                    clear_button = QPushButton("CLEAR")
                    clear_button.clicked.connect(partial(self.tab2_clear_selected, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button, len(groups[i]), 0, 1, 1)
                    
                    plot_button = QPushButton("PLOT")
                    plot_button.clicked.connect(partial(self.PLOT_tab2_Atm, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(plot_button, len(groups[i]) , 1, 1, 1)
                    
                    # 添加选项卡到 self.tab_widget_tab2
                    self.tab_widget_tab2.addTab(tab_content, tab_names[i])
            
            except Exception as e:
                self.showWarning(f"{e}")
                
        if self.A_or_I == 'I' and current_text == 'Ion':
            # 使用顶部配置区域的设置值
            SNR = float(self.SNR_LIM.text())
            window = int(self.window.text())
            
            self.target_file.SNR_filter(SNR)
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
                num_tabs = len(tab_names)
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
                    tab_layout.addWidget(clear_button, len(groups[i]), 0, 1, 1)
                    
                    plot_button = QPushButton("PLOT")
                    plot_button.clicked.connect(partial(self.PLOT_tab2_Ion, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(plot_button, len(groups[i]) , 1, 1, 1)
                    
                    
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
        SNR_CLO = float(self.SNR_LIM_CLO.text())
        SNR_OPE = float(self.SNR_LIM_OPE.text())
        window_CLO = int(self.window_CLO.text())
        window_OPE = int(self.window_OPE.text())
        self.target_file.SNR_filter(SNR_CLO,SNR_OPE,window_CLO,window_OPE)
        
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
            self.tab2.ax.set_ylabel('MW Conbination (Cycle)',fontdict=font)
            
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
            self.tab2.ax.set_ylabel('GF Combination (m) ',fontdict=font)   
            
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
            self.tab2.ax.set_ylabel('IF Combination (m)',fontdict=font) 
            
        if tab_name == 'DIF':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_CLO_DIF[k])
                    self.tab2.ax.scatter(self.target_file.CLO_time_list[:l],self.target_file.OCC_CLO_DIF[k],label = f"CLO_{self.target_file.sat1} DIF {k}",s=size)
                    
            if self.tab2.selected_options[tab_name]['行2']:
                to_plot_list = self.tab2.selected_options[tab_name]['行2']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_OPE_DIF[k])
                    self.tab2.ax.scatter(self.target_file.OPE_time_list[:l],self.target_file.OCC_OPE_DIF[k] ,label = f"OPE_{self.target_file.sat1} DIF {k}",s=size)
            self.tab2.ax.set_ylabel('DIF Conbination (cycle)',fontdict=font)  
          
        self.text_time_atm(self.tab2)
        self.fig_xlabel_time(self.tab2)
        self.tab2.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)',fontdict=font)  
        self.tab2.ax.grid(True,  which='both', linestyle='--', alpha=0.7, color='#757575')
        self.tab2.ax.legend()
        self.tab2.canvas.draw()            
        
    
    def PLOT_tab2_Ion(self,tab_name, checkboxes):
        self.tab2.figure.clf()
        self.tab2.ax = self.tab2.figure.add_subplot(111)  # 添加一个新的Axes对象
        size = 5
        SNR = float(self.SNR_LIM.text())
        window = int(self.window.text())
        
        self.target_file.SNR_filter(SNR,window)
        if tab_name == 'MW':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_MW[k])
                    self.tab2.ax.scatter(self.target_file.OCC_time_list[:l],self.target_file.OCC_MW[k],label = f"{self.target_file.sat} MW {k}",s=size)
            self.tab2.ax.set_ylabel('MW Conbination (Cycle)',fontdict=font)
            
        if tab_name == 'GF':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_GF[k])
                    self.tab2.ax.scatter(self.target_file.OCC_time_list[:l],self.target_file.OCC_GF[k],label = f"{self.target_file.sat} GF {k}",s=size)
            self.tab2.ax.set_ylabel('GF Combination (m) ',fontdict=font)      
            
        if tab_name == 'IF':
            if self.tab2.selected_options[tab_name]['行1']:
                to_plot_list = self.tab2.selected_options[tab_name]['行1']
                for k in to_plot_list:
                    l = len(self.target_file.OCC_IF[k])
                    self.tab2.ax.scatter(self.target_file.OCC_time_list[:l],self.target_file.OCC_IF[k],label = f"{self.target_file.sat} IF {k}",s=size)
            self.tab2.ax.set_ylabel('IF Combination (m)',fontdict=font) 
            
        self.text_time_ion(self.tab2)
        self.fig_xlabel_time(self.tab2)
        
        self.tab2.ax.set_xlabel(self.target_file.timetype+' Time(hh:mm:ss)',fontdict=font) 
        self.tab2.ax.grid(True,  which='both', linestyle='--', alpha=0.7, color='#757575')
        self.tab2.ax.legend()
        self.tab2.canvas.draw()           
    
    def init_tab3(self):
        tab = self.tab3
        main_layout = QVBoxLayout(tab)
        
        # 创建TabWidget
        self.tab_widget_tab3 = QTabWidget()
        main_layout.addWidget(self.tab_widget_tab3)
         
        # 连接ComboBox信号
        self.combo_box_filetype.currentIndexChanged.connect(self.update_tab3)
         
        # Matplotlib图形
        tab.figure = plt.figure()
        plt.close(tab.figure)
        tab.canvas = FigureCanvas(tab.figure)
        tab.toolbar = NavigationToolbar(tab.canvas, self)
         
        main_layout.addWidget(tab.toolbar)
        main_layout.addWidget(tab.canvas)
         
        # 设置控件大小
        tab.canvas.setMinimumSize(300, 300)
        tab.canvas.setMinimumWidth(300)
        tab.canvas.setMinimumHeight(400)
        
        self.update_tab3()

    def update_tab3(self):
        # 获取当前选择的 figure number
        num_tabs = 1
        figsize = (8, 6)  # 宽度 10，高度 6
        aspect_ratio = 'auto'
        self.tab3.figure.clf()
        # 动态调整 figure 大小
        self.tab3.figure.set_size_inches(*figsize)
        plt.close(self.tab3.figure)
        self.tab3.ax = self.tab3.figure.add_subplot(1, 1, 1)
        self.tab3.ax.set_aspect(aspect_ratio)
        self.tab3.ax.plot([], [])
        self.tab3.canvas.draw()
        
        # 清空现有的选项卡
        self.tab_widget_tab3.clear()
        
        current_text = self.combo_box_filetype.currentText()
        self.A_or_I = jug_A_or_I(self.textEdit.toPlainText())
   
        if self.A_or_I == 'A' and current_text == 'Atm':
            # 使用顶部配置区域的设置值
            SNR_CLO = float(self.SNR_LIM_CLO.text())
            SNR_OPE = float(self.SNR_LIM_OPE.text())
            window_CLO = int(self.window_CLO.text())
            window_OPE = int(self.window_OPE.text())
            
            self.target_file.SNR_filter(SNR_CLO, SNR_OPE)
            try:
                self.tab3.checkbox_labels_OCC_CLO_DI = self.target_file.OCC_CLO_DI
                self.tab3.checkbox_labels_REF_CLO_DI = self.target_file.REF_CLO_DI
                self.tab3.checkbox_labels_OCC_OPE_DI = self.target_file.OCC_OPE_DI
                self.tab3.checkbox_labels_REF_OPE_DI = self.target_file.REF_OPE_DI
                
                # 定义各行列内容
                row_labels = [
                    f"CLO_{self.target_file.sat1} :",
                    f"CLO_{self.target_file.sat2} :",
                    f"OPE_{self.target_file.sat1} :",
                    f"OPE_{self.target_file.sat2} :"
                ]
                groups = [
                    self.tab3.checkbox_labels_OCC_CLO_DI,
                    self.tab3.checkbox_labels_REF_CLO_DI,
                    self.tab3.checkbox_labels_OCC_OPE_DI,
                    self.tab3.checkbox_labels_REF_OPE_DI
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
                        
                        self.tab3.selected_options = {
                            f"选项卡{i+1}": {f"行{row+1}": [] for row in range(len(groups))}
                            for i in range(num_tabs)
                        }
                        self.tab3.checkbox_groups = {}
                        # print(self.selected_options)

                        # 添加空白列作为间距
                        tab_layout.addWidget(QLabel(), row, 1)
                        
                        for col, label in enumerate(groups[row]):
                            # print(str(label))
                            checkbox = QCheckBox(label)
                            checkbox.stateChanged.connect(partial(self.tab3_update_selected_options, tab_name=f"选项卡{i+1}", row=row, option_label=label))
                            tab_layout.addWidget(checkbox, row, col + 2)                
                            checkboxes.append(checkbox)
                            
                    clear_button = QPushButton("ALL")
                    clear_button.clicked.connect(partial(self.tab3_select_all, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)  
                    
                    clear_button = QPushButton("CLEAR")
                    clear_button.clicked.connect(partial(self.tab3_clear_selected, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    clear_button = QPushButton("EXCUTE")
                    clear_button.clicked.connect(partial(self.PLOT_tab3_Atm, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    # 保存当前选项卡的复选框
                    self.tab3.checkbox_groups[tab_names[i]] = checkboxes
                    # 设置列宽
                    tab_layout.setColumnStretch(0, 0)
                    tab_layout.setColumnStretch(1, 0)
                    tab_layout.setColumnMinimumWidth(0, 100)
                    tab_layout.setColumnMinimumWidth(1, 10)
                
                # print(self.checked_OCC_CLO_OD , self.checked_REF_OPE_OD)
                # 将选项卡内容添加到选项卡小部件
                    if i==0:
                        self.tab_widget_tab3.addTab(tab_content, f"Data Integrity")
            except Exception as e:
                # print(f"{e}")
                self.showWarning(f"Error generating checkboxes for 'Atm': {e}")
                
        elif self.A_or_I == "I" and current_text == "Ion":
            # 使用顶部配置区域的设置值
            SNR = float(self.SNR_LIM.text())
            window = int(self.window.text())
            
            self.target_file.SNR_filter(SNR)
            try:
                self.tab3.checkbox_labels_OCC = self.target_file.OCC
                
                row_labels = [
                    f"{self.target_file.sat:} :"
                ]
                groups = [
                    self.tab3.checkbox_labels_OCC
                ]
                checkboxes = []
                # 创建每个选项卡及其内容
                tab_names = ["选项卡1", "选项卡2"]
                for i in range(num_tabs):
                    tab_content = QWidget()
                    tab_layout = QGridLayout(tab_content)
                    tab_layout.setSpacing(5)
                    tab_layout.setContentsMargins(0, 0, 0, 0)
                    self.tab3.checkbox_groups = {}
                    row_labels = [f"{self.target_file.sat} :"]
                    

                    for row in range(len(groups)):
                        row_label = QLabel(row_labels[row])
                        row_label.setFixedWidth(100)
                        tab_layout.addWidget(row_label, row, 0)
                        
                        self.tab3.selected_options = {
                            f"选项卡{i+1}": {f"行{row+1}": [] for row in range(len(groups))}
                            for i in range(num_tabs)
                        }
                        self.tab3.checkbox_groups = {}
                        # print(self.selected_options)

                        # 添加空白列作为间距
                        tab_layout.addWidget(QLabel(), row, 1)
                        
                        for col, label in enumerate(groups[row]):
                            # print(str(label))
                            checkbox = QCheckBox(label)
                            checkbox.stateChanged.connect(partial(self.tab3_update_selected_options, tab_name=f"选项卡{i+1}", row=row, option_label=label))
                            tab_layout.addWidget(checkbox, row, col + 2)                
                            checkboxes.append(checkbox)
                            
                            
                    clear_button = QPushButton("ALL")
                    clear_button.clicked.connect(partial(self.tab3_select_all, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)   
                    
                    clear_button = QPushButton("CLEAR")
                    clear_button.clicked.connect(partial(self.tab3_clear_selected, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    clear_button = QPushButton("EXCUTE")
                    clear_button.clicked.connect(partial(self.PLOT_tab3_Ion, tab_name=tab_names[i], checkboxes=checkboxes))
                    tab_layout.addWidget(clear_button)
                    
                    if i==0:
                        self.tab_widget_tab3.addTab(tab_content, f"Data Integrity")

            except Exception as e:
                self.showWarning(f"Error generating checkboxes for 'Ion': {e}")

    def tab3_select_all(self, tab_name, checkboxes):
        """
        勾选指定选项卡中的所有复选框，并同步更新选中状态记录
        修复'QWidgetItem' object has no attribute 'row'错误
        """
        # 先清空现有选中状态
        self.tab3_clear_selected(tab_name, checkboxes)
        
        # 遍历所有复选框并勾选
        for checkbox in checkboxes:
            checkbox.blockSignals(True)
            checkbox.setChecked(True)
            checkbox.blockSignals(False)
        
        # 手动触发状态更新（关键修复：正确获取行索引）
        if not checkboxes:
            return  # 无复选框时直接返回
        
        layout = checkboxes[0].parentWidget().layout()
        if not isinstance(layout, QGridLayout):
            return  # 非网格布局时直接返回
        
        # 遍历网格布局中的所有位置（行和列）
        for row in range(layout.rowCount()):
            for col in range(layout.columnCount()):
                # 获取指定行列位置的item
                item = layout.itemAtPosition(row, col)
                if item is None:
                    continue  # 跳过空位置
                
                # 检查该位置的widget是否是当前复选框列表中的一个
                widget = item.widget()
                if widget in checkboxes:
                    # 找到对应的复选框，调用更新函数（row直接使用网格的行索引）
                    self.tab3_update_selected_options(
                        Qt.Checked,
                        tab_name,
                        row,  # 正确的行索引
                        widget.text()
                    )
  
                
    def tab3_update_selected_options(self, state, tab_name, row, option_label):
        # 根据状态更新对应的列表
        if state == Qt.Checked:
            if option_label not in self.tab3.selected_options[tab_name][f"行{row+1}"]:
                self.tab3.selected_options[tab_name][f"行{row+1}"].append(option_label)
        else:
            if option_label in self.tab3.selected_options[tab_name][f"行{row+1}"]:
                self.tab3.selected_options[tab_name][f"行{row+1}"].remove(option_label)
        
    def tab3_clear_selected(self, tab_name, checkboxes):
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        
        # 清空 selected_options 中对应的记录
        if hasattr(self, 'selected_options'):
            for row in self.tab3.selected_options.get(tab_name, {}):
                self.tab3.selected_options[tab_name][row].clear()
                
    def PLOT_tab3_Atm(self, tab_name, checkboxes):
            self.tab3.figure.clf()
            self.tab3.ax = self.tab3.figure.add_subplot(111)
            SNR_CLO = float(self.SNR_LIM_CLO.text())
            SNR_OPE = float(self.SNR_LIM_OPE.text())
            window_CLO = int(self.window_CLO.text())
            window_OPE = int(self.window_OPE.text())
            self.target_file.SNR_filter(SNR_CLO,SNR_OPE,window_CLO,window_OPE)
            self.target_file.DI_CHECK()
            bar_width = 0.15
            step = bar_width + 0.1
            gap = 0.2
            opacity = 0.8
            x_pos = 0
            all_xticks = []
            all_xlabels = []
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            font1 = {'family': 'Arial', 'color': 'black', 'weight': 'bold', 'size': 5, 'style': 'normal'}
            max_data = 0 
            has_legend = False  # 用于标记是否有图例需要显示
            legend_handles = []
            # 行1处理
            row1_flag = 0  # 专用标记变量
            if self.tab3.selected_options[tab_name]['行1']:
                to_plot_list = self.tab3.selected_options[tab_name]['行1']
                for idx, k in enumerate(to_plot_list):
                    row1_flag = 1
                    data_val = self.target_file.OCC_CLO_DI[k]
                    max_data = max(max_data, data_val)
                    
                    self.tab3.ax.bar(
                        x_pos, data_val, bar_width,
                        color=colors[0], alpha=opacity, edgecolor='black'
                    )
                    
                    # 文本位置处理
                    text_offset = 0.05 if idx % 2 == 0 else -0.08
                    text_y = data_val + text_offset if idx % 2 == 0 else data_val + 0.05
                    if text_y < 0.05:
                        text_y = data_val + 0.05
                    
                    self.tab3.ax.text(
                        x_pos, text_y,
                        f'{data_val*100:.1f}%',
                        ha='center', va='bottom' if idx % 2 == 0 else 'top',
                        fontdict = font1, color=colors[0]
                    )
                    
                    all_xticks.append(x_pos)
                    all_xlabels.append(f'{k}')
                    x_pos += step
            
            # 行1图例（使用正确的标记变量）
            if row1_flag:
               legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=colors[0], label=f'CLO_{self.target_file.sat1}'))
            
               x_pos += gap
            # 行2处理
            row2_flag = 0  # 专用标记变量
            if self.tab3.selected_options[tab_name]['行2']:
                to_plot_list = self.tab3.selected_options[tab_name]['行2']
                for idx, k in enumerate(to_plot_list):
                    row2_flag = 1
                    data_val = self.target_file.REF_CLO_DI[k]
                    max_data = max(max_data, data_val)
                    
                    self.tab3.ax.bar(
                        x_pos, data_val, bar_width,
                        color=colors[1], alpha=opacity, edgecolor='black'
                    )
                    
                    # 文本位置处理
                    text_offset = 0.05 if idx % 2 == 0 else -0.08
                    text_y = data_val + text_offset if idx % 2 == 0 else data_val + 0.05
                    if text_y < 0.05:
                        text_y = data_val + 0.05
                    
                    self.tab3.ax.text(
                        x_pos, text_y,
                        f'{data_val*100:.1f}%',
                        ha='center', va='bottom' if idx % 2 == 0 else 'top',
                        fontdict = font1, color=colors[1]
                    )
                    
                    all_xticks.append(x_pos)
                    all_xlabels.append(f'{k}')
                    x_pos += step
            
            # 行2图例
            if row2_flag:
                legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=colors[1], label=f'CLO_{self.target_file.sat2}'))
                x_pos += gap     
            # 行3处理
            row3_flag = 0  # 专用标记变量
            if self.tab3.selected_options[tab_name]['行3']:
                to_plot_list = self.tab3.selected_options[tab_name]['行3']
                for idx, k in enumerate(to_plot_list):
                    row3_flag = 1
                    data_val = self.target_file.OCC_OPE_DI[k]
                    max_data = max(max_data, data_val)
                    
                    self.tab3.ax.bar(
                        x_pos, data_val, bar_width,
                        color=colors[2], alpha=opacity, edgecolor='black'
                    )
                    
                    # 文本位置处理
                    text_offset = 0.05 if idx % 2 == 0 else -0.08
                    text_y = data_val + text_offset if idx % 2 == 0 else data_val + 0.05
                    if text_y < 0.05:
                        text_y = data_val + 0.05
                    
                    self.tab3.ax.text(
                        x_pos, text_y,
                        f'{data_val*100:.1f}%',
                        ha='center', va='bottom' if idx % 2 == 0 else 'top',
                        fontdict = font1, color=colors[2]
                    )
                    
                    all_xticks.append(x_pos)
                    all_xlabels.append(f'{k}')
                    x_pos += step
            
            # 行3图例
            if row3_flag:
                legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=colors[2], label=f'OPE_{self.target_file.sat1}'))
                x_pos += gap
            # 行4处理
            row4_flag = 0  # 专用标记变量
            if self.tab3.selected_options[tab_name]['行4']:
                to_plot_list = self.tab3.selected_options[tab_name]['行4']
                for idx, k in enumerate(to_plot_list):
                    row4_flag = 1
                    data_val = self.target_file.REF_OPE_DI[k]
                    max_data = max(max_data, data_val)
                    
                    self.tab3.ax.bar(
                        x_pos, data_val, bar_width,
                        color=colors[3], alpha=opacity, edgecolor='black'
                    )
                    
                    # 文本位置处理
                    text_offset = 0.05 if idx % 2 == 0 else -0.08
                    text_y = data_val + text_offset if idx % 2 == 0 else data_val + 0.05
                    if text_y < 0.05:
                        text_y = data_val + 0.05
                    
                    self.tab3.ax.text(
                        x_pos, text_y,
                        f'{data_val*100:.1f}%',
                        ha='center', va='bottom' if idx % 2 == 0 else 'top',
                        fontdict = font1, color=colors[3]
                    )
                    
                    all_xticks.append(x_pos)
                    all_xlabels.append(f'{k}')
                    x_pos += step
            
            # 行4图例
            if row4_flag:
                legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=colors[3], label=f'OPE_{self.target_file.sat2}'))
            
            # Y轴设置

            self.tab3.ax.set_ylim(0, 1.1)
            self.tab3.ax.set_yticks(np.arange(0, 1.1, 0.2))
            self.tab3.ax.set_yticklabels([0, 20 ,40,60,80,100])
            # X轴设置
            if all_xticks:
                self.tab3.ax.set_xticks(all_xticks)
                self.tab3.ax.set_xticklabels(all_xlabels, rotation=30,fontsize=6)
                
            
            # 图例设置（关键修复：只调用一次legend()）
            self.text_time_atm(self.tab3)

            # 其他设置

            self.tab3.ax.tick_params(axis='both', labelsize=8)
            self.tab3.ax.set_ylabel('Data Integrity (%)', fontdict=font)
            self.tab3.ax.grid(True, which='both', linestyle='--', alpha=0.7, color='#757575')
            if legend_handles:
                self.tab3.ax.legend(handles=legend_handles, loc='best',prop={'size':8})
            self.tab3.canvas.draw()
            
            self.target_file.write_DI()
            Show_file(self.target_file.log_DI) 
        
    def PLOT_tab3_Ion(self,tab_name,checkboxes):
            self.tab3.figure.clf()
            self.tab3.ax = self.tab3.figure.add_subplot(111)
            SNR = float(self.SNR_LIM.text())
            window = int(self.window.text())
            
            self.target_file.SNR_filter(SNR,window)
            self.target_file.DI_CHECK()
            
            bar_width = 0.15
            step = bar_width+0.05
            opacity = 0.8
            x_pos = 0
            all_xticks = []
            all_xlabels = []
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            font1 = {'family': 'Arial', 'color': 'black', 'weight': 'bold', 'size': 7.5, 'style': 'normal'}
            max_data = 0 
            has_legend = False  # 用于标记是否有图例需要显示
            legend_handles = []
            # 行1处理
            row1_flag = 0  # 专用标记变量
            if self.tab3.selected_options[tab_name]['行1']:
                to_plot_list = self.tab3.selected_options[tab_name]['行1']
                for idx, k in enumerate(to_plot_list):
                    row1_flag = 1
                    data_val = self.target_file.OCC_DI[k]
                    max_data = max(max_data, data_val)
                    
                    self.tab3.ax.bar(
                        x_pos, data_val, bar_width,
                        color=colors[0], alpha=opacity, edgecolor='black'
                    )
                    
                    # 文本位置处理
                    text_offset = 0.05 if idx % 2 == 0 else -0.08
                    text_y = data_val + text_offset if idx % 2 == 0 else data_val + 0.05
                    if text_y < 0.05:
                        text_y = data_val + 0.05
                    
                    self.tab3.ax.text(
                        x_pos, text_y,
                        f'{data_val*100:.1f}%',
                        ha='center', va='top',
                        fontdict=font1, color=colors[0]
                    )
                    
                    all_xticks.append(x_pos)
                    all_xlabels.append(f'{k}')
                    x_pos += step
            
            # 行1图例（使用正确的标记变量）
            if row1_flag:
               legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=colors[0], label=f'{self.target_file.sat}'))
                
            # Y轴设置
            self.tab3.ax.set_ylim(0, 1.1)
            self.tab3.ax.set_yticks(np.arange(0, 1.1, 0.2))
            self.tab3.ax.set_yticklabels([0, 20 ,40,60,80,100])
            
            # X轴设置
            if all_xticks:
                self.tab3.ax.set_xticks(all_xticks)
                self.tab3.ax.set_xticklabels(all_xlabels, rotation=30,fontsize=8)
            
            # 图例设置（关键修复：只调用一次legend()）
            self.text_time_ion(self.tab3)

            
            # 其他设置

            self.tab3.ax.tick_params(axis='both', labelsize=8)
            self.tab3.ax.set_ylabel('Data Integrity (%)', fontdict=font)
            self.tab3.ax.tick_params(axis='x', which='both', length=0)
            self.tab3.ax.grid(True, which='both', linestyle='--', alpha=0.7, color='#757575')
            if legend_handles:
                self.tab3.ax.legend(handles=legend_handles, loc='best')
                
            self.tab3.canvas.draw() 
            self.target_file.write_DI()
            Show_file(self.target_file.log_DI) 
            
            
    def init_tab4(self):
        # 创建一个垂直布局作为选项卡的内容
        tab4_layout = QVBoxLayout()
        tab4_layout.setSpacing(10)  # 设置布局间距

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
        self.start_time_CLO_edit.setFixedWidth(250)  # 设置文本编辑框宽度

        start_time_CLO_layout = QHBoxLayout()
        start_time_CLO_layout.addWidget(self.start_time_CLO_edit)
        start_time_CLO_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_CLO_layout.addLayout(start_time_CLO_layout)

        # 添加 End Time 字段
        end_time_CLO_label = QLabel("End Time:")
        self.end_time_CLO_edit = QLineEdit()
        self.end_time_CLO_edit.setFixedWidth(250)  # 设置文本编辑框宽度

        end_time_CLO_layout = QHBoxLayout()
        end_time_CLO_layout.addWidget(self.end_time_CLO_edit)
        end_time_CLO_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_CLO_layout.addLayout(end_time_CLO_layout)

        # 将时间范围布局添加到表单布局
        form_layout.addRow("CLO Time Range :", time_range_CLO_layout)


        '''
        创建水平布局用于 Start Time 和 End Time  CLO
        '''
        time_range_OPE_layout = QHBoxLayout()

        # 添加 Start Time 字段
        start_time_OPE_label = QLabel("Start Time:")
        self.start_time_OPE_edit = QLineEdit()
        self.start_time_OPE_edit.setFixedWidth(250)  # 设置文本编辑框宽度

        start_time_OPE_layout = QHBoxLayout()
        start_time_OPE_layout.addWidget(self.start_time_OPE_edit)
        start_time_OPE_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_OPE_layout.addLayout(start_time_OPE_layout)

        # 添加 End Time 字段
        end_time_OPE_label = QLabel("End Time:")
        self.end_time_OPE_edit = QLineEdit()
        self.end_time_OPE_edit.setFixedWidth(250)  # 设置文本编辑框宽度

        end_time_OPE_layout = QHBoxLayout()
        end_time_OPE_layout.addWidget(self.end_time_OPE_edit)
        end_time_OPE_layout.addWidget(QLabel("DD:HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_OPE_layout.addLayout(end_time_OPE_layout)

        # 将时间范围布局添加到表单布局
        form_layout.addRow("OPE Time Range :", time_range_OPE_layout)


        '''
        添加 Output File 字段
        '''
        output_file_Atm_edit_label = QLabel("Output File:")
        self.output_file_Atm_edit = QLineEdit()
        self.output_file_Atm_edit.setFixedWidth(250)  # 设置文本编辑框宽度

        output_file_Atm_edit_layout = QHBoxLayout()
        output_file_Atm_edit_layout.addWidget(self.output_file_Atm_edit)
        output_file_Atm_edit_layout.addWidget(QLabel("../data"), alignment=Qt.AlignLeft)
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
        tab4_layout.addLayout(form_layout)
        
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
        self.start_time_Ion_edit.setFixedWidth(250)  # 设置文本编辑框宽度

        start_time_Ion_layout = QHBoxLayout()
        start_time_Ion_layout.addWidget(self.start_time_Ion_edit)
        start_time_Ion_layout.addWidget(QLabel("YY-MM-DD HH:MM:SS"), alignment=Qt.AlignLeft)

        time_range_Ion_layout.addLayout(start_time_Ion_layout)

        # 添加 End Time 字段
        end_time_Ion_label = QLabel("End Time:")
        self.end_time_Ion_edit = QLineEdit()
        self.end_time_Ion_edit.setFixedWidth(250)  # 设置文本编辑框宽度

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
        self.output_file_Ion_edit.setFixedWidth(250)  # 设置文本编辑框宽度

        output_file_Ion_edit_layout = QHBoxLayout()
        output_file_Ion_edit_layout.addWidget(self.output_file_Ion_edit)
        output_file_Ion_edit_layout.addWidget(QLabel("../data"), alignment=Qt.AlignLeft)
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
        tab4_layout.addLayout(form_layout)
        # 设置选项卡的布局
        self.tab4.setLayout(tab4_layout)
    
    def init_tab5(self):
        """初始化Help选项卡"""
        tab = self.tab5
        layout = QVBoxLayout(tab)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
        <h2>PyROEX User Guide</h2>
        <p><b>Data Monitoring:</b> Visualize raw ROEX data and its changing rate.</p>
        <p><b>Data Combination:</b> Analyze combined data metrics (MW, GF, IF, DIF).</p>
        <p><b>Data Integrity:</b> Check data completeness and reliability.</p>
        <p><b>File Clipping:</b> Extract specific time ranges from ROEX files.</p>
        <p><b>Configuration:</b></p>
        <ul>
            <li>For Atm files: Set SNR limits and window sizes for CLO and OPE</li>
            <li>For Ion files: Set SNR limit and window size</li>
        </ul>
        <p><b>Usage Tips:</b></p>
        <ol>
            <li>Browse and select a ROEX file</li>
            <li>Select file type and configure settings</li>
            <li>Navigate through tabs to perform analysis</li>
            <li>Use 'Execute'or 'PLOT' buttons to run operations</li>
        </ol>
        <p>For detailed documentation, see the User Manual PDF.</p>
        """)
        
        layout.addWidget(help_text)
    
    def tab_changed(self, index):
        if index == 4:  # Help选项卡
            self.open_help_documentation()

    def open_help_documentation(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        doc_path = os.path.join(parent_dir, "doc", "User Manual.pdf")
        
        if os.path.exists(doc_path):
            webbrowser.open(doc_path)
        else:
            self.showWarning('Help documentation file not found!')
    
    def text_time_atm(self,tab):
            if tab == self.tab1:
                h1 = 1.09 ; h2 =1.13
            else:
                h1 = 1.05 ; h2 =1.09
            watermark_props = {
                'fontsize': DEFAULT_FONT_SIZE-1,        # 小字体 原为8
                'alpha': 0.7,         # 半透明，类似水印 
                'color': 'gray',      # 灰色更像水印 
                'ha': 'left',       
                'va': 'top'        
            }
            tab.ax.text(
                0.,h2, 
                f'CLO:{self.target_file.CLO_time_list[0]}-{self.target_file.filter_CLO_end_time}', 
                transform=tab.ax.transAxes,  # 使用轴坐标（0-1范围） 
                **watermark_props
            )
            tab.ax.text(
                0.,h1, 
                f'OPE:{self.target_file.OPE_time_list[0]}-{self.target_file.filter_OPE_end_time}', 
                transform=tab.ax.transAxes,  # 使用轴坐标（0-1范围） 
                **watermark_props
            )
            tab.ax.set_title(f'{self.target_file.label_kb}', 
            loc='right',   # 标题右对齐 
            pad=0,        # 可选：调整标题与图表顶部的距离（单位：磅） 
            fontdict={'weight': 'bold'}  # 可选：设置字体属性) 
            )
            
    def text_time_ion(self,tab):
            if tab == self.tab1:
                h1 = 1.09
            else:
                h1 = 1.05 
            watermark_props = {
                'fontsize': DEFAULT_FONT_SIZE-1,        # 小字体 原为8
                'alpha': 0.7,         # 半透明，类似水印 
                'color': 'gray',      # 灰色更像水印 
                'ha': 'left',       
                'va': 'top'        
            }
            tab.ax.text(
                0.,h1, 
                f'{self.target_file.OCC_time_list[0]}-{self.target_file.filter_OCC_end_time}', 
                transform=tab.ax.transAxes,  # 使用轴坐标（0-1范围） 
                **watermark_props
            )
            tab.ax.set_title(f'{self.target_file.label_kb}', 
            loc='right',   # 标题右对齐 
            pad=0,        # 可选：调整标题与图表顶部的距离（单位：磅） 
            fontdict={'weight': 'bold'}  # 可选：设置字体属性) 
            )


    def fig_xlabel_time(self,tab):
        tab.ax.xaxis.set_major_formatter(FuncFormatter(time_formatter))
        tab.ax.xaxis.set_major_locator(AutoLocator())    
        tab.ax.tick_params(axis='x', labelsize=6) 
        
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