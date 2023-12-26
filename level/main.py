from PIL import Image, ImageFilter

#открой файл с оригиналом картинки
with Image.open('original.jpg') as orig:
    print(f'''
          Size: {orig.size}
          Color: {orig.mode}
          Format: {orig.format}
          ''')

#сделай оригинал изображения чёрно-белым

#сделай оригинал изображения размытым

#поверни оригинал изображения на 180 градусов