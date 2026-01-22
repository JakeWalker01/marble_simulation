import bpy
import mathutils

# constants 
GRAVITY = 9.81 # gravitational constant
DURATION = 10 # how long animation runs 
FPS = 24 # frames per second 
TOTAL_FRAMES = int(DURATION * FPS) # calculates total fps
BOUNCINESS = 0.8 # how much energy is conserved after a bounce
RADIUS = 0.25 # radius of marble
DT = 1/FPS  # 24 fps = 0.04166 (each frame is 0.04166 s)
            # DT because blender works in frames and physics works with time, we need to turn frames to time (s)
current_pos = [0.0, 0.0, 10.0]  # position of marble
velocity = [0.0, 0.0, 0.0] # velocity of marble

scene = bpy.context.scene 
scene.render.fps = FPS # sets scene fps
depsgraph = bpy.context.evaluated_depsgraph_get() # like a map of the scene, tells blender where objects are


if "Marble" in bpy.data.objects: # is marble in outliner?
    old_obj = bpy.data.objects["Marble"] # give marble a variable
    bpy.data.objects.remove(old_obj, do_unlink=True) # delete marble and hidden data

bpy.ops.mesh.primitive_uv_sphere_add(radius=RADIUS, location=current_pos) # add sphere
obj = bpy.context.object # apply variable (obj) to current selected obj (sphere)
obj.name = "Marble" # name it marble
bpy.ops.object.shade_smooth() # make marble smooth

def object_detection(position, velocity):
    # transforms list into readable vector
    pos_vec = mathutils.Vector(position) 
    vel_vec = mathutils.Vector(velocity)
    
    if vel_vec.length > 0: # will run if ball is moving
        offset = vel_vec.normalized() * (RADIUS + 0.01) # gives us the direction of the raycast and offsets it outside the radius 
        pos_vec = pos_vec + offset # adds it to the position to avoid self-collision
    
    ray_length = (vel_vec.length * DT) * 1.05  # makes the raycast same length that frame (with tolerance (* 1.05) as vector length)
    
    if ray_length < 0.01:  # if the ball is moving slowly or stationary auto set it to 0.01
        ray_length = 0.01

    hit, location, normal, index, object, matrix = scene.ray_cast(depsgraph, pos_vec, vel_vec, distance=ray_length) # # unpacks ray_cast

    if hit:
        if object.name == "Marble":  # back up incase it calculates ray_length incorrect and still thinks its inside the marble
            return None
        return [normal.x, normal.y, normal.z]
    else:
        return None

# distance (current_z) = velocity * time
# acceleration (gravity) = velocity / time

for frame_number in range(TOTAL_FRAMES): # Eulers method - loops frame by frame updating position
    
    velocity[2] -= GRAVITY * DT # changes Z postion due to gravity
    wall_normal = object_detection(current_pos, velocity) # the normal of the wall

    if wall_normal:
        vel_vec = mathutils.Vector(velocity) # vectorising
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





