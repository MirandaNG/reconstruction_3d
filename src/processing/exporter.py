import os

def exportar_modelo_obj(puntos_3d, ruta_imagen):
    # Usa la ruta de la imagen para crear el nombre del archivo
    nombre_archivo = os.path.splitext(os.path.basename(ruta_imagen))[0] + ".obj"
    ruta = os.path.join("data", "output", nombre_archivo)

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    with open(ruta, 'w') as f:
        for punto in puntos_3d:
            f.write(f"v {punto[0]} {punto[1]} {punto[2]}\n")
        print(f"[OK] Modelo 3D guardado en {ruta}")

def guardar_como_obj(ruta_imagen, vertices, caras):
    nombre_archivo = os.path.splitext(os.path.basename(ruta_imagen))[0] + ".obj"
    ruta = os.path.join("data", "output", nombre_archivo)

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w') as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for c in caras:
            f.write(f"f {c[0]+1} {c[1]+1} {c[2]+1}\n")
    print(f"[OK] Modelo 3D guardado en {ruta}")

