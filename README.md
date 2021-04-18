# 3d-print-toolbox-modified<p>
Blender addon with utilities for 3d printing. It's based on a outdated version of the '3D Print Toolbox' by Campbell Barton. In this modified version it's possible to have more influence on the clean up settings and it gives more flexibility.<p>
<p>
The plan is for unique features in this version to be progressively added back into the original Blender Addons print3d (<p>
https://github.com/blender/blender-addons/tree/master/object_print3d_utils via my fork<p>
https://github.com/dgm3333/blender-addons/tree/master/object_print3d_utils<p>
<p>
However because some documents (such as this file and the .blend printer startup file) are likely to be useful then this repo may remain longer term...<p>
<p>
<p>
<p>
<p>
<p>
<p>
### Blender version:
Any new mods going forward will be using Blender 2.92.<p>
The original (forked code) was tested on Blender 2.80 Release Candidate 3 (windows64).<p>
If you need version for Blender 2.79 or older, check the link: [3d-print-toolbox-modified-blender2.79](https://github.com/agapas/3d-print-toolbox-modified-blender2.79)<p>
<p>
<p>
### Other useful information
The ultimate goal of this project is to have the tool automatically fix models so they can be printed with appropriate supports and modifications.<p>
In addition I would like to show in the mesh where the most likely failure points are - for SLA/DLP or FDM printers (which have quite different stresses during printing)<p>
<p>
My torture test is currently the models in StressAndSupportsVisualisation.blend which have a rough progression of difficulty<p>
Finishing with a model which is not only posable, but also has small details not even attached to the main model (and which will need to be in order for it to be printed (I don't think the last is likely to be achievable, but I'll be happy if I manage 50%)<p>
<p>
<p>
If you are looking for more useful information on modelling 3d printed parts in blender the following are good resources or addins:<p>
<p>
A webseries on precision Modeling & Blender <p>
https://www.youtube.com/playlist?list=PL6Fiih6ItYsXzUbBNz7-IvV7UJYHZzCdF<p>
<p>
Notes on 3d print toolbox in blender<p>
-	Shows in the 3d window RHS edge menu (called 3D-print - this one is called 3d printing to distinguish it). If it’s not showing try clicking the little triangle in the top RH corner of the viewport<p>
<p>
Other useful Blender Plugins<p>
Booltool<p>
-	Only visible in object mode<p>
-	Shows under Edit in RHS edge menu – if not showing click the down triangle at the top<p>
-	Can use to view slices through plane by creating a cube, select it then another object then selecting difference. Dragging the cube around will cut through the object<p>
-	To move the cube origin used shift-s position 3d cursor to origin, then R-click on object, set origin to 3d cursor.<p>
-	Use the move tool (either click the 4-arrow tool on RHS or shift-space, G (move tool)<p>
<p>
Measure tool:  (this is automatically part of Blender 2.9)<p>
<p>
Precision Drawing Tools - https://www.youtube.com/watch?v=8a4mm-zb3nk<p>
Add Mesh: Extra Objects<p>
Mesh: Looptools<p>
MeasureIt<p>
<p>
OpenSCAD importer for Blender: https://github.com/maqqr/blender-openscad-import  (this is newer than the "official" blender git)<p>
Extra Objects Addon: https://docs.blender.org/manual/en/2.92/addons/add_mesh/mesh_extra_objects.html<p>
(included in Blender installation and defines gears, pipes, etc)<p>
<p>
<p>
Other (potentially) relevant information<p>
Dicer - g-code slicer for blender (probably superseded by current code and not updated since 2014 but had some script fragments) https://github.com/BlenderCN-Org/Dicer<p>
FEM with Blender and FreeCAD - CalculiX: Complex Model: https://www.youtube.com/watch?v=t_x4x2ROXZw<p>
<p>
Not Free (and not tried but look like might have potential):<p>
Parameterizer: https://b3d.interplanety.org/en/blender-add-on-parametrizer/<p>
<p>
<p>
<p>
<p>
A 3d printer workarea - this is for specific printer, but you can modify it to suit your own.<p>
Since it's very simple, adding this to the scene will be scripted rather than requiring an entire .blend file<p>
(Possibly as an application template https://docs.blender.org/manual/en/latest/advanced/app_templates.html)<p>
But if you primarily use Blender for 3D printing then, you can use your modified version to overwrite your startup via File/Defaults/Save Startup File<p>
<p align="left"><p>
  <img src="https://github.com/dgm3333/3d-print-toolbox-modified/blob/master/images/PrinterWorkarea.png" title="current version" /><p>
</p><p>
Partially Coded portions include a redesigned interface, printer calibration section, Slicer, integration with MeshLab, and Resin Printer file export<p>
Some of the calibration models it creates (these are designed to test various aspects of the print to inform the analyser<p>
<img src="https://github.com/dgm3333/3d-print-toolbox-modified/blob/master/images/Calibration%20Models.png" title="Calibration Models" /><p>
One of the enhanced ways of identifying issues with non-manifold meshes<p>
<img src="https://github.com/dgm3333/3d-print-toolbox-modified/blob/master/images/Sliced%20Model%20-%20Non%20Manifold.png" title="Slicer - Non-Manifold View" /><p>
Models can potentially be viewed by layer (using the normal Blender ghost view)<p>
<img src="https://github.com/dgm3333/3d-print-toolbox-modified/blob/master/images/Sliced%20Model%20-%20Layer%20View.png" title="Slicer - Layer View" /><p>
<p>
<p>
<p>
### More info:<p>
Images below display the modified '3D Print Toolbox' (image on the left), the official version it was based on (middle), and the Apr 2021 official Blender version (image on the right):<p>
<p>
<p align="middle"><p>
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon.png" title="current version" width="200" height="600" />
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon_original.png" title="original '3D Print Toolbox'" width="200" height="600" />
  <img src="https://github.com/dgm3333/3d-print-toolbox-modified/blob/master/images/print3dAddon_original_2021.png" title="current version" width="200" height="600" />
</p><p>
<p>
NOTE:<p>
'Make Solid' works so far only if all selected objects are in the same collection. I'm still working on the full fix for the issue.<p>
<p>
#### Added Features<p>
<p>
* added [make-solid](https://github.com/agapas/make-solid)<p>
* made 'Check All' button more visible<p>
* completely changed 'Clean Up' part to have more influence on the clean up process<p>
* added 'Copy to Clipboard' of the Volume and Area in Report's Output<p>
<p>
#### Plans to add:<p>
<p>
* export selected objects to multiple STL<p>
<p>
### Installing<p>
<p>
* go to: File/User Preferences/Add-ons and click 'Install Add-on from File...'<p>
* select the ZIP you downloaded and click 'Install Add-on from File...'<p>
* enable the addon<p>
* save user settings to keep addon enabled over multiple blender sessions<p>
<p>
## License<p>
<p>
This project is licensed under the [GNU v3.0] License - see the [LICENSE.md](LICENSE) file for details.<p>
<p><p>

