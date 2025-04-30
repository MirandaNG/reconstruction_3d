import torch
import os
import cv2
import numpy as np
from src.models.midas.MiDaSmaster.midas.dpt_depth import DPTDepthModel
from src.models.midas.MiDaSmaster.midas.transforms import Resize, NormalizeImage, PrepareForNet
import torchvision.transforms as T
import open3d as o3d

def cargar_modelo_midas(peso="src/models/midas/weights/dpt_hybrid_384.pt"):
    modelo = DPTDepthModel(
        path=peso,
        backbone="vitb_rn50_384",
        non_negative=True
    )
    modelo.eval()
    return modelo

def estimar_profundidad(imagen_path, modelo):
    imagen = cv2.imread(imagen_path)
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    transform = T.Compose([
        Resize(
            384, 384, resize_target=None, keep_aspect_ratio=True,
            ensure_multiple_of=32, resize_method="minimal"
        ),
        NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        PrepareForNet()
    ])
    input_tensor = transform({"image": imagen_rgb})["image"]
    input_batch = torch.from_numpy(input_tensor).unsqueeze(0)

    with torch.no_grad():
        prediction = modelo.forward(input_batch)[0]
    depth = prediction.squeeze().cpu().numpy()
    return depth, imagen_rgb

def generar_nube_puntos(depth, imagen_rgb):
    h, w = depth.shape
    xx, yy = np.meshgrid(np.arange(0, w), np.arange(0, h))
    x = xx.flatten()
    y = yy.flatten()
    z = depth.flatten()

    puntos = np.stack((x, y, z), axis=1)
    colores = imagen_rgb.reshape(-1, 3) / 255.0

    # Filtrar fondo (z muy bajos)
    mask = z > np.percentile(z, 5)
    puntos = puntos[mask]
    colores = colores[mask]

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(puntos)
    pcd.colors = o3d.utility.Vector3dVector(colores)

    return pcd

def generar_relieve_desde_profundidad(depth, imagen_rgb=None, escala=1.0):
    h, w = depth.shape
    puntos = []
    colores = []

    for y in range(h):
        for x in range(w):
            z = depth[y, x] * escala
            puntos.append([x, y, z])
            if imagen_rgb is not None:
                colores.append(imagen_rgb[y, x] / 255.0)
            else:
                colores.append([0.5, 0.5, 0.5])  # Gris neutro

    puntos = np.array(puntos)
    colores = np.array(colores)

    faces = []
    for y in range(h - 1):
        for x in range(w - 1):
            i = y * w + x
            faces.append([i, i + 1, i + w])
            faces.append([i + 1, i + w + 1, i + w])

    malla = o3d.geometry.TriangleMesh()
    malla.vertices = o3d.utility.Vector3dVector(puntos)
    malla.triangles = o3d.utility.Vector3iVector(np.array(faces))
    malla.vertex_colors = o3d.utility.Vector3dVector(colores)
    malla.compute_vertex_normals()
    return malla


def reconstruir_3d_desde_imagen(imagen_path):
    # Obtener el nombre base sin extensión del archivo
    nombre = os.path.splitext(os.path.basename(imagen_path))[0]

    modelo = cargar_modelo_midas()
    depth, imagen_rgb = estimar_profundidad(imagen_path, modelo)

    # 🔧 Ajustar la profundidad al tamaño original
    depth = cv2.resize(depth, (imagen_rgb.shape[1], imagen_rgb.shape[0]), interpolation=cv2.INTER_CUBIC)

    # Generar y guardar nube de puntos
    nube = generar_nube_puntos(depth, imagen_rgb)
    ruta_nube = os.path.join("data", "output", f"{nombre}_nube.ply")
    o3d.io.write_point_cloud(ruta_nube, nube)
    print(f"[INFO] Nube de puntos exportada a: {ruta_nube}")

    # Generar y guardar relieve como malla 3D
    malla = generar_relieve_desde_profundidad(depth, imagen_rgb, escala=0.5)
    ruta_malla = os.path.join("data", "output", f"{nombre}_malla.ply")
    o3d.io.write_triangle_mesh(ruta_malla, malla)
    print(f"[INFO] Malla tipo relieve exportada a: {ruta_malla}")