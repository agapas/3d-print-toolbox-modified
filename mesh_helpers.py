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

# Generic helper functions, to be used by any modules.


import bmesh


def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """Returns a transformed, triangulated copy of the mesh"""

    assert obj.type == 'MESH'

    if apply_modifiers and obj.modifiers:
        import bpy
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        me = obj_eval.to_mesh()
        bm = bmesh.new()
        bm.from_mesh(me)
        obj_eval.to_mesh_clear()
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # TODO. remove all customdata layers.
    # would save ram

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm


def bmesh_from_object(obj):
    """Object/Edit Mode get mesh, use bmesh_to_object() to write back."""
    me = obj.data

    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(me)
    else:
        bm = bmesh.new()
        bm.from_mesh(me)

    return bm


def bmesh_to_object(obj, bm):
    """Object/Edit Mode update the object."""
    me = obj.data

    if obj.mode == 'EDIT':
        bmesh.update_edit_mesh(me, True)
    else:
        bm.to_mesh(me)
        me.update()


def bmesh_calc_area(bm):
    """Calculate the surface area."""
    return sum(f.calc_area() for f in bm.faces)


def bmesh_check_self_intersect_object(obj):
    """Check if any faces self intersect returns an array of edge index values."""
    import array
    import mathutils

    if not obj.data.polygons:
        return array.array('i', ())

    bm = bmesh_copy_from_object(obj, transform=False, triangulate=False)
    tree = mathutils.bvhtree.BVHTree.FromBMesh(bm, epsilon=0.00001)
    overlap = tree.overlap(tree)
    faces_error = {i for i_pair in overlap for i in i_pair}

    return array.array('i', faces_error)


def bmesh_face_points_random(f, num_points=1, margin=0.05):
    import random
    from random import uniform

    # for pradictable results
    random.seed(f.index)

    uniform_args = 0.0 + margin, 1.0 - margin
    vecs = [v.co for v in f.verts]

    for _ in range(num_points):
        u1 = uniform(*uniform_args)
        u2 = uniform(*uniform_args)
        u_tot = u1 + u2

        if u_tot > 1.0:
            u1 = 1.0 - u1
            u2 = 1.0 - u2

        side1 = vecs[1] - vecs[0]
        side2 = vecs[2] - vecs[0]

        yield vecs[0] + u1 * side1 + u2 * side2


def bmesh_check_thick_object(obj, thickness):
    import array
    import bpy

    # Triangulate
    bm = bmesh_copy_from_object(obj, transform=True, triangulate=False)

    # map original faces to their index.
    face_index_map_org = {f: i for i, f in enumerate(bm.faces)}
    ret = bmesh.ops.triangulate(bm, faces=bm.faces)
    face_map = ret["face_map"]
    del ret
    # old edge -> new mapping

    # Convert new/old map to index dict.

    # Create a real mesh (lame!)
    context = bpy.context
    layer = context.view_layer
    scene_collection = context.layer_collection.collection

    me_tmp = bpy.data.meshes.new(name="~temp~")
    bm.to_mesh(me_tmp)
    obj_tmp = bpy.data.objects.new(name=me_tmp.name, object_data=me_tmp)
    scene_collection.objects.link(obj_tmp)

    layer.update()
    ray_cast = obj_tmp.ray_cast

    EPS_BIAS = 0.0001

    faces_error = set()
    bm_faces_new = bm.faces[:]

    for f in bm_faces_new:
        no = f.normal
        no_sta = no * EPS_BIAS
        no_end = no * thickness
        for p in bmesh_face_points_random(f, num_points=6):
            # Cast the ray backwards
            p_a = p - no_sta
            p_b = p - no_end
            p_dir = p_b - p_a

            ok, _co, no, index = ray_cast(p_a, p_dir, distance=p_dir.length)

            if ok:
                # Add the face we hit
                for f_iter in (f, bm_faces_new[index]):
                    # if the face wasn't triangulated, just use existing
                    f_org = face_map.get(f_iter, f_iter)
                    f_org_index = face_index_map_org[f_org]
                    faces_error.add(f_org_index)

    bm.free()

    scene_collection.objects.unlink(obj_tmp)
    bpy.data.objects.remove(obj_tmp)
    bpy.data.meshes.remove(me_tmp)

    layer.update()

    return array.array('i', faces_error)


def face_is_distorted(ele, angle_distort):
    no = ele.normal
    angle_fn = no.angle

    for loop in ele.loops:
        loopno = loop.calc_normal()

        if loopno.dot(no) < 0.0:
            loopno.negate()

        if angle_fn(loopno, 1000.0) > angle_distort:
            return True

    return False






# DGM: TODO: decide to delete or keep - The following is from modified version by Agnieszka Pas
def object_merge(context, objects):
    """
    Caller must remove.
    """

    import bpy

    def cd_remove_all_but_active(seq):
        tot = len(seq)
        if tot > 1:
            act = seq.active_index
            for i in range(tot - 1, -1, -1):
                if i != act:
                    seq.remove(seq[i])

    scene = context.scene
    layer = context.view_layer
    layer_collection = context.layer_collection or layer.active_layer_collection
    scene_collection = layer_collection.collection

    # deselect all
    for obj in scene.objects:
        obj.select_set(False)

    # add empty object
    mesh_base = bpy.data.meshes.new(name="~tmp~")
    obj_base = bpy.data.objects.new(name="~tmp~", object_data=mesh_base)
    scene_collection.objects.link(obj_base)
    layer.objects.active = obj_base
    obj_base.select_set(True)

    depsgraph = context.evaluated_depsgraph_get()

    # loop over all meshes
    for obj in objects:
        if obj.type != 'MESH':
            continue

        # convert each to a mesh
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_new = obj_eval.to_mesh()

        # remove non-active uvs/vcols
        cd_remove_all_but_active(mesh_new.vertex_colors)
        cd_remove_all_but_active(mesh_new.uv_layers)

        # join into base mesh
        obj_new = bpy.data.objects.new(name="~tmp-new~", object_data=mesh_new)
        base_new = scene_collection.objects.link(obj_new)
        obj_new.matrix_world = obj.matrix_world

        fake_context = context.copy()
        fake_context["active_object"] = obj_base
        fake_context["selected_editable_objects"] = [obj_base, obj_new]

        bpy.ops.object.join(fake_context)
        del base_new, obj_new

        # remove object and its mesh, join does this
        # scene_collection.objects.unlink(obj_new)
        # bpy.data.objects.remove(obj_new)

        obj_eval.to_mesh_clear()

    layer.update()

    # return new object
    return obj_base




'''
#----------------------------------------------------------
# File make_solid_helpers.py
# Helper functions, to be used by MakeSolid class .
#----------------------------------------------------------

import bpy
import bmesh


def prepare_meshes():
    bpy.ops.object.make_single_user(object=True, obdata=True)
    bpy.ops.object.convert()
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode='EDIT')

    # selection dance for proper results
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.context.tool_settings.mesh_select_mode = (True, True, True)

    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')


def prepare_mesh(obj, select_action):
    scene = bpy.context.scene
    layer = bpy.context.view_layer

    active_object = layer.objects.active
    layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # reveal hidden vertices in mesh
    bpy.ops.mesh.reveal()

    # mesh cleanup
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.mesh.delete_loose()

    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.0001)

    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.fill_holes(sides=0)

    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()

    # back to previous settings
    bpy.ops.mesh.select_all(action=select_action)
    bpy.ops.object.mode_set(mode='OBJECT')
    layer.objects.active = active_object


def cleanup_mesh(obj):
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bm.to_mesh(mesh)
    bm.free()


def add_modifier(active, selected):
    bool_modifier = active.modifiers.new(name='Boolean', type='BOOLEAN')
    bool_modifier.object = selected
    bool_modifier.show_viewport = False
    bool_modifier.show_render = False
    bool_modifier.operation = 'UNION'
    try:
        bool_modifier.solver = 'CARVE'
    except:
        pass

    bpy.ops.object.modifier_apply(modifier='Boolean')

    view_layer = bpy.context.view_layer
    print ("layer_collection.name = " + bpy.context.layer_collection.name)
    print ("view_layer.active_layer_collection.name = " + view_layer.active_layer_collection.name)
    layer_collection = bpy.context.layer_collection or view_layer.active_layer_collection
    collection = layer_collection.collection
    collection.objects.unlink(selected)

    bpy.data.objects.remove(selected)


def make_solid_batch():
    active = bpy.context.active_object
    selected = bpy.context.selected_objects
    selected.remove(active)

    prepare_mesh(active, 'DESELECT')

    for sel in selected:
        prepare_mesh(sel, 'SELECT')
        add_modifier(active, sel)
        cleanup_mesh(active)


def is_manifold(self):
    mesh = bpy.context.active_object.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    for edge in bm.edges:
        if not edge.is_manifold:
            bm.free()
            self.report({'ERROR'}, "Boolean operation result is non-manifold")
            return False

    bm.free()
    return True

'''



