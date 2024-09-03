import bpy
import bmesh
import math
import random

def create_surface(surface_type):
    if surface_type == 'PLANE':
        bpy.ops.mesh.primitive_plane_add(size=2)
    elif surface_type == 'SPHERE':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=2, segments=64, ring_count=32)  # Aumenta a resolução da esfera
    elif surface_type == 'CYLINDER':
        bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=2, vertices=64)  # Aumenta a resolução do cilindro
    elif surface_type == 'CUBE':
        bpy.ops.mesh.primitive_cube_add(size=2)
    #elif surface_type == 'IRREGULAR':
    #    bpy.ops.mesh.primitive_ico_sphere_add(radius=1, subdivisions=4)  # Aumenta as subdivisões para mais detalhes
    #    obj = bpy.context.active_object
    #    bpy.ops.object.mode_set(mode='EDIT')
    #    bm = bmesh.from_edit_mesh(obj.data)
    #    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2, use_grid_fill=True)
    #    for v in bm.verts:
    #        v.co += v.normal * random.uniform(-0.02, 0.02)  # Reduz a distorção para manter a logo legível
    #    bmesh.update_edit_mesh(obj.data)
    #    bpy.ops.object.mode_set(mode='OBJECT')
    
    obj = bpy.context.active_object
    return obj

def add_subdivision(obj):
    subdivision = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subdivision.levels = 3  # Nível de subdivisão para mais detalhes
    subdivision.render_levels = 3

def add_displacement(obj):
    texture = bpy.data.textures.new("DisplacementTexture", type='VORONOI')
    texture.noise_scale = random.uniform(1.0, 1.5)  # Aumenta a escala do ruído para distorções menores
    texture.contrast = random.uniform(0.7, 0.9)  # Reduz o contraste para suavizar a distorção
    displace = obj.modifiers.new(name="Displace", type='DISPLACE')
    displace.texture = texture
    displace.strength = random.uniform(0.005, 0.02)  # Reduz ainda mais a força do deslocamento

def apply_logo(surface, logo_path):
    mat = bpy.data.materials.new(name="LogoMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Limpar nós existentes
    nodes.clear()

    # Criar nós
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    image_texture = nodes.new(type='ShaderNodeTexImage')
    image_texture.image = bpy.data.images.load(logo_path)

    # Conectar nós
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])  # Use o mapeamento UV
    links.new(mapping.outputs['Vector'], image_texture.inputs['Vector'])
    links.new(image_texture.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    # Ajustar mapeamento
    mapping.inputs['Scale'].default_value = (1.0, 1.0, 1.0)  # Define a escala da textura para 1:1
    mapping.inputs['Location'].default_value = (0, 0, 0)  # Centraliza a textura

    # Configurar material
    mat.blend_method = 'BLEND'
    
    surface.data.materials.append(mat)

def setup_camera():
    # Ajuste da câmera para capturar melhor os detalhes
    bpy.ops.object.camera_add(location=(0, -4, 1.5), rotation=(math.radians(70), 0, 0))
    camera = bpy.context.active_object
    camera.data.lens = 50  # Aumenta o zoom para capturar mais detalhes
    bpy.context.scene.camera = camera
    return camera

def setup_lighting():
    # Luz principal
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    sun = bpy.context.active_object
    sun.data.energy = random.uniform(3, 5)
    sun.rotation_euler = (random.uniform(0, math.pi/4), random.uniform(0, math.pi/4), random.uniform(0, 2*math.pi))

    # Luz de preenchimento
    bpy.ops.object.light_add(type='POINT', location=(-3, -3, 3))
    fill_light = bpy.context.active_object
    fill_light.data.energy = random.uniform(50, 100)
    
def orient_logo_towards_camera(surface, camera):
    # Apontar a face da textura para a câmera
    direction = camera.location - surface.location
    surface.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()

def render_scene(output_path):
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

def main(logo_path, num_variations, output_folder, image_size):
    # Configurar o tamanho da imagem
    bpy.context.scene.render.resolution_x = image_size
    bpy.context.scene.render.resolution_y = image_size

    # Limpar a cena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Configurar a câmera (apenas uma vez)
    camera = setup_camera()

    surface_types = ['PLANE', 'SPHERE', 'CYLINDER', 'CUBE']

    for i in range(num_variations):
        # Criar uma nova superfície
        surface_type = random.choice(surface_types)
        surface = create_surface(surface_type)

        # Adicionar subdivisão e deslocamento
        #add_subdivision(surface)
        #add_displacement(surface)

        # Aplicar a logo
        apply_logo(surface, logo_path)

        # Configurar iluminação (nova para cada variação)
        setup_lighting()
        
        orient_logo_towards_camera(surface, camera)

        # Rotacionar e posicionar aleatoriamente o objeto
        surface.rotation_euler = (random.uniform(0, 2*math.pi), random.uniform(0, 2*math.pi), random.uniform(0, 2*math.pi))
        surface.location = (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))

        # Renderizar a cena
        render_scene(f"{output_folder}/logo_variation_{i:03d}.png")

        # Remover objetos da cena, exceto a câmera
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = camera
        camera.select_set(False)
        bpy.ops.object.delete()

# Uso do script
logo_path = "/media/DATA/linux/workspace/scripts/img-augmentation/metta_safe_logo_square.png"
num_variations = 10
output_folder = "/media/DATA/linux/workspace/scripts/img-augmentation/output"
image_size = 1024  # Ou 512, dependendo da sua preferência

main(logo_path, num_variations, output_folder, image_size)

