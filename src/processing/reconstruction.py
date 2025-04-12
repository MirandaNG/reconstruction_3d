import subprocess
import os

def reconstruir_desde_imagenes(rutas_imagenes):
    script_path = os.path.abspath("src/processing/reconstruction_blender.py")
    blender_exe = r"c:\Users\molly\Downloads\blender-4.3.2-windows-x64\blender-4.3.2-windows-x64\blender.exe"  # Asegúrate que esta sea la ruta correcta

    # Convierte todas las rutas a absolutas
    rutas_absolutas = [os.path.abspath(r) for r in rutas_imagenes]

    command = [
        blender_exe,
        "--background",
        "--python", script_path,
        "--", *rutas_absolutas
    ]

    try:
        subprocess.run(command, check=True)
        print("[INFO] Modelo generado exitosamente con Blender.")
        return True
    except subprocess.CalledProcessError as e:
        print("[ERROR] Falló la reconstrucción con Blender.")
        print(e)
        return False