#import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class LockParamDialog(QDialog):
    def __init__(self, parent):
        super(LockParamDialog, self).__init__()
        self.parent=parent
        layout = QFormLayout()
        self.btn1 = QPushButton("设置第一个参数x（正整数即可，自动归一化到[0,1]）")
        self.btn1.clicked.connect(self.getParam1)
        self.le1 = QLabel()
        self.le1.setText(str(0))
        self.parent.param1=0
        layout.addRow(self.btn1, self.le1)
        self.setLayout(layout)
        self.btn2 = QPushButton("设置第二个参数u（正整数即可，自动归一化到(3.5699457,4])")
        self.btn2.clicked.connect(self.getParam2)
        self.le2 = QLabel()
        self.le2.setText(str(4))
        self.parent.param2 = 4
        layout.addRow(self.btn2, self.le2)
        self.setLayout(layout)

        self.btn3 = QPushButton("设置第三个参数gap（正整数即可)")
        self.btn3.clicked.connect(self.getParam3)
        self.le3 = QLabel()
        self.le3.setText(str(100))
        self.parent.param3 = 100
        layout.addRow(self.btn3, self.le3)
        self.setLayout(layout)

        self.btn4 = QPushButton("设置第四个参数startPos（正整数即可)")
        self.btn4.clicked.connect(self.getParam4)
        self.le4 = QLabel()
        self.le4.setText(str(100))
        self.parent.param4 = 100
        layout.addRow(self.btn4, self.le4)
        self.setLayout(layout)

        self.setWindowTitle("加密参数")
        self.ensure=QPushButton("确定")
        self.ensure.clicked.connect(self.doEnsure)
        self.cancel = QPushButton("取消")
        self.cancel.clicked.connect(self.doCancel)
        layout.addRow(self.ensure,self.cancel)
        self.setLayout(layout)

    def getParam1(self):
        num, ok = QInputDialog.getInt(self, "integer input dialog", "输入数字")
        if ok:
            self.le1.setText(str(num))
            self.parent.param1=(num%1000)/1000

    def getParam2(self):
        num, ok = QInputDialog.getInt(self, "integer input dialog", "输入数字")
        if ok:
            self.le2.setText(str(num))
            self.parent.param2=3.5699457+(num%round((4-3.5699457)*1000000))/1000000


    def getParam3(self):
        num, ok = QInputDialog.getInt(self, "integer input dialog", "输入数字")
        if ok:
            self.le3.setText(str(num))
            self.parent.param3=num

    def getParam4(self):
        num, ok = QInputDialog.getInt(self, "integer input dialog", "输入数字")
        if ok:
            self.le4.setText(str(num))
            self.parent.param4=num

    def doEnsure(self):
        self.hide()
        self.parent.statusBar.showMessage(
            '(0,0)像素      状态: 加密(禁用大部分功能，但可以保存画板)                   画板大小:' + str(self.parent.my_canvas.width()) +
            ' x ' + str(self.parent.my_canvas.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        self.parent.informWin.show()
        self.parent.MyWaitLock(True)
        self.parent.MyLock(self.parent.param1, self.parent.param2, self.parent.param3, self.parent.param4)
        self.parent.MyWaitLock(False)
        self.parent.informWin.hide()


    def doCancel(self):
        self.hide()
        self.parent.my_canvas.isLock = (self.parent.my_canvas.isLock == False)
        self.parent.MyDisable(self.parent.my_canvas.isLock)
        self.parent.statusBar.showMessage(
            '(0,0)像素      状态: 空闲                   画板大小:' + str(self.parent.my_canvas.width()) +
            ' x ' + str(self.parent.my_canvas.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

