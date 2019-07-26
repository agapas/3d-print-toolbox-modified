# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

#----------------------------------------------------------
# File ui.py
# Interface for this addon.
#----------------------------------------------------------

from bpy.types import Panel
import bmesh

from . import report


class Print3D_ToolBar:
    bl_label = "Print3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    _type_to_icon = {
        bmesh.types.BMVert: 'VERTEXSEL',
        bmesh.types.BMEdge: 'EDGESEL',
        bmesh.types.BMFace: 'FACESEL',
    }

    _check_all_icon = 'FORCE_VORTEX'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')

    @staticmethod
    def draw_report(layout, context):
        """Display Reports"""
        info = report.info()
        if info:
            obj = context.edit_object

            layout.label(text="Output:")
            box = layout.box()
            col = box.column(align=False)
            for i, (text, data) in enumerate(info):
                if obj and data and data[1]:
                    bm_type, bm_array = data
                    col.operator("mesh.print3d_select_report",
                        text=text,
                        icon=Print3D_ToolBar._type_to_icon[bm_type]).index = i
                elif 'Volume:' in text:
                    rowsub = col.row(align=True)
                    rowsub.label(text=text)
                    rowsub.operator("mesh.print3d_copy_volume_to_clipboard", text="", icon='COPYDOWN').volume = text
                elif 'Area:' in text:
                    rowsub = col.row(align=True)
                    rowsub.label(text=text)
                    rowsub.operator("mesh.print3d_copy_area_to_clipboard", text="", icon='COPYDOWN').area = text
                else:
                    col.label(text=text)


    def draw(self, context):
        layout = self.layout

        scene = context.scene
        print_3d = scene.print_3d

        row = layout.row()
        layout.label(text="Statistics:")
        rowsub = layout.row(align=True)
        rowsub.operator("mesh.print3d_info_volume", text="Volume")
        rowsub.operator("mesh.print3d_info_area", text="Area")
        layout.separator()

        box = layout.box()
        col = box.column()
        col.operator("object.make_solid", text="Make Solid")

        row = layout.row()
        row.label(text="Checks:")
        col = layout.column(align=True)
        col.operator("mesh.print3d_check_solid", text="Solid")
        col.operator("mesh.print3d_check_intersect", text="Intersections")
        rowsub = col.row(align=True)
        rowsub.operator("mesh.print3d_check_degenerate", text="Degenerate")
        rowsub.prop(print_3d, "threshold_zero", text="")
        rowsub = col.row(align=True)
        rowsub.operator("mesh.print3d_check_distort", text="Distorted")
        rowsub.prop(print_3d, "angle_distort", text="")
        rowsub = col.row(align=True)
        rowsub.operator("mesh.print3d_check_thick", text="Thickness")
        rowsub.prop(print_3d, "thickness_min", text="")
        rowsub = col.row(align=True)
        rowsub.operator("mesh.print3d_check_sharp", text="Edge Sharp")
        rowsub.prop(print_3d, "angle_sharp", text="")
        rowsub = col.row(align=True)
        rowsub.operator("mesh.print3d_check_overhang", text="Overhang")
        rowsub.prop(print_3d, "angle_overhang", text="")

        col = layout.column()
        col.operator("mesh.print3d_check_all",
            text="CHECK ALL",
            icon=Print3D_ToolBar._check_all_icon)

        # Added mesh clean up operators:
        row = layout.row()
        row.label(text="Clean up:")

        box = layout.box()
        col = box.column()
        col.operator("mesh.print3d_clean_degenerates", text="Degenerate Dissolve")
        col = box.column()
        col.operator("mesh.print3d_clean_doubles", text="Remove Doubles")
        col = box.column()
        col.operator("mesh.print3d_clean_loose", text="Delete Loose")
        col = box.column()
        col.operator("mesh.print3d_clean_non_planars", text="Split Non Planar Faces")
        col = box.column()
        col.operator("mesh.print3d_clean_concaves", text="Split Concave Faces")
        col = box.column()
        col.operator("mesh.print3d_clean_triangulates", text="Triangulate Faces")
        col = box.column()
        col.operator("mesh.print3d_clean_holes", text="Fill Holes")
        col = box.column()
        col.operator("mesh.print3d_clean_limited", text="Limited Dissolve")

        Print3D_ToolBar.draw_report(layout, context)
        layout.separator()

        col = layout.column()
        rowsub = col.row(align=True)
        rowsub.label(text="Export Path:")
        rowsub.prop(print_3d, "use_apply_scale", text="", icon='ORIENTATION_GLOBAL')
        rowsub.prop(print_3d, "use_export_texture", text="", icon='FILE_IMAGE')
        rowsub = col.row()
        rowsub.prop(print_3d, "export_path", text="")

        rowsub = col.row(align=True)
        rowsub.prop(print_3d, "export_format", text="")
        rowsub.operator("mesh.print3d_export", text="Export", icon='EXPORT')


# Showing panel in object mode
class VIEW3D_PT_Print3D_Object_Modified(Panel, Print3D_ToolBar):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "3D Printing"
    bl_idname = "VIEW3D_PT_print3d_object_modified"
    bl_context = "objectmode"


# Showing panel in edit mode
class VIEW3D_PT_Print3D_Mesh_Modified(Panel, Print3D_ToolBar):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "3D Printing"
    bl_idname = "VIEW3D_PT_print3d_mesh_modified"
    bl_context = "mesh_edit"
