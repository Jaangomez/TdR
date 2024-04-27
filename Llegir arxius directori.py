import os
ejemplo_dir = 'C:/Users/JoanGómezPujol/Desktop/TR/Python/Gràfics Grau'
contenido = os.listdir(ejemplo_dir)
imagenes = []
for fichero in contenido:
    if os.path.isfile(os.path.join(ejemplo_dir, fichero)) and fichero.endswith('.png'):
        imagenes.append(fichero)

print(imagenes)