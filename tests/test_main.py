#Para hacer test:
#  es importante convertir la carpeta test en un paquete, para eso crear un archivo __init__.py,
#  el nombre de los archivos debe comenzar con test_algo.py
#  por último instala pip install pytest en el entorno virtual y situate en el directorio raiz y escribe: pytest 


def test_show_ascii():
    from convert2Ascii.main import show_ascii
    my_tuple=[
        ["a","b","c","d","e"],
        ["f","g","h","i","j"],
        ["k","l","m","n","o"],
        ["p","q","r","s","t"],
        ["u","v","w","x","y"]
    ]
    assert show_ascii(my_tuple) is not None

