#Para las solicitudes API: pip install requests
import requests
#PIL significa biblioteca de imagenes de Python: pip install pillow
#usa PIL para manipular imagenes, colores, agregar texto, cambiar tamaño, etc
# https://pillow.readthedocs.io/en/latest/reference/index.html
from PIL import Image, ImageFile, ImageOps
from io import BytesIO
from constants import ascii_table,color_9_palette_rgb
import json
import os
from picture import Picture
import datetime

def similar(r1,g1,b1,r2,g2,b2):
    return ((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)**0.5


def create_ascii_with_9_color_palette(image:ImageFile, buffer_pixeles:any=None):
    pixeles=image.load()
    #characters=[]
    for y in range(image.height):
        #files=[]
        for x in range(int(image.width)):
            pixel=image.getpixel((x,y))
            r,g,b=pixel[0], pixel[1], pixel[2]
            for color in color_9_palette_rgb:
                encontrado_similar=False 
                if similar(r,g,b,
                        color_9_palette_rgb[color][0],
                        color_9_palette_rgb[color][1],
                        color_9_palette_rgb[color][2]) < 80:
                    color=color_9_palette_rgb[color]
                    pixeles[x,y]=color
                    #character:Character=Character(color,Color(r,g,b))
                    #files.append(character)
                    #encontrado_similar=True
                #if encontrado_similar==False:
                #    character:Character=Character(color,Color(0,255,0))
                #    files.append(character)
        
        #characters.append(files)
    return image
def get_pixel_9_peletes(r,g,b):
    for color in color_9_palette_rgb:
        if (color_9_palette_rgb[color][0]==r and color_9_palette_rgb[color][1]==g and color_9_palette_rgb[color][2]==b):
               return color
               
def get_picture()->Picture:
    """
    Obtiene una imagen de https://breeds.tipolisto.es/api/cat.php
    """

    response = requests.get("https://breeds.tipolisto.es/api/animal.php")
    data=json.loads(response.content)
    #Sacamos el atributo path_image del JSON
    for i in data:
        try:
            url_image="https://breeds.tipolisto.es/"+i['path_image']
            print("Get image from: "+url_image)
            img = Image.open(BytesIO(requests.get(url_image).content))
            name=i['name_es'].replace("?","-")
            name=name+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            return Picture(name, img, None)
        except:
            print("Error no se pudo acceder a la imagen: "+i['path_image'])
            return None




def extract_ascii_mode_0(buffer:ImageFile)->list:
    """
    Extract ASCII from image
    """
    ascii=[]
    width, height = buffer.size
    buffer = buffer.convert('L')
    pixeles = buffer.load()
    for y in range(height):
        ascii_row=[]
        for x in range(width):
            color = pixeles[x, y]
            ascii_row.append(ascii_table[color])
        ascii.append(ascii_row)
    return ascii

def get_identify_file(FILE_NAME)->ImageFile:
    """
    Esta es una operación diferida; esta función identifica el archivo, pero
    el archivo permanece abierto y los datos de la imagen real no se leen
    del archivo hasta que intente procesar los datos (o llame al método
    :py:meth:`~PIL.Image.Image.load`). Consulte
    :py:func:`~PIL.Image.new`. Consulte :ref:`manejo de archivos`.
    """
    img = Image.open(FILE_NAME)  
    width, height = img.size
    ratio = width / height
    #Le ponemos el tamaño que tengo el terminal o cmd
    new_width = os.get_terminal_size().columns
    new_height = int(new_width * ratio)
    image_redimensionada = img.resize((new_width, new_height))
    #image_redimensionada=image_redimensionada.crop((0, 0, new_width, new_height))
    return image_redimensionada


def get_identify_file2(FILE_NAME)->ImageFile:
    img = Image.open(FILE_NAME)  
    width, height = img.size
    ratio = width / height
    #Le ponemos el tamaño que tengo el terminal o cmd
    new_width = 100
    new_height = 150
    image_redimensionada = ImageOps.contain(img, (new_width, new_height))
    #image_redimensionada=image_redimensionada.crop((0, 0, new_width, new_height))
    return image_redimensionada

