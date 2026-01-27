import bpy
import mathutils

# constants
GRAVITY = 9.81 # gravitational constant
DURATION = 10 # how long animation runs 
FPS = 24
TOTAL_FRAMES = FPS * DURATION
BOUNCINESS = 0.8 # how much energy is conserved after a bounce
RADIUS = 0.25 # radius of marble
DT = 1/FPS  # 24 fps = 0.04166 (each frame is 0.04166 s)
            # DT because blender works in frames and physics works with time, we need to turn frames to time (s)

scene = bpy.context.scene 
depsgraph = bpy.context.evaluated_depsgraph_get() # like a map of the scene, tells blender where objects are

def object_detection(position, velocity, depsgraph):
    # transforms list into readable vector
    pos_vec = mathutils.Vector(position) 
    vel_vec = mathutils.Vector(velocity)
    
    if vel_vec.length > 0: # will run if ball is moving (if not normaliszed will do a 0/0 calc)
        offset = vel_vec.normalized() * (RADIUS + 0.01) # gives us the direction of the raycast and offsets it outside the radius 
        pos_vec = pos_vec + offset # adds it to the position to avoid self-collision
    
    ray_length = (vel_vec.length * DT) * 1.05   # (speed * time = distance)  
                                                # makes the raycast same length that frame (with tolerance (* 1.05) as vector length)
    if ray_length < 0.01: # if the ball is moving slowly or stationary auto set it to 0.01  
        ray_length = 0.01 # makes sure it will definitely collide

    hit, location, normal, index, object, matrix = scene.ray_cast(depsgraph, pos_vec, vel_vec, distance=ray_length) # # unpacks ray_cast

    if hit:
        return [normal.x, normal.y, normal.z], location
    else:
        return None, None

def calculate_path(start, velocity, depsgraph):
    current_pos = start.copy()
    current_vel = velocity.copy()
    path_point = [current_pos]

    for any in range(TOTAL_FRAMES):
        current_vel[2] -= GRAVITY * DT
        normal, hit = object_detection(current_pos, current_vel, depsgraph)

        if normal:
            normal_vec = mathutils.Vector(normal)
            current_pos = hit + (normal_vec * RADIUS)
            current_vel = current_vel.reflect(normal_vec) * BOUNCINESS 

        current_pos += current_vel * DT
        path_point.append(current_pos.copy())
    return path_point

def curve_visuliser(points):
    curve_name = "Trajectory"

    curve_obj = bpy.data.objects.get(curve_name)

    if not curve_obj:
        curve_data = bpy.data.curves.new(curve_name, type='CURVE')
        curve_data.dimensions = '3D'
        curve_obj = bpy.data.objects.new(curve_name, curve_data)
        bpy.context.collection.objects.link(curve_obj)
    
    if not curve_obj.data.splines:
        curve_obj.data.splines.new('POLY')

    spline = curve_obj.data.splines[0]

    if len(spline.points) != len(points):
        spline.points.add(len(points) - len(spline.points))

    for i, p in enumerate(points):
        spline.points[i].co = (p.x, p.y, p.z, 1.0)

def live_handler(scene, depsgraph):
    marble = bpy.data.objects.get("Marble")
    if not marble: return

    start_pos = marble.location
    start_vel = mathutils.Vector((0.0, 0.0, 0.0))

    points = calculate_path(start_pos, start_vel, depsgraph)
    curve_visuliser(points)

bpy.app.handlers.depsgraph_update_post.clear() 
bpy.app.handlers.depsgraph_update_post.append(live_handler)

"doesnt follow path exactly, work on fix 28/1/26"