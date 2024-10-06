import sqlite3
import datetime
import constants

class ImageReference():
    def __init__(self, name:str, path_image_file:str):
        self.name=name
        self.date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.path_image_file=path_image_file


class SqliteClient():
    def __init__(self,PATH_ASSETS:str, version:int):
        self.version=version
        self.conn=sqlite3.connect(PATH_ASSETS+"database.db")
        self.cursor=self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS images (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        date TEXT,
                        path_image_file TEXT
                    )""")
        
        if self.version==1:
            """
            #1 Forma de insertar datos
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES ('coco', 'coco.png')")
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES ('pop', 'popo.png')")
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES ('kikin', 'kikin.png')")
            self.insert(image1)
            self.insert(image2)
            self.insert(image3)
            self.conn.commit()
            """
            """
            #2 forma de insertar datos
            image_File1=ImageReference("coco","coco.png")
            image_File2=ImageReference("pop","popo.png")
            image_File3=ImageReference("kikin","kikin.png")
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES (?,?)", (image_File1.name, image_File1.date, image_File1.path_image_file))
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES (?,?)", (image_File2.name, image_File1.date, image_File2.path_image_file))
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES (?,?)", (image_File3.name, image_File1.date, image_File3.path_image_file))
            """
            """
            #3 Forma de insertar datos
            image_File1=ImageReference("coco","coco.png")
            image_File2=ImageReference("pop","popo.png")
            image_File3=ImageReference("kikin","kikin.png")
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES (:name,:date,:path_image_file)", {
                "name":image_File1.name, 
                "date":image_File1.date,
                "path_image_file":image_File1.path_image_file
                }
            )
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES (:name,:date,:path_image_file)", {
                "name":image_File2.name,
                "date":image_File2.date, 
                "path_image_file":image_File2.path_image_file
                }
            )
            self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES (:name,:date,:path_image_file)", {
                "name":image_File3.name, 
                "date":image_File3.date,
                "path_image_file":image_File3.path_image_file
                }
            )

            """

            """
            #4 Forma de insertar datos
            many_images=[
                ("coco","10/10/2020","coco.png"),
                ("pop","01/01/2024","popo.png"),
                ("kikin","21/01/2023","kikin.png")
            ]
        
            self.cursor.executemany("INSERT INTO images (name, date, path_image_file) VALUES (:name, :date, :path_image_file)", many_images )
            """


    def close(self):
        self.conn.close()
    def insert(self, name:str, path_image_file:str):
        name=name.replace("?","-")
        path_image_file=path_image_file.replace("?","-")
        image=ImageReference(name, path_image_file)
        self.cursor.execute("INSERT INTO images (name, date, path_image_file) VALUES (?, ?, ?)", (image.name, image.date, image.path_image_file))
        self.conn.commit()

    def getAll(self):
        self.cursor.execute("SELECT * FROM images")
        return self.cursor.fetchall()
        #fechone regresa solo un registro
        #print(c.fetchone())
        #fechmany regresa varios registros
        #print(c.fetchmany(2))
        #fechall regresa todos los registros
        #print(c.fetchall())
    def getName(self, name:str):
        self.cursor.execute("SELECT * FROM images WHERE name = ?", (name,))
        return self.cursor.fetchone()   
    def getById(self, id:int):
        self.cursor.execute("SELECT * FROM images WHERE id = ?", (id,))
        return self.cursor.fetchone()
    def delete(self, id:int):
        self.cursor.execute("DELETE FROM images WHERE id = ?", (id,))
        self.conn.commit()
    def check_exists_by_name(self, name:str):
        self.cursor.execute("SELECT * FROM images WHERE name = ?", (name,))
        if self.cursor.fetchone():
            return True
        else:
            return False
    def check_exists_by_id(self, id:int):
        self.cursor.execute("SELECT * FROM images WHERE id = ?", (id,))
        if self.cursor.fetchone():
            return True
        else:
            return False
        
    





