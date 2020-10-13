import math
import copy
class FigureType():
    Unknown=0
    DDALine=1
    BresenhamLine=2
    DDAPolygon=3
    BresenhamPolygon=4
    Oval=5
    Bezier=6
    B_spline=7
    Pencil_Figure=8
    Brush_Figure=9
    Eraser_Figure=10
    Charactor=11

class MyPoint:
    def __init__(self):
        self.x=0
        self.y=0

    def X(self):
        return self.x

    def Y(self):
        return self.y


class MyFigure:
    def __init__(self):
        self.figure_type = FigureType.Unknown
        self.color_r=0
        self.color_g=0
        self.color_b=0
        self.isOperating=1
        self.op_first_point=MyPoint()
        self.op_second_point=MyPoint()
        self.thickNess=0
        self.operatingPoint=0
        self.isFilled=False
        self.filled_color_r=0
        self.filled_color_g = 0
        self.filled_color_b = 0

    def setOperatingPoint(self,x,y):
        pass

    def setColor(self,a,b,c):
        self.color_r=a
        self.color_g=b
        self.color_b=c

    def setFilledColor(self,a,b,c):
        self.filled_color_r = a
        self.filled_color_g = b
        self.filled_color_b = c

    def setThickNess(self,x):
        self.thickNess=round(x)

    def isAPoint(self):
        pass

    def setOpFirstPoint(self,a,b):
        self.op_first_point.x=  round(a)
        self.op_first_point.y = round(b)

    def setOpSecondPoint(self,a,b):
        self.op_second_point.x=round(a)
        self.op_second_point.y = round(b)

    def FillAlgorithms(self,painted_point):
        pass

    def MovePoint(self):
        detaX = self.op_second_point.X() - self.op_first_point.X()
        detaY = self.op_second_point.Y() - self.op_first_point.Y()
        self.operatingPoint.x=round(self.operatingPoint.x+detaX)
        self.operatingPoint.y=round(self.operatingPoint.y+detaY)
        self.setOpFirstPoint(round(self.op_second_point.x), round(self.op_second_point.y))

    def MoveItem(self):
        detaX = self.op_second_point.X() - self.op_first_point.X()
        detaY = self.op_second_point.Y() - self.op_first_point.Y()
        self.MoveAlgorithms(round(detaX), round(detaY))
        self.setOpFirstPoint(round(self.op_second_point.x), round(self.op_second_point.y))

    def MoveAlgorithms(self,detaX,detaY):
        pass

    def getCentre(self):
        pass

    def RotateItem(self,centre_point):
        vec1_x=self.op_first_point.x-centre_point.x
        vec1_y=self.op_first_point.y-centre_point.y
        vec2_x=self.op_second_point.x-centre_point.x
        vec2_y=self.op_second_point.y-centre_point.y
        vec1_mold=math.sqrt(vec1_x*vec1_x+vec1_y*vec1_y)
        vec2_mold=math.sqrt(vec2_x*vec2_x+vec2_y*vec2_y)
        vec1_2_mold=vec1_mold*vec2_mold
        sin_angle=(vec1_x*vec2_y-vec2_x*vec1_y)/vec1_2_mold
        cos_angle=(vec1_x*vec2_x+vec1_y*vec2_y)/vec1_2_mold
        self.RotateAlgorithms(centre_point,sin_angle,cos_angle)
        self.setOpFirstPoint(round(self.op_second_point.x), round(self.op_second_point.y))

    def RotateAlgorithms(self,centre_point,sin_angle,cos_angle):
        pass

    def ScaleItem(self,centre_point):
        vec1_x=self.op_first_point.x-centre_point.x
        vec1_y=self.op_first_point.y-centre_point.y
        vec2_x=self.op_second_point.x-centre_point.x
        vec2_y=self.op_second_point.y-centre_point.y
        vec1_mold=math.sqrt(vec1_x*vec1_x+vec1_y*vec1_y)
        vec2_mold=math.sqrt(vec2_x*vec2_x+vec2_y*vec2_y)
        if(vec1_mold==0):
            time=1
        else:
            time=vec2_mold/vec1_mold
        self.ScaleAlgorithms(centre_point,time)
        self.setOpFirstPoint(round(self.op_second_point.x), round(self.op_second_point.y))

    def ScaleAlgorithms(self,centre_point,time):
        pass

    def ClipItem(self,method):
        #method==0 Cohen_Sutherland
        #method==1 liang_Barsky
        self.ClipAlgorithms(self.op_first_point,self.op_second_point,method)

    def ClipAlgorithms(self,point_a,point_b,method):
        pass

    def isClosed(self):
        pass

class MyLine(MyFigure):
    def __init__(self, isDDA):
        super(MyLine, self).__init__()
        self.first_point=MyPoint()
        self.second_point=MyPoint()

        if(isDDA==1):
            self.figure_type=FigureType.DDALine
        else:
            self.figure_type=FigureType.BresenhamLine

    def setOperatingPoint(self,x,y):
        detax=self.first_point.x - x
        detay=self.first_point.y - y
        s1=detax*detax+detay*detay
        detax = self.second_point.x - x
        detay = self.second_point.y - y
        s2 = detax * detax + detay * detay
        if s1<s2:
            self.operatingPoint=self.first_point
        else:
            self.operatingPoint=self.second_point


    def setFirstPoint(self,a,b):
        self.first_point.x=round(a)
        self.first_point.y=round(b)

    def setSecondPoint(self,a,b):
        self.second_point.x=round(a)
        self.second_point.y=round(b)

    def isAPoint(self):
        if(self.first_point.x==self.second_point.x and self.first_point.y==self.second_point.y):
            return True
        else:
            return False


    def MoveAlgorithms(self,detaX,detaY):
        self.first_point.x += round(detaX)
        self.first_point.y += round(detaY)
        self.second_point.x += round(detaX)
        self.second_point.y += round(detaY)


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=round((self.first_point.x+self.second_point.x)/2)
        rtn.y = round((self.first_point.y + self.second_point.y) / 2)
        return rtn

    def RotateAlgorithms(self,centre_point,sin_angle,cos_angle):
        x=self.first_point.x-centre_point.x
        y=self.first_point.y-centre_point.y
        self.first_point.x=round(centre_point.x+x*cos_angle-y*sin_angle)
        self.first_point.y=round(centre_point.y+x*sin_angle+y*cos_angle)
        x = self.second_point.x - centre_point.x
        y = self.second_point.y - centre_point.y
        self.second_point.x = round(centre_point.x + x * cos_angle - y * sin_angle)
        self.second_point.y = round(centre_point.y + x * sin_angle + y * cos_angle)

    def ScaleAlgorithms(self,centre_point,time):
        x = self.first_point.x - centre_point.x
        y = self.first_point.y - centre_point.y
        self.first_point.x = round(centre_point.x + x * time)
        self.first_point.y = round(centre_point.y + y * time)

        x = self.second_point.x - centre_point.x
        y = self.second_point.y - centre_point.y
        self.second_point.x = round(centre_point.x + x * time)
        self.second_point.y = round(centre_point.y + y * time)

    def computeCode(self,xmin,xmax,ymin,ymax,x0,y0):
        code=0
        if x0<xmin:
            code=code|1
        if x0>xmax:
            code=code|2
        if y0<ymin:
            code=code|4
        if y0>ymax:
            code=code|8

        return code

    def ClipAlgorithms(self, point_a, point_b,method):
        if (point_a.x > point_b.x):
            xmax = round(point_a.x)
            xmin = round(point_b.x)
        else:
            xmin = round(point_a.x)
            xmax = round(point_b.x)

        if (point_a.y > point_b.y):
            ymax = round(point_a.y)
            ymin = round(point_b.y)
        else:
            ymin = round(point_a.y)
            ymax = round(point_b.y)
        x0 = round(self.first_point.x)
        y0 = round(self.first_point.y)
        x1 = round(self.second_point.x)
        y1 = round(self.second_point.y)

        if (method == 0):
            # clip by Cohen Sutherland
            code0=self.computeCode(xmin,xmax,ymin,ymax,x0,y0)
            code1=self.computeCode(xmin,xmax,ymin,ymax,x1,y1)
            while(True):
                if(not (code0|code1)):
                    self.first_point.x = round(x0)
                    self.first_point.y = round(y0)
                    self.second_point.x = round(x1)
                    self.second_point.y = round(y1)
                    return
                elif(code0 & code1):
                    self.first_point.x = 0
                    self.first_point.y = 0
                    self.second_point.x = 0
                    self.second_point.y = 0
                    return
                else:
                    #可能有交点了
                    if code0:
                        if code0&1:
                            y0=y0+(y1-y0)*(xmin-x0)/(x1-x0)
                            x0=xmin
                        elif code0&2:
                            y0=y0+(y1-y0)*(xmax-x0)/(x1-x0)
                            x0=xmax
                        elif code0&4:
                            x0=x0+(x1-x0)*(ymin-y0)/(y1-y0)
                            y0=ymin
                        elif code0&8:
                            x0=x0+(x1-x0)*(ymax-y0)/(y1-y0)
                            y0=ymax

                    else:
                        if code1 & 1:
                            y1 = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                            x1 = xmin
                        elif code1 & 2:
                            y1 = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                            x1 = xmax
                        elif code1 & 4:
                            x1 = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                            y1 = ymin
                        elif code1 & 8:
                            x1 = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                            y1 = ymax
                    code0 = self.computeCode(xmin, xmax, ymin, ymax, x0, y0)
                    code1=  self.computeCode(xmin,xmax,ymin,ymax,x1,y1)

        elif (method==1):
            # clip by Liang Barsky
            # 0 1 2 3 左右下上
            p=[]
            p.append(x0-x1)
            p.append(-1*p[0])
            p.append(y0-y1)
            p.append(-1*p[2])
            q=[]
            q.append(x0-xmin)
            q.append(xmax-x0)
            q.append(y0-ymin)
            q.append(ymax-y0)
            u0=0
            u1=1
            isOut=False
            for i in range(0,4):
                #对四个边分别判断
                if p[i]<0:
                    #只可能是进入这个边内
                    u0=max(u0,q[i]/p[i])
                    if u0>u1:
                        #直线完全在界外
                        isOut=True
                        break
                elif p[i]>0:
                    #只可能是离开这个边
                    u1=min(u1,q[i]/p[i])
                    if u0>u1:
                        isOut=True
                        break
                elif q[i]<0:
                    #只可能是平行于这个边且在这个边以外
                    isOut=True
                    break
            if(isOut):
                self.first_point.x = 0
                self.first_point.y = 0
                self.second_point.x = 0
                self.second_point.y = 0
                return
            else:
                self.first_point.x = round(x0+u0*p[1])
                self.first_point.y = round(y0+u0*p[3])
                self.second_point.x = round(x0+u1*p[1])
                self.second_point.y = round(y0+u1*p[3])
                return
        else:
            # clip by Nicholl Lee Nicholl
            code0 = self.computeCode(xmin, xmax, ymin, ymax, x0, y0)
            code1 = self.computeCode(xmin, xmax, ymin, ymax, x1, y1)
            if (not (code0 | code1)):
                self.first_point.x = round(x0)
                self.first_point.y = round(y0)
                self.second_point.x = round(x1)
                self.second_point.y = round(y1)
                return
            elif (code0 & code1):
                self.first_point.x = 0
                self.first_point.y = 0
                self.second_point.x = 0
                self.second_point.y = 0
                return
            else:
                if code0==0 and x0>xmin and x0<xmax:
                    #第一种情况，第一个点在内部或上下界
                    k1=(ymax-y0)/(xmin-x0)
                    k2=(ymax-y0)/(xmax-x0)
                    k3=(ymin-y0)/(xmin-x0)
                    k4=(ymin-y0)/(xmax-x0)
                    if x0==x1 and y1>ymax:
                        self.setSecondPoint(x0,ymax)
                    elif x0==x1 and y1<ymin:
                        self.setSecondPoint(x0,ymin)
                    else:
                        k=(y1-y0)/(x1-x0)
                        if (k>=k2 or k<=k1)and y1>ymax:
                            self.setSecondPoint((ymax-y0)/k+x0,ymax)
                        elif k>k1 and k<k3 and x1<xmin:
                            self.setSecondPoint(xmin,k*(xmin-x0)+y0)
                        elif (k>=k3 or k<=k4) and y1<ymin:
                            self.setSecondPoint((ymin-y0)/k+x0,ymin)
                        elif k>k4 and k<k2 and x1>xmax:
                            self.setSecondPoint(xmax,k*(xmax-x0)+y0)
                elif code0==0 and x0==xmin:
                    #第二种情况，第一个点在左界
                    k2 = (ymax - y0) / (xmax - x0)
                    k4 = (ymin - y0) / (xmax - x0)
                    if x0 == x1 and y1 > ymax:
                        self.setSecondPoint(x0, ymax)
                    elif x0 == x1 and y1 < ymin:
                        self.setSecondPoint(x0, ymin)
                    else:
                        k = (y1 - y0) / (x1 - x0)
                        if k >= k2 and y1 > ymax:
                            self.setSecondPoint((ymax - y0) / k + x0, ymax)
                        elif x1 < xmin:
                            self.setSecondPoint(x0, y0)
                        elif k <= k4 and y1 < ymin:
                            self.setSecondPoint((ymin - y0) / k + x0, ymin)
                        elif k > k4 and k < k2 and x1 > xmax:
                            self.setSecondPoint(xmax, k * (xmax - x0) + y0)
                elif code0==0 and x0==xmax:
                    #第三种情况，第一个点在右界
                    k1 = (ymax - y0) / (xmin - x0)
                    k3 = (ymin - y0) / (xmin - x0)
                    if x0 == x1 and y1 > ymax:
                        self.setSecondPoint(x0, ymax)
                    elif x0 == x1 and y1 < ymin:
                        self.setSecondPoint(x0, ymin)
                    else:
                        k = (y1 - y0) / (x1 - x0)
                        if k <= k1 and y1 > ymax:
                            self.setSecondPoint((ymax - y0) / k + x0, ymax)
                        elif k > k1 and k < k3 and x1 < xmin:
                            self.setSecondPoint(xmin, k * (xmin - x0) + y0)
                        elif k >= k3  and y1 < ymin:
                            self.setSecondPoint((ymin - y0) / k + x0, ymin)
                        elif x1 > xmax:
                            self.setSecondPoint(x0, y0)
                elif code0==1 or code0==2:
                    #第四个情况，第一个点在左边或右边，右边则先对称变换到左边
                    xc = round((xmin + xmax) / 2)
                    if code0==2:
                        x0=xc+xc-x0
                        x1=xc+xc-x1
                    k1 = (ymax - y0) / (xmin - x0)
                    k2 = (ymax - y0) / (xmax - x0)
                    k3 = (ymin - y0) / (xmin - x0)
                    k4 = (ymin - y0) / (xmax - x0)
                    k=(y1-y0)/(x1-x0)
                    if code1==0:
                        self.setFirstPoint(xmin,k*(xmin-x0)+y0)
                        self.setSecondPoint(x1,y1)
                    elif k>=k2 and k<=k1:
                        self.setFirstPoint(xmin,k*(xmin-x0)+y0)
                        self.setSecondPoint((ymax-y0)/k+x0,ymax)
                    elif k>k4 and k<k2:
                        self.setFirstPoint(xmin,k*(xmin-x0)+y0)
                        self.setSecondPoint(xmax,k*(xmax-x0)+y0)
                    elif k>=k3 and k<=k4:
                        self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                        self.setSecondPoint((ymin - y0) / k + x0, ymin)
                    else:
                        self.setFirstPoint(0,0)
                        self.setSecondPoint(0,0)
                    if code0==2:
                        x0 = xc + xc - self.first_point.x
                        x1 = xc + xc - self.second_point.x
                        self.setFirstPoint(x0,self.first_point.y)
                        self.setSecondPoint(x1,self.second_point.y)

                elif code0==4 or code0==8:
                    #第五个情况，第一个点在上边或下边，下边则先对称变换到上边，考虑第一个点在左边界延长线或右边界延长线情况
                    yc = round((ymin + ymax) / 2)
                    if code0 == 4:
                        y0 = yc + yc - y0
                        y1 = yc + yc - y1
                    if x0==xmin:
                        k2 = (ymax - y0) / (xmax - x0)
                        k4 = (ymin - y0) / (xmax - x0)
                        if x1 == x0:
                            if code1 == 0:
                                self.setFirstPoint(x0, ymax)
                                self.setSecondPoint(x1, y1)
                            else:
                                self.setFirstPoint(x0, ymax)
                                self.setSecondPoint(x1, ymin)
                        else:
                            k = (y1 - y0) / (x1 - x0)
                            if code1 == 0:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint(x1, y1)
                            elif k < k4:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint((ymin - y0) / k + x0, ymin)
                            elif k >= k4 and k <= k2:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint(xmax, k * (xmax - x0) + y0)
                            else:
                                self.setFirstPoint(0, 0)
                                self.setSecondPoint(0, 0)
                    elif x0==xmax:
                        k1 = (ymax - y0) / (xmin - x0)
                        k3 = (ymin - y0) / (xmin - x0)
                        if x1 == x0:
                            if code1 == 0:
                                self.setFirstPoint(x0, ymax)
                                self.setSecondPoint(x1, y1)
                            else:
                                self.setFirstPoint(x0, ymax)
                                self.setSecondPoint(x1, ymin)
                        else:
                            k = (y1 - y0) / (x1 - x0)
                            if code1 == 0:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint(x1, y1)
                            elif k <= k3 and k >= k1:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint(xmin, k * (xmin - x0) + y0)
                            elif k > k3:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint((ymin - y0) / k + x0, ymin)
                            else:
                                self.setFirstPoint(0, 0)
                                self.setSecondPoint(0, 0)
                    else:
                        k1 = (ymax - y0) / (xmin - x0)
                        k2 = (ymax - y0) / (xmax - x0)
                        k3 = (ymin - y0) / (xmin - x0)
                        k4 = (ymin - y0) / (xmax - x0)
                        if x1 == x0:
                            if code1 == 0:
                                self.setFirstPoint(x0, ymax)
                                self.setSecondPoint(x1, y1)
                            else:
                                self.setFirstPoint(x0, ymax)
                                self.setSecondPoint(x1, ymin)
                        else:
                            k = (y1 - y0) / (x1 - x0)
                            if code1 == 0:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint(x1, y1)
                            elif k <= k3 and k >= k1:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint(xmin, k * (xmin - x0) + y0)
                            elif k > k3 or k < k4:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint((ymin - y0) / k + x0, ymin)
                            elif k >= k4 and k <= k2:
                                self.setFirstPoint((ymax - y0) / k + x0, ymax)
                                self.setSecondPoint(xmax, k * (xmax - x0) + y0)
                            else:
                                self.setFirstPoint(0, 0)
                                self.setSecondPoint(0, 0)
                    if code0 == 4:
                        y0 = yc + yc - self.first_point.y
                        y1 = yc + yc - self.second_point.y
                        self.setFirstPoint(self.first_point.x, y0)
                        self.setSecondPoint(self.second_point.x, y1)

                elif code0==9 or code0==10 or code0==5 or code0==6:
                    #第六个情况，第一个点在左上角，左下角、右上角、右下角则变换到左上角
                    xc = round((xmin + xmax) / 2)
                    yc = round((ymin + ymax) / 2)
                    if code0==10 or code0==6:
                        x0=xc+xc-x0
                        x1=xc+xc-x1
                    if code0==5 or code0==6:
                        y0=yc+yc-y0
                        y1=yc+yc-y1
                    k1 = (ymax - y0) / (xmin - x0)
                    k2 = (ymax - y0) / (xmax - x0)
                    k3 = (ymin - y0) / (xmin - x0)
                    k4 = (ymin - y0) / (xmax - x0)
                    k=(y1-y0)/(x1-x0)
                    if k1>k4:
                        if code1 == 0 and k<=k1:
                            self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                            self.setSecondPoint(x1, y1)
                        elif code1==0 and k>k1:
                            self.setFirstPoint((ymax-y0)/k+x0, ymax)
                            self.setSecondPoint(x1, y1)
                        elif k>=k1 and k<=k2:
                            self.setFirstPoint((ymax - y0) / k + x0, ymax)
                            self.setSecondPoint(xmax, k * (xmax - x0) + y0)
                        elif k>k4 and k<k1:
                            self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                            self.setSecondPoint(xmax, k * (xmax - x0) + y0)
                        elif k>=k3 and k<=k4:
                            self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                            self.setSecondPoint((ymin - y0) / k + x0, ymin)
                        else:
                            self.setFirstPoint(0, 0)
                            self.setSecondPoint(0, 0)
                    elif k1==k4:
                        if code1 == 0 and k <= k1:
                            self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                            self.setSecondPoint(x1, y1)
                        elif code1 == 0 and k > k1:
                            self.setFirstPoint((ymax - y0) / k + x0, ymax)
                            self.setSecondPoint(x1, y1)
                        elif k >= k4 and k <= k2:
                            self.setFirstPoint((ymax - y0) / k + x0, ymax)
                            self.setSecondPoint(xmax, k * (xmax - x0) + y0)
                        elif k >= k3 and k <k4:
                            self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                            self.setSecondPoint((ymin - y0) / k + x0, ymin)
                        else:
                            self.setFirstPoint(0, 0)
                            self.setSecondPoint(0, 0)
                    else:
                        if code1 == 0 and k <= k1:
                            self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                            self.setSecondPoint(x1, y1)
                        elif code1 == 0 and k > k1:
                            self.setFirstPoint((ymax - y0) / k + x0, ymax)
                            self.setSecondPoint(x1, y1)
                        elif k >= k4 and k <= k2:
                            self.setFirstPoint((ymax - y0) / k + x0, ymax)
                            self.setSecondPoint(xmax, k * (xmax - x0) + y0)
                        elif k > k1 and k < k4:
                            self.setFirstPoint((ymax - y0) / k + x0, ymax)
                            self.setSecondPoint((ymin - y0) / k + x0, ymin)
                        elif k >= k3 and k <= k1:
                            self.setFirstPoint(xmin, k * (xmin - x0) + y0)
                            self.setSecondPoint((ymin - y0) / k + x0, ymin)
                        else:
                            self.setFirstPoint(0, 0)
                            self.setSecondPoint(0, 0)

                    if code0 == 10 or code0 == 6:
                        x0 = xc + xc - self.first_point.x
                        x1 = xc + xc - self.second_point.x
                        self.setFirstPoint(x0, self.first_point.y)
                        self.setSecondPoint(x1, self.second_point.y)

                    if code0 == 5 or code0 == 6:
                        y0 = yc + yc - self.first_point.y
                        y1 = yc + yc - self.second_point.y
                        self.setFirstPoint(self.first_point.x, y0)
                        self.setSecondPoint(self.second_point.x, y1)


    def isClosed(self):
        return False

class MyPolygon(MyFigure):
    def __init__(self, isDDA):
        super(MyPolygon, self).__init__()
        self.pointList=[]

        if(isDDA==1):
            self.figure_type=FigureType.DDAPolygon
        else:
            self.figure_type=FigureType.BresenhamPolygon

    def setOperatingPoint(self,x,y):
        smin=0
        for i in range(0,len(self.pointList)):
            detax = self.pointList[i].x - x
            detay = self.pointList[i].y - y
            s = detax * detax + detay * detay
            if i==0:
                self.operatingPoint=self.pointList[0]
                smin=s
            elif s<smin:
                self.operatingPoint=self.pointList[i]
                smin=s

    def addPoint(self,a,b):
        #添加新的数据点
        tmp=MyPoint()
        tmp.x=round(a)
        tmp.y=round(b)
        self.pointList.append(tmp)

    def getFirstPointX(self):
        return self.pointList[0].x

    def getFirstPointY(self):
        return self.pointList[0].y

    def updateNPoint(self,a,b,N):
        tmp = MyPoint()
        tmp.x = round(a)
        tmp.y = round(b)
        self.pointList[round(N - 1)] = tmp

    def updatePoint(self,a,b):
        #修改最后一个数据点
        num=len(self.pointList)
        tmp = MyPoint()
        tmp.x = round(a)
        tmp.y = round(b)
        self.pointList[num-1]=tmp

    def getLine(self,startIndex):
        if(self.figure_type==FigureType.DDAPolygon):
            tmp= MyLine(1)
        else: tmp=MyLine(0)
        num=len(self.pointList)
        tmp.setColor(self.color_r,self.color_g,self.color_b)
        tmp.setThickNess(self.thickNess)
        tmp.setFirstPoint(self.pointList[startIndex].X(),self.pointList[startIndex].Y())
        tmp.setSecondPoint(self.pointList[(startIndex+1)%num].X(), self.pointList[(startIndex+1)%num].Y())
        return tmp

    def isAPoint(self):
        for i in range(0,len(self.pointList)-1):
            if(self.pointList[i].x!=self.pointList[i+1].x or self.pointList[i].y!=self.pointList[i+1].y):
                return False
        return True

    def checkLeftValue(self,i):
        standard=self.pointList[i].y
        lengP=len(self.pointList)
        index=(lengP+i-1)%lengP
        while(not index==i):
            if not self.pointList[index].y==standard:
                return self.pointList[index].y
            index=(index-1+lengP)%lengP
        return standard

    def checkRightValue(self,i):
        standard = self.pointList[i].y
        lengP = len(self.pointList)
        index = (i + 1)%lengP
        while (not index == i):
            if not self.pointList[index].y == standard:
                return self.pointList[index].y
            index = (index + 1 ) % lengP
        return standard


    def FillAlgorithms(self,painted_point):
        #扫描转换填充算法
        #step1 getMinY and getMaxY
        minY=round(self.pointList[0].y)
        maxY=minY
        for i in range(1, len(self.pointList)):
            if self.pointList[i].y>maxY:
                maxY=round(self.pointList[i].y)
            elif self.pointList[i].y<minY:
                minY=round(self.pointList[i].y)

        #step2 initial Order Edge Table
        OET=[]
        for i in range(minY,maxY+1):
            OET.append([])
        lenP=len(self.pointList)
        for i in range(0,lenP):
            x1=self.pointList[i].x
            y1=self.pointList[i].y
            x2=self.pointList[(i+1)%lenP].x
            y2=self.pointList[(i+1)%lenP].y
            if y1<y2:
                kT=(x1-x2)/(y1-y2)
                if(self.checkLeftValue(i)<y1):
                    OET[y1+1-minY].append([y2,x1+kT,kT])
                else:
                    OET[y1-minY].append([y2,x1,kT])
            elif y1>y2:
                kT=(x1-x2)/(y1-y2)
                if(self.checkRightValue((i+1)%lenP)<y2):
                    OET[y2+1-minY].append([y1,x2+kT,kT])
                else:
                    OET[y2-minY].append([y1,x2,kT])
        #step3 fill from y=minY
        y=0
        LenY=maxY-minY+1
        while(y<LenY and len(OET[y])==0):
            y=y+1
        if(y==LenY):
            return
        #step4 initial Activity Edge Table
        AET=[]
        for i in range(0,len(OET[y])):
            #insert Sort
            if(len(AET)==0):
                AET.append(OET[y][i])
            else:
                insert_pos=len(AET)
                for j in range(0, len(AET)):
                    if(AET[j][1]>OET[y][i][1]):
                        insert_pos=j
                        break
                if insert_pos==len(AET):
                    AET.append(OET[y][i])
                else:
                    AET.insert(insert_pos,OET[y][i])
        #step5 do loop while AET is not empty
        while(len(AET)>0):
            #fill color at line y+YMin
            index=0
            while(index<len(AET)):
                for i in range(round(AET[index][1]),round(AET[index+1][1])+1):
                    painted_point.append([i,y+minY,self.filled_color_r,self.filled_color_g,self.filled_color_b])
                index=index+2
            #delete line not need later
            i=0
            while(i<len(AET)):
                if AET[i][0]==y+minY:
                    del AET[i]
                else:
                    i=i+1
            #compute next crossed point
            for i in range(0,len(AET)):
                tmp=copy.deepcopy(AET[i])
                del AET[i]
                tmp[1]=tmp[1]+tmp[2]
                if (len(AET) == 0):
                    AET.append(tmp)
                else:
                    insert_pos = i
                    for j in range(0, i):
                        if (AET[j][1] > tmp[1]):
                            insert_pos = j
                            break
                    AET.insert(insert_pos, tmp)
            #compute next y
            y=y+1
            if(y>maxY-minY):
                return

            #add new table into AET
            for i in range(0, len(OET[y])):
                # insert Sort
                if (len(AET) == 0):
                    AET.append(OET[y][i])
                else:
                    insert_pos = len(AET)
                    for j in range(0, len(AET)):
                        if (AET[j][1] > OET[y][i][1]):
                            insert_pos = j
                            break
                    if insert_pos == len(AET):
                        AET.append(OET[y][i])
                    else:
                        AET.insert(insert_pos, OET[y][i])
        return

    def isClosed(self):
        return len(self.pointList)>2


    def MoveAlgorithms(self,detaX,detaY):
        for i in range(0, len(self.pointList)):
            self.pointList[i].x += round(detaX)
            self.pointList[i].y += round(detaY)


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=0
        rtn.y=0
        leng=len(self.pointList)
        for i in range(0,leng):
            rtn.x +=self.pointList[i].x
            rtn.y +=self.pointList[i].y
        rtn.x=round(rtn.x/leng)
        rtn.y=round(rtn.y/leng)
        return rtn


    def RotateAlgorithms(self, centre_point, sin_angle, cos_angle):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * cos_angle - y * sin_angle)
            self.pointList[i].y = round(centre_point.y + x * sin_angle + y * cos_angle)

    def ScaleAlgorithms(self,centre_point,time):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * time)
            self.pointList[i].y = round(centre_point.y + y * time)

    def ClipAlgorithms(self, point_a, point_b,method):
        if (point_a.x > point_b.x):
            xmax = round(point_a.x)
            xmin = round(point_b.x)
        else:
            xmin = round(point_a.x)
            xmax = round(point_b.x)

        if (point_a.y > point_b.y):
            ymax = round(point_a.y)
            ymin = round(point_b.y)
        else:
            ymin = round(point_a.y)
            ymax = round(point_b.y)

        if method==0:
            #Sutherland_Hodgeman 多边形裁剪算法
            #step1 剪左边界
            List1=[]
            L=len(self.pointList)
            if(L>0):
                lastx=self.pointList[L-1].x
                lasty=self.pointList[L-1].y
                for i in range(0,len(self.pointList)):
                    if lastx<xmin:
                        if self.pointList[i].x<xmin:
                            pass
                        else:
                            k=(self.pointList[i].y-lasty)/(self.pointList[i].x-lastx)
                            q=MyPoint()
                            q.x=xmin
                            q.y=round(k*(xmin-lastx)+lasty)
                            List1.append(q)
                            List1.append(copy.deepcopy(self.pointList[i]))
                    else:
                        if self.pointList[i].x<xmin:
                            k = (self.pointList[i].y - lasty) / (self.pointList[i].x - lastx)
                            q = MyPoint()
                            q.x = xmin
                            q.y = round(k * (xmin - lastx) + lasty)
                            List1.append(q)
                        else:
                            List1.append(copy.deepcopy(self.pointList[i]))
                    lastx=self.pointList[i].x
                    lasty=self.pointList[i].y

            #step2 剪右边界
            List2=[]
            L = len(List1)
            if L>0:
                lastx = List1[L - 1].x
                lasty = List1[L - 1].y
                for i in range(0, len(List1)):
                    if lastx > xmax:
                        if List1[i].x > xmax:
                            pass
                        else:
                            k = (List1[i].y - lasty) / (List1[i].x - lastx)
                            q = MyPoint()
                            q.x = xmax
                            q.y = round(k * (xmax - lastx) + lasty)
                            List2.append(q)
                            List2.append(copy.deepcopy(List1[i]))
                    else:
                        if List1[i].x > xmax:
                            k = (List1[i].y - lasty) / (List1[i].x - lastx)
                            q = MyPoint()
                            q.x = xmax
                            q.y = round(k * (xmax - lastx) + lasty)
                            List2.append(q)
                        else:
                            List2.append(copy.deepcopy(List1[i]))
                    lastx = List1[i].x
                    lasty = List1[i].y

            #step3 剪上边界
            List3=[]
            L = len(List2)
            if L>0:
                lastx = List2[L - 1].x
                lasty = List2[L - 1].y
                for i in range(0, len(List2)):
                    if lasty > ymax:
                        if List2[i].y > ymax:
                            pass
                        else:
                            m = (List2[i].x - lastx) / (List2[i].y - lasty)
                            q = MyPoint()
                            q.x = round(m * (ymax - lasty) + lastx)
                            q.y = ymax
                            List3.append(q)
                            List3.append(copy.deepcopy(List2[i]))
                    else:
                        if List2[i].y > ymax:
                            m = (List2[i].x - lastx) / (List2[i].y - lasty)
                            q = MyPoint()
                            q.x = round(m * (ymax - lasty) + lastx)
                            q.y = ymax
                            List3.append(q)
                        else:
                            List3.append(copy.deepcopy(List2[i]))
                    lastx = List2[i].x
                    lasty = List2[i].y

            #step4 剪下边界
            List4=[]
            L = len(List3)
            if L>0:
                lastx = List3[L - 1].x
                lasty = List3[L - 1].y
                for i in range(0, len(List3)):
                    if lasty < ymin:
                        if List3[i].y < ymin:
                            pass
                        else:
                            m = (List3[i].x - lastx) / (List3[i].y - lasty)
                            q = MyPoint()
                            q.x = round(m * (ymin - lasty) + lastx)
                            q.y = ymin
                            List4.append(q)
                            List4.append(copy.deepcopy(List3[i]))

                    else:
                        if List3[i].y < ymin:
                            m = (List3[i].x - lastx) / (List3[i].y - lasty)
                            q = MyPoint()
                            q.x = round(m * (ymin - lasty) + lastx)
                            q.y = ymin
                            List4.append(q)
                        else:
                            List4.append(copy.deepcopy(List3[i]))
                    lastx=List3[i].x
                    lasty=List3[i].y
            self.pointList=List4

class MyPencilFigure(MyFigure):
    def __init__(self):
        super(MyPencilFigure, self).__init__()
        self.pointList=[]
        self.figure_type=FigureType.Pencil_Figure

    def setOperatingPoint(self,x,y):
        smin=0
        for i in range(0,len(self.pointList)):
            detax = self.pointList[i].x - x
            detay = self.pointList[i].y - y
            s = detax * detax + detay * detay
            if i==0:
                self.operatingPoint=self.pointList[0]
                smin=s
            elif s<smin:
                self.operatingPoint=self.pointList[i]
                smin=s

    def addPoint(self,a,b):
        #添加新的数据点
        tmp=MyPoint()
        tmp.x=round(a)
        tmp.y=round(b)
        self.pointList.append(tmp)

    def getLine(self,startIndex):
        if(self.figure_type==FigureType.DDAPolygon):
            tmp= MyLine(1)
        else: tmp=MyLine(0)
        num=len(self.pointList)
        tmp.setColor(self.color_r,self.color_g,self.color_b)
        tmp.setThickNess(self.thickNess)
        tmp.setFirstPoint(self.pointList[startIndex].X(),self.pointList[startIndex].Y())
        tmp.setSecondPoint(self.pointList[(startIndex+1)%num].X(), self.pointList[(startIndex+1)%num].Y())
        return tmp

    def isAPoint(self):
        for i in range(0,len(self.pointList)-1):
            if(self.pointList[i].x!=self.pointList[i+1].x or self.pointList[i].y!=self.pointList[i+1].y):
                return False
        return True

    def MoveAlgorithms(self,detaX,detaY):
        for i in range(0, len(self.pointList)):
            self.pointList[i].x += round(detaX)
            self.pointList[i].y += round(detaY)


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=0
        rtn.y=0
        leng=len(self.pointList)
        for i in range(0,leng):
            rtn.x +=self.pointList[i].x
            rtn.y +=self.pointList[i].y
        rtn.x=round(rtn.x/leng)
        rtn.y=round(rtn.y/leng)
        return rtn


    def RotateAlgorithms(self, centre_point, sin_angle, cos_angle):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * cos_angle - y * sin_angle)
            self.pointList[i].y = round(centre_point.y + x * sin_angle + y * cos_angle)

    def ScaleAlgorithms(self,centre_point,time):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * time)
            self.pointList[i].y = round(centre_point.y + y * time)

    def ClipAlgorithms(self, point_a, point_b,method):
        pass

    def isClosed(self):
        return False

class MyBrushFigure(MyFigure):
    def __init__(self):
        super(MyBrushFigure, self).__init__()
        self.pointList=[]
        self.figure_type=FigureType.Brush_Figure

    def setOperatingPoint(self,x,y):
        smin=0
        for i in range(0,len(self.pointList)):
            detax = self.pointList[i].x - x
            detay = self.pointList[i].y - y
            s = detax * detax + detay * detay
            if i==0:
                self.operatingPoint=self.pointList[0]
                smin=s
            elif s<smin:
                self.operatingPoint=self.pointList[i]
                smin=s

    def addPoint(self,a,b):
        #添加新的数据点
        tmp=MyPoint()
        tmp.x=round(a)
        tmp.y=round(b)
        self.pointList.append(tmp)

    def getLine(self,startIndex):
        if(self.figure_type==FigureType.DDAPolygon):
            tmp= MyLine(1)
        else: tmp=MyLine(0)
        num=len(self.pointList)
        tmp.setColor(self.color_r,self.color_g,self.color_b)
        tmp.setThickNess(self.thickNess+5)
        tmp.setFirstPoint(self.pointList[startIndex].X(),self.pointList[startIndex].Y())
        tmp.setSecondPoint(self.pointList[(startIndex+1)%num].X(), self.pointList[(startIndex+1)%num].Y())
        return tmp

    def isAPoint(self):
        for i in range(0,len(self.pointList)-1):
            if(self.pointList[i].x!=self.pointList[i+1].x or self.pointList[i].y!=self.pointList[i+1].y):
                return False
        return True

    def MoveAlgorithms(self,detaX,detaY):
        for i in range(0, len(self.pointList)):
            self.pointList[i].x += round(detaX)
            self.pointList[i].y += round(detaY)


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=0
        rtn.y=0
        leng=len(self.pointList)
        for i in range(0,leng):
            rtn.x +=self.pointList[i].x
            rtn.y +=self.pointList[i].y
        rtn.x=round(rtn.x/leng)
        rtn.y=round(rtn.y/leng)
        return rtn


    def RotateAlgorithms(self, centre_point, sin_angle, cos_angle):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * cos_angle - y * sin_angle)
            self.pointList[i].y = round(centre_point.y + x * sin_angle + y * cos_angle)

    def ScaleAlgorithms(self,centre_point,time):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * time)
            self.pointList[i].y = round(centre_point.y + y * time)

    def ClipAlgorithms(self, point_a, point_b,method):
        pass

    def isClosed(self):
        return False

class MyEraserFigure(MyFigure):
    def __init__(self):
        super(MyEraserFigure, self).__init__()
        self.pointList=[]
        self.figure_type=FigureType.Eraser_Figure

    def setOperatingPoint(self,x,y):
        smin=0
        for i in range(0,len(self.pointList)):
            detax = self.pointList[i].x - x
            detay = self.pointList[i].y - y
            s = detax * detax + detay * detay
            if i==0:
                self.operatingPoint=self.pointList[0]
                smin=s
            elif s<smin:
                self.operatingPoint=self.pointList[i]
                smin=s

    def addPoint(self,a,b):
        #添加新的数据点
        tmp=MyPoint()
        tmp.x=round(a)
        tmp.y=round(b)
        self.pointList.append(tmp)

    def getLine(self,startIndex):
        if(self.figure_type==FigureType.DDAPolygon):
            tmp= MyLine(1)
        else: tmp=MyLine(0)
        num=len(self.pointList)
        tmp.setColor(self.color_r,self.color_g,self.color_b)
        tmp.setThickNess(2*(self.thickNess+5))
        tmp.setFirstPoint(self.pointList[startIndex].X(),self.pointList[startIndex].Y())
        tmp.setSecondPoint(self.pointList[(startIndex+1)%num].X(), self.pointList[(startIndex+1)%num].Y())
        return tmp

    def isAPoint(self):
        for i in range(0,len(self.pointList)-1):
            if(self.pointList[i].x!=self.pointList[i+1].x or self.pointList[i].y!=self.pointList[i+1].y):
                return False
        return True

    def MoveAlgorithms(self,detaX,detaY):
        pass


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=0
        rtn.y=0
        leng=len(self.pointList)
        for i in range(0,leng):
            rtn.x +=self.pointList[i].x
            rtn.y +=self.pointList[i].y
        rtn.x=round(rtn.x/leng)
        rtn.y=round(rtn.y/leng)
        return rtn


    def RotateAlgorithms(self, centre_point, sin_angle, cos_angle):
        pass

    def ScaleAlgorithms(self,centre_point,time):
        pass

    def ClipAlgorithms(self, point_a, point_b,method):
        pass

    def isClosed(self):
        return False


class MyOval(MyFigure):
    def __init__(self):
        super(MyOval, self).__init__()
        self.first_point=MyPoint()
        self.second_point=MyPoint()
        self.figure_type=FigureType.Oval

    def setOperatingPoint(self,x,y):
        detax=self.first_point.x - x
        detay=self.first_point.y - y
        s1=detax*detax+detay*detay
        detax = self.second_point.x - x
        detay = self.second_point.y - y
        s2 = detax * detax + detay * detay
        if s1<s2:
            self.operatingPoint=self.first_point
        else:
            self.operatingPoint=self.second_point

    def setFirstPoint(self, a, b):
        self.first_point.x = round(a)
        self.first_point.y = round(b)

    def setSecondPoint(self, a, b):
        self.second_point.x = round(a)
        self.second_point.y = round(b)

    def isAPoint(self):
        if(self.first_point.x==self.second_point.x and self.first_point.y==self.second_point.y):
            return True
        else:
            return False

    def FillAlgorithms(self,painted_point):
        #区域种子填充算法
        Twoa=abs(self.second_point.x-self.first_point.x)
        Twob=abs(self.second_point.y-self.first_point.y)
        Twoa2=Twoa*Twoa
        Twob2=Twob*Twob
        if(Twoa==0 or Twob==0):
            return
        centerX=round((self.first_point.x+self.second_point.x)/2)
        centerY=round((self.first_point.y+self.second_point.y)/2)
        twoCenterX=centerX+centerX
        twoCenterY=centerY+centerY
        leftBound=0
        rightBound=0
        downBound=0
        upBound=0
        if(self.first_point.x<self.second_point.x):
            leftBound=self.first_point.x
            rightBound=self.second_point.x
        else:
            leftBound=self.second_point.x
            rightBound=self.first_point.x
        if(self.first_point.y<self.second_point.y):
            downBound=self.first_point.y
            upBound=self.second_point.y
        else:
            downBound=self.second_point.y
            upBound=self.first_point.y
        tagTable=[[0 for i in range(downBound,upBound+1)]for i in range(leftBound,rightBound+1)]
        PointStack=[]
        PointStack.append([centerX,centerY])
        while(len(PointStack)>0):
            tmp=PointStack.pop()
            detax=(tmp[0]-centerX)
            detay=(tmp[1]-centerY)
            detax2=detax*detax
            detay2=detay*detay
            value=detax2/Twoa2+detay2/Twob2
            if(4*value<=1):
                painted_point.append([tmp[0],tmp[1],self.filled_color_r,self.filled_color_g,self.filled_color_b])
                painted_point.append([twoCenterX-tmp[0], tmp[1], self.filled_color_r, self.filled_color_g, self.filled_color_b])
                painted_point.append([tmp[0], twoCenterY-tmp[1], self.filled_color_r, self.filled_color_g, self.filled_color_b])
                painted_point.append([twoCenterX-tmp[0], twoCenterY - tmp[1], self.filled_color_r, self.filled_color_g, self.filled_color_b])
                x=tmp[0]-leftBound
                y=tmp[1]-downBound
                tagTable[x][y]=1
                if x<Twoa and tagTable[x+1][y]==0:
                    PointStack.append([x+1+leftBound,y+downBound])
                if y<Twob and tagTable[x][y+1]==0:
                    PointStack.append([x+leftBound,y+1+downBound])

        return

    def MoveAlgorithms(self, detaX, detaY):
        self.first_point.x += round(detaX)
        self.first_point.y += round(detaY)
        self.second_point.x += round(detaX)
        self.second_point.y += round(detaY)


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=round((self.first_point.x+self.second_point.x)/2)
        rtn.y = round((self.first_point.y + self.second_point.y) / 2)
        return rtn

    def RotateAlgorithms(self, centre_point, sin_angle, cos_angle):
        pass

    def ScaleAlgorithms(self,centre_point,time):
        x = self.first_point.x - centre_point.x
        y = self.first_point.y - centre_point.y
        self.first_point.x = round(centre_point.x + x * time)
        self.first_point.y = round(centre_point.y + y * time)

        x = self.second_point.x - centre_point.x
        y = self.second_point.y - centre_point.y
        self.second_point.x = round(centre_point.x + x * time)
        self.second_point.y = round(centre_point.y + y * time)

    def ClipAlgorithms(self, point_a, point_b,method):
        pass

    def isClosed(self):
        return True

class MyCurve(MyFigure):
    def __init__(self, isBezier):
        super(MyCurve, self).__init__()
        self.pointList=[]
        if(isBezier==1):
            self.figure_type=FigureType.Bezier
        else:
            self.figure_type=FigureType.B_spline

    def setOperatingPoint(self,x,y):
        smin=0
        for i in range(0,len(self.pointList)):
            detax = self.pointList[i].x - x
            detay = self.pointList[i].y - y
            s = detax * detax + detay * detay
            if i==0:
                self.operatingPoint=self.pointList[0]
                smin=s
            elif s<smin:
                self.operatingPoint=self.pointList[i]
                smin=s



    def addPoint(self,a,b):
        #添加新的数据点
        tmp=MyPoint()
        tmp.x=round(a)
        tmp.y=round(b)
        self.pointList.append(tmp)

    def updatePoint(self,a,b):
        #修改最后一个数据点
        num=len(self.pointList)
        tmp = MyPoint()
        tmp.x = round(a)
        tmp.y = round(b)
        self.pointList[num-1]=tmp

    def isAPoint(self):
        for i in range(0,len(self.pointList)-1):
            if(self.pointList[i].x!=self.pointList[i+1].x or self.pointList[i].y!=self.pointList[i+1].y):
                return False
        return True

    def MoveAlgorithms(self, detaX, detaY):
        for i in range(0, len(self.pointList)):
            self.pointList[i].x += round(detaX)
            self.pointList[i].y += round(detaY)


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=0
        rtn.y=0
        leng=len(self.pointList)
        for i in range(0,leng):
            rtn.x +=self.pointList[i].x
            rtn.y +=self.pointList[i].y
        rtn.x=round(rtn.x/leng)
        rtn.y=round(rtn.y/leng)
        return rtn

    def RotateAlgorithms(self, centre_point, sin_angle, cos_angle):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * cos_angle - y * sin_angle)
            self.pointList[i].y = round(centre_point.y + x * sin_angle + y * cos_angle)

    def ScaleAlgorithms(self,centre_point,time):
        for i in range(0,len(self.pointList)):
            x=self.pointList[i].x-centre_point.x
            y=self.pointList[i].y-centre_point.y
            self.pointList[i].x = round(centre_point.x + x * time)
            self.pointList[i].y = round(centre_point.y + y * time)

    def ClipAlgorithms(self, point_a, point_b,method):
        pass

    def isClosed(self):
        return False


class MyCharactor(MyFigure):
    def __init__(self):
        super(MyCharactor, self).__init__()
        self.figure_type=FigureType.Charactor
        self.isNum=False
        self.id=0
        self.posx=0
        self.posy=0

    def setPos(self,a,b):
        self.posx=round(a)
        self.posy=round(b)

    def setContent(self,isNum,id):
        self.id=id
        self.isNum=isNum

    def MoveAlgorithms(self, detaX, detaY):
        self.posx += round(detaX)
        self.posy += round(detaY)


    def getCentre(self):
        rtn=MyPoint()
        rtn.x=0
        rtn.y=0
        rtn.x=round(self.posx)
        rtn.y=round(self.posy)
        return rtn

    def RotateAlgorithms(self, centre_point, sin_angle, cos_angle):
        pass

    def ScaleAlgorithms(self,centre_point,time):
        pass

    def ClipAlgorithms(self, point_a, point_b,method):
        pass

    def isClosed(self):
        return False

class DrawingProcess:
    def __init__(self):
        self.current_index=-1  #刚开始进度为空
        #self.board_process=[]  #存储每一步操作后的画板图片
        #self.figure_process=[] #存储每一步操作所绘制的图形
        self.record_list=[] #存储一个记录的列表，每个元素是一个记录，且每个记录是figure的列表

    def to_init(self):
        for i in range(0,len(self.record_list)):
            del self.record_list[i][0:]

        del self.record_list[0:]
        self.record_list=[]
        self.current_index=-1
