
#To use meshlab filters on Blender meshes
#Details are at:
#https://pypi.org/project/pymeshlab/

# You first need to install pymeshlab
#You can do this from the Blender scripting workspace in Blender 2.92
# BUT you have to have admininistor priviledges so for Windows users
#JUST THIS ONCE open Blender by R-clicking on it in the start menu and select"Run as Administrator"

#Open up the System Console (under the Window menu)
#Then paste the following into the scripting workspace and run it

#--- FROM HERE ---#
'''
import subprocess
import sys
import os
 
# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
 
# upgrade pip
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
 
# install required packages
subprocess.call([python_exe, "-m", "pip", "install", "pymeshlab"])

print("DONE")
'''
#--- TO HERE ---#

'''

#Now exit Blender and restart it normally


After restart you can import meshlab using Blender Python and pass it meshes and run filters on them without having to save and load it back and forth as a file
This is a simple script to check it's working.
Output will appear in the System Console window (not the main Blender Python window)
Incidentally when I import pymeshlab I get the following error in the Blender python console but not in the System console, and it seems to work fine (so I just ignore it)
  Warning: Unable to load the following plugins:
    filter_sketchfab.dll: filter_sketchfab.dll does not seem to be a Qt Plugin.*
  Cannot load library C:…\filter_sketchfab.dll: The specified module could not be found.

Also for more information see:
#https://pymeshlab.readthedocs.io/en/latest/tutorials.html



import pymeshlab
print("\n\n")
pymeshlab.print_pymeshlab_version()
print("\n\n")

filters = pymeshlab.filter_list()
print("AVAILABLE FILTERS ARE")
for f in filters:
    print(f)
print("\n\n")

print("SPECIFIC FILTER PARAMETERS can be listed for each filter, eg:-")
print(">>> pymeshlab.print_filter_parameter_list('discrete_curvatures')")
pymeshlab.print_filter_parameter_list('discrete_curvatures')
'''



'''
AVAILABLE FILTERS ARE
alpha_complex_shape
ambient_occlusion
annulus
box_cube
build_a_polyline_from_selected_edges
change_the_current_layer
change_visibility_of_layers
clamp_vertex_quality
close_holes
clustered_vertex_sampling
color_noise
colorize_by_border_distance
colorize_by_face_quality
colorize_by_geodesic_distance_from_a_given_point
colorize_by_geodesic_distance_from_the_selected_points
colorize_by_vertex_quality
colorize_curvature_apss
colorize_curvature_rimls
compact_faces
compact_vertices
compute_area_perimeter_of_selection
compute_curvature_principal_directions
compute_geometric_measures
compute_normals_for_point_sets
compute_planar_section
compute_topological_measures
compute_topological_measures_for_quad_meshes
conditional_face_selection
conditional_vertex_selection
cone
convert_pervertex_uv_into_perwedge_uv
convert_perwedge_uv_into_pervertex_uv
convex_hull
craters_generation
create_selection_perimeter_polyline
create_solid_wireframe
cross_field_creation
csg_operation
curvature_flipping_optimization
cut_mesh_along_crease_edges
define_new_per_face_attribute
define_new_per_vertex_attribute
delaunay_triangulation
delete_all_faces
delete_all_non_selected_rasters
delete_all_non_visible_mesh_layers
delete_current_mesh
delete_current_raster
delete_selected_faces
delete_selected_faces_and_vertices
delete_selected_vertices
depth_complexity
depth_smooth
dilate_selection
directional_geom_preserv
discrete_curvatures
disk_vertex_coloring
distance_from_reference_mesh
dodecahedron
duplicate_current_layer
dust_accumulation
equalize_vertex_color
erode_selection
estimate_radius_from_density
export_active_rasters_cameras_to_file
fit_a_plane_to_selection
flatten_visible_layers
fractal_displacement
fractal_terrain
generate_scalar_harmonic_field
geometric_cylindrical_unwrapping
gpu_filter_example_
grid_generator
hausdorff_distance
hc_laplacian_smooth
icosahedron
image_alignment_mutual_information
image_registration_global_refinement_using_mutual_information
implicit_surface
import_cameras_for_active_rasters_from_file
invert_faces_orientation
invert_selection
iso_parametrization_build_atlased_mesh
iso_parametrization_main
iso_parametrization_remeshing
iso_parametrization_transfer_between_meshes
laplacian_smooth
laplacian_smooth_surface_preserving
marching_cubes_apss
marching_cubes_rimls
matrix_freeze_current_matrix
matrix_invert_current_matrix
matrix_reset_current_matrix
matrix_set_copy_transformation
matrix_set_from_translation_rotation_scale
merge_close_vertices
merge_wedge_texture_coord
mesh_element_sampling
mls_projection_apss
mls_projection_rimls
montecarlo_sampling
move_selected_faces_to_another_layer
move_selected_vertices_to_another_layer
noisy_isosurface
normalize_face_normals
normalize_vertex_normals
octahedron
parameterization__texturing_from_registered_rasters
parameterization_from_registered_rasters
parametrization_flat_plane
parametrization_trivial_per_triangle
parametrization_voronoi_atlas
per_face_color_function
per_face_quality_according_to_triangle_shape_and_aspect_ratio
per_face_quality_function
per_face_quality_histogram
per_face_quality_stat
per_vertex_color_function
per_vertex_geometric_function
per_vertex_normal_function
per_vertex_quality_function
per_vertex_quality_histogram
per_vertex_quality_stat
per_vertex_texture_function
per_wedge_texture_function
perlin_color
permesh_color_scattering
planar_flipping_optimization
point_cloud_simplification
points_cloud_movement
points_on_a_sphere
poisson_disk_sampling
project_active_rasters_color_to_current_mesh
project_active_rasters_color_to_current_mesh_filling_the_texture
project_current_raster_color_to_current_mesh
quality_from_raster_coverage_face
quality_from_raster_coverage_vertex
quality_mapper_applier
random_component_color
random_face_color
random_vertex_displacement
re_compute_face_normals
re_compute_per_polygon_face_normals
re_compute_vertex_normals
re_orient_all_faces_coherentely
re_orient_vertex_normals_using_cameras
refine_user_defined
regular_recursive_sampling
remeshing_isotropic_explicit_remeshing
remove_duplicate_faces
remove_duplicate_vertices
remove_isolated_folded_faces_by_edge_flip
remove_isolated_pieces_wrt_diameter
remove_isolated_pieces_wrt_face_num
remove_t_vertices_by_edge_collapse
remove_t_vertices_by_edge_flip
remove_unreferenced_vertices
remove_vertices_wrt_quality
remove_zero_area_faces
rename_current_mesh
rename_current_raster
repair_non_manifold_edges_by_removing_faces
repair_non_manifold_edges_by_splitting_vertices
repair_non_manifold_vertices_by_splitting
saturate_vertex_quality
scaledependent_laplacian_smooth
select_all
select_border
select_by_face_quality
select_by_vertex_quality
select_connected_faces
select_crease_edges
select_faces_by_color
select_faces_by_view_angle
select_faces_from_vertices
select_faces_with_edges_longer_than
select_folded_faces
select_non_manifold_edges_
select_non_manifold_vertices
select_none
select_outliers
select_problematic_faces
select_self_intersecting_faces
select_small_disconnected_component
select_vertex_texture_seams
select_vertices_from_faces
select_visible_points
set_mesh_camera
set_raster_camera
set_texture
shape_diameter_function
simplification_clustering_decimation
simplification_edge_collapse_for_marching_cube_meshes
simplification_quadric_edge_collapse_decimation
simplification_quadric_edge_collapse_decimation_with_texture
smooth_face_normals
smooth_laplacian_face_color
smooth_laplacian_vertex_color
smooth_vertex_quality
smooths_normals_on_a_point_sets
snap_mismatched_borders
sphere
sphere_cap
split_in_connected_components
stratified_triangle_sampling
structure_synth_mesh_creation
subdivision_surfaces_butterfly_subdivision
subdivision_surfaces_catmull_clark
subdivision_surfaces_loop
subdivision_surfaces_ls3_loop
subdivision_surfaces_midpoint
surface_reconstruction_ball_pivoting
surface_reconstruction_screened_poisson
surface_reconstruction_vcg
taubin_smooth
tetrahedron
texel_sampling
torus
transfer_color_face_to_vertex
transfer_color_mesh_to_face
transfer_color_texture_to_vertex
transfer_color_vertex_to_face
transfer_texture_to_vertex_color_1_or_2_meshes
transfer_vertex_attributes_to_texture_1_or_2_meshes
transfer_vertex_color_to_texture
transform_align_to_principal_axis
transform_flip_and_or_swap_axis
transform_rotate
transform_rotate_camera_or_set_of_cameras
transform_rotate_to_fit_to_a_plane
transform_scale_camera_or_set_of_cameras
transform_scale_normalize
transform_the_camera_extrinsics_or_all_the_cameras_of_the_project
transform_translate_camera_or_set_of_cameras
transform_translate_center_set_origin
tri_to_quad_by_4_8_subdivision
tri_to_quad_by_smart_triangle_pairing
turn_into_a_pure_triangular_mesh
turn_into_quad_dominant_mesh
twostep_smooth
uniform_mesh_resampling
unsharp_mask_color
unsharp_mask_geometry
unsharp_mask_normals
unsharp_mask_quality
vertex_attribute_seam
vertex_attribute_transfer
vertex_color_brightness_contrast_gamma
vertex_color_colourisation
vertex_color_desaturation
vertex_color_filling
vertex_color_invert
vertex_color_levels_adjustment
vertex_color_noise
vertex_color_thresholding
vertex_color_white_balance
vertex_linear_morphing
vertex_quality_from_camera
volumetric_obscurance
volumetric_sampling
voronoi_filtering
voronoi_sampling
voronoi_scaffolding
voronoi_vertex_coloring
'''





import bpy
import pymeshlab
import numpy      



def exportMeshToMeshLab(blenderMesh):
    # NB pymeshlab is fussy
    # verts and faces have to be provided in a numpy array with verts as type float64 and faces as int32
    # faces have to be triangulated - quads and ngons are not allowed
    
    verts = []  #numpyp.empty((0,3), float64)
    for v in blenderMesh.vertices:
            verts.append([v.co[0], v.co[1], v.co[2]])
    verts = numpy.asarray(verts, dtype=numpy.float64)
    if len(verts) == 0:
        print("No vertices were found, so function aborting")
        return
#    print(verts.shape)   # must report (numOfVerts, 3)
#    print(verts.dtype.name)   # must report float64


    faces = []
    tooManyVerts = False
    for poly in blenderMesh.polygons:
        curFace = []
        for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
            curFace.append(blenderMesh.loops[loop_index].vertex_index)
        if len(curFace) == 3:
            faces.append(curFace)
        else:
            tooManyVerts = True
            
            
    if tooManyVerts:
        print("WARNING: Meshlab will only accept faces with THREE vertices")
    if len(faces) == 0:
        print("No triangular faces were found, so function aborting")
        return
    faces = numpy.asarray(faces, dtype=numpy.int32)
#    print(faces.shape)   # must report (numOfVerts, 3)
#    print(faces.dtype.name)

    # create a new Mesh with the two arrays
    meshlabMesh = pymeshlab.Mesh(verts, faces)

    # create a new MeshSet (a meshset can have multiple meshes each in a differnt layer - but that's not covered with this function)
    meshlabMeshSet = pymeshlab.MeshSet()

    # add the mesh to the MeshSet with the current name
    meshlabMeshSet.add_mesh(meshlabMesh, blenderMesh.name)

    return meshlabMeshSet


def importMeshFromMeshLab(meshlabMesh):
    # NB from_pydata in Blender is fussy
    # verts and faces have to be provided in a standard Python list (NOT a numpy array)
    
    verts = meshlabMesh.current_mesh().vertex_matrix().tolist()
    faces = meshlabMesh.current_mesh().face_matrix().tolist()
    #name = meshlabMesh.current_mesh().mesh_name()   # TODO: return this
    
    return verts, faces  #, name


print("START")

# Export a Blender mesh to MeshLab
me = bpy.context.object.data
mls = exportMeshToMeshLab(me)            # (mls = meshlabMeshSet)


# apply filter to the current selected mesh (last loaded)
mls.compute_geometric_measures()

# compute the geometric measures of the current mesh
# and save the results in the out_dict dictionary
out_dict = ms.compute_geometric_measures()

# get the average edge length from the dictionary
avg_edge_length = out_dict['avg_edge_length']

# get the total edge length
total_edge_length = out_dict['total_edge_length']

# get the mesh volume
mesh_volume = out_dict['mesh_volume']

# get the surface area
surf_area = out_dict['surface_area']

# checks with bounds (for numerical errors)
assert (0.023 < avg_edge_length < 0.024)
assert (105.343 < total_edge_length < 105.344)
assert (0.025 < mesh_volume < 0.026)
assert (0.694 < surf_area < 0.695)



# *** CLEANING ***
#remove_zero_area_faces
#remove_duplicate_vertices
#remove_duplicate_faces
#merge_close_vertices
#close_holes


# *** POTENTIAL ISSUES ***
#select_small_disconnected_component


# *** DECREASING POLYGONS/COMPLEXITY *** #
#simplification_clustering_decimation
#simplification_edge_collapse_for_marching_cube_meshes
#simplification_quadric_edge_collapse_decimation
#simplification_quadric_edge_collapse_decimation_with_texture

# parameters
#Target number of faces: Here type the number of polygons you wish your file to have. This procedure is called reduction of polygons also known as mesh decimation.
#Quality threshold: You can select a number between 0 and 1. The recommended entry is 1 as it gives satisfying results. This parameter affects the original model’s shape (ex. bad shaped faces etc. ). So in order for the software to calculate the original shape of the model with only well shaped faces, it requires to enter a high number of faces as it allows more freedom in the final triangle shape.
#Preserve Boundary of the Mesh: Here you should click on this option, as it has to do with preserving the mesh boundaries. Since your file is going under a simplification process, it is essential not to destroy boundaries of the mesh, such as exposed edges etc..
#Preserve Normal: Here you should also select this option if it is not already on by default. With this action you prevent the software to flip face normals and preserves the orientation of the surface.
#Optimal position of simplified vertices: This option should also be on by default. It is essential for preventing the edges from collapsing and substituting the original mesh.
#Planar simplification: This option should be activated when there are flat surfaces on the model that you want to be tessellated. This parameter affects the quality of the shape of the final triangles on planar portions of the mesh and improves the accuracy/complexity ratio.




# Import a MeshLab mesh to Blender
verts, faces = importMeshFromMeshLab(meshlabMeshSet)
mesh = bpy.data.meshes.new("meshFromMeshLab")  # add the new mesh
mesh.from_pydata(verts, [], faces)   # this could also be done as a bmesh too...
ob = bpy.data.objects.new("meshFromMeshLab", mesh)
bpy.context.collection.objects.link(ob)


print(verts)
print(faces)

print("DONE")



