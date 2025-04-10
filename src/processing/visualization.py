import os
import vtk
from tkinter import filedialog

def mostrar_modelo(ruta_modelo=None):
    # Si no se pasa una ruta como argumento, abrir el cuadro de diálogo
    if ruta_modelo is None:
        ruta_modelo = filedialog.askopenfilename(
            title="Selecciona un modelo 3D",
            initialdir=os.path.join("data", "output"),
            filetypes=[("Archivos OBJ", "*.obj")]
        )

    if not ruta_modelo:
        print("[INFO] No se seleccionó ningún archivo.")
        return

    print(f"[INFO] Visualizando: {ruta_modelo}")

    # Crear un lector de archivos OBJ
    reader = vtk.vtkOBJReader()
    reader.SetFileName(ruta_modelo)

    # Crear un mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Crear un actor para mostrar la geometría
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Crear un renderer, una ventana de renderizado y un interactor
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.4)  # Color de fondo

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Iniciar la visualización
    render_window.Render()
    render_window_interactor.Start()