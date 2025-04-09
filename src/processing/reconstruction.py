from .triangulation_utils import procesar_imagenes_con_triangulacion, generar_relieve_desde_una_imagen

def reconstruir_desde_imagenes(rutas):
    if len(rutas) == 1:
        generar_relieve_desde_una_imagen(rutas[0])
        return "relieve.obj"
    elif len(rutas) >= 2:
        procesar_imagenes_con_triangulacion(rutas)
        return "triangulacion.obj"
    else:
        return None
