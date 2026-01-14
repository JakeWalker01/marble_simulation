import bpy


GRAVITY = 9.81
START_HEIGHT = 0
DURATION = 10
FPS = 24
TOTAL_FRAMES = int(DURATION * FPS)


bpy.context.scene.render.fps = FPS

# clean up
if "Marble" in bpy.data.objects:
    old_obj = bpy.data.objects["Marble"]
    bpy.data.objects.remove(old_obj, do_unlink=True)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0, 0, START_HEIGHT))
obj = bpy.context.object
obj.name = "Marble"

current_z = START_HEIGHT
velocity_z = 0.0
dt = 1/FPS # 24fps = 0.04166 (each frame is 0.04166 s)

# dt because blender works in frames and physics works with time, we need to turn frames to time (s)

# distance (current_z) = velocity * time
# acceleration (gravity) = velocity / time
for frame_number in range(TOTAL_FRAMES):
    current_z -= velocity_z * dt # (-=) because the ball is moving down
    velocity_z += GRAVITY * dt 
    
    obj.location.z = current_z
    obj.keyframe_insert(data_path="location", frame=frame_number) 







