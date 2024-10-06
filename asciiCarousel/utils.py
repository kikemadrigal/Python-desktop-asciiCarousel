def rgbtoint32(rgb):
    color = 0
    for c in rgb[::-1]:
        color = (color<<8) + c
        # Do not forget parenthesis.
        # color<< 8 + c is equivalent of color << (8+c)
    return color

def int32torgb(color):
    rgb = []
    for i in range(3):
        rgb.append(color&0xff)
        color = color >> 8
    return rgb

print("blanco")
blanco = [255,255,255]
hex_blanco = rgbtoint32(blanco)
print(blanco)
print("Blanco: ", hex_blanco, hex(hex_blanco))

amarillo = [255,255,224]
hex_amarillo = rgbtoint32(amarillo)
print(amarillo)
print("Amarillo: ", hex_amarillo, hex(hex_amarillo))

verde = [245,255,250]
hex_verde = rgbtoint32(verde)
print(verde)
print("verde: ", hex_verde, hex(hex_verde))

gris = [211,211,211]
hex_gris = rgbtoint32(gris)
print(gris)
print("gris: ", hex_gris, hex(hex_gris))

azul = [135,206,235]
hex_azul = rgbtoint32(azul)
print(azul)
print("azul: ", hex_azul, hex(hex_azul))

rojo = [255,127,80]
hex_rojo = rgbtoint32(rojo)
print(rojo)
print("rojo: ", hex_rojo, hex(hex_rojo))

negro = [0,0,0]
hex_negro = rgbtoint32(negro)
print(negro)
print("negro: ", hex_negro, hex(hex_negro))


#print(rgb_c)