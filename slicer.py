import bpy, bmesh
from bpy import context as C
from mathutils import Vector

def newobj(bm, name):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    ob = bpy.data.objects.new(name,me)
    #C.scene.objects.link(ob)
    bpy.data.collections['Slices'].objects.link(ob)
    return ob

# https://blender.stackexchange.com/questions/32283/what-are-all-values-in-bound-box
def bounds(obj, local=False):

    local_coords = obj.bound_box[:]
    om = obj.matrix_world

    if not local:    
        worldify = lambda p: om * Vector(p[:]) 
        coords = [worldify(p).to_tuple() for p in local_coords]
    else:
        coords = [p[:] for p in local_coords]

    rotated = zip(*coords[::-1])

    push_axis = []
    for (axis, _list) in zip('xyz', rotated):
        info = lambda: None
        info.max = max(_list)
        info.min = min(_list)
        info.distance = info.max - info.min
        push_axis.append(info)

    import collections

    originals = dict(zip(['x', 'y', 'z'], push_axis))

    o_details = collections.namedtuple('object_details', 'x y z')
    
    
    return o_details(**originals)

object_details = bounds(C.object, True)

bpy.ops.object.mode_set(mode='OBJECT')


if not "Slices" in bpy.data.collections:
    bpy.context.scene.collection.children.link(bpy.data.collections.new("Slices"))




# split the model into parts along the direction of the unit vector (normal)
# in steps of step_size in local coordinate space 
#(this ignores the scale property, so make sure to apply it before)


# If you want to slice at a different angle then just change the normal, and start
# far enough down the z-axis to ensure the plane will slice the entire model
# You can calculate step size to give appropriate thickness slices with sqrt(x*x + y*y +  z*z)
# although this strategy won't work if you want to cut perpendicular to the z- axis
# in that case you'll need to change the start and stop
step_size = 0.01
startLoc = object_details.z.min
stopLoc = object_details.z.max
normalOfSlice = (0,0,1)

steps = int((stopLoc - startLoc)/step_size) + 1    # + 1 because we want the faces on either end
print("Slicing into ", steps, "slices")

lBound = 1

halving = [steps]
slices = []
slices.append(bmesh.new())
slices[0].from_mesh(C.object.data)



while (halving[-1] > lBound):
    if lBound + 1 < halving[-1]:
        # At the moment we're just created successively halved copies of the mesh.
        # And adding them to the list
        # Even though we are duplicate meshes and running the function twice 
        # it is still faster than operating from an original (uncopied) mesh because the bisect function 
        # 1. doesn't seem to index the geometry in any way (so time is proportional to the mesh size)
        #    Splitting at this stage effectively creates indexed bits of meshes)
        # 2. There appears to be no way to create an inner and an outer copy
        #    in the same step (eg by passing in two bmesh objects to the bisect function) 
        #    Thus the bisect function has to be run once on each copy

        curSlice = int(lBound+(halving[-1]-lBound)/2)
        slicePoint = startLoc+curSlice*step_size
        halving.append(curSlice)
        print ("slice",lBound, halving[-1])

        slices.append[slices[-1].copy())
        #This slices the original mesh and discards geometry 
        # on the inner =  lower index = negative side of the plane
        bmesh.ops.bisect_plane(
            slices[-2], 
            geom=bisection_inner.verts[:]+bisection_inner.edges[:]+bisection_inner.faces[:], 
            plane_co=(0,0,slicePoint), 
            plane_no=normalOfSlice,
            clear_inner=True)

        #This slices the duplicated copy of the mesh and discards geometry 
        # on the outer = higher index = positive side of the plane
        bmesh.ops.bisect_plane(
            slices[-1], 
            geom=bisection_inner.verts[:]+bisection_inner.edges[:]+bisection_inner.faces[:], 
            plane_co=(0,0,slicePoint), 
            plane_no=normalOfSlice,
            clear_outer=True)

    
    else:
        # we've just halved the slice directly above the lower bound so slice again to extract 
        # the top and bottom vertex loops (ie discarding the inner and outer geometry for both) 
        # then create two objects from the data
        # Finallyn step back up to next level clearing out the redundant slice data
        
        bisection_lBound = slices[-1].copy()
        upperSlicePoint = startLoc+curSlice*step_size
        lowerSlicePoint = startLoc+(curSlice-1)*step_size
        
        #This slices the mesh and discards the inner elements
        bmesh.ops.bisect_plane(
            slices[-1], 
            geom=bisection_outer.verts[:]+bisection_outer.edges[:]+bisection_outer.faces[:], 
            plane_co=(0,0,upperSlicePoint), 
            plane_no=normalOfSlice, 
            clear_inner=True,
            clear_outer=True)
        newobj(slices[-1], "bisect-"+str(upperSlicePoint))
            
        #This slices the duplicated copy of the mesh and discards the outer elements
        bmesh.ops.bisect_plane(
            bisection_lBound, 
            geom=bisection_inner.verts[:]+bisection_inner.edges[:]+bisection_inner.faces[:], 
            plane_co=(0,0,lowerSlicePoint), 
            plane_no=normalOfSlice, 
            clear_inner=True,
            clear_outer=True)
        newobj(bisection_inner, "bisect-"+str(lowerSlicePoint))
            
        print ("extracted:",lBound, halving[-1])
        lBound = halving[-1]+1
        print ("update: lb1",lBound, halving[-1])
        print ("del:",halving[-1])
        del halving[-1]
        del slices[-1]
        bisection_lBound.free()  # free and prevent further access            
        
    if len(halving) == 0:
        break
   
       



'''        

bisection_outer = bmesh.new()
bisection_outer.from_mesh(C.object.data)


for i in range(steps+1):
    # duplicate the larger portion of the mesh 
    bisection_inner = bisection_outer.copy()
    #This slices the mesh and discards the inner elements
    bmesh.ops.bisect_plane(
        bisection_outer, 
        geom=bisection_outer.verts[:]+bisection_outer.edges[:]+bisection_outer.faces[:], 
        plane_co=(0,0,curSlice), 
        plane_no=normalOfSlice, 
        clear_inner=True)
    #This slices the duplicated copy of the mesh and discards the outer elements
    bmesh.ops.bisect_plane(
        bisection_inner, 
        geom=bisection_inner.verts[:]+bisection_inner.edges[:]+bisection_inner.faces[:], 
        plane_co=(0,0,curSlice), 
        plane_no=normalOfSlice, 
        clear_outer=True)
        
    # When you're down to one layer thickness only you can 
    # * slice with both clear_inner=True and clear_outer=True to keep only the vertex/edge loops
    # * recreate the face
    newobj(bisection_inner, "bisect-"+str(curSlice))
    #bpy.data.objects[no.name].select_set(True) # Blender 2.8x
    #bpy.ops.object.delete() 
    #no.delete()
    bisection_inner.free()  # free and prevent further access
    curSlice+=step_size
'''

slices.free()  # free and prevent further access
C.object.user_clear()  # without this, removal would raise an error.
bpy.data.objects.remove(C.object, True)










'''
Print Mesh ID


import Blender 
from Blender import Window 
 
sce = Blender.Scene.GetCurrent() 
objects = sce.objects 
 
print "---
" 
for ob in objects: 
    edit = False 
    if Window.EditMode(): 
        Window.EditMode(0) 
        edit = True 
    if ob.getType() == 'Mesh': 
        mesh = ob.getData(mesh=1) 
        for i in range(len(mesh.verts)): 
            v = mesh.verts[i] 
            if v.sel == 1: 
                print "vert: "+str(i) 
    if edit: 
        Window.EditMode(1)  


Custom Data Layers


The Blender BMesh Python API supports custom-data-layers per vert/edge/face/loop. Per face, it only supports the types (float, int, string, tex), so you'll have to make your own vectors and colors out of floats.

The code would be something like:

import bpy
import bmesh

ob = bpy.context.object

# create a bmesh editing context...
bm = bmesh.new()

# if we're in edit mode, there is already a BMesh available, else make one
if bpy.context.mode == 'EDIT_MESH':
    bm.from_edit_mesh(ob.data)
else:        
    bm.from_mesh(ob.data)

# Make the layers..
tag_number = bm.faces.layers.integer.new('number_tag')
tag_vector_x = bm.faces.layers.float.new('vector_tag_x')
tag_vector_y = bm.faces.layers.float.new('vector_tag_y')
tag_vector_z = bm.faces.layers.float.new('vector_tag_z')
tag_color_r = bm.faces.layers.float.new('color_tag_r')
tag_color_g = bm.faces.layers.float.new('color_tag_g')
tag_color_b = bm.faces.layers.float.new('color_tag_b')

# fetch the layers
tag_number = bm.faces.layers.integer.get('number_tag')
tag_vector_x = bm.faces.layers.float.get('vector_tag_x')
tag_vector_y = bm.faces.layers.float.get('vector_tag_y')
tag_vector_z = bm.faces.layers.float.get('vector_tag_z')
tag_color_r = bm.faces.layers.float.get('color_tag_r')
tag_color_g = bm.faces.layers.float.get('color_tag_g')
tag_color_b = bm.faces.layers.float.get('color_tag_b')

# set the tag value for a particular face
bm.edges[face_no][tag_number] = new_number_tag_value



'''