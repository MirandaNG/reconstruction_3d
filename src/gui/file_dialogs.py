from tkinter import filedialog

def seleccionar_imagenes():
    rutas = filedialog.askopenfilenames(
        title="Seleccionar imágenes",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
    )
    return list(rutas)

def seleccionar_modelo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar modelo 3D",
        filetypes=[("Modelos 3D", "*.obj *.ply")]
    )
    return ruta