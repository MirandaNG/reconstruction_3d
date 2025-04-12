import bpy
import os
import math
import sys

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.images:
        bpy.data.images.remove(block)

def reconstruir_con_una_imagen(ruta_imagen):
    limpiar_escena()
    print(f"[INFO] Reconstruyendo modelo con una sola imagen: {ruta_imagen}")
    # Plano + textura (igual que antes)
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
    plano = bpy.context.active_object
    mat = bpy.data.materials.new(name="MaterialImagen")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(ruta_imagen)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
    plano.data.materials.append(mat)
    nombre = os.path.splitext(os.path.basename(ruta_imagen))[0]
    ruta_out = os.path.join("data", "output", f"{nombre}.glb")
    bpy.ops.export_scene.gltf(filepath=ruta_out, export_format='GLB')
    print(f"[INFO] Modelo exportado a: {ruta_out}")

def reconstruir_con_multiples_imagenes(rutas):
    limpiar_escena()
    print(f"[INFO] Reconstruyendo con {len(rutas)} imágenes...")
    distancia = 3
    for i, ruta in enumerate(rutas):
        x = math.cos(math.radians(i * 360 / len(rutas))) * distancia
        y = math.sin(math.radians(i * 360 / len(rutas))) * distancia
        bpy.ops.mesh.primitive_plane_add(size=2, location=(x, y, 0))
        plano = bpy.context.active_object
        mat = bpy.data.materials.new(name=f"Material_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_image.image = bpy.data.images.load(ruta)
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
        plano.data.materials.append(mat)
    nombre = os.path.splitext(os.path.basename(rutas[0]))[0]
    ruta_out = os.path.join("data", "output", f"{nombre}_multi.glb")
    bpy.ops.export_scene.gltf(filepath=ruta_out, export_format='GLB')
    print(f"[INFO] Modelo exportado a: {ruta_out}")

if __name__ == "__main__":
    args = sys.argv
    rutas = args[args.index("--") + 1:]  # Solo lo que viene después de "--"
    if len(rutas) == 1:
        reconstruir_con_una_imagen(rutas[0])
    elif len(rutas) > 1:
        reconstruir_con_multiples_imagenes(rutas)
    else:
        print("[ERROR] No se proporcionaron imágenes.")
