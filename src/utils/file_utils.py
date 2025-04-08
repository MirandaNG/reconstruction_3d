from tkinter import filedialog

def guardar_modelo():
    opciones = [("Archivo OBJ", "*.obj"), ("Archivo STL", "*.stl"), ("Archivo Blender", "*.blend")]
    archivo = filedialog.asksaveasfilename(
        title="Guardar modelo 3D",
        defaultextension=".obj",
        filetypes=opciones
    )

    if archivo:
        extension = archivo.split('.')[-1].lower()
        if extension not in ['obj', 'stl', 'blend']:
            return "Formato no válido", None
        return extension, archivo
    return None, None
