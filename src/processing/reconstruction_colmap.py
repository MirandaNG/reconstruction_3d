import os
import subprocess
import shutil
import uuid

def ejecutar_colmap(lista_rutas_imagenes, salida_dir):
    temp_id = str(uuid.uuid4())
    imagenes_dir = os.path.join("data", "temp_colmap_input", temp_id)
    os.makedirs(imagenes_dir, exist_ok=True)

    for ruta in lista_rutas_imagenes:
        nombre = os.path.basename(ruta)
        destino = os.path.join(imagenes_dir, nombre)
        if not os.path.exists(destino):
            shutil.copy(ruta, destino)

    sparse_dir = os.path.join(salida_dir, "sparse")
    database_path = os.path.join(salida_dir, "database.db")
    model_text_path = os.path.join(salida_dir, "model_text.ply")

    for carpeta in [sparse_dir]:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
    if os.path.exists(database_path):
        os.remove(database_path)
    if os.path.exists(model_text_path):
        os.remove(model_text_path)

    os.makedirs(sparse_dir, exist_ok=True)

    colmap_path = os.path.abspath("src/models/colmap/colmap-x64-windows-nocuda/bin/colmap.exe")
    qt_plugin_path = os.path.abspath("src/models/colmap/colmap-x64-windows-nocuda/plugins")
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugin_path

    print("[INFO] Iniciando extracción de características...")
    subprocess.run([
        colmap_path, "feature_extractor",
        "--database_path", database_path,
        "--image_path", imagenes_dir,
        "--SiftExtraction.max_num_features", "25000",
        "--SiftExtraction.peak_threshold", "0.0025",
        "--SiftExtraction.edge_threshold", "10"
    ], check=True)

    print("[INFO] Características extraídas. Iniciando coincidencias...")
    subprocess.run([
        colmap_path, "exhaustive_matcher",
        "--database_path", database_path,
        "--ExhaustiveMatching.block_size", "50"
    ], check=True)

    print("[INFO] Coincidencias generadas. Ejecutando mapper...")
    subprocess.run([
        colmap_path, "mapper",
        "--database_path", database_path,
        "--image_path", imagenes_dir,
        "--output_path", sparse_dir,
        "--Mapper.ba_local_max_num_iterations", "100",
        "--Mapper.ba_global_max_num_iterations", "200",
        "--Mapper.init_min_num_inliers", "20",
        "--Mapper.init_max_error", "6",
        "--Mapper.abs_pose_min_num_inliers", "15",
        "--Mapper.abs_pose_max_error", "10"
    ], check=True)

    # Convertir modelo sparse a PLY
    subprocess.run([
        colmap_path, "model_converter",
        "--input_path", os.path.join(sparse_dir, "0"),
        "--output_path", model_text_path,
        "--output_type", "PLY"
    ], check=True)

    # Elimina las imágenes temporales
    shutil.rmtree(imagenes_dir, ignore_errors=True)

    print(f"[INFO] Reconstrucción sparse completada. Modelo exportado a: {model_text_path}")