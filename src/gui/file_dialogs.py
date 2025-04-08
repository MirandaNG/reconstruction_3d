from tkinter import filedialog

def seleccionar_imagenes():
    rutas = filedialog.askopenfilenames(
        title="Seleccionar imágenes",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
    )
    return list(rutas)