#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import cg_algorithms as alg
import Figure as fig
import numpy as np
from PIL import Image
import copy
import math

class CliConrtol:
    def __init__(self, in_addr,out_addr):
        self.in_addr=in_addr
        self.out_addr=out_addr
        self.item_dict={}
        self.pen_color = np.zeros(3, np.uint8)
        self.width = 0
        self.height = 0
        self.cli_alg=alg.MyAlgorithms()

    def Work(self):
        with open(self.in_addr, 'r') as fp:
            line = fp.readline()
            while line:
                self.ParseLine(line)
                line = fp.readline()

    def ResetCanvas(self,width,height):
        self.width = width
        self.height = height
        self.item_dict={}
    def SaveCanvas(self,save_name):
        canvas = np.zeros([self.height, self.width, 3], np.uint8)
        canvas.fill(255)
        painted_point = []
        for fig_v in self.item_dict.values():
            if fig_v.figure_type == fig.FigureType.DDALine:
                self.cli_alg.DrawingLineDDA(painted_point, fig_v)

            elif fig_v.figure_type == fig.FigureType.BresenhamLine:
                self.cli_alg.DrawingLineBresenham(painted_point,fig_v)
            elif fig_v.figure_type == fig.FigureType.DDAPolygon:
                self.cli_alg.DrawingPolygonDDA(painted_point,fig_v)
            elif fig_v.figure_type == fig.FigureType.BresenhamPolygon:
                self.cli_alg.DrawingPolygonBresenham(painted_point,fig_v)
            elif fig_v.figure_type==fig.FigureType.Oval:
                self.cli_alg.DrawingOval(painted_point,fig_v)
            elif fig_v.figure_type==fig.FigureType.Bezier:
                self.cli_alg.DrawingBezier(painted_point,fig_v)
            elif fig_v.figure_type==fig.FigureType.B_spline:
                self.cli_alg.DrawingB_spline(painted_point,fig_v)

        for j in range(0, len(painted_point)):
            tmpx = painted_point[j][0]
            tmpy = self.height-1-painted_point[j][1]
            r = painted_point[j][2]
            g = painted_point[j][3]
            b = painted_point[j][4]
            if (0 <= tmpx and tmpx < self.width and 0 <= tmpy and tmpy < self.height):
                canvas[tmpy, tmpx] = [r, g, b]
        Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')

    def SetColor(self,r,g,b):
        self.pen_color[0] = r
        self.pen_color[1] = g
        self.pen_color[2] = b

    def DrawLine(self,item_id,x0,y0,x1,y1,algorithm):
        if (algorithm == "DDA"):
            f_tmp = fig.MyLine(1)
        else:
            f_tmp = fig.MyLine(0)
        f_tmp.setFirstPoint(x0, y0)
        f_tmp.setSecondPoint(x1, y1)
        f_tmp.setColor(self.pen_color[0], self.pen_color[1], self.pen_color[2])
        f_tmp.isOperating = 0
        self.item_dict[item_id] = f_tmp

    def DrawPolygon(self,item_id,pointList,algorithm):
        if (algorithm == "DDA"):
            f_tmp = fig.MyPolygon(1)
        else:
            f_tmp = fig.MyPolygon(0)
        for p in pointList:
            f_tmp.addPoint(p[0],p[1])
        f_tmp.setColor(self.pen_color[0], self.pen_color[1], self.pen_color[2])
        f_tmp.isOperating = 0
        self.item_dict[item_id] = f_tmp

    def DrawOval(self,item_id,x0,y0,x1,y1):
        f_tmp=fig.MyOval()
        f_tmp.setFirstPoint(x0, y0)
        f_tmp.setSecondPoint(x1, y1)
        f_tmp.setColor(self.pen_color[0], self.pen_color[1], self.pen_color[2])
        f_tmp.isOperating = 0
        self.item_dict[item_id] = f_tmp

    def DrawCurve(self,item_id,pointList,algorithm):
        if (algorithm == "Bezier"):
            f_tmp = fig.MyCurve(1)
        else:
            f_tmp = fig.MyCurve(0)
        for p in pointList:
            f_tmp.addPoint(p[0],p[1])
        f_tmp.setColor(self.pen_color[0], self.pen_color[1], self.pen_color[2])
        f_tmp.isOperating = 0
        self.item_dict[item_id] = f_tmp

    def ParseLine(self,line):
        line = line.strip().split(' ')
        if line[0] == 'resetCanvas':
            self.ResetCanvas(int(line[1]),int(line[2]))
        elif line[0] == 'saveCanvas':
            self.SaveCanvas(line[1])
        elif line[0] == 'setColor':
            self.SetColor(int(line[1]),int(line[2]),int(line[3]))
        elif line[0] == 'drawLine':
            self.DrawLine(line[1],int(line[2]),int(line[3]),int(line[4]),int(line[5]),line[6])
        elif line[0] =='drawPolygon':
            pointList=[]
            i=2
            while(i<len(line)-1):
                pointList.append([int(line[i]),int(line[i+1])])
                i=i+2
            self.DrawPolygon(line[1],pointList,line[len(line)-1])
        elif line[0]=='drawEllipse':
            self.DrawOval(line[1],int(line[2]),int(line[3]),int(line[4]),int(line[5]))
        elif line[0]=='drawCurve':
            pointList = []
            i = 2
            while (i < len(line) - 1):
                pointList.append([int(line[i]), int(line[i + 1])])
                i = i + 2
            self.DrawCurve(line[1],pointList,line[len(line)-1])
        elif line[0]=='translate':
            self.item_dict[line[1]].MoveAlgorithms(int(line[2]),int(line[3]))
        elif line[0]=='rotate':
            p=fig.MyPoint()
            p.x=int(line[2])
            p.y=int(line[3])
            r=-1*int(line[4])
            pi=math.pi
            self.item_dict[line[1]].RotateAlgorithms(p,math.sin(pi*r/180),math.cos(pi*r/180))
        elif line[0]=='scale':
            p=fig.MyPoint()
            p.x=int(line[2])
            p.y=int(line[3])
            time=float(line[4])
            self.item_dict[line[1]].ScaleAlgorithms(p,time)
        elif line[0]=='clip':
            p1 = fig.MyPoint()
            p1.x = int(line[2])
            p1.y = int(line[3])
            p2 = fig.MyPoint()
            p2.x = int(line[4])
            p2.y = int(line[5])
            if line[6]=='Cohen-Sutherland':
                method=0
            else:
                method=1
            self.item_dict[line[1]].ClipAlgorithms(p1, p2,method)



if __name__ == '__main__':
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)
    cli_control = CliConrtol(input_file,output_dir)
    cli_control.Work()




