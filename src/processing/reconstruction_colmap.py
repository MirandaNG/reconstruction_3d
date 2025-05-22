import os
import subprocess
import shutil
import uuid

def ejecutar_colmap(lista_rutas_imagenes, salida_dir):
    # Crear carpeta temporal con un nombre único
    temp_id = str(uuid.uuid4())
    imagenes_dir = os.path.join("data", "temp_colmap_input", temp_id)
    os.makedirs(imagenes_dir, exist_ok=True)

    # Copiar las imágenes seleccionadas por el usuario
    for ruta in lista_rutas_imagenes:
        nombre = os.path.basename(ruta)
        destino = os.path.join(imagenes_dir, nombre)
        if not os.path.exists(destino):
            shutil.copy(ruta, destino)

    sparse_dir = os.path.join(salida_dir, "sparse")
    model_text_path = os.path.join(salida_dir, "model_text.ply")
    database_path = os.path.join(salida_dir, "database.db")

    # Limpiar resultados anteriores
    for carpeta in [sparse_dir]:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
    if os.path.exists(database_path):
        os.remove(database_path)
    if os.path.exists(model_text_path):
        os.remove(model_text_path)

    os.makedirs(sparse_dir, exist_ok=True)

    # Ruta al ejecutable de COLMAP
    colmap_path = os.path.abspath("src/models/colmap/colmap-x64-windows-nocuda/bin/colmap.exe")
    qt_plugin_path = os.path.abspath("src/models/colmap/colmap-x64-windows-nocuda/plugins")
    print(f"[DEBUG] Plugin Qt: {qt_plugin_path}")
    print(f"[DEBUG] Existe directorio plugins: {os.path.exists(qt_plugin_path)}")
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugin_path

    print(f"[DEBUG] Ejecutando COLMAP desde: {colmap_path}")

    print("[INFO] Iniciando extracción de características...")
    subprocess.run([
        colmap_path, "feature_extractor",
        "--database_path", database_path,
        "--image_path", imagenes_dir,
        "--SiftExtraction.max_num_features", "15000",
        "--SiftExtraction.peak_threshold", "0.003",
        "--SiftExtraction.edge_threshold", "10"
    ], check=True)
    print("[INFO] Características extraídas.")

    try:
        result = subprocess.run([
            colmap_path, "exhaustive_matcher",
            "--database_path", database_path,
            "--ExhaustiveMatching.block_size", "50"
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("[ERROR] Falló exhaustive_matcher:", e)
        print("[STDOUT]", e.stdout)
        print("[STDERR]", e.stderr)
        raise

    print("[INFO] Coincidencias generadas exitosamente.")
    print("[STDOUT]", result.stdout)
    print("[STDERR]", result.stderr)

    subprocess.run([
    colmap_path, "mapper",
    "--database_path", database_path,
    "--image_path", imagenes_dir,
    "--output_path", sparse_dir,
    "--Mapper.ba_local_max_num_iterations", "50",  # Más refinamiento local
    "--Mapper.ba_global_max_num_iterations", "100",  # Más refinamiento global
    "--Mapper.init_min_num_inliers", "50",  # Permite inicialización más fácil
    "--Mapper.init_max_error", "6",  # Más tolerancia al error en la inicialización
    "--Mapper.abs_pose_min_num_inliers", "25",
    "--Mapper.abs_pose_max_error", "10"
], check=True)

    subprocess.run([
        colmap_path, "model_converter",
        "--input_path", os.path.join(sparse_dir, "0"),
        "--output_path", model_text_path,
        "--output_type", "PLY"
    ], check=True)

    modelo_ply = os.path.join(model_text_path, "model_text.ply")
    if os.path.exists(modelo_ply):
        nombre_modelo = os.path.splitext(os.path.basename(lista_rutas_imagenes[0]))[0]
        ruta_salida_ply = os.path.join("data", "output", f"{nombre_modelo}_colmap.ply")
        shutil.move(modelo_ply, ruta_salida_ply)

        # Limpiar input temporal
        shutil.rmtree(imagenes_dir, ignore_errors=True)

        print(f"[INFO] Modelo generado y guardado en: {ruta_salida_ply}")
        return ruta_salida_ply
    else:
        print(f"[ERROR] El modelo PLY no se generó correctamente en {model_text_path}")
        return None