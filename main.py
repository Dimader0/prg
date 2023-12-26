from PIL import Image, ImageFilter

def print_info_image(image:Image.Image):
    print(f'''
    Size: {image.size}
    Color: {image.mode}
    Format: {image.format}
    ''')


def do_bw():
    with Image.open('original.jpg') as orig:
        print_info_image(orig)  
        wb = orig.convert('L')
        wb.show()
        wb.save('wb_pic.jpg')
        print_info_image(wb)

def do_blur():
    with Image.open('original.jpg') as orig:
        blur = orig.filter(ImageFilter.BLUR)
        blur.show()
        print_info_image(blur)

if __name__ == '__main__':
    do_blur()