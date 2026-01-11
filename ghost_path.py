import bpy

if "Marble" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Marble"], do_unlink=True)
    
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0, 0, 10))
bpy.context.object.name = "Marble"


if "Marble" in bpy.data.objects:
    target_obj = bpy.data.objects["Marble"]
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = target_obj
    target_obj.select_set(True)
    bpy.ops.object.shade_smooth()
    bpy.ops.rigidbody.objects_add()
    target_obj.rigid_body.type = "ACTIVE"
    target_obj.rigid_body.mass = 1
    

print("Created marble successfully")

print("Simulating physics path")
