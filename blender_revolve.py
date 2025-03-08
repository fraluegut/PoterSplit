import bpy
import os

# 📂 Configuración de la ruta del archivo SVG
SVG_FILE = r"C:\Users\franc\PycharmProjects\PoterSplit\output\imagen_limpiada.svg"

def import_and_revolve(svg_path):
    """
    Importa un perfil SVG en Blender, lo convierte en malla,
    lo cierra con una cara, lo rota 90° en X y lo revoluciona 360°.
    """
    print("🚀 Iniciando script en Blender...")

    if not os.path.exists(svg_path):
        print(f"❌ Error: No se encontró el archivo SVG en {svg_path}")
        return

    print(f"🟢 Importando SVG desde: {svg_path}")

    # **1️⃣ Eliminar todos los objetos en la escena**
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("🗑️ Escena limpiada.")

    # **2️⃣ Importar SVG**
    bpy.ops.import_curve.svg(filepath=svg_path)
    print("📥 SVG importado correctamente.")

    # **3️⃣ Seleccionar el objeto importado**
    imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'CURVE']

    if not imported_objects:
        print("❌ Error: No se pudo encontrar la curva importada en la escena.")
        return

    curve_obj = imported_objects[0]
    bpy.context.view_layer.objects.active = curve_obj
    bpy.ops.object.select_all(action='DESELECT')
    curve_obj.select_set(True)

    print(f"✅ Objeto importado: {curve_obj.name}")

    # **4️⃣ Convertir la curva en malla**
    bpy.ops.object.convert(target='MESH')
    print("🔄 Convertido a malla.")

    # **5️⃣ Asegurar que la base se cierra con una cara**
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.edge_face_add()
    bpy.ops.object.editmode_toggle()
    print("🛠️ Base cerrada correctamente.")

    # **6️⃣ Aplicar transformaciones antes de girar**
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # **7️⃣ Rotar -90° en el eje X**
    bpy.ops.transform.rotate(value=-1.5708, orient_axis='X')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    print("🔄 Rotado -90° en el eje X.")

    # **8️⃣ Aplicar modificador de revolución (Screw)**
    bpy.ops.object.modifier_add(type='SCREW')
    screw_mod = curve_obj.modifiers["Screw"]
    screw_mod.angle = 6.28319  # 360° en radianes
    screw_mod.axis = 'Z'
    screw_mod.steps = 64
    screw_mod.use_merge_vertices = True
    screw_mod.use_smooth_shade = True
    screw_mod.center = 0
    screw_mod.screw_offset = 0
    print("🔄 Revolución 360° aplicada correctamente.")

    print("✅ Proceso completado en Blender.")


# --- USO ---
import_and_revolve(SVG_FILE)
