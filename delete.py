bl_info = {
    "name": "Delete Fully Hidden Objects",
    "author": "ChatGPT",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Cleanup",
    "description": "Deletes objects hidden in both viewport and render, then saves the file",
    "category": "Object",
}

import bpy


class OBJECT_OT_delete_fully_hidden(bpy.types.Operator):
    bl_idname = "object.delete_fully_hidden"
    bl_label = "Delete Hidden (Viewport + Render)"
    bl_description = "Deletes objects invisible in viewport and disabled for render, then saves the file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        objs_to_delete = []

        for obj in scene.objects:
            viewport_hidden = not obj.visible_get()
            render_hidden = obj.hide_render

            if viewport_hidden and render_hidden:
                objs_to_delete.append(obj)

        for obj in objs_to_delete:
            bpy.data.objects.remove(obj, do_unlink=True)

        # ---- AUTO SAVE ----
        if bpy.data.is_saved:
            bpy.ops.wm.save_mainfile()
            self.report(
                {'INFO'},
                f"{len(objs_to_delete)} object(s) deleted and file saved"
            )
        else:
            self.report(
                {'WARNING'},
                f"{len(objs_to_delete)} object(s) deleted. File NOT saved (never saved before)"
            )

        return {'FINISHED'}


class VIEW3D_PT_delete_hidden_panel(bpy.types.Panel):
    bl_label = "Cleanup"
    bl_idname = "VIEW3D_PT_delete_hidden_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cleanup"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            OBJECT_OT_delete_fully_hidden.bl_idname,
            icon='TRASH'
        )


def register():
    bpy.utils.register_class(OBJECT_OT_delete_fully_hidden)
    bpy.utils.register_class(VIEW3D_PT_delete_hidden_panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_delete_fully_hidden)
    bpy.utils.unregister_class(VIEW3D_PT_delete_hidden_panel)


if __name__ == "__main__":
    register()
