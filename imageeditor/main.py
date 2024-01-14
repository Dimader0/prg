from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter
from os import *

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Графічний редактор")
main_win.resize(700,500)
lb_picture = QLabel("Зоображення")
file_list = QListWidget()
btn_open_folder = QPushButton("Папка")
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_mirror = QPushButton("Дзеркально")
btn_sharpness = QPushButton("Різкість")
btn_black_white = QPushButton("Ч/Б")

main_layout = QHBoxLayout()

button_layout = QHBoxLayout()

col_1  = QVBoxLayout()
col_2 = QVBoxLayout()

button_layout.addWidget(btn_left)
button_layout.addWidget(btn_right)
button_layout.addWidget(btn_mirror)
button_layout.addWidget(btn_sharpness)
button_layout.addWidget(btn_black_white)

col_1.addWidget(btn_open_folder)
col_1.addWidget(file_list)

col_2.addWidget(lb_picture)
col_2.addLayout(button_layout)

main_layout.addLayout(col_1, 20)
main_layout.addLayout(col_2, 80)
main_win.setLayout(main_layout)

workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(filenames, extenshions):
    result = []
    for filename in filenames:
        for ext in extenshions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    chooseWorkdir()
    extenshions = ['.jpg', '.png', '.gif', '.bmp']
    result = filter(listdir(workdir), extenshions)
    file_list.clear
    file_list.addItems(result)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    
    def loadImage(self, filename):
        self.filename = filename
        file_path = path.join(workdir, filename)
        self.image = Image.open(file_path)
    
    def showImage(self, path):
        lb_picture.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_picture.width(), lb_picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
        lb_picture.setPixmap(pixmapimage)
        lb_picture.show()

    def saveImage(self):
        save_path = path.join(workdir, self.save_dir)
        if not (path.exists(save_path) or path.isdir(save_path)):
            mkdir(save_path)
        file_path = path.join(save_path, self.filename)
        self.image.save(file_path)
    
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(path.join(workdir, filename))


btn_black_white.clicked.connect(workimage.do_bw)
file_list.itemClicked.connect(showChosenImage)
btn_open_folder.clicked.connect(showFilenamesList)
main_win.show()
app.exec_()