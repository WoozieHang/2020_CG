#import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class NewInputDialog(QDialog):
    def __init__(self, parent):
        super(NewInputDialog, self).__init__()
        self.parent=parent
        layout = QFormLayout()
        self.w_tmp=self.parent.my_canvas.width()
        self.h_tmp=self.parent.my_canvas.height()
        self.btn1 = QPushButton("设置画板宽度")
        self.btn1.clicked.connect(self.getWidth)
        self.le1 = QLabel()
        self.le1.setText(str(self.w_tmp))
        layout.addRow(self.btn1, self.le1)
        self.setLayout(layout)
        self.btn2 = QPushButton("设置画板高度")
        self.btn2.clicked.connect(self.getHeight)
        self.le2 = QLabel()
        self.le2.setText(str(self.h_tmp))
        layout.addRow(self.btn2, self.le2)
        self.setLayout(layout)
        self.setWindowTitle("新建画板")
        self.ensure=QPushButton("确定")
        self.ensure.clicked.connect(self.doEnsure)
        self.cancel = QPushButton("取消")
        self.cancel.clicked.connect(self.doCancel)
        layout.addRow(self.ensure,self.cancel)
        self.setLayout(layout)

    def getWidth(self):
        num, ok = QInputDialog.getInt(self, "integer input dualog", "输入数字")
        if ok:
            self.le1.setText(str(num))
            self.w_tmp=num

    def getHeight(self):
        num, ok = QInputDialog.getInt(self, "integer input dualog", "输入数字")
        if ok:
            self.le2.setText(str(num))
            self.h_tmp=num

    def doEnsure(self):
        self.parent.resetByWH(self.w_tmp, self.h_tmp)
        self.hide()


    def doCancel(self):
        self.hide()

