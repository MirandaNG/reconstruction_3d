import open3d as o3d
import os

def mostrar_modelo(ruta_modelo):
    if not os.path.exists(ruta_modelo):
        print(f"[ERROR] El archivo no existe: {ruta_modelo}")
        return

    extension = os.path.splitext(ruta_modelo)[1].lower()

    modelo = o3d.io.read_triangle_mesh(ruta_modelo)
    if not modelo.has_triangles():
        modelo = o3d.io.read_point_cloud(ruta_modelo)

    # Crear visualizador personalizado
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Visualización 3D")

    vis.add_geometry(modelo)

    # Fondo gris (RGB entre 0 y 1)
    opt = vis.get_render_option()
    opt.background_color = [0.8, 0.8, 0.8]  # Gris claro

    vis.run()
    vis.destroy_window()