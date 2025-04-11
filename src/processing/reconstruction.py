from src.processing.reconstruction_blender import reconstruir_con_una_imagen, reconstruir_con_multiples_imagenes

def reconstruir_desde_imagenes(rutas_imagenes):
    if len(rutas_imagenes) == 1:
        return reconstruir_con_una_imagen(rutas_imagenes[0])
    elif len(rutas_imagenes) > 1:
        return reconstruir_con_multiples_imagenes(rutas_imagenes)
    else:
        print("[ERROR] No se proporcionaron imágenes.")
        return None
