import bpy
import os
import math

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.images:
        bpy.data.images.remove(block)

def reconstruir_con_una_imagen(ruta_imagen):
    limpiar_escena()
    print(f"[INFO] Reconstruyendo modelo con una sola imagen: {ruta_imagen}")

    # Crear un plano y mapear la imagen como textura
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
    plano = bpy.context.active_object

    # Crear material
    mat = bpy.data.materials.new(name="MaterialImagen")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    # Crear nodo de textura de imagen
    tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(ruta_imagen)

    # Conectar al BSDF
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

    # Asignar material al plano
    if plano.data.materials:
        plano.data.materials[0] = mat
    else:
        plano.data.materials.append(mat)

    # Exportar como OBJ
    nombre_modelo = os.path.splitext(os.path.basename(ruta_imagen))[0]
    ruta_salida = os.path.join("data", "output", f"{nombre_modelo}.obj")
    bpy.ops.export_scene.obj(filepath=ruta_salida)
    print(f"[INFO] Modelo exportado a: {ruta_salida}")
    return ruta_salida


def reconstruir_con_multiples_imagenes(rutas_imagenes):
    limpiar_escena()
    print(f"[INFO] Reconstruyendo modelo con {len(rutas_imagenes)} imágenes...")

    distancia = 3  # Separación entre planos
    for i, ruta in enumerate(rutas_imagenes):
        x = math.cos(math.radians(i * 360 / len(rutas_imagenes))) * distancia
        y = math.sin(math.radians(i * 360 / len(rutas_imagenes))) * distancia

        # Crear plano
        bpy.ops.mesh.primitive_plane_add(size=2, location=(x, y, 0))
        plano = bpy.context.active_object

        # Crear material con la imagen
        mat = bpy.data.materials.new(name=f"Material_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]

        tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_image.image = bpy.data.images.load(ruta)

        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

        # Asignar material
        if plano.data.materials:
            plano.data.materials[0] = mat
        else:
            plano.data.materials.append(mat)

    # Exportar modelo combinado
    nombre_modelo = os.path.splitext(os.path.basename(rutas_imagenes[0]))[0]
    ruta_salida = os.path.join("data", "output", f"{nombre_modelo}_multi.obj")
    bpy.ops.export_scene.obj(filepath=ruta_salida)
    print(f"[INFO] Modelo exportado a: {ruta_salida}")
    return ruta_salida