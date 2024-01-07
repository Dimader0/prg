from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout
from Pil import Image, ImageFilter

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Графічний редактор")
lb_picture = QLabel("Зоображення")
file_list = QListWidget()
btn_open_folder = QPushButton("Папка")
btn_left = QPushButton("")
btn_right = QPushButton("")
btn_mirror = QPushButton("")
btn_sharpness = QPushButton("")
btn_black_white = QPushButton("")

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

main_layout.addLayout(col_1)
main_layout.addLayout(col_2)
main_win.setLayout(main_layout)


main_win.show()
app.exec_()