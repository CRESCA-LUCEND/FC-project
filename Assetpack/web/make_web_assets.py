"""Builds web-ready assets from the asset pack (run headless, never touches the source files):

    blender -b can_3d.blend --factory-startup --python web/make_web_assets.py

Writes into Assetpack/web/:
    can_rhubarb.glb, can_lemon.glb   - the 500 ml can, metres, base at y=0, glTF PBR materials, Draco compressed
    *.webp                           - every PNG render resized to max 2400 px (alpha kept)
"""
import os
import bpy

PACK = os.path.dirname(bpy.data.filepath)
OUT = os.path.join(PACK, "web")
os.makedirs(OUT, exist_ok=True)

objs = [o for o in bpy.data.objects if o.type == 'MESH']
body = next(o for o in objs if o.data.uv_layers and "Bottom" not in o.name and "Tab" not in o.name and "Top" not in o.name)

# ---- geometry: one subdivision level is plenty on screen, condensation off, can stands at the origin
for o in objs:
    for m in list(o.modifiers):
        if m.type == 'SUBSURF':
            m.levels = 1
        elif m.type == 'NODES':
            o.modifiers.remove(m)
off = body.location.copy()            # base of the can goes to the origin
for o in objs:
    o.location -= off
    o.rotation_euler = (0, 0, 0)

# ---- simple glTF-friendly materials
def pbr(name, color=(0.8, 0.8, 0.82, 1), metal=1.0, rough=0.28, image=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if image:
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = image
        nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    return m

alu = pbr("aluminium", (0.80, 0.80, 0.82, 1), 1.0, 0.3)
lid = pbr("aluminium_lid", (0.86, 0.86, 0.88, 1), 1.0, 0.22)
for o in objs:
    if o is body:
        continue
    o.data.materials.clear()
    o.data.materials.append(lid if ("Top" in o.name or "Tab" in o.name) else alu)
    o.name = "can_" + ("lid" if "Top" in o.name else "tab" if "Tab" in o.name else "base")
body.name = "can_body"

for flavour in ("rhubarb", "lemon"):
    img = bpy.data.images.load(os.path.join(PACK, f"label_{flavour}_500ml_final.png"), check_existing=True)
    label = pbr(f"label_{flavour}", metal=0.3, rough=0.3, image=img)
    body.data.materials.clear(); body.data.materials.append(label)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, f"can_{flavour}.glb"), export_format='GLB',
                              use_selection=True, export_apply=True, export_yup=True,
                              export_draco_mesh_compression_enable=True, export_image_format='WEBP')

# ---- web versions of the renders
for f in sorted(os.listdir(PACK)):
    if not f.lower().endswith(".png") or f.startswith("label_"):
        continue
    im = bpy.data.images.load(os.path.join(PACK, f))
    w, h = im.size
    k = min(1.0, 2400 / max(w, h))
    if k < 1:
        im.scale(int(w * k), int(h * k))
    im.file_format = 'WEBP'
    im.filepath_raw = os.path.join(OUT, os.path.splitext(f)[0].replace("0001", "") + ".webp")
    im.save()
    bpy.data.images.remove(im)
print("WEB_ASSETS_DONE", sorted(os.listdir(OUT)))
