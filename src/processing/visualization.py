import os
import vtk
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

    # Leer el archivo OBJ
    reader = vtk.vtkOBJReader()
    reader.SetFileName(ruta_modelo)
    reader.Update()

    # Crear un mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Crear un actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Configurar el renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.4)

    # Crear ventana e interactor
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Mostrar ventana
    render_window.Render()
    interactor.Start()