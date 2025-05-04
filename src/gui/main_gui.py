import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox

from src.gui.file_dialogs import seleccionar_imagenes
from src.processing.reconstruction_depth import reconstruir_3d_desde_imagen as reconstruccion_midas
from src.processing.reconstruction_colmap import ejecutar_colmap as reconstruccion_colmap
from src.processing.visualization import mostrar_modelo
#from src.utils.file_utils import guardar_modelo

rutas_imagenes = []

# Función para mover las imágenes seleccionadas a data/input
def mover_imagenes_a_input(imagenes):
    directorio_destino = "data/input"
    os.makedirs(directorio_destino, exist_ok=True)

    rutas_destino = []
    for imagen in imagenes:
        nombre_imagen = os.path.basename(imagen)
        destino = os.path.join(directorio_destino, nombre_imagen)
        shutil.copy(imagen, destino)
        rutas_destino.append(destino)

    return rutas_destino

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Reconstrucción 3D desde Imágenes")
    ventana.geometry("450x300")

    def cargar_imagenes():
        global rutas_imagenes
        rutas_imagenes = seleccionar_imagenes()

        if not rutas_imagenes:
            messagebox.showwarning("Advertencia", "No se seleccionaron imágenes.")
            return

        rutas_imagenes = mover_imagenes_a_input(rutas_imagenes)

        if len(rutas_imagenes) == 1:
            opcion = "MiDaS (1 imagen)"
        else:
            opcion = "COLMAP (múltiples imágenes)"

        reconfirmar = messagebox.askyesno(
            "Confirmar Reconstrucción",
            f"Seleccionaste {len(rutas_imagenes)} imagen(es).\nUsarás: {opcion}.\n¿Continuar?"
        )

        if not reconfirmar:
            return

        # Reconstrucción
        if len(rutas_imagenes) == 1:
            modelo_generado = reconstruccion_midas(rutas_imagenes[0])
        else:
            modelo_generado = reconstruccion_colmap(rutas_imagenes, "data/output")

        if modelo_generado:
            messagebox.showinfo("Éxito", "El modelo se generó y guardó automáticamente en la carpeta de salida.")
        else:
            messagebox.showerror("Error", "No se generó el modelo correctamente.")

    def visualizar_modelo():
        mostrar_modelo()

    ttk.Button(ventana, text="Cargar Imágenes y Reconstruir", command=cargar_imagenes).pack(pady=15)
    ttk.Button(ventana, text="Visualizar Modelo Existente", command=visualizar_modelo).pack(pady=10)

    ventana.mainloop()