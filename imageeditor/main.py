# Завантажуємо графічні віджети
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QMainWindow, QAction
# Завнтажуємо класи для показу зоображення і іконок меню
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
# Завантажуємо модулі для редагування, збереження і завантаження картинок
from PIL import Image, ImageFilter
# Дозволяє працювати з шляхами і папками
from os import *
# окреме вікно яке дозволяє малювати
from paintwindow import*
from styles import style

app = QApplication([])
main_win = QMainWindow()
screen = QWidget()
main_win.setWindowTitle("Графічний редактор")
main_win.resize(1000,600)

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


workdir = '' # створення глобальної змінної для збереження робочої папки
# вибір робочої папки
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

# відфільтровує файли, залишаючи тільки графічні
def filter(filenames, extenshions):
    result = []
    for filename in filenames:
        for ext in extenshions:
            if filename.endswith(ext):
                result.append(filename)
    return result

# завантаження відфільтрованих файлів 
def showFilenamesList():
    chooseWorkdir()
    extenshions = ['.jpg', '.png', '.gif', '.bmp']
    result = filter(listdir(workdir), extenshions)
    file_list.clear
    file_list.addItems(result)

# клас для редагування картинок
class ImageProcessor():
    def __init__(self):
        self.image = None # об'єкт картинки
        self.dir = None # робоча папка
        self.filename = None # назва файлу з яким ми зараз працюємо
        self.save_dir = "Modified/" # папка для збереження модифікованих файлів
    
    # завантаження картинки
    def loadImage(self, filename):
        self.filename = filename
        file_path = path.join(workdir, filename) #об'єднання шляху до картинки з ім'ям картинки
        self.image = Image.open(file_path) #відкрити картинку за шляхом
    
    # відображення картинки
    def showImage(self, path):
        lb_picture.hide()
        pixmapimage = QPixmap(path) # відкрити картинку
        w, h = lb_picture.width(), lb_picture.height() # підігнати розміри картинки під розміри полотна
        pixmapimage = pixmapimage.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio) # відключити деформацію картинки
        lb_picture.setPixmap(pixmapimage) # вставляємо картинку в полотно
        lb_picture.show()

    # збереження модифікованої картинки
    def saveImage(self):
        save_path = path.join(workdir, self.save_dir)
        if not (path.exists(save_path) or path.isdir(save_path)): # якщо папка для збереження не існує
            mkdir(save_path) # створюємо папку для збереження
        file_path = path.join(save_path, self.filename) # шлях до папки для збереження та назва файлу картинки
        self.image.save(file_path) # збереження картинки
    
    # чорно-білий фільтр
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    # поворот наліво
    def rotate_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    # поворот направо
    def rotate_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    # відзеркалення
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    # різкість
    def do_sharpness(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

# об'єкт класу для оборобки картинки
workimage = ImageProcessor()

# обрати зі списку картинку для обробки
def showChosenImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(path.join(workdir, filename))

# створення менюбар
menubar = main_win.menuBar()
file_menu = menubar.addMenu("Файл") # створення меню Файл
open_action = QAction("Open", main_win)
open_action.setShortcut("Ctrl+0")
save_action = QAction(QIcon("ImageEditor\8666542_save_icon.png"), "Save", main_win)
save_action.setShortcut("Ctrl+s")
close_action = QAction("Close", main_win)
close_action.setShortcut("Ctrl+q")
new_action = QAction("New", main_win)
new_action.setShortcut("Ctrl+n")
# додаємо дії до меню Файл
file_menu.addAction(new_action)
file_menu.addAction(open_action)
file_menu.addAction(save_action)
file_menu.addAction(close_action)

editor_menu = menubar.addMenu("Editor") # створення меню Editor
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
# додаємо дії до меню Файл
editor_menu.addAction(rotate_right_act)
editor_menu.addAction(rotate_left_act)
editor_menu.addAction(do_mirror_act)
editor_menu.addAction(do_sharpness_act)
editor_menu.addAction(do_bw_act)

# створення вікна для малювання
def createCanvas():
    global col_2
    canvas = PaintWindow()
    col_2.addWidget(canvas)

# збереження картинки у вибрану папку
def save_file():
    file_name, _ = QFileDialog.getSaveFileName(main_win, "Save File", "", "JPEG (*.jpg);;PNG (*.png);;GIF (*.gif)")

    if file_name:
        image = Image.open(workdir + '/' + workimage.save_dir + '/' + file_list.currentItem().text())
        image.save(file_name, "JPEG")

# відкриття одної картинки
def open_file():
    file_name, _ = QFileDialog.getOpenFileName(main_win, "Open File", "", "JPEG (*.jpg);;PNG (*.png);;GIF (*.gif)")
    
    if file_name:
        workimage.showImage(file_name)
        workimage.image = Image.open(file_name)


# підключення кнопок
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