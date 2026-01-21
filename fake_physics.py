import bpy
import mathutils


GRAVITY = 9.81
DURATION = 10
FPS = 24
TOTAL_FRAMES = int(DURATION * FPS)
BOUNCINESS = 0.8
DT = 1/FPS  # 24 fps = 0.04166 (each frame is 0.04166 s)
            # DT because blender works in frames and physics works with time, we need to turn frames to time (s)
current_pos = [0.0, 0.0, 10.0]  
velocity = [0.0, 0.0, 0.0]

scene = bpy.context.scene
scene.render.fps = FPS
depsgraph = bpy.context.evaluated_depsgraph_get() # like a map of the scene, tells you where objects are


# clean up
if "Marble" in bpy.data.objects:
    old_obj = bpy.data.objects["Marble"]
    bpy.data.objects.remove(old_obj, do_unlink=True)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(current_pos[0], current_pos[1], current_pos[2]))
obj = bpy.context.object
obj.name = "Marble"

def object_detection(position, velocity):
    position_vector = mathutils.Vector(position) # transforms the list into readable vector
    velocity_vector = mathutils.Vector(velocity)
    
    hit, location, normal, index, object, matrix = scene.ray_cast(depsgraph, position_vector, velocity_vector, distance=0.3)

    if hit:
        return [normal.x, normal.y, normal.z]
    else:
        return None

# distance (current_z) = velocity * time
# acceleration (gravity) = velocity / time

for frame_number in range(TOTAL_FRAMES):
    
    velocity[2] -= GRAVITY * DT
    wall_normal = object_detection(current_pos, velocity)

    if wall_normal:
        vel_vec = mathutils.Vector(velocity)
        norm_vec = mathutils.Vector(wall_normal)
        reflect_vec = vel_vec.reflect(norm_vec)
        reflect_vec = reflect_vec * BOUNCINESS
        velocity = [reflect_vec.x, reflect_vec.y, reflect_vec.z]

    current_pos[0] += velocity[0] * DT
    current_pos[1] += velocity[1] * DT
    current_pos[2] += velocity[2] * DT
        
    obj.location = (current_pos[0], current_pos[1], current_pos[2])
    obj.keyframe_insert(data_path="location", frame=frame_number)

    print(current_pos[2])


"fix ball collision glitch"





