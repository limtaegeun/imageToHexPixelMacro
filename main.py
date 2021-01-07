# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from os import listdir
from os.path import isfile, join
import pathlib
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
def get_image():
    global imageFiles
    # Use a breakpoint in the code line below to debug your script.
    mypath = pathlib.Path().absolute()
    imageFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    return list(filter(lambda x: x.find('.jpg') != -1 or x.find('.png') != -1, imageFiles))

def convert_pixel_to_hex(filePath):
    image = Image.open(filePath)
    dpi = image.info['dpi']
    width, height = image.size
    print(dpi, width, height)
    pixel_per_mm = dpi[0] / 25.4
    pixel_per_5mm = pixel_per_mm * 5
    colors = image.getpixel((0,0))
    print(colors, rgb_to_hex(colors))
    hex_pixel_list = []
    for y in range(round(height / pixel_per_5mm)):
        row = []
        for x in range(round(width / pixel_per_5mm)):
            rgb_colors = image.getpixel((round(x * pixel_per_5mm + 15),round( y * pixel_per_5mm + 15)))
            row.append(rgb_to_hex(rgb_colors))
        hex_pixel_list.append(row)
    return (hex_pixel_list, image.size, pixel_per_5mm)


def drawImage(hex_list, canvasSize, filePath, pixel_per_5mm):
    img = Image.new('RGB', (canvasSize[0], canvasSize[1]), color=(255, 255, 255))
    fnt = ImageFont.truetype('NotoSans-Regular.ttf', 11)
    d = ImageDraw.Draw(img)
    for y_idx, y_value in enumerate(hex_list):
        for x_idx, x_value in enumerate(y_value):
            d.text((round(x_idx * pixel_per_5mm + 15), round(y_idx * pixel_per_5mm + 15)), x_value, font=fnt, fill=(0, 0, 0))
    pathlib.Path("./hex").mkdir(parents=True, exist_ok=True)
    img.save('./hex/' + filePath )

def rgb_to_hex(rgb):
    r, g, b = rgb
    return hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

if __name__ == '__main__':
    images = get_image()
    print(images)
    for image in images:
        hex_list, size, pixel_p_5m = convert_pixel_to_hex(image)
        print(len(hex_list), len(hex_list[0]), size, pixel_p_5m)
        drawImage(hex_list, size, image, pixel_p_5m)

