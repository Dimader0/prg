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
        blur.save('blur_pic.jpg')
        print_info_image(blur)

def do_rotate():
    with Image.open('original.jpg') as orig:
        rot = orig.transpose(Image.ROTATE_180)
        rot.show()
        rot.save('rot_pic.jpg')
        print_info_image(rot)

if __name__ == '__main__':
    do_bw()
    do_blur()
    do_rotate()