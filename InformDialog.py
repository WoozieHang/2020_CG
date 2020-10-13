#import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class InformDialog(QDialog):
    def __init__(self, parent):
        super(InformDialog, self).__init__()
        self.parent=parent
        layout = QFormLayout()
        self.le1 = QLabel()
        self.le1.setText("正在加密，请稍等...")
        self.btn1 = QPushButton(" ")
        layout.addRow(self.btn1,self.le1)
        self.setLayout(layout)
        self.setWindowTitle("提示:正在加密，请稍等...")

class InformDialog2(QDialog):
    def __init__(self, parent):
        super(InformDialog2, self).__init__()
        self.parent=parent
        layout = QFormLayout()
        self.le1 = QLabel()
        self.le1.setText("正在解密，请稍等...")
        self.btn1 = QPushButton(" ")
        layout.addRow(self.btn1, self.le1)
        self.setLayout(layout)
        self.setWindowTitle("提示:正在解密，请稍等...")


