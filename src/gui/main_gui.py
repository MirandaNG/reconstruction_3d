import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.file_dialogs import seleccionar_imagenes
from src.processing.reconstruction import reconstruir_desde_imagenes
from src.processing.visualization import mostrar_modelo
from src.utils.file_utils import guardar_modelo

rutas_imagenes = []

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Reconstrucción 3D desde imágenes")
    ventana.geometry("400x300")

    def cargar_imagenes():
        global rutas_imagenes
        rutas_imagenes = seleccionar_imagenes()
        if rutas_imagenes:
            messagebox.showinfo("Imágenes seleccionadas", f"{len(rutas_imagenes)} imagen(es) cargada(s).")

    def reconstruir_modelo():
        if rutas_imagenes:
            modelo = reconstruir_desde_imagenes(rutas_imagenes)
            messagebox.showinfo("Reconstrucción", f"Modelo generado: {modelo}")
        else:
            messagebox.showwarning("Error", "No se han seleccionado imágenes.")

    def guardar_modelo_3d():
        formato, ruta = guardar_modelo()
        if ruta:
            messagebox.showinfo("Guardado", f"Modelo exportado como {formato} en:\n{ruta}")
        elif formato == "Formato no válido":
            messagebox.showerror("Error", "Formato de archivo no válido.")

    # Botones GUI
    ttk.Button(ventana, text="Cargar Imágenes", command=cargar_imagenes).pack(pady=10)
    ttk.Button(ventana, text="Reconstruir Modelo", command=reconstruir_modelo).pack(pady=10)
    ttk.Button(ventana, text="Guardar Modelo 3D", command=guardar_modelo_3d).pack(pady=10)
    ttk.Button(ventana, text="Previsualizar Modelo", command=mostrar_modelo).pack(pady=10)

    ventana.mainloop()