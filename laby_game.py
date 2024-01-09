import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect


class MazeGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Maze Game')

        # 迷路のマップ（0は通路、1は壁、2はゴール）
        self.maze_map = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 2, 1],
        ]

        # プレイヤーの初期位置
        self.player_x = 1
        self.player_y = 1

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cell_width = self.width() / len(self.maze_map[0])
        cell_height = self.height() / len(self.maze_map)

        for y in range(len(self.maze_map)):
            for x in range(len(self.maze_map[y])):
                if self.maze_map[y][x] == 1:  # 壁を描画
                    painter.setBrush(QColor(0, 0, 0))
                    painter.drawRect(x * cell_width, y * cell_height, cell_width, cell_height)
                elif self.maze_map[y][x] == 2:  # ゴールを描画
                    painter.setBrush(QColor(0, 255, 0))
                    painter.drawRect(x * cell_width, y * cell_height, cell_width, cell_height)

        # プレイヤーを描画
        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(self.player_x * cell_width, self.player_y * cell_height, cell_width, cell_height)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Right:
            self.move_player(1, 0)  # 右に移動
        elif key == Qt.Key.Key_Left:
            self.move_player(-1, 0)  # 左に移動
        elif key == Qt.Key.Key_Up:
            self.move_player(0, -1)  # 上に移動
        elif key == Qt.Key.Key_Down:
            self.move_player(0, 1)  # 下に移動

        self.update()  # ゲーム画面を再描画

    def move_player(self, dx, dy):
        # 移動先が壁でないことを確認してからプレイヤーを移動
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if 0 <= new_x < len(self.maze_map[0]) and 0 <= new_y < len(self.maze_map):
            if self.maze_map[new_y][new_x] != 1:  # 壁でない場合のみ移動
                self.player_x = new_x
                self.player_y = new_y

                # ゴールに到達した場合
                if self.maze_map[new_y][new_x] == 2:
                    print("Goal reached!")


def main():
    app = QApplication(sys.argv)
    window = MazeGame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
