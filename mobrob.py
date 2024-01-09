#知能ロボティクス論　第9回

#課題　ロボットシミュレーションの機能拡張

#１　GUIのサイズ変更
#２　ロボットのサイズと自己位置推定領域のサイズ変更（縮小2分の1）
#３　キーイベントの追加（停止、自己位置推定領域リセット、allリセット）
#４　自己位置pのテキスト表示


from PyQt5.QtGui import QKeyEvent
import numpy as np
import numpy.linalg as la
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


#画面のサイズ変更
# WIDTH = 800
# HEIGHT = 800
WIDTH = 1830 
HEIGHT = 900 

PX_PER_M = WIDTH / 10
B = 0.342   #トレッド

def _x(x):
    return x * PX_PER_M + WIDTH / 2

def _y(y):
    return -y * PX_PER_M + HEIGHT / 2

class Mobrob(QMainWindow):
    def __init__(self):
        super().__init__()
        self.p0= np.array([[0],[0],[0]])    #真値
        self.p = np.array(self.p0)              #推定値
        self.sp = np.diag([1, 1, 0.1]) #sigma_p
        self.dsl = 0.0
        self.dsr = 0.0
        self.initUI()
        self.timer = QTimer()
        self.timer.setInterval(1000 // 60)
        self.timer.timeout.connect(self.step)
        self.timer.start()
        self.setFocusPolicy(Qt.StrongFocus)
        

    def step(self):
        self.p0 = move_robot(self.p0, self.dsl, self.dsr)
        self.p = move_robot(self.p, self.dsl * (1 + np.random.randn() * 0.01), 
                            self.dsr * (1 + np.random.randn() * 0.01)
        )

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

        #テキストの更新
        self.update_text_label()

    #テキスト更新用の関数
    def update_text_label(self):
        text = f"p: {self.p}"
        self.text_label.setText(text)


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

        #自己位置pの表示
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(self.text_label)
        


    def keyPressEvent(self, ev: QKeyEvent | None) -> None:
        key = ev.key()
        if key == Qt.Key.Key_Escape: sys.exit(0)
        elif key == Qt.Key.Key_Right:
            self.dsl += 0.001
            self.dsr -= 0.001
        elif key == Qt.Key.Key_Left:
            self.dsl -= 0.001
            self.dsr += 0.001
        elif key == Qt.Key.Key_Up:
            self.dsl += 0.001
            self.dsr += 0.001
        elif key == Qt.Key.Key_Down:
            self.dsl -= 0.001
            self.dsr -= 0.001


        #キーイベント追加
            
        #停止
        elif key == Qt.Key.Key_Space:
            self.dsl = 0.0
            self.dsr = 0.0
        #自己位置推定領域リセット
        elif key == Qt.Key.Key_Backspace:
            self.sp = np.diag([1, 1, 0.1]) #reset sigma_p
        #allリセット
        elif key == Qt.Key.Key_R:
            self.p0= np.array([[0],[0],[0]])    #真値
            self.p = np.array(self.p0)              #推定値
            self.sp = np.diag([1, 1, 0.1]) #sigma_p
            self.dsl = 0.0
            self.dsr = 0.0
        

        return super().keyPressEvent(ev)


    def draw(self):
        p = QPainter(self.label.pixmap())
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.eraseRect(0, 0, WIDTH, HEIGHT)
        p.setBrush(QColor(0x00ffff))

        # ロボットサイズ更更

        # p.drawEllipse(
        #     int(_x(self.p0[0, 0] - B / 2)),
        #     int(_y(self.p0[1, 0] + B / 2)),
        #     int(B * PX_PER_M),
        #     int(B * PX_PER_M)
        # )

        p.drawEllipse(
            int(_x(self.p0[0,0] - B / 4)),
            int(_y(self.p0[1,0] + B / 4)),
            int(B * PX_PER_M / 2),
            int(B * PX_PER_M / 2)
        )

        p.drawLine(   #ロボットの向いている方向
            int(_x(self.p0[0,0])),
            int(_y(self.p0[1,0])),
            int(_x(self.p0[0,0] + np.cos(self.p0[2, 0]) * 0.5)),
            int(_y(self.p0[1,0] + np.sin(self.p0[2, 0]) * 0.5))
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

            #自己位置推定領域サイズ変更
            # p.drawLine(
            #     int(_x(self.p0[0, 0] + xs[i])),
            #     int(_y(self.p0[1, 0] + ys[i])),
            #     int(_x(self.p0[0, 0] + xs[i + 1])),
            #     int(_y(self.p0[1, 0] + ys[i + 1]))
            # )

            p.drawLine(
                int(_x(self.p0[0,0] + xs[i] / 2)),
                int(_y(self.p0[1,0] + ys[i] / 2)),
                int(_x(self.p0[0,0] + xs[i + 1] / 2)),
                int(_y(self.p0[1,0] + ys[i + 1] / 2))
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