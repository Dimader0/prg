from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QMainWindow, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter
from os import *
from paintwindow import*
from styles import style

app = QApplication([])
main_win = QMainWindow()
screen = QWidget()
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
screen.setLayout(main_layout)

main_win.setCentralWidget(screen)

def createCanvas():
    global col_2
    canvas = PaintWindow()
    col_2.addWidget(canvas)

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

    def rotate_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def rotate_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_sharpness(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(path.join(workdir, filename))

menubar = main_win.menuBar()
file_menu = menubar.addMenu("Файл")
open_action = QAction("Open", main_win)
open_action.setShortcut("Ctrl+0")
save_action = QAction(QIcon("ImageEditor\8666542_save_icon.png"), "Save", main_win)
save_action.setShortcut("Ctrl+s")
close_action = QAction("Close", main_win)
close_action.setShortcut("Ctrl+q")
new_action = QAction("New", main_win)
new_action.setShortcut("Ctrl+n")
file_menu.addAction(new_action)
file_menu.addAction(open_action)
file_menu.addAction(save_action)
file_menu.addAction(close_action)

editor_menu = menubar.addMenu("Editor")
do_bw_act = QAction("Ч/Б", main_win)
do_bw_act.setShortcut("Ctrl+x")
do_sharpness_act = QAction("Різкість", main_win)
do_sharpness_act.setShortcut("Ctrl+p")
do_mirror_act = QAction("Дзеркально", main_win)
do_mirror_act.setShortcut("Ctrl+m")
rotate_left_act = QAction("Вліво", main_win)
rotate_left_act.setShortcut("Ctrl+l")
rotate_right_act = QAction("Вправо", main_win)
rotate_right_act.setShortcut("Ctrl+r")
editor_menu.addAction(rotate_right_act)
editor_menu.addAction(rotate_left_act)
editor_menu.addAction(do_mirror_act)
editor_menu.addAction(do_sharpness_act)
editor_menu.addAction(do_bw_act)

def save_file():
    file_name, _ = QFileDialog.getSaveFileName(main_win, "Save File", "", "JPEG (*.jpg);;PNG (*.png);;GIF (*.gif)")

    if file_name:
        image = Image.open(workdir + '/' + workimage.save_dir + '/' + file_list.currentItem().text())
        image.save(file_name, "JPEG")

def open_file():
    file_name, _ = QFileDialog.getOpenFileName(main_win, "Open File", "", "JPEG (*.jpg);;PNG (*.png);;GIF (*.gif)")
    
    if file_name:
        workimage.showImage(file_name)
        workimage.image = Image.open(file_name)


btn_sharpness.clicked.connect(workimage.do_sharpness)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_right.clicked.connect(workimage.rotate_right)
btn_left.clicked.connect(workimage.rotate_left)
btn_black_white.clicked.connect(workimage.do_bw)
file_list.itemClicked.connect(showChosenImage)
btn_open_folder.clicked.connect(showFilenamesList)
save_action.triggered.connect(save_file)
open_action.triggered.connect(open_file)
close_action.triggered.connect(main_win.close)
new_action.triggered.connect(createCanvas)
do_bw_act.triggered.connect(workimage.do_bw)
do_mirror_act.triggered.connect(workimage.do_mirror)
do_sharpness_act.triggered.connect(workimage.do_sharpness)
rotate_left_act.triggered.connect(workimage.rotate_left)
rotate_right_act.triggered.connect(workimage.rotate_right)

main_win.setStyleSheet(style)

main_win.show()
app.exec_()