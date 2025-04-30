import subprocess
import os
from tkinter import filedialog

def mostrar_modelo():
    # Cuadro de diálogo para que el usuario seleccione el archivo
    ruta_modelo = filedialog.askopenfilename(
        title="Selecciona un archivo de modelo 3D",
        filetypes=[("Archivos GLTF", "*.glb"), ("Archivos OBJ", "*.obj"), ("Archivos PLY", "*.ply")]
    )
    
    if not ruta_modelo:
        print("[ERROR] No se seleccionó ningún archivo.")
        return

    # Verificar si el archivo existe
    if not os.path.exists(ruta_modelo):
        print(f"[ERROR] El archivo {ruta_modelo} no existe.")
        return

    # Ruta al ejecutable de Blender
    blender_exe = r"c:\Users\molly\Downloads\blender-4.3.2-windows-x64\blender-4.3.2-windows-x64\blender.exe"  # Asegúrate de tener la ruta correcta
    script_path = os.path.abspath("src/processing/visualization_blender.py")  # Ruta al script de Blender

    # Convertir la ruta del archivo a absoluta
    ruta_modelo_absoluta = os.path.abspath(ruta_modelo)

    command = [
        blender_exe,
        "--background",  # Ejecuta Blender en segundo plano sin interfaz gráfica
        "--python", script_path,
        "--", ruta_modelo_absoluta  # Pasamos el archivo seleccionado como argumento
    ]

    try:
        subprocess.run(command, check=True)
        print(f"[INFO] Modelo generado exitosamente con Blender: {ruta_modelo_absoluta}")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Falló la visualización con Blender.")
        print(e)