
#from PyQt5.QtWidgets import QLabel
#from PyQt5.QtGui import QPainter, QMouseEvent, QColor,QImage,QPixmap,qRgb,QColor
#from PyQt5.QtWidgets import (
#    QApplication,
#    QMainWindow,
#    qApp,
#    QGraphicsScene,
#    QGraphicsView,
#    QGraphicsItem,
#    QListWidget,
#    QHBoxLayout,
#    QWidget,
#    QLabel,
#    QStyleOptionGraphicsItem)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#import sys
from enum import Enum
from Figure import MyLine,DrawingProcess,FigureType,MyPolygon,MyOval,MyCurve,MyPoint,MyPencilFigure,MyBrushFigure,MyEraserFigure,MyCharactor
import copy
from PyQt5.QtWidgets import QMessageBox
from numpy import *
from pylab import *

class DrawingState(Enum):
    Free=0
    LineDDA_Ready=1
    LineDDA_Doing=2
    LineBresenham_Ready=3
    LineBresenham_Doing=4
    PolygonDDA_Ready=5
    PolygonDDA_Doing=6
    PolygonBresenham_Ready=7
    PolygonBresenham_Doing=8
    Oval_Ready=9
    Oval_Doing=10
    Bezier_Ready=11
    Bezier_Doing=12
    B_spline_Ready=13
    B_spline_Doing=14
    Move_Ready=15
    Move_Doing=16
    Rotate_Ready=17
    Rotate_Doing=18
    Scale_Ready=19
    Scale_Doing=20
    Cohen_Sutherland_Ready=21
    Cohen_Sutherland_Doing=22
    Liang_Barsky_Ready=23
    Liang_Barsky_Doing=24
    Rectangle_Ready=25
    Rectangle_Doing=26
    Triangle_Ready=27
    Triangle_Doing=28
    Pencil_Ready=29
    Pencil_Doing=30
    Brush_Ready=31
    Brush_Doing=32
    Eraser_Ready=33
    Eraser_Doing=34
    Choose_Ready=35
    Choose_Doing=36
    Fill_Ready=37
    Nicholl_Lee_Nicholl_Ready=38
    Nicholl_Lee_Nicholl_Doing=39
    Sutherland_Hodgeman_Ready=40
    Sutherland_Hodgeman_Doing=41
    Word_Ready=42

class MyCanvas(QLabel):
    def __init__(self, parent):
        super(QLabel, self).__init__()
        self.parent=parent
        self.penColor=QColor(0,0,0)
        self.thickNess=0
        self.currentChoose=-1
        self.centre_point=MyPoint()
        self.centre_use=0
        self.rect_use=0
        self.CopyFigure=0
        self.CopyUsed=0
        self.WordPosx=0
        self.WordPosy=0
        self.isLock=False

    def ChooseInitial(self,id):
        '''
        id          0           1      2         3              4               5
        meanning    move      rotate   scale     clip_Cohen     clip_Liang      choose
        '''
        index=self.parent.drawing_process.current_index

        if (index >= 0 ):
            leng = len(self.parent.drawing_process.record_list[index])
            if(leng>0):
                if(id==0):
                    self.parent.drawing_state = DrawingState.Move_Ready
                elif(id==1):
                    self.parent.drawing_state=DrawingState.Rotate_Ready
                    self.centre_use = 1
                    self.centre_point = self.parent.drawing_process.record_list[index][0].getCentre()
                elif (id == 2):
                    self.parent.drawing_state = DrawingState.Scale_Ready
                    self.centre_use = 1
                    self.centre_point = self.parent.drawing_process.record_list[index][0].getCentre()
                elif(id==3):
                    self.parent.drawing_state = DrawingState.Cohen_Sutherland_Ready
                elif(id==4):
                    self.parent.drawing_state = DrawingState.Liang_Barsky_Ready
                elif(id==5):
                    self.parent.drawing_state=DrawingState.Choose_Ready
                elif(id==6):
                    self.parent.drawing_state=DrawingState.Fill_Ready
                elif(id==7):
                    self.parent.drawing_state=DrawingState.Nicholl_Lee_Nicholl_Ready
                elif(id==8):
                    self.parent.drawing_state=DrawingState.Sutherland_Hodgeman_Ready

                self.parent.statusBar.showMessage('(0,0)像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                           ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
                self.currentChoose = 0
                self.parent.drawing_process.record_list[index][0].isOperating=1
                self.MyFresh(index)
        else:
            self.currentChoose = -1
            self.MyFresh(index)
            self.parent.drawing_state = DrawingState.Free
            self.parent.statusBar.showMessage(
                '(0,0)像素      状态: 空闲                   画板大小:' + str(self.width()) +
                ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))

            QMessageBox.about(self, '提示', '没有可操作的图元')


    def ChooseNext(self,id):
        index = self.parent.drawing_process.current_index
        if (index >= 0):
            leng = len(self.parent.drawing_process.record_list[index])
            if(leng>0):
                self.parent.drawing_process.record_list[index][self.currentChoose].isOperating = 0
                self.currentChoose =(self.currentChoose+1) %leng
                self.parent.drawing_process.record_list[index][self.currentChoose].isOperating = 1
                if (id == 1 or id==2):
                    self.centre_point = self.parent.drawing_process.record_list[index][self.currentChoose].getCentre()
                self.MyFresh(index)
        else:
            self.currentChoose = -1

    def ChooseLast(self,id):
        index = self.parent.drawing_process.current_index
        if (index >= 0):
            leng = len(self.parent.drawing_process.record_list[index])
            if(leng>0):
                self.parent.drawing_process.record_list[index][self.currentChoose].isOperating = 0
                self.currentChoose = (self.currentChoose +leng- 1) % leng
                self.parent.drawing_process.record_list[index][self.currentChoose].isOperating = 1
                if (id == 1 or id==2):
                    self.centre_point = self.parent.drawing_process.record_list[index][self.currentChoose].getCentre()
                self.MyFresh(index)
        else:
            self.currentChoose = -1



    def ChooseEnd(self,id):
        index = self.parent.drawing_process.current_index
        if(self.currentChoose!=-1 and index>=0):
            self.parent.drawing_process.record_list[index][self.currentChoose].isOperating = 0
            self.currentChoose=-1
            self.centre_use=0
            self.MyFresh(index)
            self.parent.drawing_state = DrawingState.Free
            self.CopyUsed=0
            self.CopyFigure=0


    def MyFresh(self, index):
        #tmp_image =  QImage(self.width(),self.height(),QImage.Format_RGB32)
        #tmp_image.fill(QColor(255,255,255))
        self.parent.is_changed=1
        tmp_image=self.parent.background_image.copy()
        painted_point=[] #存放被画的点
        if(index==-1):
            pass
        elif(len(self.parent.drawing_process.record_list)>index):
            for i in range(0,len(self.parent.drawing_process.record_list[index])):
                if(self.parent.drawing_process.record_list[index][i].figure_type==FigureType.DDALine):
                    self.parent.my_algorithms.DrawingLineDDA(painted_point, self.parent.drawing_process.record_list[index][i])
                elif(self.parent.drawing_process.record_list[index][i].figure_type==FigureType.BresenhamLine):
                    self.parent.my_algorithms.DrawingLineBresenham(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.DDAPolygon):
                    self.parent.my_algorithms.DrawingPolygonDDA(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.BresenhamPolygon):
                    self.parent.my_algorithms.DrawingPolygonBresenham(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.Oval):
                    self.parent.my_algorithms.DrawingOval(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.Bezier):
                    self.parent.my_algorithms.DrawingBezier(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.B_spline):
                    self.parent.my_algorithms.DrawingB_spline(painted_point,self.parent.drawing_process.record_list[index][i])
                elif(self.parent.drawing_process.record_list[index][i].figure_type == FigureType.Pencil_Figure):
                    self.parent.my_algorithms.DrawingPencilFigure(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.Brush_Figure):
                    self.parent.my_algorithms.DrawingBrushFigure(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.Eraser_Figure):
                    self.parent.my_algorithms.DrawingEraserFigure(painted_point,self.parent.drawing_process.record_list[index][i])
                elif (self.parent.drawing_process.record_list[index][i].figure_type == FigureType.Charactor):
                    self.parent.my_algorithms.DrawingCharactor(painted_point,self.parent.drawing_process.record_list[index][i])
            #中心点的显示
            if self.centre_use:
                for x in range(-3, 3):
                    for y in range(-3, 3):
                        painted_point.append([self.centre_point.x + x, self.centre_point.y + y, 255, 0, 0])

            #裁剪矩形的显示
            if self.rect_use:
                tmp_pol=MyPolygon(0)
                tmp_pol.setColor(255,0,0)
                tmp_pol.isOperating=0
                curr_fig=copy.deepcopy(self.parent.drawing_process.record_list[index][self.currentChoose])
                xa=curr_fig.op_first_point.x
                ya=curr_fig.op_first_point.y
                xb=curr_fig.op_second_point.x
                yb=curr_fig.op_second_point.y
                tmp_pol.addPoint(xa,ya)
                tmp_pol.addPoint(xb,ya)
                tmp_pol.addPoint(xb,yb)
                tmp_pol.addPoint(xa,yb)
                self.parent.my_algorithms.DrawingPolygonBresenham(painted_point,tmp_pol)

            for j in range(0,len(painted_point)):
                tmpx=painted_point[j][0]
                tmpy=painted_point[j][1]
                r=painted_point[j][2]
                g=painted_point[j][3]
                b=painted_point[j][4]
                if (0 <= tmpx and tmpx < self.width() and 0 <= tmpy and tmpy < self.height()):
                    tmp_image.setPixel(tmpx,tmpy,qRgb(r,g,b))

        self.setPixmap(QPixmap().fromImage(tmp_image))

    def mousePressEvent(self, event):
        s=event.localPos()
        if (self.parent.drawing_state == DrawingState.Free):
            if self.isLock==False:
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 空闲                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
            else:
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 加密(禁用大部分功能，但可以保存画板)                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))


        elif(self.parent.drawing_state == DrawingState.LineDDA_Ready):
            tmp = MyLine(1)
            tmp.setColor(self.penColor.red(),self.penColor.green(),self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.setFirstPoint(int(s.x()), int(s.y()))
            if(len(self.parent.drawing_process.record_list)!=1+self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if(self.parent.drawing_process.current_index==-1):
                record_tmp=[]
            else:
                record_tmp=copy.deepcopy(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.LineDDA_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif(self.parent.drawing_state == DrawingState.LineDDA_Doing):
            pass #print("状态机DDA有问题")

        elif (self.parent.drawing_state == DrawingState.LineBresenham_Ready):
            tmp = MyLine(0)
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.setFirstPoint(int(s.x()), int(s.y()))
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.LineBresenham_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.LineBresenham_Doing):
            pass #print("状态机Bresenham有问题")

        elif (self.parent.drawing_state == DrawingState.PolygonDDA_Ready):
            tmp = MyPolygon(1)
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))  # 起始点
            tmp.addPoint(int(s.x()), int(s.y()))  # 移动点，位置待确定
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.PolygonDDA_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons () == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.PolygonDDA_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][leng - 1].addPoint(
                int(s.x()), int(s.y()))
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.PolygonDDA_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][leng - 1].updatePoint(
                int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index = self.parent.drawing_process.current_index + 1
            self.parent.drawing_state = DrawingState.PolygonDDA_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.PolygonBresenham_Ready):
            tmp = MyPolygon(0)
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))  # 起始点
            tmp.addPoint(int(s.x()), int(s.y()))  # 移动点，位置待确定
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.PolygonBresenham_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons () == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.PolygonBresenham_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][leng - 1].addPoint(
                int(s.x()), int(s.y()))
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.PolygonBresenham_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][leng - 1].updatePoint(
              int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index = self.parent.drawing_process.current_index + 1
            self.parent.drawing_state = DrawingState.PolygonBresenham_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Rectangle_Ready):
            tmp = MyPolygon(0)
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))
            tmp.addPoint(int(s.x()), int(s.y()))
            tmp.addPoint(int(s.x()), int(s.y()))
            tmp.addPoint(int(s.x()), int(s.y()))
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Rectangle_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Rectangle_Doing):
            pass #print("状态机Rectangle有问题")
        elif (self.parent.drawing_state == DrawingState.Pencil_Ready):
            tmp = MyPencilFigure()
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Pencil_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Pencil_Doing):
            pass #print("状态机Pencil_Doing有问题")

        elif (self.parent.drawing_state == DrawingState.Brush_Ready):
            tmp = MyBrushFigure()
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Brush_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Brush_Doing):
            pass #print("状态机Brush_Doing有问题")

        elif (self.parent.drawing_state == DrawingState.Eraser_Ready):
            tmp = MyEraserFigure()
            tmp.setColor(255, 255,255)
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Eraser_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Eraser_Doing):
            pass #print("状态机Eraser_Doing有问题")

        elif (self.parent.drawing_state == DrawingState.Triangle_Ready):
            tmp = MyPolygon(0)
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))
            tmp.addPoint(int(s.x()), int(s.y()))
            tmp.addPoint(int(s.x()), int(s.y()))
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Triangle_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Triangle_Doing):
            pass #print("状态机Triangle有问题")

        elif (self.parent.drawing_state == DrawingState.Oval_Ready):
            tmp = MyOval()
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.setFirstPoint(int(s.x()), int(s.y()))
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Oval_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Oval_Doing):
            pass #print("状态机Oval有问题")

        elif (self.parent.drawing_state == DrawingState.Bezier_Ready):
            tmp = MyCurve(1)
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))  # 起始点
            tmp.addPoint(int(s.x()), int(s.y()))  # 移动点，位置待确定
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Bezier_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons () == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Bezier_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][leng - 1].addPoint(
                int(s.x()), int(s.y()))
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Bezier_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][leng - 1].updatePoint(
                int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index = self.parent.drawing_process.current_index + 1
            self.parent.drawing_state = DrawingState.Bezier_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.B_spline_Ready):
            tmp = MyCurve(0)
            tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
            tmp.setThickNess(self.thickNess)
            tmp.addPoint(int(s.x()), int(s.y()))  # 起始点
            tmp.addPoint(int(s.x()), int(s.y()))  # 移动点，位置待确定
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
            if (self.parent.drawing_process.current_index == -1):
                record_tmp = []
            else:
                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp.append(tmp)
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.B_spline_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.B_spline_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][leng - 1].addPoint(
                int(s.x()), int(s.y()))
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.B_spline_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updatePoint(
                int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index = self.parent.drawing_process.current_index + 1
            self.parent.drawing_state = DrawingState.B_spline_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Choose_Ready):
            if (self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type == FigureType.Charactor):
                QMessageBox.about(self, '提示', '无法调整字符')
            else:
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].setOpFirstPoint(s.x(), s.y())
                record_tmp[self.currentChoose].setOperatingPoint(s.x(), s.y())
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.parent.drawing_state = DrawingState.Choose_Doing
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Choose_Doing):
            pass  # print("状态机Choose图元有问题")
        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Choose_Ready):
            self.ChooseEnd(5)

        elif(event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Move_Ready):
            if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

            record_tmp = copy.deepcopy(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
            record_tmp[self.currentChoose].setOpFirstPoint(s.x(),s.y())
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][self.currentChoose].isOperating=0
            self.parent.drawing_process.record_list.append(record_tmp)
            self.parent.drawing_state = DrawingState.Move_Doing
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Move_Doing):
            pass #print("状态机Move图元有问题")

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Move_Ready):
            self.ChooseEnd(0)

        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Rotate_Ready):
            if(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type==FigureType.Oval):
                QMessageBox.about(self, '提示', '无法旋转椭圆')

            elif (self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type == FigureType.Charactor):
                QMessageBox.about(self, '提示', '无法旋转字符')

            else:
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].setOpFirstPoint(s.x(), s.y())
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.parent.drawing_state = DrawingState.Rotate_Doing
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                                ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Rotate_Doing):
            pass  # print("状态机Rotate图元有问题")

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Rotate_Ready):
            self.ChooseEnd(1)

        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Scale_Ready):
            if (self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type == FigureType.Charactor):
                QMessageBox.about(self, '提示', '无法放缩字符')
            else:
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].setOpFirstPoint(s.x(), s.y())
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.parent.drawing_state = DrawingState.Scale_Doing
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))



        elif (self.parent.drawing_state == DrawingState.Scale_Doing):
            pass  # print("状态机Scale图元有问题")

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Scale_Ready):
            self.ChooseEnd(2)

        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            tp=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type
            if (not tp == FigureType.DDALine) and (not tp==FigureType.BresenhamLine):
                QMessageBox.about(self, '提示', '只能裁剪线段')

            else:
                self.rect_use=1
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].setOpFirstPoint(s.x(), s.y())
                record_tmp[self.currentChoose].setOpSecondPoint(s.x(), s.y())
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.parent.drawing_state = DrawingState.Cohen_Sutherland_Doing
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                                ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Cohen_Sutherland_Doing):
            pass  # print("状态机Cohen_Sutherland图元有问题")

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            self.ChooseEnd(3)

        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Liang_Barsky_Ready):
            tp=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type
            if (not tp == FigureType.DDALine) and (not tp==FigureType.BresenhamLine):
                QMessageBox.about(self, '提示', '只能裁剪线段')

            else:
                self.rect_use = 1
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].setOpFirstPoint(s.x(), s.y())
                record_tmp[self.currentChoose].setOpSecondPoint(s.x(), s.y())
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.parent.drawing_state = DrawingState.Liang_Barsky_Doing
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                                ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Liang_Barsky_Doing):
            pass  # print("状态机Liang_Barsky图元有问题")

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Liang_Barsky_Ready):
            self.ChooseEnd(4)


        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Fill_Ready):

            if (not self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][self.currentChoose].isClosed()):
                QMessageBox.about(self, '提示', '只能填充封闭图元')

            else:
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].isFilled = (record_tmp[self.currentChoose].isFilled==False)
                record_tmp[self.currentChoose].setFilledColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())

                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.MyFresh(self.parent.drawing_process.current_index + 1)
                self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                                  ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Fill_Ready):
            self.ChooseEnd(6)

        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            tp=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type
            if (not tp == FigureType.DDALine) and (not tp==FigureType.BresenhamLine):
                QMessageBox.about(self, '提示', '只能裁剪线段')

            else:
                self.rect_use = 1
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].setOpFirstPoint(s.x(), s.y())
                record_tmp[self.currentChoose].setOpSecondPoint(s.x(), s.y())
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.parent.drawing_state = DrawingState.Nicholl_Lee_Nicholl_Doing
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                                ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Doing):
            pass  # print("状态机Nicholl_Lee_Nicholl图元有问题")

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            self.ChooseEnd(7)
        elif (event.buttons() == QtCore.Qt.LeftButton and self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            tp=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                self.currentChoose].figure_type
            if (not tp == FigureType.DDAPolygon) and (not tp==FigureType.BresenhamPolygon):
                QMessageBox.about(self, '提示', '只能裁剪多边形')

            else:
                self.rect_use = 1
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]

                record_tmp = copy.deepcopy(
                    self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp[self.currentChoose].setOpFirstPoint(s.x(), s.y())
                record_tmp[self.currentChoose].setOpSecondPoint(s.x(), s.y())
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
                    self.currentChoose].isOperating = 0
                self.parent.drawing_process.record_list.append(record_tmp)
                self.parent.drawing_state = DrawingState.Sutherland_Hodgeman_Doing
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                                ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Doing):
            pass  # print("状态机Sutherland_Hodgeman图元有问题")

        elif (event.buttons() == QtCore.Qt.RightButton and self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            self.ChooseEnd(8)
        elif(self.parent.drawing_state==DrawingState.Word_Ready):
            self.WordPosx=int(s.x())
            self.WordPosy=int(s.y())
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 就绪       字符输出位置(' + str(self.WordPosx) + ',' + str(
                self.WordPosy) + ')                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))



    def mouseMoveEvent(self, event):
        s = event.localPos()
        if(self.parent.drawing_state==DrawingState.Free):
            if self.isLock == False:
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 空闲                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
            else:
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 加密(禁用大部分功能，但可以保存画板)                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))

        elif(self.parent.drawing_state==DrawingState.LineDDA_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
            ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.LineDDA_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 操作                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index+1][leng-1].setSecondPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index+1)
        elif (self.parent.drawing_state == DrawingState.LineBresenham_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.LineBresenham_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].setSecondPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.PolygonDDA_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.PolygonDDA_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updatePoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.PolygonBresenham_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.PolygonBresenham_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updatePoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Rectangle_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Rectangle_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            tmpx=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].getFirstPointX()
            tmpy=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].getFirstPointY()
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updateNPoint(int(s.x()), tmpy,2)

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updateNPoint(int(s.x()), int(s.y()),3)
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updatePoint(tmpx, int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)
        elif (self.parent.drawing_state == DrawingState.Pencil_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Pencil_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].addPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)
        elif (self.parent.drawing_state == DrawingState.Brush_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Brush_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].addPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Eraser_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Eraser_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].addPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Triangle_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Triangle_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            tmpx=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].getFirstPointX()
            tmpy=self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].getFirstPointY()
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updateNPoint(int(s.x()), tmpy,2)
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updatePoint(round((tmpx+int(s.x()))/2), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Oval_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Oval_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].setSecondPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Bezier_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Bezier_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updatePoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)
        elif (self.parent.drawing_state == DrawingState.B_spline_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.B_spline_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].updatePoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Choose_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Choose_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].MovePoint()

            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Move_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Move_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].MoveItem()
            self.MyFresh(self.parent.drawing_process.current_index + 1)
        elif (self.parent.drawing_state == DrawingState.Rotate_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Rotate_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].RotateItem(self.centre_point)

            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Scale_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Scale_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].ScaleItem(self.centre_point)

            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Cohen_Sutherland_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Liang_Barsky_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Liang_Barsky_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)
        elif (self.parent.drawing_state == DrawingState.Fill_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y())) +
                                              ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Doing):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 操作                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.MyFresh(self.parent.drawing_process.current_index + 1)

        elif (self.parent.drawing_state == DrawingState.Word_Ready):
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 就绪       字符输出位置(' + str(self.WordPosx) + ',' + str(
                self.WordPosy) + ')                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))


    def mouseReleaseEvent(self, event):
        s = event.localPos()
        if (self.parent.drawing_state == DrawingState.Free):
            if self.isLock == False:
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 空闲                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))
            else:
                self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                    int(s.y())) + ') 像素      状态: 加密(禁用大部分功能，但可以保存画板)                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.LineDDA_Ready):
            pass #print("状态机DDA有问题")
        elif (self.parent.drawing_state == DrawingState.LineDDA_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].setSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating=0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.LineDDA_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.LineBresenham_Ready):
            pass #print("状态机Bresenham有问题")
        elif (self.parent.drawing_state == DrawingState.LineBresenham_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].setSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.LineBresenham_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Rectangle_Ready):
            pass    #print("状态机Rectangle有问题")
        elif (self.parent.drawing_state == DrawingState.Rectangle_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Rectangle_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Pencil_Ready):
            pass    #print("状态机Pencil有问题")
        elif (self.parent.drawing_state == DrawingState.Pencil_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Pencil_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Brush_Ready):
            pass    #print("状态机Brush有问题")
        elif (self.parent.drawing_state == DrawingState.Brush_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Brush_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))
        elif (self.parent.drawing_state == DrawingState.Eraser_Ready):
            pass    #print("状态机Eraser有问题")
        elif (self.parent.drawing_state == DrawingState.Eraser_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Eraser_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))


        elif (self.parent.drawing_state == DrawingState.Triangle_Ready):
            pass  # print("状态机Triangle有问题")
        elif (self.parent.drawing_state == DrawingState.Triangle_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index = self.parent.drawing_process.current_index + 1
            self.parent.drawing_state = DrawingState.Triangle_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
                                              + ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))


        elif (self.parent.drawing_state == DrawingState.Oval_Ready):
            pass    #print("状态机Oval有问题")
        elif (self.parent.drawing_state == DrawingState.Oval_Doing):
            leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].setSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                leng - 1].isOperating = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Oval_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Choose_Ready):
            pass    #print("状态机Choose有问题") 也可能是按下了鼠标中间滑轮，啥都不用做

        elif (self.parent.drawing_state == DrawingState.Choose_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].MovePoint()
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Choose_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Move_Ready):
            pass    #print("状态机Move有问题") 也可能是按下了鼠标中间滑轮，啥都不用做

        elif (self.parent.drawing_state == DrawingState.Move_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].MoveItem()
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Move_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Rotate_Ready):
            pass    #可能是按下了鼠标中间滑轮，也可能是想旋转椭圆没成功，所以啥都不用做

        elif (self.parent.drawing_state == DrawingState.Rotate_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                    self.currentChoose].RotateItem(self.centre_point)

            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Rotate_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Scale_Ready):
            pass    #可能是按下了鼠标中间滑轮，所以啥都不用做

        elif (self.parent.drawing_state == DrawingState.Scale_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))

            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                    self.currentChoose].ScaleItem(self.centre_point)

            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Scale_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            pass    #print("状态机Cohen_Sutherland有问题") 也可能是按下了鼠标中间滑轮，啥都不用做

        elif (self.parent.drawing_state == DrawingState.Cohen_Sutherland_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].ClipItem(0)
            self.rect_use = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Cohen_Sutherland_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Liang_Barsky_Ready):
            pass    #print("状态机Liang_Barsky有问题") 也可能是按下了鼠标中间滑轮，啥都不用做

        elif (self.parent.drawing_state == DrawingState.Liang_Barsky_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].ClipItem(1)
            self.rect_use = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Liang_Barsky_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            pass    #print("状态机Nicholl_Lee_Nicholl有问题") 也可能是按下了鼠标中间滑轮，啥都不用做

        elif (self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].ClipItem(2)
            self.rect_use = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Nicholl_Lee_Nicholl_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            pass    #print("状态机Sutherland_Hodgeman有问题") 也可能是按下了鼠标中间滑轮，啥都不用做

        elif (self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Doing):
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].setOpSecondPoint(int(s.x()), int(s.y()))
            self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
                self.currentChoose].ClipItem(0)
            self.rect_use = 0
            self.MyFresh(self.parent.drawing_process.current_index + 1)
            self.parent.drawing_process.current_index=self.parent.drawing_process.current_index+1
            self.parent.drawing_state = DrawingState.Sutherland_Hodgeman_Ready
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(int(s.y()))
            + ') 像素      状态: 就绪                   画板大小:'+str(self.width())+
                                   ' x '+str(self.height())+'     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

        elif (self.parent.drawing_state == DrawingState.Word_Ready):
            self.WordPosx = int(s.x())
            self.WordPosy = int(s.y())
            self.parent.statusBar.showMessage('(' + str(int(s.x())) + ',' + str(
                int(s.y())) + ') 像素      状态: 就绪       字符输出位置(' + str(self.WordPosx) + ',' + str(
                self.WordPosy) + ')                   画板大小:' + str(self.width()) +
                                              ' x ' + str(self.height()) + '     操作序列' + str(
                self.parent.drawing_process.current_index + 1) + '/' + str(
                len(self.parent.drawing_process.record_list)))

    def FigureCopy(self):
        index = self.parent.drawing_process.current_index
        self.CopyFigure = self.parent.drawing_process.record_list[index][self.currentChoose]
        self.CopyUsed=1
        self.parent.statusBar.showMessage('(' + str(0) + ',' + str(0)
                                          + ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                          ' x ' + str(self.height()) + '     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)) + '已复制到粘贴板')

    def FigurePaste(self):
        if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
            del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
        if (self.parent.drawing_process.current_index == -1):
            record_tmp = []
        else:
            record_tmp = copy.deepcopy(
                self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
        self.parent.drawing_process.record_list[self.parent.drawing_process.current_index][
            self.currentChoose].isOperating = 0

        record_tmp.append(copy.deepcopy(self.CopyFigure))
        self.parent.drawing_process.record_list.append(record_tmp)
        leng = len(self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1])
        p = self.CopyFigure.getCentre()
        detax = round(self.width() / 2) - p.x
        detay = round(self.height() / 2) - p.y
        self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
            leng - 1].MoveAlgorithms(detax, detay)
        self.parent.drawing_process.record_list[self.parent.drawing_process.current_index + 1][
            leng - 1].isOperating = 0
        self.MyFresh(self.parent.drawing_process.current_index + 1)
        self.parent.drawing_process.current_index = self.parent.drawing_process.current_index + 1
        self.parent.statusBar.showMessage('(' + str(0) + ',' + str(0) +
                                          ') 像素      状态: 就绪                   画板大小:' + str(self.width()) +
                                          ' x ' + str(self.height()) + '     操作序列' + str(
            self.parent.drawing_process.current_index + 1) + '/' + str(
            len(self.parent.drawing_process.record_list)))

    def drawHist(self,tag):
        ImageTmp = QPixmap.toImage(self.pixmap())
        M = self.height()
        N = self.width()
        num=M*N
        arrayTmp=[]
        if tag==0:
            for i in range(0, num):
                r = QColor(ImageTmp.pixel(round(i % N), round(i / N))).red()
                arrayTmp.append(r)
        elif tag==1:
            for i in range(0, num):
                g = QColor(ImageTmp.pixel(round(i % N), round(i / N))).green()
                arrayTmp.append(g)
        else:
            for i in range(0, num):
                b = QColor(ImageTmp.pixel(round(i % N), round(i / N))).blue()
                arrayTmp.append(b)

        data=array(arrayTmp)
        # 对数据进行切片，将数据按照从最小值到最大值分组，分成20组
        bins = linspace(min(data), max(data), 20)

        # 这个是调用画直方图的函数，意思是把数据按照从bins的分割来画
        hist(data, bins)
        # 设置出横坐标
        xlabel('value of rgb')
        # 设置纵坐标的标题
        ylabel('frequency of rgb')
        # 设置整个图片的标题
        title('frequency distribute of rgb')

        # 展示出我们的图片
        print('平均', mean(data))

        print('方差', data.var())
        print('标准差', data.std())
        show()


    def MyKeyPressEvent(self, event):
        if(self.parent.drawing_state==DrawingState.Move_Ready):
            if event.key()==Qt.Key_A:
                self.ChooseLast(0)
            elif event.key()==Qt.Key_D:
                self.ChooseNext(0)

        elif (self.parent.drawing_state == DrawingState.Rotate_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(1)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(1)

        elif (self.parent.drawing_state == DrawingState.Scale_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(2)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(2)

        elif (self.parent.drawing_state == DrawingState.Cohen_Sutherland_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(3)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(3)

        elif (self.parent.drawing_state == DrawingState.Liang_Barsky_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(4)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(4)
        elif (self.parent.drawing_state == DrawingState.Choose_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(5)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(5)
            elif event.key()==Qt.Key_C:
                self.FigureCopy()
            elif event.key()==Qt.Key_V:
               self.FigurePaste()

        elif (self.parent.drawing_state == DrawingState.Fill_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(6)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(6)

        elif (self.parent.drawing_state == DrawingState.Nicholl_Lee_Nicholl_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(7)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(7)

        elif (self.parent.drawing_state == DrawingState.Sutherland_Hodgeman_Ready):
            if event.key() == Qt.Key_A:
                self.ChooseLast(8)
            elif event.key() == Qt.Key_D:
                self.ChooseNext(8)

        elif self.parent.drawing_state==DrawingState.Free:
            if event.key()==Qt.Key_R:
                self.drawHist(0)
            elif event.key()==Qt.Key_G:
                self.drawHist(1)
            elif event.key()==Qt.Key_B:
                self.drawHist(2)

        elif(self.parent.drawing_state==DrawingState.Word_Ready):
            legal=False
            if event.key() == Qt.Key_A:
                legal=True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 0)
            elif event.key()==Qt.Key_B:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 1)
            elif event.key()==Qt.Key_C:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 2)
            elif event.key()==Qt.Key_D:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 3)
            elif event.key()==Qt.Key_E:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 4)
            elif event.key()==Qt.Key_F:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 5)
            elif event.key()==Qt.Key_G:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 6)
            elif event.key()==Qt.Key_H:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 7)
            elif event.key()==Qt.Key_I:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 8)
            elif event.key()==Qt.Key_J:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 9)
            elif event.key()==Qt.Key_K:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 10)
            elif event.key()==Qt.Key_L:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 11)
            elif event.key()==Qt.Key_M:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 12)
            elif event.key()==Qt.Key_N:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 13)
            elif event.key()==Qt.Key_O:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 14)
            elif event.key()==Qt.Key_P:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 15)
            elif event.key()==Qt.Key_Q:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 16)
            elif event.key()==Qt.Key_R:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 17)
            elif event.key()==Qt.Key_S:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 18)
            elif event.key()==Qt.Key_T:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 19)
            elif event.key()==Qt.Key_U:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 20)
            elif event.key()==Qt.Key_V:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 21)
            elif event.key()==Qt.Key_W:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 22)
            elif event.key()==Qt.Key_X:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 23)
            elif event.key()==Qt.Key_Y:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 24)
            elif event.key()==Qt.Key_Z:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 25)
            elif event.key()==Qt.Key_0:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 0)
            elif event.key()==Qt.Key_1:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 1)
            elif event.key()==Qt.Key_2:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 2)
            elif event.key()==Qt.Key_3:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 3)
            elif event.key()==Qt.Key_4:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 4)
            elif event.key()==Qt.Key_5:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 5)
            elif event.key()==Qt.Key_6:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 6)
            elif event.key()==Qt.Key_7:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 7)
            elif event.key()==Qt.Key_8:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 8)
            elif event.key()==Qt.Key_9:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(1, 9)
            elif event.key()==Qt.Key_Space:
                legal = True
                tmp = MyCharactor()
                tmp.setColor(self.penColor.red(), self.penColor.green(), self.penColor.blue())
                tmp.setPos(self.WordPosx, self.WordPosy)
                tmp.setContent(0, 26)

            if legal:
                if (len(self.parent.drawing_process.record_list) != 1 + self.parent.drawing_process.current_index):
                    del self.parent.drawing_process.record_list[1 + self.parent.drawing_process.current_index:]
                if (self.parent.drawing_process.current_index == -1):
                    record_tmp = []
                else:
                    record_tmp = copy.deepcopy(
                        self.parent.drawing_process.record_list[self.parent.drawing_process.current_index])
                record_tmp.append(tmp)
                self.parent.drawing_process.record_list.append(record_tmp)
                self.WordPosx = self.WordPosx + 64
                if self.WordPosx >= self.width():
                    self.WordPosx = 0
                    self.WordPosy = self.WordPosy + 64
                    if self.WordPosy >= self.height():
                        self.WordPosy = 0
                self.MyFresh(self.parent.drawing_process.current_index + 1)
                self.parent.drawing_process.current_index = self.parent.drawing_process.current_index + 1
                self.parent.statusBar.showMessage('(' + str(0) + ',' + str(
                    0) + ') 像素      状态: 就绪       字符输出位置(' + str(self.WordPosx) + ',' + str(
                    self.WordPosy) + ')                   画板大小:' + str(self.width()) +
                                                  ' x ' + str(self.height()) + '     操作序列' + str(
                    self.parent.drawing_process.current_index + 1) + '/' + str(
                    len(self.parent.drawing_process.record_list)))






    def mouseDoubleClickEvent(self, event):
        s = event.localPos()
        if(self.parent.drawing_state==DrawingState.Rotate_Ready or self.parent.drawing_state==DrawingState.Scale_Ready):
            self.centre_point.x=s.x()
            self.centre_point.y=s.y()
            self.MyFresh(self.parent.drawing_process.current_index)
