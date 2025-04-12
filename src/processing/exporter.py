import os
import shutil
from tkinter import filedialog

# Puedes añadir más extensiones aquí si en el futuro usas .fbx, .ply, etc.
EXTENSIONES_VALIDAS = [".obj", ".glb"]

def guardar_modelo():
    ruta_origen = encontrar_modelo_mas_reciente()

    if not ruta_origen:
        print("[ERROR] No se encontró ningún modelo para guardar.")
        return None, None

    extension = os.path.splitext(ruta_origen)[1].lower()

    ruta_destino = filedialog.asksaveasfilename(
        defaultextension=extension,
        filetypes=[("Archivo 3D", "*" + extension)],
        initialfile=os.path.basename(ruta_origen)
    )

    if ruta_destino:
        shutil.copy(ruta_origen, ruta_destino)
        print(f"[INFO] Modelo guardado en: {ruta_destino}")
        return extension.upper().replace(".", ""), ruta_destino
    else:
        return None, None

def encontrar_modelo_mas_reciente():
    carpeta_output = os.path.join("data", "output")
    if not os.path.exists(carpeta_output):
        return None

    archivos = [
        os.path.join(carpeta_output, f)
        for f in os.listdir(carpeta_output)
        if os.path.splitext(f)[1].lower() in EXTENSIONES_VALIDAS
    ]

    if not archivos:
        return None

    return max(archivos, key=os.path.getctime)