
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

class PaintWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ініціалізація користувацького інтерфейсу
        self.initUI()

    def initUI(self):
        # Встановлення розміру та назви вікна
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Paint Application')

        # Створення мітки для відображення малюнка
        self.canvas = QLabel(self)
        self.canvas.setAlignment(Qt.AlignTop)
        self.canvas.setStyleSheet("border: 2px solid black;")

        # Створення QPixmap для робочої області та встановлення білого фону
        self.image = QPixmap(self.size())
        self.image.fill(Qt.white)
        self.canvas.setPixmap(self.image)

        # Змінна для збереження останньої точки для малювання ліній
        self.last_point = None

        # Встановлення макету та мітки як центрального віджета
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

        # Додати меню для збереження малюнка
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        saveAction = fileMenu.addAction('Save')
        saveAction.triggered.connect(self.saveImage)

    def mousePressEvent(self, event):
        # Обробка події натискання лівої кнопки миші
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        # Обробка події руху миші при утриманні лівої кнопки
        if event.buttons() and Qt.LeftButton and self.last_point:
            # Отримання об'єкта QPainter та малювання лінії
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.drawLine(self.last_point, event.pos())
            painter.end()
            self.last_point = event.pos()
            self.canvas.setPixmap(self.image)

    def mouseReleaseEvent(self, event):
        # Обробка події відпускання лівої кнопки миші
        if event.button == Qt.LeftButton:
            self.last_point = None

    def saveImage(self):
        # Відкриття діалогового вікна для вибору місця та імені файлу
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)")

        if filePath:
            # Збереження малюнка у вибраний файл
            self.image.save(filePath)


