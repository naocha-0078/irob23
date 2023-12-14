import numpy as np
import numpy.linalg as la
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



WIDTH = 800 
HEIGHT = 800 
PX_PER_M = WIDTH / 10
B = 0.342   #トレッド

def _x(x):
    return x * PX_PER_M + WIDTH / 2

def _y(y):
    return -y * PX_PER_M + HEIGHT / 2

class Mobrob(QMainWindow):
    def __init__(self):
        super().__init__()
        self.p0= np.array([[1],[0.5],[0.2]])    #真値
        self.p = np.array(self.p0)              #推定値
        self.sp = np.array(self.p0)
        self.sp = np.array([1, -0.2, 0],[-0.2, 0.5, 0],[0, 0, 0.1])
        self.initUI()
        self.timer = QTimer()
        self.timer.setInterval(1000 // 60)
        self.timer.timeout.connect(self.step)
        self.timer.start()

    def step(self):
        self.p0[0,0] += 0.01
        self.draw()
        self.update()

    def initUI(self):
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.label = QLabel()
        canvas = QPixmap(800, 800)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw()
        self.show()

    def draw(self):
        p = QPainter(self.label.pixmap())
        p.eraseRect(0, 0, WIDTH, HEIGHT)
        p.setBrush(QColor(0x00ffff))
        p.drawEllipse(
           int(_x(self.p0[0,0] - B / 2)),
           int(_y(self.p0[1,0] + B / 2)),
           int(B * PX_PER_M),
           int(B * PX_PER_M)
        )

        p.drrawLine(   #ロボットの向いている方向
            int(_x(self.p0[0,0])),
            int(_y(self.p0[1,0])),
            int(_x(self.p0[0,0]) + np.cos(self.p0[2, 0] * 0.5)),
            int(_y(self.p0[1,0]) + np.sin(self.p0[2, 0] * 0.5))
        )

        #Σの楕円
        sxy = self.sp[0:2, 0:2]
        w,v = la.eig(sxy)
        lmd = np.diag(w)
        theta = np.arange(0, 2 * np.pi + 0.4, 0.2)
        c = np.array([np.cos(theta), np.sin(theta)])
        x = v.dot((lmd ** 2).dot(c))
        xs = list(x[0])
        ys = list(x[1])
        for i in range(len(xs) - 1):
            p.drawLine(
                int(_x(self.p0[0,0] + xs[i])),
                int(_y(self.p0[1,0] + ys[i])),
                int(_x(self.p0[0,0] + xs[i + 1])),
                int(_y(self.p0[1,0] + ys[i + 1]))
            )        

        p.end()



def move_robot(p, dsl, dsr):
    dt = (dsr - dsl) / B
    r = (dsl + dsr) / (2*dt)
    dx = 2*r *np.sin(dt / 2) * np.cos(p[2,0] + dt /2)
    dy = 2*r *np.sin(dt / 2) * np.sin(p[2,0] + dt /2)

    return p + np.array([[dx],[dy],[dt]])


app = QApplication(sys.argv)
mb = Mobrob()
app.exec()