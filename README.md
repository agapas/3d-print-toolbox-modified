# 3d-print-toolbox-modified
Blender addon with utilities for 3d printing. It's based on '3D Print Toolbox' by Campbell Barton. In this modified version it's possible to have more influence on the clean up settings and it gives more flexibility.

### Blender version:
Any new mods going forward will be using Blender 2.92.
The original (forked code) was tested on Blender 2.80 Release Candidate 3 (windows64).
If you need version for Blender 2.79 or older, check the link: [3d-print-toolbox-modified-blender2.79](https://github.com/agapas/3d-print-toolbox-modified-blender2.79)


### Other useful informmation
A webseries on precision Modeling & Blender 
https://www.youtube.com/playlist?list=PL6Fiih6ItYsXzUbBNz7-IvV7UJYHZzCdF

Notes on 3d print toolbox in blender
-	Only visible in edit mode
-	Shows in the 3d window RHS edge menu (called 3D-print). If it’s not showing try clicking the little triangle in the top RH corner of the viewport

Other useful Blender Plugins
Booltool
-	Only visible in object mode
-	Shows under Edit in RHS edge menu – if not showing click the down triangle at the top
-	Can use to view slices through plane by creating a cube, select it then another object then selecting difference. Dragging the cube around will cut through the object
-	To move the cube origin used shift-s position 3d cursor to origin, then R-click on object, set origin to 3d cursor.
-	Use the move tool (either click the 4-arrow tool on RHS or shift-space, G (move tool)

Measure tool:  (this is automatically part of Blender 2.9)

Precision Drawing Tools - https://www.youtube.com/watch?v=8a4mm-zb3nk
Add Mesh: Extra Objects
Mesh: Looptools
MeasureIt







### More info:
Images below display original '3D Print Toolbox' (image on the left) and current modified version (image on the right):

<p align="middle">
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon_original.png" title="original '3D Print Toolbox'" width="200" height="600" />
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon.png" title="current version" width="200" height="600" />
</p>

NOTE:
'Make Solid' works so far only if all selected objects are in the same collection. I'm still working on the full fix for the issue.

#### Added Features

* added [make-solid](https://github.com/agapas/make-solid)
* made 'Check All' button more visible
* completely changed 'Clean Up' part to have more influence on the clean up process
* added 'Copy to Clipboard' of the Volume and Area in Report's Output

#### Plans to add:

* export selected objects to multiple STL

### Installing

* go to: File/User Preferences/Add-ons and click 'Install Add-on from File...'
* select the ZIP you downloaded and click 'Install Add-on from File...'
* enable the addon
* save user settings to keep addon enabled over multiple blender sessions

## License

This project is licensed under the [GNU v3.0] License - see the [LICENSE.md](LICENSE) file for details.
