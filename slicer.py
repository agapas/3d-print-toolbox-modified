import bpy, bmesh
from bpy import context as C
from mathutils import Vector

# This code will slice the selected object into a set of vertices and edges
# along the direction of the unit vector (normal)
# in steps of step_size in local coordinate space 
#(this ignores the scale property, so make sure to apply it before)
# If you want to slice at a different angle then just change the normal, and start
# far enough down the z-axis to ensure the plane will slice the entire model
# You can calculate step size to give appropriate thickness slices with sqrt(x*x + y*y +  z*z)
# NB this strategy won't work if you want to cut perpendicular to the z- axis
# in that case you'll need to change the code a bit more


def newobj(bm, name):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
#    if (len(me.vertices) == 0 and len(me.edges) == 0):
#        return
    print("Building Object with: ", len(me.vertices), " vertices,", len(me.edges), " edges,", len(me.loops), " loops,")
    ob = bpy.data.objects.new(name,me)
    #C.scene.objects.link(ob)
    bpy.data.collections['Slices'].objects.link(ob)
    return ob


def facesFromSlice(bm, objName):
    # unfortunately this doesn't seem to return faces
    # print(len(ret['geom'])) = same as vertex+edge count
    # need to walk around perimeter of each loop and add vertices to an array, then do bm.faces.new((v1, v2, v3))

    # set up initiation variables                
    addedFace = False

    vts = bm.verts
    edg = bm.edges                            
    fac = bm.faces

    edg.ensure_lookup_table()
    vts.ensure_lookup_table()
    fac.ensure_lookup_table()

    # did bisect even produce anything?
    print("Generated BMesh with: ", len(vts), " verts,", len(edg), " edges,", len(fac), " faces,")
            
            
    # Now going to step through all the vertices
    # initially set up some lists for tracking if vertices have been visited (should probably have been dicts)
    vertsToVisit = len(vts)
    print("vertsToVisit0=",vertsToVisit)
    if vertsToVisit == 0:
        print("No verts. Skipping...")
    else:
        # more initiation variables
        curVert = None
        vertLoop = []
        doneVert = []
        for d in range(len(vts)):
            doneVert.append(d)
            
        # now loop until all the vertices have been visited to ensure multiple independent loops are found
        while vertsToVisit>0:
            if curVert == None:    # we're either the first time through, or have just added a face
                for d in doneVert:
                    if d != -1:
                        vertLoop = [vts[d]]
                        doneVert[vts[d].index] = -1
                        print("loopStrt=",vts[d].index)
                        #vertsToVisit-=1
                        break
            if len(vertLoop) == 0:    # no vert found not already visited
                break
            print("vertsToVisit1=",vertsToVisit)
            
            # find the end of first edge which doesn't loop back to the start vert
            try:
                # cope with error: IndexError: BMElemSeq[index]: index 1 out of range
                nextEdge = vertLoop[0].link_edges[1]
            except:
                print("ERROR: IndexError: BMElemSeq[index]: index 1 out of range")
                print("   Level not processed further")
                break
            if nextEdge.verts[0] == vertLoop[0]:
                curVert = nextEdge.verts[1]
            else:
                curVert = nextEdge.verts[0]

            if curVert == vertLoop[0]:    # the current vertex is the starting vertex, so a face can't be generated
                vertLoop=[]
                curVert = None
                print("curVert == vertLoop[0]")
            elif doneVert[curVert.index] == -1:
                print("doneVert[curVert.index] == -1:", curVert.index)    # the current vertex has already been visited
                break
            else:
                # we have a vertex which is valid
                vertLoop.append(curVert)
                doneVert[curVert.index] = -1
                vertsToVisit-=1
                print("vertLoop+",curVert.index, "vertsToVisit2=",vertsToVisit)
                starting = True

                while (starting or (curVert != vertLoop[0] and vertsToVisit > 0)):
                    starting = False
                    # select the next edge NOT going back to the previous vertex
                    if len(curVert.link_edges)<2:
                        print("ERROR: less than 2 vertices for an edge: dropping out of layer processing")
                        vertsToVisit = 0
                        break
                    nextEdge = curVert.link_edges[0]
                    if doneVert[nextEdge.verts[0].index] == -1 and doneVert[nextEdge.verts[1].index] == -1:
                        nextEdge = curVert.link_edges[1]
                    if doneVert[nextEdge.verts[0].index] == -1 and doneVert[nextEdge.verts[1].index] == -1:
                        # the current edges loop back on themselves
                        
                        # check the edges aren't linking back to the start vertex
                        if (curVert.link_edges[0].verts[0].index == vertLoop[0].index,
                          curVert.link_edges[0].verts[1].index == vertLoop[0].index,
                          curVert.link_edges[1].verts[0].index == vertLoop[0].index,
                          curVert.link_edges[1].verts[1].index == vertLoop[0].index):
                          
                            
                            # if they do loop back to start we've closed the loop, so add it as a face
                            try:
                                # sometimes get error: ValueError: faces.new(verts): face already exists
                                fac.new(vertLoop)
                            except:
                                print("ERROR: IndexError: ValueError: faces.new(verts): face already exists")
                                print("   Face not processed further")
                                pass
                            vertLoop = []
                            curVert = None
                            print("Adding face", len(fac))
                            fac.ensure_lookup_table()
                            print("  face.area = ",fac[-1].calc_area())
                            addedFace = True
                            break
                        else:  


                            print("Failed to close loop")
                            print(
                              curVert.link_edges[0].verts[0].index,
                              curVert.link_edges[0].verts[1].index,
                              curVert.link_edges[1].verts[0].index,
                              curVert.link_edges[1].verts[1].index)
                            vertLoop = []
                            curVert = None
                            break
                            
                    # select the end of the edge NOT attached to the current vertex
                    nextVert = nextEdge.verts[0]
                    if curVert == nextVert:
                        nextVert = nextEdge.verts[1]
                    curVert = nextVert
                                       
                        
                    if curVert == vertLoop[0]:
                        # we've closed the loop, so add it as a face
                        fac.new(vertLoop)
                        vertLoop = []
                        curVert = None
                        print("Adding face", len(fac))
                        addedFace = True
                        break
                    
                    if doneVert[curVert.index] == -1:
                        break
                    
                    # we haven't closed the loop so add the current vertex to the loop and continue on
                    vertLoop.append(curVert)
                    doneVert[curVert.index] = -1 
                    vertsToVisit-=1
                    print("vertLoop+",curVert.index, "vertsToVisit3=",vertsToVisit)

                # debugging: why have I dropped out of the while loop?
                print("dropped out of while:-")
                print(" addedFace = ", addedFace == True)
                print(" starting = ", starting)
                if len(vertLoop) > 0:
                    print(" curVert != vertLoop[0] = ", curVert != vertLoop[0])
                print(" vertsToVisit > 0 = ", vertsToVisit > 0)
                print("")
                if curVert != None:
                    print(" doneVert[curVert.index] != -1 = ", doneVert[curVert.index] != -1)
                addedFace = False
        ob = newobj(bm, "bisect-"+str(objName))
        print("Added: ", ob.name)    






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

    #bb = bounds(obj)
    #print("bounds(bb) = ((",bb.x.min,",",bb.x.max,"),(",bb.y.min,",",bb.y.max,"),(",bb.z.min,",",bb.z.max,"))")    

def tri_area( co1, co2, co3 ):
    return (co1 * co2) / 2.0


# UID Code
def make_key(obj):
    return hash(obj.name + str(time.time()))
def get_id(self):
    if "id" not in self.keys():
        self["id"] = make_key(self)
    return self["id"]

# set the id type to all objects.
#bpy.types.Object.id = property(get_id)
# could store them in the file as a datastore in the window manager.
#wm = bpy.context.window_manager
#wm["objects"] = 0
#rna = wm.get("_RNA_UI", {})
#rna["objects"] = {o.name: o.id for o in bpy.data.objects}
#wm["objects"] = len(rna["objects"])
#wm["_RNA_UI"] = rna











# This code will slice the selected object into a set of vertices and edges
# along the direction of the unit vector (normal)
# in steps of step_size in local coordinate space 
#(this ignores the scale property, so make sure to apply it before)
# If you want to slice at a different angle then just change the normal, and start
# far enough down the z-axis to ensure the plane will slice the entire model
# You can calculate step size to give appropriate thickness slices with sqrt(x*x + y*y +  z*z)
# NB this strategy won't work if you want to cut perpendicular to the z- axis
# in that case you'll need to change the code a bit more

def slicer(step_size = 0.01, normalOfSlice = (0,0,1)):

    object_details = bounds(C.object, True)
    bpy.ops.object.mode_set(mode='OBJECT')

    # If necessary create a new collection to hold the slices
    if not "Slices" in bpy.data.collections:
        bpy.context.scene.collection.children.link(bpy.data.collections.new("Slices"))


    startLoc = object_details.z.min
    stopLoc = object_details.z.max

    steps = int((stopLoc - startLoc)/step_size) + 1    # + 1 because we want the faces on either end
    print("")
    print("********************   STARTING NEW RUN   ********************")
    print("Slicing into ", steps, "slices")
    print("between dimensions of: ", startLoc, ":", stopLoc)

    lBound = 0

    halving = [steps]
    slices = []
    slices.append(bmesh.new())
    slices[0].from_mesh(C.object.data)


    # Add UIDs to the faces of the original object which will be propogated through the model
    # for these purposes just using the original ID will be fine
    #faceUID = bm.faces.layers.integer.new('faceUID')
    #faceUID = bm.faces.layers.integer.get('faceUID')
    #for face in bm.faces:
    #    face[faceUID] = new_UID()
        

    #while (halving[-1] > lBound):
    while len(halving) > 0:
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
            print ("Splitting Mesh into 2 halves with bounds: ",lBound, ":", halving[-1], ":", halving[-2], "and SlicePoint=", startLoc+lBound*step_size, "-", slicePoint, "-", startLoc+halving[-2]*step_size )


            slices.append(slices[-1].copy())
            #This slices the original mesh and discards geometry 
            # on the inner =  lower index = negative side of the plane
            bmesh.ops.bisect_plane(
                slices[-2], 
                geom=slices[-2].verts[:]+slices[-2].edges[:]+slices[-2].faces[:], 
                plane_co=(0,0,slicePoint-step_size), 
                plane_no=normalOfSlice,
                clear_inner=True)

            #This slices the duplicated copy of the mesh and discards geometry 
            # on the outer = higher index = positive side of the plane
            bmesh.ops.bisect_plane(
                slices[-1], 
                geom=slices[-1].verts[:]+slices[-1].edges[:]+slices[-1].faces[:], 
                plane_co=(0,0,slicePoint+step_size), 
                plane_no=normalOfSlice,
                clear_outer=True)

            #print("len(slices) post splitting: ",len(slices))
            
        else:
            # we've just halved the slice directly above the lower bound so slice again to extract 
            # the top and bottom vertex loops (ie discarding the inner and outer geometry for both) 
            # then create two objects from the data
            # Finally step back up to next level clearing out the redundant slice data
            curSlice = int(lBound+(halving[-1]-lBound)/2)
            upperSlicePoint = startLoc+(curSlice+1.5)*step_size
            lowerSlicePoint = startLoc+(curSlice+0.5)*step_size
            
            slices.append(slices[-1].copy())
            print("Extracting last two layers: lowerSlicePoint = ",lowerSlicePoint, "upperSlicePoint = ",upperSlicePoint)
    #        for vert in slices[-1].verts:
    #            print( 'v %f %f %f' % (vert.co.x, vert.co.y, vert.co.z) )
            
            
            #This time slice the mesh and discard both inner and outer geometry to just leave the vertex loops
            cut = bmesh.ops.bisect_plane(
                slices[-2], 
                geom=slices[-2].verts[:]+slices[-2].edges[:]+slices[-2].faces[:], 
                plane_co=(0,0,upperSlicePoint), 
                plane_no=normalOfSlice,
                clear_inner=True,
                clear_outer=True)
                
            if cut:
                facesFromSlice(slices[-2], upperSlicePoint)
            #newobj(slices[-2], "bisect-"+str(upperSlicePoint))

            #This time slice the mesh and discard both inner and outer geometry to just leave the vertex loops
            cut = bmesh.ops.bisect_plane(
                slices[-1], 
                geom=slices[-1].verts[:]+slices[-1].edges[:]+slices[-1].faces[:], 
                plane_co=(0,0,lowerSlicePoint), 
                plane_no=normalOfSlice,
                clear_inner=True,
                clear_outer=True)
               
            if cut:
                facesFromSlice(slices[-1], lowerSlicePoint)
  
                
                
            #print("halving list = ", halving)
            #print ("extracted:",lBound, halving[-1])
            lBound = halving[-1]+1
            #print ("update: lb1",lBound, halving[-1])
            #print ("del:",halving[-1])
            del halving[-1]
            #print("len(slices) post extraction: ",len(slices))
            del slices[-2:]
            #print("len(slices) post drop end: ",len(slices))
            #print("len(halving) post drop end: ",len(slices))
            
       
    print("FINISHED")
    print("Sliced object into ", steps, "slices each ", step_size, "unit thick")
    slices.clear()
    #C.object.user_clear()  # without this, removal would raise an error.
    #bpy.data.objects.remove(C.object, True)       


#slicer(step_size = 0.01, normalOfSlice = (0,0,1))
#slicer(0.01, (0,0,1))