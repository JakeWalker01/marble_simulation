import time
import bpy

MARBLE_SPEED = 5.0
SOURCE_NAME = "key_1"

scene = bpy.context.scene #setup
fps = scene.render.fps

source_obj = bpy.data.objects.get(SOURCE_NAME)

if source_obj is None:
    raise ValueError(f"Could not find object named '{SOURCE_NAME}'!")

collection_name = "MarbleTrack"

if collection_name in bpy.data.collections:
    track_col = bpy.data.collections[collection_name]

    for obj in track_col.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

else:
    track_col = bpy.data.collections.new(collection_name)
    scene.collection.children.link(track_col)

print(f"Generating track for {len(scene.timeline_markers)} markers...")

for marker in scene.timeline_markers:
    frame =  marker.frame
    time_seconds = frame/fps
    y_location = MARBLE_SPEED * time_seconds

    new_obj = source_obj.copy()
    new_obj.data = source_obj.data.copy()
    new_obj.name = f"Key_Frame_f{frame}"

    new_obj.location = (0, y_location, -1.0)
    track_col.objects.link(new_obj)

print("Track generation complete!")