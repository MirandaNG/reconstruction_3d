import bpy
import sys

def cargar_y_mostrar_modelo():
    # Obtener la ruta del modelo desde los argumentos pasados
    ruta_modelo = sys.argv[-1]

    # Limpiar la escena de Blender
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Cargar el modelo (dependiendo de su extensión)
    if ruta_modelo.endswith(".glb"):
        bpy.ops.import_scene.gltf(filepath=ruta_modelo)
    elif ruta_modelo.endswith(".obj"):
        bpy.ops.import_scene.obj(filepath=ruta_modelo)
    elif ruta_modelo.endswith(".ply"):
        bpy.ops.import_mesh.ply(filepath=ruta_modelo)

    # Ajustar la cámara para ver el modelo
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.view3d.camera_to_view_selected()

    # Configurar la visualización en Blender
    bpy.context.view_layer.objects.active = bpy.context.view_layer.objects[0]
    bpy.ops.object.shade_smooth()

# Ejecutar la función
cargar_y_mostrar_modelo()
