import bpy

scene = bpy.context.scene
obj = bpy.context.object

if obj is None:
    raise RuntimeError("No active object")

start = scene.frame_start
end = scene.frame_end

threshold = 0.05

# --- PERFORMANCE FIX ---
# Stop viewport updates while scanning
bpy.context.view_layer.update()

# Initialize prev correctly
scene.frame_set(start)
prev = obj.scale.x

scene.frame_set(start + 1)
current = obj.scale.x

for frame in range(start + 2, end + 1):
    scene.frame_set(frame)
    next = obj.scale.x
    
    if current > prev and current > next:
        print("peaks at frame:", frame - 1)
        continue
    
    prev = current
    current = next
   

