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


def threshold_value(current, prev, threshold=0.2):
    if abs(current - prev) >= threshold:
        return True
    else:
        return False

for frame in range(start + 1, end):

    scene.frame_set(frame - 1)
    prev = obj.scale.x

    scene.frame_set(frame)
    current = obj.scale.x

    scene.frame_set(frame + 1)
    next_val = obj.scale.x

    if current > prev and current > next_val:
        if threshold_value(current, prev):
            print("beat at ", frame)


"""
Mostly works, but has issues.
Example: around frame 70 the curve has two small beats close together.
The first one gets detected because the value keeps rising,
but the second one doesn’t because the change isn’t steep enough /
it never becomes a clear peak.
Basically this method struggles with small or clustered beats.
"""

