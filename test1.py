import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Mobrob(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 800)
        self.label = QLabel()
        canvas = QPixmap(800, 800)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw()
        self.show()

    def draw(self):
        p = QPainter(self.label.pixmap())
        p.setBrush(QColor(0x00ffff))
        p.drawEllipse(200, 300, 400, 200)
        p.end()



B = 0.342                   #トレッド
p0= np.array([[1],[0.5],[0]]) #真値
p = np.array(p0)            #推定値

def move_robo(p, dsl, dsr):
    dt = (dsr - dsl) / B
    r = (dsl + dsr) / (2*dt)
    dx = 2*r *np.sin(dt / 2) * np.cos(p[2,0] + dt /2)
    dy = 2*r *np.sin(dt / 2) * np.sin(p[2,0] + dt /2)

    return p + np.array([[dx],[dy],[dt]])

print(p0)
print(move_robo(p0, 1, 0.5))

app = QApplication(sys.argv)
mb = Mobrob()
app.exec()