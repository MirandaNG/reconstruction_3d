import os
import open3d as o3d
from tkinter import filedialog

def mostrar_modelo():
    ruta_modelo = filedialog.askopenfilename(
        title="Selecciona un modelo 3D",
        initialdir=os.path.join("data", "output"),
        filetypes=[("Archivos OBJ", "*.obj")]
    )

    if not ruta_modelo:
        print("[INFO] No se seleccionó ningún archivo.")
        return

    print(f"[INFO] Visualizando: {ruta_modelo}")
    malla = o3d.io.read_triangle_mesh(ruta_modelo)
    if not malla.has_vertices():
        print("[ERROR] El modelo no contiene vértices.")
        return

    o3d.visualization.draw_geometries([malla])
