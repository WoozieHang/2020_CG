#from Figure import MyFigure,MyLine,MyPoint
import math
class MyAlgorithms:
    def DrawingLineDDA(self,painted_point,fig):
        if(fig.isOperating):
            interval=3
        else:interval=1

        count=0

        #print("dda")
        # 先求出斜率k
        point_a=fig.first_point
        point_b=fig.second_point

        if fig.isOperating:
            for x in range(-3, 3):
                for y in range(-3, 3):
                    painted_point.append([point_a.X() + x, point_a.Y() + y, 150, 150, 150])
                    painted_point.append([point_b.X() + x, point_b.Y() + y, 150, 150, 150])

        #一个点的情况
        if(fig.isAPoint()):
            for x in range(0,fig.thickNess+1):
                for y in range(0,fig.thickNess+1):
                    painted_point.append([point_a.X()+x,point_a.Y()+y,150,150,150])
            return

        #考虑斜率不存在的情况
        if(point_a.X()==point_b.X()):
            if(point_a.Y()<point_b.Y()):
                tmpx=point_a.X()
                tmpy=point_a.Y()
                dsty=point_b.Y()
            else:
                tmpx = point_b.X()
                tmpy = point_b.Y()
                dsty = point_a.Y()
            while (tmpy <= dsty):
                if(count%interval==0):
                    for x in range(0, fig.thickNess + 1):
                        for y in range(0, fig.thickNess + 1):
                            painted_point.append([tmpx+x,tmpy+y,fig.color_r,fig.color_g,fig.color_b])
                count = (count + 1) % interval
                tmpy = tmpy + 1
            return
        k = (0.0 + point_b.Y() - point_a.Y()) / (point_b.X() - point_a.X())
        #再考虑斜率的绝对值小于1的情况
        if(-1<=k and k<=1):
            if (point_a.X() < point_b.X()):
                tmpx = point_a.X()
                tmpy = point_a.Y()
                dstx = point_b.X()
            else:
                tmpx = point_b.X()
                tmpy = point_b.Y()
                dstx = point_a.X()
            while (tmpx <= dstx):
                if (count % interval == 0):
                    for x in range(0, fig.thickNess + 1):
                        for y in range(0, fig.thickNess + 1):
                            painted_point.append([tmpx+x,round(tmpy)+y,fig.color_r,fig.color_g,fig.color_b])
                count = (count + 1) % interval
                tmpx = tmpx+1
                tmpy = tmpy + k
        #最后是斜率绝对值大于1的情况
        else:
            if (point_a.Y() < point_b.Y()):
                tmpx = point_a.X()
                tmpy = point_a.Y()
                dsty = point_b.Y()
            else:
                tmpx = point_b.X()
                tmpy = point_b.Y()
                dsty = point_a.Y()
            while (tmpy <= dsty):
                if (count % interval == 0):
                    for x in range(0, fig.thickNess + 1):
                        for y in range(0, fig.thickNess + 1):
                            painted_point.append([round(tmpx)+x,tmpy+y,fig.color_r,fig.color_g,fig.color_b])
                count = (count + 1) % interval
                tmpx = tmpx + 1/k
                tmpy = tmpy + 1
        return


    def DrawingLineBresenham(self,painted_point,fig):
        #print("bresenham")
        # 先求出斜率k
        if (fig.isOperating):
            interval = 3
        else:
            interval = 1
        count = 0
        point_a = fig.first_point
        point_b = fig.second_point

        if fig.isOperating:
            for x in range(-3, 3):
                for y in range(-3, 3):
                    painted_point.append([point_a.X() + x, point_a.Y() + y, 150, 150, 150])
                    painted_point.append([point_b.X() + x, point_b.Y() + y, 150, 150, 150])

        #一个点的情况
        if(fig.isAPoint()):
            for x in range(0, fig.thickNess + 1):
                for y in range(0, fig.thickNess + 1):
                    painted_point.append([point_a.X()+x,point_a.Y()+y,150,150,150])
            return

        # 考虑斜率不存在的情况
        if (point_a.X() == point_b.X()):
            if (point_a.Y() < point_b.Y()):
                tmpx = point_a.X()
                tmpy = point_a.Y()
                dsty = point_b.Y()
            else:
                tmpx = point_b.X()
                tmpy = point_b.Y()
                dsty = point_a.Y()
            while (tmpy <= dsty):
                if (count % interval == 0):
                    for x in range(0, fig.thickNess + 1):
                        for y in range(0, fig.thickNess + 1):
                            painted_point.append([tmpx+x, tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                count = (count + 1) % interval
                tmpy = tmpy + 1
            return
        k = (0.0 + point_b.Y() - point_a.Y()) / (point_b.X() - point_a.X())
        # 再考虑斜率的绝对值小于1的情况
        if (-1 <= k and k <= 1):
            if (point_a.X() < point_b.X()):
                tmpx = point_a.X()
                tmpy = point_a.Y()
                dstx = point_b.X()
                dsty = point_b.Y()
            else:
                tmpx = point_b.X()
                tmpy = point_b.Y()
                dstx = point_a.X()
                dsty = point_a.Y()
            detax=abs(dstx-tmpx)
            detay=abs(dsty-tmpy)
            p=2*detay-detax
            deta=1
            if(dsty<tmpy):
                deta=-1
            #print(deta)
            while (tmpx <= dstx):
                if (count % interval == 0):
                    for x in range(0, fig.thickNess + 1):
                        for y in range(0, fig.thickNess + 1):
                            painted_point.append([tmpx+x, tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                count = (count + 1) % interval
                if(p>=0):
                    tmpy=tmpy+deta
                    p=p+2*detay-2*detax
                else:
                    p=p+2*detay
                tmpx = tmpx + 1

        # 最后是斜率绝对值大于1的情况
        else:
            if (point_a.Y() < point_b.Y()):
                tmpx = point_a.X()
                tmpy = point_a.Y()
                dsty = point_b.Y()
                dstx = point_b.X()
            else:
                tmpx = point_b.X()
                tmpy = point_b.Y()
                dsty = point_a.Y()
                dstx = point_a.X()
            detax = abs(dstx - tmpx)
            detay = abs(dsty - tmpy)
            p = 2 * detax - detay
            deta = 1
            if (dstx < tmpx):
                deta = -1
            while (tmpy <= dsty):
                if (count % interval == 0):
                    for x in range(0, fig.thickNess + 1):
                        for y in range(0, fig.thickNess + 1):
                            painted_point.append([tmpx+x, tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                count = (count + 1) % interval
                if (p >= 0):
                    tmpx = tmpx + deta
                    p = p + 2 * detax - 2 * detay
                else:
                    p = p + 2 * detax
                tmpy = tmpy + 1
        return

    def DrawingPolygonDDA(self,painted_point,fig):
        pNum=len(fig.pointList)
        for i in range(0,pNum):
            lineTmp=fig.getLine(i)
            lineTmp.isOperating=fig.isOperating
            self.DrawingLineDDA(painted_point,lineTmp)

        if fig.isFilled == True:
            fig.FillAlgorithms(painted_point)
        return

    def DrawingPolygonBresenham(self,painted_point,fig):
        pNum=len(fig.pointList)
        for i in range(0,pNum):
            lineTmp=fig.getLine(i)
            lineTmp.isOperating=fig.isOperating
            self.DrawingLineBresenham(painted_point,lineTmp)

        if fig.isFilled == True:
            fig.FillAlgorithms(painted_point)
        return

    def DrawingPencilFigure(self,painted_point,fig):
        pNum = len(fig.pointList)
        for i in range(0, pNum-1):
            lineTmp = fig.getLine(i)
            lineTmp.isOperating = fig.isOperating
            self.DrawingLineBresenham(painted_point, lineTmp)
        return

    def DrawingBrushFigure(self,painted_point,fig):
        pNum = len(fig.pointList)
        for i in range(0, pNum-1):
            lineTmp = fig.getLine(i)
            lineTmp.isOperating = fig.isOperating
            self.DrawingLineBresenham(painted_point, lineTmp)
        return

    def DrawingEraserFigure(self,painted_point,fig):
        pNum = len(fig.pointList)
        for i in range(0, pNum-1):
            lineTmp = fig.getLine(i)
            lineTmp.isOperating =fig.isOperating
            self.DrawingLineBresenham(painted_point, lineTmp)
        return

    def DrawingOval(self,painted_point,fig):
        if fig.isFilled == True:
            fig.FillAlgorithms(painted_point)

      #初始化
        if (fig.isOperating):
            interval = 3
            for x in range(-3, 3):
                for y in range(-3, 3):
                    painted_point.append([fig.first_point.X() + x, fig.first_point.Y() + y, 150, 150, 150])
                    painted_point.append([fig.second_point.X() + x, fig.second_point.Y() + y,  150, 150, 150])

        else:
            interval = 1

        #一个点的情况
        if(fig.isAPoint()):
            for x in range(0, fig.thickNess + 1):
                for y in range(0, fig.thickNess + 1):
                    painted_point.append([fig.first_point.X()+x,fig.first_point.Y()+y,150,150,150])
            return

        count = 0
        rx=round(0.5*abs((fig.first_point.X()-fig.second_point.X())))
        ry=round(0.5*abs((fig.first_point.Y()-fig.second_point.Y())))
        rx2=rx*rx
        ry2=ry*ry
        tworx2=2*rx2
        twory2=2*ry2
        xc=round(0.5*(fig.first_point.X()+fig.second_point.X()))
        yc=round(0.5*(fig.first_point.Y()+fig.second_point.Y()))

        #迭代点初始化
        tmpx=0
        tmpy=ry
        px=0
        py=tworx2*tmpy  #为了减少循环判断的乘法次数
        #决策参数初值
        pl=round(ry2-rx2*ry+rx2/4)
        #开始第一阶段迭代

        if (count % interval == 0):
            for x in range(0, fig.thickNess + 1):
                for y in range(0, fig.thickNess + 1):
                    painted_point.append([xc + tmpx+x, yc + tmpy+x, fig.color_r, fig.color_g, fig.color_b])
                    painted_point.append([xc + tmpx+y, yc - tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                    painted_point.append([xc - tmpx+y, yc + tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                    painted_point.append([xc - tmpx+x, yc - tmpy+y, fig.color_r, fig.color_g, fig.color_b])
        count = (count + 1) % interval
        while(px+twory2<py-(pl>=0)*tworx2):
            if(pl<0):
                tmpx=tmpx+1
                px=px+twory2
                pl=pl+px+ry2
            else:
                tmpx=tmpx+1
                px = px + twory2
                tmpy=tmpy-1
                py=py-tworx2
                pl = pl + px -py + ry2
            if (count % interval == 0):
                for x in range(0, fig.thickNess + 1):
                    for y in range(0, fig.thickNess + 1):
                        painted_point.append([xc + tmpx+x, yc + tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                        painted_point.append([xc + tmpx+x, yc - tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                        painted_point.append([xc - tmpx+x, yc + tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                        painted_point.append([xc - tmpx+x, yc - tmpy+y, fig.color_r, fig.color_g, fig.color_b])
            count = (count + 1) % interval
        #第二阶段初始化
        p=round(ry2*(tmpx+0.5)*(tmpx+0.5)+rx2*(tmpy-1)*(tmpy-1)-rx2*ry2)
        #开始第二阶段迭代
        while(tmpy>0):
            if (pl > 0):
                tmpy = tmpy - 1
                py = py - tworx2
                pl = pl - py + rx2
            else:
                tmpy = tmpy - 1
                py = py - tworx2
                tmpx = tmpx + 1
                px = px + twory2
                pl = pl + px - py + rx2
            if (count % interval == 0):
                for x in range(0, fig.thickNess + 1):
                    for y in range(0, fig.thickNess + 1):
                        painted_point.append([xc + tmpx+x, yc + tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                        painted_point.append([xc + tmpx+x, yc - tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                        painted_point.append([xc - tmpx+x, yc + tmpy+y, fig.color_r, fig.color_g, fig.color_b])
                        painted_point.append([xc - tmpx+x, yc - tmpy+y, fig.color_r, fig.color_g, fig.color_b])
            count = (count + 1) % interval
        return

    def com(self,a,b):
        sum=1
        if(b<a-b):
            b=a-b
        for i in range(b+1,a+1):
            sum=sum*i
        for i in range(1,a-b+1):
            sum=round(sum/i)

        return sum

    def DrawingBezier(self,painted_point,fig):
        n = len(fig.pointList)
        if fig.isOperating:
            m=n*30
            for i in range(0, n):
                for x in range(-3, 3):
                    for y in range(-3, 3):
                        painted_point.append([fig.pointList[i].X()+x,fig.pointList[i].Y()+y,150,150,150])
        else: m=n*300

        #一个点的情况
        if(fig.isAPoint()):
            for x in range(0, fig.thickNess + 1):
                for y in range(0, fig.thickNess + 1):
                    painted_point.append([fig.pointList[0].X()+x,fig.pointList[0].Y()+y,150,150,150])
            return

        for i in range(0,m+1):
           t=i/m
           tmp = math.pow(1-t,n - 1 )
           tmpx = tmp * fig.pointList[0].X()
           tmpy = tmp * fig.pointList[0].Y()
           for k in range(1, n):
               tmp = self.com(n - 1, k) * math.pow(t,k) * math.pow(1-t,n-1-k)
               tmpx = tmpx + tmp * fig.pointList[k].X()
               tmpy = tmpy + tmp * fig.pointList[k].Y()
           for x in range(0, fig.thickNess + 1):
               for y in range(0, fig.thickNess + 1):
                   painted_point.append([round(tmpx)+x, round(tmpy)+y, fig.color_r, fig.color_g, fig.color_b])

        return

    '''
    def B_spline_Base(self,u,i,k):
        #按书上的递归定义，输入u、i、k给出相应基函数的值
        #如果用矩阵的方式，就不用调用此递归函数，直接在矩阵中初始化好基函数
        if(k==1):
            if(i<=u and u<i+1):
                return 1
            else:
                return 0
        else:
            rtn=((u-i)/(k-1))*self.B_spline_Base(u,i,k-1)+((i+k-u)/(k-1))*self.B_spline_Base(u,i+1,k-1)
            return  rtn
            
    def DrawingB_spline(self, painted_point, fig):
        #书上的递归算法，比较通用，但是没必要，因为可以算出四阶均匀b样条的矩阵，计算复杂度低了很多
        k=4 #三次B样条4阶
        n=len(fig.pointList)
        if fig.isOperating:
            deta=0.01
            for i in range(0,n):
                for x in range(-3, 3):
                    for y in range(-3, 3):
                        painted_point.append([fig.pointList[i].X()+x,fig.pointList[i].Y()+y,150,150,150])
                        
        else: deta=0.0005*n
        
        #一个点的情况
        if(fig.isAPoint()):
            painted_point.append([fig.pointList[0].X(),fig.pointList[0].Y(),150,150,150])
            return 
            
        if n >= 4:
            u=k-1
            while(u<n):
                tmpx = 0
                tmpy = 0
                int_u=int(u)
                for i in range(int_u+1-k, int_u+1):
                    tmp = self.B_spline_Base(u,i,k)
                    tmpx = tmpx + tmp * fig.pointList[i].X()
                    tmpy = tmpy + tmp * fig.pointList[i].Y()
                if (not tmpx == 0) and (not tmpy == 0):
                    painted_point.append([round(tmpx), round(tmpy), fig.color_r, fig.color_g, fig.color_b])
                u=u+deta
            
        return
    '''
    def DrawingB_spline(self, painted_point, fig):
        #矩阵计算方法
        n = len(fig.pointList)
        if fig.isOperating:
            deta = 0.0035*n
            for i in range(0,n):
                for x in range(-3, 3):
                    for y in range(-3, 3):
                        painted_point.append([fig.pointList[i].X() + x, fig.pointList[i].Y() + y, 150, 150, 150])
        else:
            deta = 0.0001 * n

        #一个点的情况
        if(fig.isAPoint()):
            for x in range(0, fig.thickNess + 1):
                for y in range(0, fig.thickNess + 1):
                    painted_point.append([fig.pointList[0].X()+x,fig.pointList[0].Y()+y,150,150,150])
            return

        if n>= 4:
            u=3
            while(u<n):
                tmpx = 0
                tmpy = 0
                int_u = int(u)
                t=u-int_u
                t2=t*t
                t3=t2*t
                list_tmp = [-t3 + 3 * t2 - 3 * t + 1, 3 * t3 - 6 * t2 + 4, -3 * t3 + 3 * t2 + 3 * t + 1, t3]
                #一块区域最多用到4个控制点，有局部性
                for i in range(0,4):
                    tmpx = tmpx+fig.pointList[i+int_u-3].X()*list_tmp[i]/6
                    tmpy = tmpy+fig.pointList[i+int_u-3].Y()*list_tmp[i]/6
                if((not tmpx==0) and (not tmpy ==0)):
                    for x in range(0, fig.thickNess + 1):
                        for y in range(0, fig.thickNess + 1):
                            painted_point.append([round(tmpx)+x, round(tmpy)+y, fig.color_r, fig.color_g, fig.color_b])
                u = u + deta
        return

    def DrawingCharactor(self, painted_point, fig):
        if fig.isNum:
            if fig.id==0:
                # 0
                hzk16=[[0,0],[0,0],[1,128],[2,64],[4,32],[4,32],[4,32],[4,32],[4,32],[4,32],[4,32],[2,64],[1,128]]
            elif fig.id == 1:
                # 1
                hzk16 =[[0,0],[0,0],[1,0],[3,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[3,128]]
            elif fig.id == 2:
                # 2
                hzk16 =[[0,0],[0,0],[7,128],[8,64],[8,64],[0,64],[0,128],[0,128],[1,0],[2,0],[4,0],[8,64],[15,192]]
            elif fig.id == 3:
                # 3
                hzk16 =[[0,0],[0,0],[7,128],[8,64],[8,64],[0,64],[0,128],[3,0],[0,128],[0,64],[8,64],[8,64],[7,128]]
            elif fig.id == 4:
                # 4
                hzk16 =[[0,0],[0,0],[0,128],[0,128],[1,128],[2,128],[2,128],[4,128],[8,128],[31,224],[0,128],[0,128],[1,192]]
            elif fig.id == 5:
                # 5
                hzk16 =[[0,0],[0,0],[7,224],[4,0],[4,0],[4,0],[7,128],[4,64],[0,32],[0,32],[4,32],[4,64],[3,128]]
            elif fig.id == 6:
                # 6
                hzk16 =[[0,0],[0,0],[1,192],[2,32],[4,32],[4,0],[5,128],[6,64],[4,32],[4,32],[4,32],[2,64],[1,128]]
            elif fig.id == 7:
                # 7
                hzk16 =[[0,0],[0,0],[7,224],[8,32],[8,64],[0,128],[0,128],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0]]
            elif fig.id == 8:
                # 8
                hzk16 =[[0,0],[0,0],[3,192],[4,32],[4,32],[4,32],[2,64],[1,128],[2,64],[4,32],[4,32],[4,32],[3,192]]
            elif fig.id == 9:
                # 9
                hzk16 =[[0,0],[0,0],[1,128],[2,64],[4,32],[4,32],[4,32],[2,96],[1,160],[0,32],[4,32],[4,64],[3,128]]
            else:
                hzk16=[]
        else:
            if fig.id==0:
                #a
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[7,0],[8,128],[8,128],[3,128],[4,128],[8,128],[8,128],[7,64]]

            elif fig.id==1:
                #b
                hzk16=[[0,0],[4,0],[12,0],[4,0],[4,0],[4,0],[5,128],[6,64],[4,32],[4,32],[4,32],[4,64],[7,128]]
            elif fig.id==2:
                #c
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[3,128],[4,64],[8,64],[8,0],[8,0],[8,0],[4,64],[3,128]]
            elif fig.id==3:
                #d
                hzk16=[[0,0],[0,0],[0,192],[0,64],[0,64],[0,64],[7,64],[8,192],[8,64],[8,64],[8,64],[8,192],[7,96]]
            elif fig.id==4:
                #e
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[3,128],[4,64],[8,64],[15,192],[8,0],[8,0],[4,64],[3,128]]
            elif fig.id==5:
                #f
                hzk16=[[0,0],[0,0],[0,224],[1,16],[1,0],[7,128],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[3,128]]
            elif fig.id==6:
                #g
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[3,224],[4,64],[4,64],[3,128],[4,0],[4,0],[7,192],[8,32],[8,32],[7,192]]
            elif fig.id==7:
                #h
                hzk16=[[0,0],[0,0],[4,0],[12,0],[4,0],[5,192],[6,32],[4,32],[4,32],[4,32],[4,32],[4,32],[14,112]]
            elif fig.id==8:
                #i
                hzk16=[[0,0],[0,0],[1,0],[1,0],[0,0],[3,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[3,128]]
            elif fig.id==9:
                #j
                hzk16=[[0,0],[1,0],[1,0],[0,0],[3,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[17,0],[14,0]]
            elif fig.id==10:
                #k
                hzk16=[[0,0],[0,0],[12,0],[4,0],[4,0],[4,224],[4,64],[4,128],[7,0],[4,128],[4,128],[4,64],[14,96]]
            elif fig.id==11:
                #l
                hzk16=[[0,0],[0,0],[3,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[3,128]]
            elif fig.id==12:
                #m
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[110,112],[49,136],[33,8],[33,8],[33,8],[33,8],[33,8],[115,156]]
            elif fig.id==13:
                #n
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[13,192],[6,32],[4,32],[4,32],[4,32],[4,32],[4,32],[14,112]]
            elif fig.id==14:
                #o
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[3,128],[4,64],[8,32],[8,32],[8,32],[8,32],[4,64],[3,128]]
            elif fig.id==15:
                #p
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[13,192],[6,32],[4,32],[4,32],[4,32],[6,32],[5,192],[4,0],[4,0],[14,0]]
            elif fig.id==16:
                #q
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[3,160],[4,96],[4,32],[4,32],[4,32],[4,96],[3,160],[0,32],[0,32],[0,112]]
            elif fig.id==17:
                #r
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[6,192],[3,32],[2,0],[2,0],[2,0],[2,0],[2,0],[7,0]]
            elif fig.id==18:
                #s
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[3,64],[4,192],[4,64],[3,0],[0,128],[4,64],[6,64],[5,128]]
            elif fig.id==19:
                #t
                hzk16=[[0,0],[0,0],[0,0],[0,0],[2,0],[2,0],[7,192],[2,0],[2,0],[2,0],[2,0],[2,64],[1,128]]
            elif fig.id==20:
                #u
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[12,192],[4,64],[4,64],[4,64],[4,64],[4,192],[3,96]]
            elif fig.id==21:
                #v
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[14,224],[4,64],[4,64],[2,128],[2,128],[2,128],[1,0],[1,0]]
            elif fig.id==22:
                #w
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[59,184],[17,16],[17,16],[9,160],[10,160],[14,224],[4,64],[4,64]]
            elif fig.id==23:
                #x
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[14,224],[4,64],[2,128],[1,0],[1,0],[2,128],[4,64],[14,224]]
            elif fig.id==24:
                #y
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[14,224],[4,64],[4,64],[2,128],[2,128],[2,128],[1,0],[1,0],[10,0],[4,0]]
            elif fig.id==25:
                #z
                hzk16=[[0,0],[0,0],[0,0],[0,0],[0,0],[7,224],[4,64],[0,128],[0,128],[1,0],[2,0],[4,32],[7,224]]
            else:
                #space
                hzk16=[]

        for i in range(0,len(hzk16)):
            for j in range(0,2):
                for k in range(0,8):
                    if hzk16[i][j]&(128>>k):
                        for p in range(0,4):
                            for q in range(0,4):
                                painted_point.append([round(fig.posx+(8*j+k)*4+q),round(fig.posy+i*4+p), fig.color_r, fig.color_g, fig.color_b])



