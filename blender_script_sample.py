# create_futuristic_shape3.py
import bpy

# 1. Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 2. Create a torus
bpy.ops.mesh.primitive_torus_add(
    major_radius=1.0,
    minor_radius=0.3,
    location=(0,0,0)
)
torus_obj = bpy.context.active_object
torus_obj.name = "FuturisticTwistedTorus"

# 3. Add a twist modifier
twist_mod = torus_obj.modifiers.new("TwistMod", 'SIMPLE_DEFORM')
twist_mod.deform_method = 'TWIST'
twist_mod.angle = 1.5  # in radians (~86 degrees)
twist_mod.origin = None

# Apply the modifier
bpy.ops.object.modifier_apply(modifier="TwistMod")

# 4. Neon-cyan glass material with fallback
mat = bpy.data.materials.new("NeonCyanGlassTorus")
mat.use_nodes = True
mat.use_backface_culling = False

bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    # Transmission fallback
    has_transmission = any(inp.name == "Transmission" for inp in bsdf.inputs)
    if has_transmission:
        bsdf.inputs["Transmission"].default_value = 1.0
        bsdf.inputs["Roughness"].default_value    = 0.0
    else:
        alpha_inp = bsdf.inputs.get("Alpha", None)
        if alpha_inp:
            alpha_inp.default_value = 0.2
            mat.blend_method = 'BLEND'
    # Emission fallback
    emiss_inp = bsdf.inputs.get("Emission", None)
    emiss_str = bsdf.inputs.get("Emission Strength", None)
    if emiss_inp and emiss_str:
        emiss_inp.default_value = (0.0, 1.0, 1.0, 1.0)
        emiss_str.default_value = 10.0
    else:
        # Build pure Emission node
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        # Avoid modifying the collection while iterating by
        # converting it to a list first
        for node in list(nodes):
            nodes.remove(node)
        emission_node = nodes.new("ShaderNodeEmission")
        emission_node.inputs["Color"].default_value    = (0.0, 1.0, 1.0, 1.0)
        emission_node.inputs["Strength"].default_value = 10.0
        output_node = nodes.new("ShaderNodeOutputMaterial")
        links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])

# Assign material
if not torus_obj.data.materials:
    torus_obj.data.materials.append(mat)
else:
    torus_obj.data.materials[0] = mat

# 5. Export
usd_path = "/Users/ivancampos/Downloads/futuristicShape3.usd"
bpy.ops.wm.usd_export(
    filepath=usd_path,
    check_existing=False,
    export_textures=True,
    export_materials=True
)
print(f"Exported Twisted Torus to: {usd_path}")
