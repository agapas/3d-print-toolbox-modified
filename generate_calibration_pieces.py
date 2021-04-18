# generate calibration pieces

#def areaCircle

# a number of STLs are potentially promising for "real world" torture testing including
# Polypearl Tower:
# https://www.thingiverse.com/thing:2064029
# New York:
#https://www.thingiverse.com/thing:1557864 - just this file:-
#https://cdn.thingiverse.com/assets/4d/e2/2e/31/9f/Final_City2_fixed.stl
# Eiffel Tower:
#https://pinshape.com/items/11574-3d-printed-eiffel-tower-seetheworld
# Train Tunnel Arch
#https://www.thingiverse.com/thing:3275820





import bpy

printerBedXmm =130
printerBedYmm = 75

#3840 x 2160



def createMesh(name, origin, collection, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
    # Link object to scene (not currently required as linked to autosupports elsewhere)
    #bpy.context.scene.collection.objects.link( ob )
 
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
 
    # Update mesh with new data
    me.update(calc_edges=True)
    if collection == "":
        bpy.context.scene.collection.objects.link(ob)
    else:
        bpy.data.collections[collection].objects.link(ob)
    return ob



#Inverted Square Pyramid - testing baseplate vs printface binding
verts = [(7.5,7.5,0),(-7.5,7.5,0),(-7.5,-7.5,0),(7.5,-7.5,0), (5,5,10),(-5,5,10),(-5,-5,10),(5,-5,10)]
faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]
obj = createMesh('squarePyramidNarrowing', (0,0,0), "", verts, [], faces)

verts = [(5,5,-0.1),(-5,5,-0.1),(-5,-5,-0.1),(5,-5,-0.1), (5,5,10.1),(-5,5,10.1),(-5,-5,10.1),(5,-5,10.1)]
faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]
obj = createMesh('squarePyramidNarrowing', (0,0,0), "", verts, [], faces)



'''

#Checkerboard Recursive Fine Features
#(NB base cube not sizing properly)
bpy.ops.mesh.primitive_cube_add(size=20, enter_editmode=False, align='WORLD', location=(10, 10, -5), scale=(1, 1, 1))

def checkerboard(left, front, bottom, blocksize, reps, recursion):
    for x in range(reps):
        if x % 2 == 0:
            for y in range(0,reps,2):
                bpy.ops.mesh.primitive_cube_add(size=blocksize, enter_editmode=False, align='WORLD', 
                    location=(left+(x+0.5)*blocksize, front+(y+0.5)*blocksize, bottom+blocksize/2), scale=(1, 1, 1))
                if recursion>0:
                    checkerboard(left+x*blocksize, front+y*blocksize, bottom+blocksize, blocksize/4, reps, recursion-1)
        else:
            for y in range(1,reps,2):
                bpy.ops.mesh.primitive_cube_add(size=blocksize, enter_editmode=False, align='WORLD', 
                    location=(left+(x+0.5)*blocksize, front+(y+0.5)*blocksize, bottom+blocksize/2), scale=(1, 1, 1))
                if recursion>0:
                    checkerboard(left+x*blocksize, front+y*blocksize, bottom+blocksize, blocksize/4, reps, recursion-1)

checkerboard(0, 0, 2.5, 5, 4, 3)







#Narrowing Hollow Cone - testing minimum wall thickness
bpy.ops.mesh.primitive_cone_add(
    vertices=360, 
    radius1=7.5, 
    radius2=5,
    depth=10, 
    enter_editmode=False, 
    align='WORLD', 
    location=(-100, 0, 5), 
    scale=(1, 1, 1))
bpy.ops.mesh.primitive_cone_add(
    vertices=360, 
    radius1=5, 
    radius2=5,
    depth=10, 
    enter_editmode=False, 
    align='WORLD', 
    location=(-100, 0, 5), 
    scale=(1, 1, 1))
bpy.context.object.modifiers["Boolean.001"].object = bpy.data.objects["Icosphere.001"]











#Inverted Cone - testing baseplate vs printface binding
bpy.ops.mesh.primitive_cone_add(
    vertices=360, 
    radius1=5.6419, 
    radius2=18.14189822,
    depth=25, 
    enter_editmode=False, 
    align='WORLD', 
    location=(50, 0, 12.5), 
    scale=(1, 1, 1))


#Inverted Square Pyramid - testing baseplate vs printface binding
verts = [(5,5,0),(-5,5,0),(-5,-5,0),(5,-5,0),(17.5,17.5,25),(-17.5,17.5,25),(-17.5,-17.5,25),(17.5,-17.5,25)]
faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]
obj = createMesh('squarePyramid', (0,0,0), "", verts, [], faces)





#Square Hourglass - testing printface vs interlayer binding
verts = [(10,10,0),(-10,10,0),(-10,-10,0),(10,-10,0),
         (5,5,5),(-5,5,5),(-5,-5,5),(5,-5,5),
         (17.5,17.5,30),(-17.5,17.5,30),(-17.5,-17.5,30),(17.5,-17.5,30)]
faces = [(0, 1, 2, 3), 
         (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7), 
         (4, 8, 9, 5), (5, 9, 10, 6), (6, 10, 11, 7), (8, 4, 7, 11), 
         (8, 11, 10, 9), ]
obj = createMesh('squareHourglass', (0,0,0), "", verts, [], faces)



# Circular Hourglass - testing printface vs interlayer binding
#Create Cone base
bpy.ops.mesh.primitive_cone_add(
    vertices=360, 
    radius1=11.2838, 
    radius2=5.6419, 
    depth=5, 
    enter_editmode=False, 
    align='WORLD', 
    location=(50, 0, 2.5), 
    scale=(1, 1, 1))
    
bpy.ops.mesh.primitive_cone_add(
    vertices=360, 
    radius1=5.6419, 
    radius2=18.14189822,
    depth=25, 
    enter_editmode=False, 
    align='WORLD', 
    location=(50, 0, 17.5), 
    scale=(1, 1, 1))








    

#1x1x1 cube
bpy.ops.mesh.primitive_cube_add(size=20, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))





# Hollow Dome
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, radius=10, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.ops.mesh.primitive_cube_add(size=32, enter_editmode=False, align='WORLD', location=(0, 0, -16), rotation=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cube"]
bpy.ops.mesh.primitive_ico_sphere_add(radius=13, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.modifiers["Boolean.001"].object = bpy.data.objects["Icosphere.001"]



# Arch

bpy.ops.mesh.primitive_cylinder_add(
    vertices=360,
    radius=10, 
    depth=10, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0), 
    rotation=(1.5708, 0, 0), 
    scale=(1, 1, 1))

bpy.ops.mesh.primitive_cylinder_add(
    vertices=360,
    radius=13, 
    depth=5, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0), 
    rotation=(1.5708, 0, 0), 
    scale=(1, 1, 1))

bpy.ops.mesh.primitive_cube_add(size=32, enter_editmode=False, align='WORLD', location=(0, 0, -16), rotation=(0, 0, 0), scale=(1, 1, 1))
    
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cylinder"]


'''