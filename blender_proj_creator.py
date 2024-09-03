import bpy
import math

def create_project(logo_path):
    # Limpar a cena existente
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Adicionar uma esfera
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=64, ring_count=32)
    sphere = bpy.context.active_object
    
    # Criar um material novo
    mat = bpy.data.materials.new(name="LogoMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    # Adicionar o nó de textura da imagem
    tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(logo_path)
    
    # Conectar a textura ao BSDF
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
    
    # Aplicar o material à esfera
    if sphere.data.materials:
        sphere.data.materials[0] = mat
    else:
        sphere.data.materials.append(mat)
    
    # Adicionar uma câmera
    bpy.ops.object.camera_add(location=(0, -3, 1.5), rotation=(math.radians(75), 0, 0))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera
    
    # Adicionar iluminação
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    light = bpy.context.active_object
    light.data.energy = 3

    # Salvar o arquivo do projeto
    bpy.ops.wm.save_as_mainfile(filepath="logo_project.blend")

# Caminho da logo
logo_path = "metta_safe_logo_square.png"  # Substitua pelo caminho da sua logo

# Criar o projeto
create_project(logo_path)

