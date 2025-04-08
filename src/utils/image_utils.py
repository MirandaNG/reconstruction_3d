from PIL import Image

def cargar_y_redimensionar(ruta, tamaño=(512, 512)):
    imagen = Image.open(ruta)
    imagen = imagen.resize(tamaño)
    return imagen
