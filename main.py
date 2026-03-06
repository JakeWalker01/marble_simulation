import bpy # blender library
import mathutils # blender math tools

START_POS = mathutils.Vector((0.0, 0.0, 10.0)) # starting position of marble 
START_VEL = mathutils.Vector((0.0, 0.0, 0.0)) # starting velocity of marble
GRAVITY = 9.81 # the negative acceleration on the z axis
DURATION = 10 # the length of the animation
FPS = 24 # the amount of frames per second (smoothness)
TOTAL_FRAMES = int(DURATION * FPS) # total number of frames in the scene
BOUNCINESS = 0.8 # how much eneergy is conserved after collision
RADIUS = 0.25 # radius of the marble
DT = 1/FPS # the exact amount of time per frame (for real word physics)

class PhysicsEngine:
    
    @staticmethod # calculates math
    def object_detection(pos, vel, depsgraph): 
        """Grabs the current position and velocity of the object shoot an invisible laser"""
        position = mathutils.Vector(pos)
        velocity = mathutils.Vector(vel) 
        scene = bpy.context.scene

        if velocity.length > 0:
            ray_length = RADIUS + (velocity.length * DT)
            direction = velocity.normalized()
            
            hit, location, normal, index, hit_object, matrix = scene.ray_cast(depsgraph, position, direction, distance=ray_length)

            if hit and hit_object.name != "Marble":
                return normal, location 
        return None, None

    @staticmethod
    def update_position(pos, vel, depsgraph): 
        position = mathutils.Vector(pos)
        velocity = mathutils.Vector(vel) 

        velocity.z -= GRAVITY * DT

        normal, hit_location = PhysicsEngine.object_detection(position, velocity, depsgraph)

        if normal:
            position = hit_location + (normal * RADIUS)
            velocity = velocity.reflect(normal) * BOUNCINESS 
        else:
            position += velocity * DT

        return position, velocity

class MainMenu(bpy.types.Panel):
    bl_label = "Marble Simulation"
    bl_idname = "VIEW3D_PT_main_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Marble"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "livePrediction", text="Toggle Path", toggle=True, icon="RENDER_STILL")
        layout.separator()

        row3 = layout.row()
        row3.scale_y = 1.5
        row3.operator("marble.animation", text="Bake Animation", icon="FILE_TICK")

class LivePrediction(bpy.types.Operator):
    bl_idname = "marble.predict_path"
    bl_label = "Predict Path"

    @staticmethod
    def update_path(scene, depsgraph):
        marble = scene.objects.get("Marble")
        if not marble:
            return

        current_pos = marble.location.copy()
        current_vel = START_VEL.copy()
        path_points = []

        for i in range(TOTAL_FRAMES):
            path_points.append(current_pos.copy())
            current_pos, current_vel = PhysicsEngine.update_position(current_pos, current_vel, depsgraph)

        obj = bpy.data.objects.get("Marble_Path_Line")
        if obj is None:
            mesh = bpy.data.meshes.new("MarblePath_Mesh")
            obj = bpy.data.objects.new("Marble_Path_Line", mesh)
            scene.collection.objects.link(obj)
            obj.hide_select = True
            obj.display_type = 'WIRE'
        else:
            mesh = obj.data

        verts = [v.to_tuple() for v in path_points]
        edges = [(i, i + 1) for i in range(len(verts) - 1)]
        
        mesh.clear_geometry() 
        mesh.from_pydata(verts, edges, [])
        mesh.update()

    def execute(self, context):
        scene = context.scene
        depsgraph = context.evaluated_depsgraph_get()
        LivePrediction.update_path(scene, depsgraph)
        return {'FINISHED'}

class BakeAnimation(bpy.types.Operator):
    bl_idname = "marble.animation"
    bl_label = "Bake Animation"

    def execute(self, context):
        scene = context.scene
        marble = scene.objects.get("Marble")
        depsgraph = context.evaluated_depsgraph_get()

        if not marble:
            self.report({'ERROR'}, "Marble not found!")
            return {'CANCELLED'}

        if marble.animation_data:
            marble.animation_data_clear()

        current_pos = marble.location.copy()
        current_vel = START_VEL.copy()

        for frame in range(scene.frame_start, scene.frame_end + 1):
            marble.location = current_pos
            marble.keyframe_insert(data_path="location", frame=frame)
            current_pos, current_vel = PhysicsEngine.update_position(current_pos, current_vel, depsgraph)

        self.report({'INFO'}, "Scene Baked")
        return {'FINISHED'}

def update_live_toggle(self, context):
    if not self.livePrediction:
        obj = bpy.data.objects.get("Marble_Path_Line")
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

def live_prediction_handler(scene, depsgraph):
    if hasattr(scene, "livePrediction") and scene.livePrediction:
        for update in depsgraph.updates:
            if update.id.name != "Marble_Path_Line":
                LivePrediction.update_path(scene, depsgraph)
                break

classes = [
    LivePrediction,
    MainMenu,
    BakeAnimation
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.livePrediction = bpy.props.BoolProperty(
        name="Live Prediction",
        default=False,
        update=update_live_toggle
    )
    
    if live_prediction_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(live_prediction_handler)

def unregister():
    handlers = bpy.app.handlers.depsgraph_update_post
    for h in handlers:
        if h.__name__ == "live_prediction_handler":
            handlers.remove(h)
        
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    if hasattr(bpy.types.Scene, "livePrediction"):
        del bpy.types.Scene.livePrediction
    
    obj = bpy.data.objects.get("Marble_Path_Line")
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)

if __name__ == "__main__":
    register()