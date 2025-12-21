import bpy

scene = bpy.context.scene
obj = bpy.context.object

if obj is None:
    raise RuntimeError("No active object")


start = scene.frame_start
end = scene.frame_end

bpy.context.view_layer.update()

scene.frame_set(start)
prev = obj.scale.x

scene.frame_set(start + 1)
current = obj.scale.x

def threshold():
    if 

    
for frame in range(start + 1, end):

    scene.frame_set(frame - 1)
    prev = obj.scale.x

    scene.frame_set(frame)
    current = obj.scale.x

    scene.frame_set(frame + 1)
    next_val = obj.scale.x

    if current > prev and current > next_val:
        print("Peak at frame", frame)

