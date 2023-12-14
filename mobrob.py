from PyQt5.QtGui import QKeyEvent
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
        self.sp = np.diag([1, 1, 0.1]) #sigma_p
        self.dsl = 0.0
        self.dsr = 0.0
        self.initUI()
        self.timer = QTimer()
        self.timer.setInterval(1000 // 60)
        self.timer.timeout.connect(self.step)
        self.timer.start()

    def step(self):
        self.p0 = move_robot(self.p0, self.dsl, self.dsr)
        self.p = move_robot(self.p, self.dsl * (1 + np.random.randn() * 0.01), self.dsr * (1 + np.random.randn() * 0.01))

        #prediction update
        tt = self.p[2, 0] + (self.dsr - self.dsl) / 2 / B
        jp = np.array([                                 #Jacobian p
            [1, 0, -(self.dsr + self.dsl) / 2 * np.sin(tt)],
            [0, 1,  (self.dsr + self.dsl) / 2 * np.cos(tt)],
            [0, 0, 1]
        ])

        ju = np.array([                                 
            [np.cos(tt) / 2 - (self.dsr + self.dsl) / 4 / B * np.sin(tt),
             np.cos(tt) / 2 + (self.dsr + self.dsl) / 4 / B * np.sin(tt)],
            [np.sin(tt) / 2 + (self.dsr + self.dsl) / 4 / B * np.cos(tt),
             np.sin(tt) / 2 - (self.dsr + self.dsl) / 4 / B * np.cos(tt)],
            [1 / B, -1 / B]
        ])

        su = np.diag([np.abs(self.dsr * 0.1),np.abs(self.dsl * 0.1)])
        self.sp = jp.dot(self.sp).dot(jp.T) + ju.dot(su).dot(ju.T)

        self.draw()
        self.update()

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.label = QLabel()
        canvas = QPixmap(WIDTH, HEIGHT)
        self.label.setPixmap(canvas)
        button = QPushButton("quit")
        button.clicked.connect(lambda: sys.exit(0))
        layout.addWidget(self.label)
        layout.addWidget(button)
        self.setCentralWidget(widget)
        self.show()


    def keyPressEvent(self, ev: QKeyEvent | None) -> None:
        key = ev.key()
        if key == Qt.Key.Key_Escape: sys.exit(0)
        elif key == Qt.Key.Key_Right:
            self.dsl += 0.005
            self.dsr -= 0.005
        elif key == Qt.Key.Key_Left:
            self.dsl -= 0.005
            self.dsr += 0.005
        elif key == Qt.Key.Key_Up:
            self.dsl += 0.005
            self.dsr += 0.005
        elif key == Qt.Key.Key_Down:
            self.dsl -= 0.005
            self.dsr -= 0.005
        return super().keyPressEvent(ev)


    def draw(self):
        p = QPainter(self.label.pixmap())
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.eraseRect(0, 0, WIDTH, HEIGHT)
        p.setBrush(QColor(0x00ffff))
        p.drawEllipse(
           int(_x(self.p0[0,0] - B / 2)),
           int(_y(self.p0[1,0] + B / 2)),
           int(B * PX_PER_M),
           int(B * PX_PER_M)
        )

        p.drawLine(   #ロボットの向いている方向
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
    if dsl != dsr:
        dt = (dsr - dsl) / B
        r = (dsl + dsr) / (2*dt)
        dx = 2*r *np.sin(dt / 2) * np.cos(p[2,0] + dt /2)
        dy = 2*r *np.sin(dt / 2) * np.sin(p[2,0] + dt /2)
        print(dx, dy, dt, p.shape)
    else:
        dt = 0
        dx = dsl * np.cos(p[2, 0])
        dy = dsr * np.sin(p[2, 0])

    return p + np.array([[dx],[dy],[dt]])


app = QApplication(sys.argv)
mb = Mobrob()
app.exec()