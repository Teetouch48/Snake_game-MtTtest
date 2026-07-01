import sys
import random

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor


class SnakeGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake Game")
        self.setFixedSize(600, 600)

        self.block = 20

        self.snake = [
            [300,300],
            [280,300],
            [260,300]
        ]

        self.food = self.create_food()

        self.direction = "RIGHT"

        self.score = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(100)



    def create_food(self):

        x = random.randrange(
            0,
            600,
            self.block
        )

        y = random.randrange(
            0,
            600,
            self.block
        )

        return [x,y]



    def paintEvent(self,event):

        painter = QPainter(self)

        # background
        painter.fillRect(
            0,
            0,
            600,
            600,
            QColor("#111111")
        )


        # food
        painter.setBrush(
            QColor("#ff3333")
        )

        painter.drawRect(
            self.food[0],
            self.food[1],
            self.block,
            self.block
        )


        # snake
        painter.setBrush(
            QColor("#00ff66")
        )

        for part in self.snake:

            painter.drawRect(
                part[0],
                part[1],
                self.block,
                self.block
            )


        # score
        painter.setPen(
            QColor("white")
        )

        painter.drawText(
            20,
            30,
            f"Score: {self.score}"
        )



    def move(self):

        head = self.snake[0].copy()


        if self.direction=="UP":
            head[1]-=self.block

        elif self.direction=="DOWN":
            head[1]+=self.block

        elif self.direction=="LEFT":
            head[0]-=self.block

        elif self.direction=="RIGHT":
            head[0]+=self.block



        # ชนกำแพง

        if (
            head[0]<0 or
            head[0]>=600 or
            head[1]<0 or
            head[1]>=600
        ):
            self.game_over()
            return



        # ชนตัวเอง

        if head in self.snake:
            self.game_over()
            return



        self.snake.insert(
            0,
            head
        )


        # กินอาหาร

        if head == self.food:

            self.score += 1
            self.food = self.create_food()

        else:

            self.snake.pop()



        self.update()



    def keyPressEvent(self,event):

        key = event.key()


        if key == Qt.Key_Up and self.direction!="DOWN":
            self.direction="UP"

        elif key == Qt.Key_Down and self.direction!="UP":
            self.direction="DOWN"

        elif key == Qt.Key_Left and self.direction!="RIGHT":
            self.direction="LEFT"

        elif key == Qt.Key_Right and self.direction!="LEFT":
            self.direction="RIGHT"



    def game_over(self):

        self.timer.stop()

        QMessageBox.information(
            self,
            "Game Over",
            f"คะแนน: {self.score}"
        )

        self.close()



app = QApplication(sys.argv)

game = SnakeGame()

game.show()

sys.exit(app.exec())