from PIL import ImageFile
class Picture():
    def __init__(self, name:str, image_file:ImageFile, ascii:list):
        self.name=name
        self.image_file=image_file
        self.ascii=ascii
