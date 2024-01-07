from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
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

btn_open_folder.clicked.connect(showFilenamesList)
main_win.show()
app.exec_()