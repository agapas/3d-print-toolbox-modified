# 3d-print-toolbox-modified
Blender addon with utilities for 3d printing. It's based on a outdated version of the '3D Print Toolbox' by Campbell Barton. In this modified version it's possible to have more influence on the clean up settings and it gives more flexibility.

The plan is for unique features in this version to be progressively added back into the original Blender Addons print3d (
https://github.com/blender/blender-addons/tree/master/object_print3d_utils via my fork
https://github.com/dgm3333/blender-addons/tree/master/object_print3d_utils

However because some documents (such as this file and the .blend printer startup file) are likely to be useful then this repo may remain longer term...






### Blender version:
Any new mods going forward will be using Blender 2.92.
The original (forked code) was tested on Blender 2.80 Release Candidate 3 (windows64).
If you need version for Blender 2.79 or older, check the link: [3d-print-toolbox-modified-blender2.79](https://github.com/agapas/3d-print-toolbox-modified-blender2.79)


### Other useful informmation
The ultimate goal of this project is to have the tool automatically fix models so they can be printed with appropriate supports and modifications.
In addition I would like to show in the mesh where the most likely failure points are - for SLA/DLP or FDM printers (which have quite different stresses during printing)

My torture test is currently the models in StressAndSupportsVisualisation.blend which have a rough progression of difficulty
Finishing with a model which is not only posable, but also has small details not even attached to the main model (and which will need to be in order for it to be printed (I don't think the last is likely to be achievable, but I'll be happy if I manage 50%)


If you are looking for more useful information on modelling 3d printed parts in blender the following are good resources or addins:

A webseries on precision Modeling & Blender 
https://www.youtube.com/playlist?list=PL6Fiih6ItYsXzUbBNz7-IvV7UJYHZzCdF

Notes on 3d print toolbox in blender
-	Shows in the 3d window RHS edge menu (called 3D-print - this one is called 3d printing to distinguish it). If it’s not showing try clicking the little triangle in the top RH corner of the viewport

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



A 3d printer workarea - this is for specific printer, but you can modify it to suit your own.
Since it's very simple, adding this to the scene will be scripted rather than requiring an entire .blend file
(Possibly as an application template https://docs.blender.org/manual/en/latest/advanced/app_templates.html)
But if you primarily use Blender for 3D printing then, you can use your modified version to overwrite your startup via File/Defaults/Save Startup File
<p align="left">
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/PrinterWorkarea.png" title="current version" width="200" height="600" />
</p>


### More info:
Images below display the modified '3D Print Toolbox' (image on the left), the official version it was based on (middle), and the Apr 2021 official Blender version (image on the right):

<p align="middle">
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon.png" title="current version" width="200" height="600" />
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon_original.png" title="original '3D Print Toolbox'" width="200" height="600" />
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon_original_2021.png" title="current version" width="200" height="600" />

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
