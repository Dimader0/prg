from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QMouseEvent, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

class paintWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)

        self.canvas = QLabel(self)
        self.canvas.setAlignment(Qt.AlignTop)
        self.canvas.setStyleSheet("border: 2px solid black;")

        self.image = QPixmap(self.size())
        self.image.fill(Qt.white)
        self.canvas.setPixmap(self.image)

        self.last_point = None

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.button() and Qt.LeftButton and self.last_point:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.drawLine(self.last_point, event.pos())
            painter.end()
            self.last_point = event.pos()
            self.canvas.setPixmap(self.image)

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.last_point = None
    
