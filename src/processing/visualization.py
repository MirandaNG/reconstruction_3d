import open3d as o3d
import os

def mostrar_modelo(ruta_modelo):
    if not os.path.exists(ruta_modelo):
        print(f"[ERROR] El modelo {ruta_modelo} no existe.")
        return

    print(f"[INFO] Mostrando modelo: {ruta_modelo}")
    malla = o3d.io.read_triangle_mesh(ruta_modelo)
    if not malla.has_vertex_normals():
        malla.compute_vertex_normals()

    o3d.visualization.draw_geometries([malla])