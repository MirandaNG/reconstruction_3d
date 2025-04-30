import os
import shutil
from tkinter import filedialog

def guardar_modelo():
    # Cuadro de diálogo para elegir el archivo más reciente
    ruta_origen = encontrar_modelo_mas_reciente()

    if not ruta_origen:
        print("[ERROR] No se encontró ningún modelo para guardar.")
        return None, None

    # Cuadro de diálogo para seleccionar la ruta de destino y formato
    ruta_destino = filedialog.asksaveasfilename(
        defaultextension=".obj",
        filetypes=[("Archivo OBJ", "*.obj"), ("Archivo GLTF", "*.glb"), ("Archivo PLY", "*.ply")],
        initialfile=os.path.basename(ruta_origen)
    )

    if ruta_destino:
        shutil.copy(ruta_origen, ruta_destino)
        print(f"[INFO] Modelo guardado en: {ruta_destino}")
        return "OBJ", ruta_destino
    else:
        return None, None

def encontrar_modelo_mas_reciente():
    carpeta_output = os.path.join("data", "output")
    if not os.path.exists(carpeta_output):
        return None

    archivos = [os.path.join(carpeta_output, f) for f in os.listdir(carpeta_output) if f.endswith(".ply")]
    if not archivos:
        return None

    return max(archivos, key=os.path.getctime)