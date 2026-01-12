import bpy

#initial setup
start_velocity = (0.0, 0.0, 0.0)
start_location = (0, 0, 10)
gravity = 9.81
fps = 24
duration = 5.0

for obj_name in ["Marble", "Trajectory_Path"]:
    if obj_name in bpy.data.objects:
        obj = bpy.data.objects[obj_name]
        bpy.data.objects.remove(obj, do_unlink=True)

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

print("Calculating path...")

path_point = []

x, y, z = start_location
vx, vy, vz = start_velocity
dt = 1.0/fps

for frame in range(int(fps * duration)):
    path_point.append((x, y, z, 1.0))
    
    x += vx * dt
    y += vy * dt
    z += vz * dt

    vz -= gravity * dt

curve_data = bpy.data.curves.new("Trajectory_data", type="CURVE")
curve_data.dimensions = "3D"

polyline = curve_data.splines.new('POLY')
polyline.points.add(len(path_point) - 1) 

for i, coord in enumerate(path_point):
    polyline.points[i].co = coord

curve_obj = bpy.data.objects.new('Trajectory_Path', curve_data)
bpy.context.collection.objects.link(curve_obj)

print("Trajectory line created!")