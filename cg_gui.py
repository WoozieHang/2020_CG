import sys
from mainwindow import *
import cg_algorithms as alg
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QLabel,
    QStyleOptionGraphicsItem,
    QScrollArea,
    QScrollBar,
    QHBoxLayout, QVBoxLayout,QPushButton,
    QFileDialog,QColorDialog,QMessageBox,QDialog
    )
from PyQt5.QtGui import QPainter, QMouseEvent, QColor,QPixmap,QImage,QIcon,qRgb
from PyQt5.QtCore import QRectF,Qt
from MyCanvas import MyCanvas, DrawingState
from Figure import DrawingProcess
from cg_algorithms import MyAlgorithms
from NewInputDialog import  NewInputDialog
from PIL import Image,ImageQt
from LockParamDialog import LockParamDialog
from InformDialog import  InformDialog,InformDialog2


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        #设置画板管理信息
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("画图")
        self.setWindowIcon(QIcon("resouce/ProgressIcon.png"))
        self.my_canvas = MyCanvas(self)
        self.my_canvas.setGeometry(0, 0, 2000, 1000)
        self.background_image =QImage(self.my_canvas.width(),self.my_canvas.height(),QImage.Format_RGB32)
        self.background_image.fill(QColor(255,255,255))
        self.file_address=""
        self.is_changed=0
        self.my_canvas.setPixmap(QPixmap.fromImage(self.background_image))
        #self.my_canvas.setStyleSheet("background-color:rgb(255,255,255)")
        self.my_canvas.setMouseTracking(True)
        self.scroll = QScrollArea(self.centralWidget)
        self.scroll.setWidget(self.my_canvas)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.centralWidget.setLayout(self.vbox)

        self.drawing_state = DrawingState.Free
        self.drawing_process = DrawingProcess()
        self.my_algorithms = MyAlgorithms()
        self.statusBar.showMessage('(0,0)像素      状态: 空闲                   画板大小:'+str(self.my_canvas.width())+
                                   ' x '+str(self.my_canvas.height())+'     操作序列' + str(
        self.drawing_process.current_index + 1) + '/' + str(
        len(self.drawing_process.record_list)))
        self.NewWin = NewInputDialog(self)
        self.param1=0
        self.param2=0
        self.param3=0
        self.param4=0
        self.LockParamWin=LockParamDialog(self)
        self.informWin=InformDialog(self)
        self.informWin.setGeometry(500,500,400,50)
        self.informWin2=InformDialog2(self)
        self.informWin2.setGeometry(500, 500, 400, 50)


    def synState(self):
        if (self.drawing_state == DrawingState.PolygonDDA_Doing):
            leng = len(self.drawing_process.record_list[self.drawing_process.current_index + 1])
            self.drawing_process.current_index = self.drawing_process.current_index + 1
            self.drawing_state = DrawingState.PolygonDDA_Ready
            self.drawing_process.record_list[self.drawing_process.current_index][leng-1].isOperating=0
            self.my_canvas.MyFresh(self.drawing_process.current_index)

        elif (self.drawing_state == DrawingState.PolygonBresenham_Doing):
            leng = len(self.drawing_process.record_list[self.drawing_process.current_index + 1])
            self.drawing_process.current_index = self.drawing_process.current_index + 1
            self.drawing_state = DrawingState.PolygonBresenham_Ready
            self.drawing_process.record_list[self.drawing_process.current_index][leng - 1].isOperating = 0
            self.my_canvas.MyFresh(self.drawing_process.current_index)
        elif (self.drawing_state == DrawingState.Bezier_Doing):
            leng = len(self.drawing_process.record_list[self.drawing_process.current_index + 1])
            self.drawing_process.current_index = self.drawing_process.current_index + 1
            self.drawing_state = DrawingState.Bezier_Ready
            self.drawing_process.record_list[self.drawing_process.current_index][leng - 1].isOperating = 0
            self.my_canvas.MyFresh(self.drawing_process.current_index)
        elif (self.drawing_state == DrawingState.B_spline_Doing):
            leng = len(self.drawing_process.record_list[self.drawing_process.current_index + 1])
            self.drawing_process.current_index = self.drawing_process.current_index + 1
            self.drawing_state = DrawingState.B_spline_Ready
            self.drawing_process.record_list[self.drawing_process.current_index][leng - 1].isOperating = 0
            self.my_canvas.MyFresh(self.drawing_process.current_index)
        elif(self.drawing_state==DrawingState.Move_Ready):
            self.my_canvas.ChooseEnd(0)
        elif(self.drawing_state==DrawingState.Rotate_Ready):
            self.my_canvas.ChooseEnd(1)
        elif (self.drawing_state == DrawingState.Scale_Ready):
            self.my_canvas.ChooseEnd(2)
        elif (self.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            self.my_canvas.ChooseEnd(3)
        elif (self.drawing_state == DrawingState.Liang_Barsky_Ready):
            self.my_canvas.ChooseEnd(4)
        elif (self.drawing_state == DrawingState.Choose_Ready):
            self.my_canvas.ChooseEnd(5)
        elif (self.drawing_state == DrawingState.Fill_Ready):
            self.my_canvas.ChooseEnd(6)
        elif (self.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            self.my_canvas.ChooseEnd(7)
        elif (self.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            self.my_canvas.ChooseEnd(8)


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.centralWidget.setMinimumSize(QtCore.QSize(self.width(), self.height()-116))
        self.centralWidget.setMaximumSize(QtCore.QSize(self.width(), self.height()-116))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.synState()
        if(self.is_changed==1):
            reply = QMessageBox.question(None, '提示', '是否保存画板？', QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save()
            else:
                pass
            self.is_changed=0


    @QtCore.pyqtSlot()
    def on_actionDDA_triggered(self):
        self.synState()
        self.drawing_state=DrawingState.LineDDA_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:'+str(self.my_canvas.width())+
                                   ' x '+str(self.my_canvas.height())+'     操作序列' + str(
        self.drawing_process.current_index + 1) + '/' + str(
        len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionBresenham_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.LineBresenham_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionDDA2_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.PolygonDDA_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionBresenham2_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.PolygonBresenham_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionRectangle_triggered(self):
        self.synState()
        self.drawing_state=DrawingState.Rectangle_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionPencil_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.Pencil_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionBrush_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.Brush_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionEraser_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.Eraser_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionTriangle_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.Triangle_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))


    @QtCore.pyqtSlot()
    def on_actionOval_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.Oval_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionBezier_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.Bezier_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionB_spline_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.B_spline_Ready
        self.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionWord_triggered(self):
        self.synState()
        self.drawing_state = DrawingState.Word_Ready
        self.my_canvas.WordPosx=0
        self.my_canvas.WordPosy=0
        self.statusBar.showMessage('(0,0)像素      状态: 就绪       字符输出位置(0,0)                   画板大小:' + str(self.my_canvas.width()) +
                                   ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionChoose_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(5)

    @QtCore.pyqtSlot()
    def on_actionFill_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(6)
    def MyDisable(self,check):
        self.actionNew.setDisabled(check)
        self.actionOpenFile.setDisabled(check)
        self.actionPencil.setDisabled(check)
        self.actionBrush.setDisabled(check)
        self.actionEraser.setDisabled(check)
        self.actionDDA.setDisabled(check)
        self.actionBresenham.setDisabled(check)
        self.actionDDA2.setDisabled(check)
        self.actionRectangle.setDisabled(check)
        self.actionTriangle.setDisabled(check)
        self.actionBresenham2.setDisabled(check)
        self.actionOval.setDisabled(check)
        self.actionBezier.setDisabled(check)
        self.actionB_spline.setDisabled(check)
        self.actionWord.setDisabled(check)
        self.actionColor.setDisabled(check)
        self.actionThick.setDisabled(check)
        self.actionNormal.setDisabled(check)
        self.actionThin.setDisabled(check)
        self.actionChoose.setDisabled(check)
        self.actionLast.setDisabled(check)
        self.actionNext.setDisabled(check)
        self.actionCopy.setDisabled(check)
        self.actionPaste.setDisabled(check)
        self.actionMove.setDisabled(check)
        self.actionRotate.setDisabled(check)
        self.actionScale.setDisabled(check)
        self.actionCohen_Sutherland.setDisabled(check)
        self.actionLiang_Barsky.setDisabled(check)
        self.actionNicholl_Lee_Nicholl.setDisabled(check)
        self.actionSutherland_Hodgeman.setDisabled(check)
        self.actionFill.setDisabled(check)
        self.actionUndo.setDisabled(check)
        self.actionRedo.setDisabled(check)
        self.actionClear.setDisabled(check)

    def MyWaitLock(self,check):
        self.actionSaveFile.setDisabled(check)
        self.actionSave_as.setDisabled(check)
        self.actionLock.setDisabled(check)


    def MyLock(self,x,u,gap,pos):
        ImageTmp=QPixmap.toImage(self.my_canvas.pixmap())
        M=self.my_canvas.height()
        N=self.my_canvas.width()
        #logistic 混沌序列
        #参数
        for i in range(0,5000):
            x=u*x*(1-x)
        sequence=[]
        sequence.append(x)
        for i in range(0,3*M*N):
            last=sequence[i]
            sequence.append(u*last*(1-last))
        #归一到255并混沌序列加密
        for i in range(0,M*N):
            sequence[3*i]=round(sequence[3*i]*255)
            sequence[3*i+1]=round(sequence[3*i+1]*255)
            sequence[3*i+2]=round(sequence[3*i+2]*255)

            c=QColor(ImageTmp.pixel(round(i%N),round(i/N)))
            r=int(c.red())^sequence[3*i]
            g=int(c.green())^sequence[3*i+1]
            b=int(c.blue())^sequence[3*i+2]

            ImageTmp.setPixel(round(i%N),round(i/N),qRgb(r,g,b))
        #约瑟夫置乱加密
        sequence = []
        tag=[i for i in range(0,M*N)]
        num=M*N
        pos = pos % (M * N)
        while(len(tag)>0):
            pos = (pos + gap - 1) % len(tag)
            sequence.append(tag[pos])
            del tag[pos]

        ImageTmpCp=ImageTmp.copy()
        for i in range(0,num):
            r=QColor(ImageTmpCp.pixel(round(sequence[i]%N),round(sequence[i]/N))).red()
            g=QColor(ImageTmpCp.pixel(round(sequence[i]%N),round(sequence[i]/N))).green()
            b=QColor(ImageTmpCp.pixel(round(sequence[i]%N),round(sequence[i]/N))).blue()
            ImageTmp.setPixel(round(i%N),round(i/N),qRgb(r,g,b))
        self.my_canvas.setPixmap(QPixmap().fromImage(ImageTmp))


    def MyUnLock(self,x,u,gap,pos):
        ImageTmp = QPixmap.toImage(self.my_canvas.pixmap())
        M = self.my_canvas.height()
        N = self.my_canvas.width()
        pos=pos%(M*N)
        # 约瑟夫置乱解密
        sequence = []
        tag = [i for i in range(0, M * N)]
        num = M * N
        while (len(tag) > 0):
            pos = (pos + gap - 1) % len(tag)
            sequence.append(tag[pos])
            del tag[pos]

        ImageTmpCp = ImageTmp.copy()
        for i in range(0, num):
            r = QColor(ImageTmpCp.pixel(round(i % N), round(i / N))).red()
            g = QColor(ImageTmpCp.pixel(round(i % N), round(i / N))).green()
            b =  QColor(ImageTmpCp.pixel(round(i % N), round(i / N))).blue()
            ImageTmp.setPixel(round(sequence[i] % N), round(sequence[i] / N) , qRgb(r, g, b))

        for i in range(0, 5000):
            x = u * x * (1 - x)
        sequence = []
        sequence.append(x)
        for i in range(0, 3 * M * N):
            last = sequence[i]
            sequence.append(u * last * (1 - last))
        for i in range(0, M * N):
            sequence[3 * i] = round(sequence[3 * i] * 255)
            sequence[3 * i + 1] = round(sequence[3 * i + 1] * 255)
            sequence[3 * i + 2] = round(sequence[3 * i + 2] * 255)
            c = QColor(ImageTmp.pixel(round(i % N), round(i / N)))
            r = int(c.red()) ^ sequence[3*i]
            g = int(c.green()) ^ sequence[3*i+1]
            b = int(c.blue()) ^ sequence[3*i+2]
            ImageTmp.setPixel(round(i % N), round(i / N), qRgb(r, g, b))
        self.my_canvas.setPixmap(QPixmap().fromImage(ImageTmp))
        #self.my_canvas.MyFresh(self.drawing_process.current_index)

    @QtCore.pyqtSlot()
    def on_actionLock_triggered(self):
        self.synState()
        self.drawing_state=DrawingState.Free
        self.my_canvas.isLock=(self.my_canvas.isLock==False)
        self.MyDisable(self.my_canvas.isLock)
        if self.my_canvas.isLock:
            self.LockParamWin.show()

        else:
            self.statusBar.showMessage(
                '(0,0)像素      状态: 空闲                   画板大小:' + str(self.my_canvas.width()) +
                ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
                    self.drawing_process.current_index + 1) + '/' + str(
                    len(self.drawing_process.record_list)))
            self.informWin2.show()
            self.MyUnLock(self.param1,self.param2,self.param3,self.param4)
            self.informWin2.hide()

    @QtCore.pyqtSlot()
    def on_actionCopy_triggered(self):
        if (self.drawing_state == DrawingState.Choose_Ready):
            self.my_canvas.FigureCopy()
        else:
            QMessageBox.about(self, '提示', '请先进入选择模式')

    @QtCore.pyqtSlot()
    def on_actionPaste_triggered(self):
        if (self.drawing_state == DrawingState.Choose_Ready):
            if (self.my_canvas.CopyUsed):
                self.my_canvas.FigurePaste()
            else:
                QMessageBox.about(self, '提示', '粘贴板为空')
        else:
            QMessageBox.about(self, '提示', '请先进入选择模式')

    @QtCore.pyqtSlot()
    def on_actionLast_triggered(self):
        if (self.drawing_state == DrawingState.Move_Ready):
            self.my_canvas.ChooseLast(0)
        elif (self.drawing_state == DrawingState.Rotate_Ready):
            self.my_canvas.ChooseLast(1)
        elif (self.drawing_state == DrawingState.Scale_Ready):
            self.my_canvas.ChooseLast(2)
        elif (self.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            self.my_canvas.ChooseLast(3)
        elif (self.drawing_state == DrawingState.Liang_Barsky_Ready):
            self.my_canvas.ChooseLast(4)
        elif (self.drawing_state == DrawingState.Choose_Ready):
            self.my_canvas.ChooseLast(5)
        elif (self.drawing_state == DrawingState.Fill_Ready):
            self.my_canvas.ChooseLast(6)
        elif (self.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            self.my_canvas.ChooseLast(7)
        elif (self.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            self.my_canvas.ChooseLast(8)

    @QtCore.pyqtSlot()
    def on_actionNext_triggered(self):
        if (self.drawing_state == DrawingState.Move_Ready):
            self.my_canvas.ChooseNext(0)
        elif (self.drawing_state == DrawingState.Rotate_Ready):
            self.my_canvas.ChooseNext(1)
        elif (self.drawing_state == DrawingState.Scale_Ready):
            self.my_canvas.ChooseNext(2)
        elif (self.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            self.my_canvas.ChooseNext(3)
        elif (self.drawing_state == DrawingState.Liang_Barsky_Ready):
            self.my_canvas.ChooseNext(4)
        elif (self.drawing_state == DrawingState.Choose_Ready):
            self.my_canvas.ChooseNext(5)
        elif (self.drawing_state == DrawingState.Fill_Ready):
            self.my_canvas.ChooseNext(6)
        elif (self.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            self.my_canvas.ChooseNext(7)
        elif (self.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            self.my_canvas.ChooseNext(8)

    @QtCore.pyqtSlot()
    def on_actionMove_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(0)

    @QtCore.pyqtSlot()
    def on_actionRotate_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(1)

    @QtCore.pyqtSlot()
    def on_actionScale_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(2)

    @QtCore.pyqtSlot()
    def on_actionCohen_Sutherland_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(3)

    @QtCore.pyqtSlot()
    def on_actionLiang_Barsky_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(4)

    @QtCore.pyqtSlot()
    def on_actionNicholl_Lee_Nicholl_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(7)

    @QtCore.pyqtSlot()
    def on_actionSutherland_Hodgeman_triggered(self):
        self.synState()
        self.my_canvas.ChooseInitial(8)


    @QtCore.pyqtSlot()
    def on_actionUndo_triggered(self):
        self.synState()
        if(self.drawing_process.current_index>=0):
            self.drawing_process.current_index-=1
            self.my_canvas.MyFresh(self.drawing_process.current_index)

        self.statusBar.showMessage('(0,0)像素      状态: 空闲                   画板大小:'+str(self.my_canvas.width())+
                                   ' x '+str(self.my_canvas.height())+'     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))


    @QtCore.pyqtSlot()
    def on_actionRedo_triggered(self):
        self.synState()
        if(self.drawing_process.current_index<len(self.drawing_process.record_list)-1):
            self.drawing_process.current_index+=1
            self.my_canvas.MyFresh(self.drawing_process.current_index)

        self.statusBar.showMessage('(0,0)像素      状态: 空闲                   画板大小:'+str(self.my_canvas.width())+
                                   ' x '+str(self.my_canvas.height())+'     操作序列' + str(
            self.drawing_process.current_index + 1) + '/' + str(
            len(self.drawing_process.record_list)))

    @QtCore.pyqtSlot()
    def on_actionNew_triggered(self):
        self.synState()
        if(self.is_changed==1):
            reply = QMessageBox.question(None, '提示', '是否保存画板？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save()
            else:
                pass
            self.is_changed=0
        self.NewWin.w_tmp = self.my_canvas.width()
        self.NewWin.h_tmp = self.my_canvas.height()
        self.NewWin.le1.setText(str(self.NewWin.w_tmp))
        self.NewWin.le2.setText(str(self.NewWin.h_tmp))
        self.NewWin.show()

    @QtCore.pyqtSlot()
    def on_actionSaveFile_triggered(self):
        self.synState()
        self.save()

    @QtCore.pyqtSlot()
    def on_actionSave_as_triggered(self):
        self.synState()
        self.save_as()

    @QtCore.pyqtSlot()
    def on_actionOpenFile_triggered(self):
        self.synState()
        if(self.is_changed==1):
            reply = QMessageBox.question(None, '提示', '是否保存画板？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save()
            else:
                pass
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "文件打开",
                                                                "./",
                                                                "Bitmap Files (*.bmp);;JPG (*.jpg);;PNG (*.png);;All Files (*)")  # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            #print("\n取消选择\n")
            return

        self.file_address = fileName_choose
        im=Image.open(self.file_address)
        self.resetByImage(ImageQt.ImageQt(im))
        self.is_changed = 0

    @QtCore.pyqtSlot()
    def on_actionClear_triggered(self):
        self.synState()
        self.drawing_process.to_init()
        self.drawing_state = DrawingState.Free
        self.my_canvas.MyFresh(self.drawing_process.current_index + 1)
        self.statusBar.showMessage(
            '(0,0)像素      状态: 空闲                   画板大小:' + str(self.my_canvas.width()) +
            ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
                self.drawing_process.current_index + 1) + '/' + str(
                len(self.drawing_process.record_list)))
        self.is_changed = 1

    @QtCore.pyqtSlot()
    def on_actionColor_triggered(self):
        self.synState()
        col=QColorDialog.getColor()
        self.my_canvas.penColor=col

    @QtCore.pyqtSlot()
    def on_actionThick_triggered(self):
        self.synState()
        self.my_canvas.thickNess =2

    @QtCore.pyqtSlot()
    def on_actionNormal_triggered(self):
        self.synState()
        self.my_canvas.thickNess = 1

    @QtCore.pyqtSlot()
    def on_actionThin_triggered(self):
        self.synState()
        self.my_canvas.thickNess = 0

    @QtCore.pyqtSlot()
    def on_actionExit_triggered(self):
        self.synState()
        if(self.is_changed==1):
            reply = QMessageBox.question(None, '提示', '是否保存画板？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save()
            else:
                pass
        self.is_changed=0
        sys.exit()

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        self.synState()
        QMessageBox.about(self, '关于\'画图\'', '版本1.0\n\n@2020 吴紫航。保留所有权利\n\n联系邮箱:401986905@qq.com\n\n地址:南京大学仙林校区\n')

    def resetByWH(self,w,h):
        self.my_canvas.setGeometry(0, 0, w, h)
        self.drawing_process.to_init()
        self.drawing_state = DrawingState.Free
        self.background_image = QImage(self.my_canvas.width(), self.my_canvas.height(), QImage.Format_RGB32)
        self.background_image.fill(QColor(255, 255, 255))
        self.my_canvas.MyFresh(self.drawing_process.current_index)
        self.file_address=[]
        self.statusBar.showMessage(
            '(0,0)像素      状态: 空闲                   画板大小:' + str(self.my_canvas.width()) +
            ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
                self.drawing_process.current_index + 1) + '/' + str(
                len(self.drawing_process.record_list)))
        self.is_changed = 0

    def resetByImage(self,openedImage):
        self.my_canvas.setGeometry(0, 0, openedImage.width(), openedImage.height())
        self.drawing_process.to_init()
        self.drawing_state = DrawingState.Free
        self.background_image = openedImage
        self.my_canvas.MyFresh(self.drawing_process.current_index)
        self.statusBar.showMessage(
            '(0,0)像素      状态: 空闲                   画板大小:' + str(self.my_canvas.width()) +
            ' x ' + str(self.my_canvas.height()) + '     操作序列' + str(
                self.drawing_process.current_index + 1) + '/' + str(
                len(self.drawing_process.record_list)))
        self.is_changed = 0

    def save_as(self):
            #另存为文件，并且将软件重新绑定图片文件路径
            fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "文件保存",
                                                                "./",
                                                                "Bitmap Files (*.bmp);;JPG (*.jpg);;PNG (*.png);;All Files (*)")
            if fileName_choose == "":
                #print("\n取消选择")
                return
            #print(fileName_choose)
            if fileName_choose.endswith("bmp")==False \
                and fileName_choose.endswith("BMP")==False \
                and fileName_choose.endswith("jpg")==False \
                and fileName_choose.endswith("JPG")==False \
                and fileName_choose.endswith("png") == False \
                and fileName_choose.endswith("PNG") == False:
                if filetype=="Bitmap Files (*.bmp)":
                    fileName_choose=fileName_choose+".bmp"
                elif filetype=="JPG (*.jpg)":
                    fileName_choose=fileName_choose+".jpg"
                elif filetype=="PNG (*.png)":
                    fileName_choose=fileName_choose+".png"
                else: fileName_choose=fileName_choose+".bmp"


            ImageQt.fromqpixmap(self.my_canvas.pixmap()).save(fileName_choose)
            self.file_address=fileName_choose
            self.is_changed = 0

    def save(self):
        #对参数的检查都在之前完成，假定此时参数都没错误
        if(len(self.file_address)==0):
            self.save_as()
        else:
            ImageQt.fromqpixmap(self.my_canvas.pixmap()).save(self.file_address)
            self.is_changed = 0

    def keyPressEvent(self, event):
        self.my_canvas.MyKeyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
