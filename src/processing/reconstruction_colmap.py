import os
import subprocess

def ejecutar_colmap(imagenes_dir, salida_dir):
    matches_dir = os.path.join(salida_dir, "matches")
    sparse_dir = os.path.join(salida_dir, "sparse")
    model_text_dir = os.path.join(salida_dir, "model_text")

    os.makedirs(matches_dir, exist_ok=True)
    os.makedirs(sparse_dir, exist_ok=True)

    # Ruta completa al ejecutable de COLMAP
    colmap_path = os.path.abspath("src/models/colmap/colmap-x64-windows-nocuda/bin/colmap.exe")

    # Ejecutar los comandos de COLMAP
    subprocess.run([colmap_path, "feature_extractor",
                    "--database_path", os.path.join(salida_dir, "database.db"),
                    "--image_path", imagenes_dir], check=True)

    subprocess.run([colmap_path, "exhaustive_matcher",
                    "--database_path", os.path.join(salida_dir, "database.db")], check=True)

    subprocess.run([colmap_path, "mapper",
                    "--database_path", os.path.join(salida_dir, "database.db"),
                    "--image_path", imagenes_dir,
                    "--output_path", sparse_dir], check=True)

    subprocess.run([colmap_path, "model_converter",
                    "--input_path", sparse_dir,
                    "--output_path", model_text_dir,
                    "--output_type", "PLY"], check=True)

    # Obtener nombre de la primera imagen
    primera_imagen = os.listdir(imagenes_dir)[0]
    nombre_modelo = os.path.splitext(primera_imagen)[0]

    modelo_ply = os.path.join(model_text_dir, "model.ply")
    if os.path.exists(modelo_ply):
        print(f"[INFO] Modelo generado en formato PLY: {modelo_ply}")

        ruta_salida_ply = os.path.join("data", "output", f"{nombre_modelo}.ply")
        os.rename(modelo_ply, ruta_salida_ply)

        print(f"[INFO] Modelo guardado como PLY en: {ruta_salida_ply}")
    else:
        print(f"[ERROR] El modelo PLY no se generó correctamente en {model_text_dir}")
