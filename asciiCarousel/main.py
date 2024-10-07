#Para las solicitudes API: pip install requests
import requests
#PIL significa biblioteca de imagenes de Python: pip install pillow
#usa PIL para manipular imagenes, colores, agregar texto, cambiar tamaño, etc
# https://pillow.readthedocs.io/en/latest/reference/index.html
from PIL import ImageFile
#from convert2Ascii import __app_name__,__version__
from imageHandler import *
#para manipular el sistema operativo: https://docs.python.org/es/3/library/os.html
import os
#Typer permite ponerle colorines y manejor los parámtros de entrada
#https://typer.tiangolo.com/#use-typer-in-your-code
import typer
from typing_extensions import Annotated
#Para la animación de cargando
import threading
import time
import sys
#pickle nos permite serializar objetos
import pickle
from data.database import SqliteClient 
from picture import Picture
#from rembg import remove


class Cancellation():
    def __init__(self):
       self.is_cancelled = False

    def cancel(self):
       self.is_cancelled = True

def edit_menu()->str:
    print("""           ====== Menu edit ======""")
    print("""a) add database | l) show images | L) show images without preview | d) delete image | c) carrusel | s / enter) exit""")
    option = input("Elige una opcion: ")
    return option
def show_menu()->str:
    print("""
                     ======= Menu change mode ======
                        Enter->to continue
                        0->Mode 0 (image black and white)
                            0-1->Mode 0, with remove background
                            0-2->Mode 0, not preview image
                            0-3->Mode 0, not preview & remove background
                            0-4->Mode 0, color yellow
                            0-5->Mode 0, color green
                        1->Modo 1 (image with colors)
                            1-1->Mode 1, with remove background
                            1-2->Mode 1, not preview image
                            1-3->Mode 1, not preview & remove background
                        S->Exit
        """)
    option = input("Elige una opcion: ")
    return option
def print_ascii(ascii:list, color:str="white")->None:
    """Muestra el resultado en pantalla
        Se le puede pasar un color"""
    columns_in_terminal=os.get_terminal_size().columns
    typer.secho("#"*columns_in_terminal, fg=typer.colors.GREEN, bg=typer.colors.WHITE)
    typer.secho("#"*columns_in_terminal, fg=typer.colors.GREEN, bg=typer.colors.WHITE)
    print("")
    for row in ascii:
        for caracter in row:
            if (color == "white"):
                typer.secho(caracter, nl=False, fg=typer.colors.WHITE, bold=True)
            elif (color == "black"):
                typer.secho(caracter, nl=False, fg=typer.colors.BLACK, bold=True)
            elif (color == "red"):
                typer.secho(caracter, nl=False, fg=typer.colors.RED, bold=True)
            elif (color == "green"):
                typer.secho(caracter, nl=False, fg=typer.colors.GREEN, bold=True)
            elif (color == "blue"):
                typer.secho(caracter, nl=False, fg=typer.colors.BLUE, bold=True)
            elif (color == "yellow"):
                typer.secho(caracter, nl=False, fg=typer.colors.YELLOW, bold=True)
            elif (color == "purple"):
                typer.secho(caracter, nl=False, fg=typer.colors.MAGENTA, bold=True)
            else:
                typer.secho(caracter, nl=False, fg=typer.colors.WHITE, bold=True)            
        print("")
    print("")
    typer.secho("#"*columns_in_terminal, fg=typer.colors.GREEN, bg=typer.colors.WHITE)
    typer.secho("#"*columns_in_terminal, fg=typer.colors.GREEN, bg=typer.colors.WHITE)

def print_ascii_with_colors(image:ImageFile, ascii:list)->None:
    """Muestra el resultado en pantalla"""
    for y in range(image.height):
        for x in range(image.width):
            pixel=image.getpixel((x,y))
            r,g,b=pixel[0], pixel[1], pixel[2]
            # "Blanco"    "Beige"    "Amarillo"     "Celeste"   "Verde"     "Gris"     "Azul"    "Rojo"    "Negro"
            if(get_pixel_9_peletes(r,g,b)=="Blanco"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.WHITE, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Beige"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.CYAN, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Amarillo"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.BRIGHT_YELLOW, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Celeste"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.BLUE, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Verde"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.GREEN, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Gris"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.WHITE, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Azul"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.BLUE, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Rojo"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.RED, bold=True)
            elif(get_pixel_9_peletes(r,g,b)=="Negro"):
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.BLACK, bold=True)
            else:
                typer.secho(ascii[y][x], nl=False, fg=typer.colors.WHITE, bold=True)  
        print("")

def loading_animation(*cancellation):
    cancel = cancellation[0]
    characters=["|","/","-","\\"]
    
    while (True):
        if cancel.is_cancelled==True: break
        for i in range(4):
            if i==3: i=0
            sys.stdout.write(f'\rCargando... {characters[i]}')
            sys.stdout.flush()
            time.sleep(0.1)

    
        

def main(mode:int=1, color:str="white", notshow: Annotated[bool, typer.Option("--notshow")] = False, rembg: Annotated[bool, typer.Option("--rembg")] = False):       
    ascii=[]    
    app_name="asciiCarousel"
    if(rembg):
        app_name="asciiCarousel-rembg"
    local_data_dir = os.getenv('LOCALAPPDATA')
    absolute_dir=local_data_dir+"\\"+app_name+"\\"
    PATH_ASSETS = absolute_dir+"assets\\"
    FILE_NAME = PATH_ASSETS+"temp.png"
    PATH_IMAGES = PATH_ASSETS+"images\\"
    DATABASE = PATH_ASSETS+"database.db"
    if not os.path.isdir(absolute_dir):
        os.mkdir(absolute_dir)
    if not os.path.isdir(PATH_ASSETS):
        os.mkdir(PATH_ASSETS)
    #C:\\Users\\kikem\\AppData\\Local\\asciiCarousel\\assets\\images\\
    #C:\Users\kikem\AppData\Local\asciiCarousel\assets
    if not os.path.isdir(PATH_IMAGES):
        os.mkdir(PATH_IMAGES)

    database=SqliteClient(DATABASE,1)
    #image es la imagen en su tamaño natural
    image=None
    #image2 es la imagen final modificada
    image2=None
    
    while True:
        #Cambia el tamanio del terminal
        cmd = 'mode 118'
        os.system(cmd)
        #Limpiamos el terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Options: Mode", mode, ", color: ",color, ", not show: ",notshow,", remove bg: ", rembg)
        # Crear y ejecutar el hilo de la animación
        cancel_animation = Cancellation()
        loading_thread = threading.Thread(target=loading_animation, args=(cancel_animation, 1,2))
        loading_thread.start()


        #Obtenemos la imageFile (el buffer) de internet
        picture:Picture = get_picture()

        if(picture is None):
            print("Error: The image could not be downloaded from the internet")
            cancel_animation.is_cancelled=True
            loading_thread.join()
            break
        else:
            image = picture.image_file
            #Creamos la imagen en el pc
            image = image.convert("RGB")
            image.save(FILE_NAME)
            #Mostramos la foto original
            if(not notshow):
                image.show()
                
            """
            #==========================Borrar fondo============================
            if (rembg):
                image=open(FILE_NAME, 'rb')
                imageBytes=remove(image.read())
                open(FILE_NAME, 'wb').write(imageBytes)
                image=Image.open(FILE_NAME)
            #==================================================================
            """
            
            
            #Obtenemos la imagen identificada
            file_identify=get_identify_file2(FILE_NAME)
            #Extraemos la información de los caracteres de la imagen
            ascii=extract_ascii_mode_0(file_identify)
            if(len(ascii) == 0):
                print("Error: La lista ASCII no puede ser vacia")
                break
        if(os.path.exists(FILE_NAME)):        
            if(mode == 0):  
                cancel_animation.is_cancelled=True
                loading_thread.join()
                text_description_mode="Este modo convierte la imagen en escala de grises obteniendo por cada pixel un valor entre 0 y 255 que es un valor asociado a una tabla."
                yellow_style=typer.style("Estás en el modo 0", fg=typer.colors.YELLOW, bold=True)
                red_style=typer.style(text_description_mode, fg=typer.colors.RED, bold=True)
                message=f"{yellow_style}, {red_style}"
                typer.echo(message=message)  
                print_ascii(ascii, color)
            elif(mode == 1): 
                typer.secho("Estás en el modo 1",  fg=typer.colors.YELLOW, bold=True)
                image2=create_ascii_with_9_color_palette(file_identify)
                if (not notshow):
                    image2.show()
                cancel_animation.is_cancelled=True
                loading_thread.join()
                print("el tamanio de la imagen convertida es {}x{}".format(image2.width, image2.height))
                print_ascii_with_colors(image2, ascii)
            elif(mode == 2):
                #print("Estás en el modo 2")
                #ascii=create_ascii_with_16_color_palette(buffer)
                pass
            else:
                print(f"Error: El modo {mode} no existe")
                break
        else:
            print("Error: No se ha podido leer el archivo con la imagen")

        edit="x"
        while edit != "":
            edit=edit_menu()
            if(edit == "a" or edit == "A"):
                #Comprobamos si existe el archivo en la base de datos
                if(database.check_exists_by_name(picture.name)):
                    print("La imagen ya existe en la base de datos")
                else:
                    print("Añadiendo image a la base de datos...")
                    #Grabamos la imagen final en assets
                    path_image=PATH_IMAGES+picture.name+".png"
                    image2.save(path_image)
                    print("Imagen guardada en "+path_image)
                    #Creamos el objeto Picture
                    picture_to_save=Picture(picture.name, image2, ascii)
                    #Lo insertamos en la base de datos
                    database.insert(picture.name, path_image)
                    #Serilizamos el objeto Picture
                    pickle.dump(picture_to_save, open(path_image+".pkl", "wb"))
                    print("Sprite anadido a la base de datos")
            elif(edit == "l" or edit == "L"):
                print("Listando images en la base de datos")
                images=database.getAll()
                if images is None or len(images) == 0:
                    print("No hay imagenes en la base de datos")
                else:
                    for image in images:
                        print("Id: "+str(image[0])+" | Name: "+image[1]+" | date: "+image[2]+" | Path: "+image[3])
                
                    ver=input("Introduzca el número de imagen que desea ver: ")
                    image_reference=database.getById(ver)
                    if(image_reference is None):
                        print("La imagen no existe en la base de datos")
                    else:
                        print("Id: "+str(image_reference[0])+" | Name: "+image_reference[1]+" | date: "+image_reference[2]+" | Path: "+image_reference[3])
                        with open(image_reference[3]+".pkl", 'rb') as f:
                            image_save = pickle.load(f)
                            print("Image: "+image_save.name)
                            print_ascii_with_colors(image_save.image_file, image_save.ascii)
                            img = Image.open(image_reference[3])  
                            if(edit!="L"):
                                img.show()
            elif(edit == "d" or edit == "d"):
                images=database.getAll()
                if images is None:
                    print("No hay imagenes en la base de datos")
                else:
                    for image in images:
                        print("Id: "+str(image[0])+" | Name: "+image[1]+" | date: "+image[2]+" | Path: "+image[3])
                    delete=input("Introduzca el número de imagen que desea eliminar: ")
                    print("Eliminando image de la base de datos...")
                    if(database.check_exists_by_id(delete)):
                        image_reference=database.getById(delete)
                        path_image=PATH_IMAGES+image_reference[1]+".png"
                        os.remove(path_image)
                        os.remove(path_image+".pkl")
                        database.delete(delete)
                        print("Image eliminada de la base de datos")
                    else:
                        print("La imagen no existe en la base de datos")
            elif(edit == "c" or edit == "C"):
                images=database.getAll()
                if images is None:
                    print("No hay imagenes en la base de datos")
                else:
                    size=len(images)-1
                    count=0
                    while True:
                        if count > size:
                            count=0
                        print("Id: "+str(images[count][0])+" | Name: "+images[count][1]+" | date: "+images[count][2]+" | Path: "+images[count][3])
                        print ("Press Ctrl+C to stop")
                        os.system('cls' if os.name == 'nt' else 'clear')
                        image_reference=database.getById(images[count][0])
                        with open(image_reference[3]+".pkl", 'rb') as f:
                            image_save = pickle.load(f)
                            print("Image: "+image_save.name)
                            print_ascii_with_colors(image_save.image_file, image_save.ascii)
                        time.sleep(1)
                        count+=1
                            
                        
            elif(edit == "e" or edit == "E"):
                break
            elif(edit == "s" or edit == "S"):
                break

            
        response = show_menu()
        if(response == "0"):
            mode=0
            color="white"
            notshow=False
            rembg=False
        # 0-1->Mode 0, with remove background
        elif(response == "0-1"):
            color="white"
            mode=0
            notshow=False
            rembg=True
        # 0-2->Mode 0, not preview image
        elif(response == "0-2"):
            color="white"
            mode=0
            notshow=True
            rembg=False
        # 0-3->Mode 0, not preview & remove background
        elif(response == "0-3"):
            color="white"
            mode=0
            notshow=True
            rembg=True
        #0-4->Mode 0, color yellow
        elif(response == "0-4"):
            mode=0
            color="yellow" 
            notshow=False
            rembg=False
        #0-5->Mode 0, color green
        elif(response == "0-5"):
            mode=0
            color="green"
            notshow=False
            rembg=False
        #   1->Modo 1 (image with colors)
        elif(response == "1"):
            mode=1
            notshow=False
            rembg=False
        # 1-1->Mode 1, with remove background
        elif(response == "1-1"):
            mode=1
            notshow=False
            rembg=True
        # 1-2->Mode 1, not preview image
        elif(response == "1-2"):
            mode=1
            notshow=True
            rembg=False
        # 1-3->Mode 1, not preview & remove background
        elif(response == "1-3"):
            mode=1
            notshow=True
            rembg=True
        # S->Exit
        elif(response == "s" or response == "S"):
            break          

if __name__ == "__main__":

    typer.run(main)






   
        

