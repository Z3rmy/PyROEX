# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 11:30:58 2025

@author: 22185
"""
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
import UI_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI_window.MainWindow()
    window.show()
    sys.exit(app.exec_())
