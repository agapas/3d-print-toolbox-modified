# 3d-print-toolbox-modified
Blender addon with utilities for 3d printing. It's based on '3D Print Toolbox' by Campbell Barton. In this modified version it's possible to have more influence on the clean up settings and it gives more flexibility.

### Blender version:
Tested on Blender 2.80 Release Candidate 3 (windows64).
If you need version for Blender 2.79 or older, check the link: [3d-print-toolbox-modified-blender2.79](https://github.com/agapas/3d-print-toolbox-modified-blender2.79)

### More info:
Images below display original '3D Print Toolbox' (image on the left) and current modified version (image on the right):

<p align="middle">
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon_original.png" title="original '3D Print Toolbox'" width="200" height="600" />
  <img src="https://raw.githubusercontent.com/agapas/3d-print-toolbox-modified/master/images/print3dAddon.png" title="current version" width="200" height="600" />
</p>

NOTE:
'Make Solid' works so far only if all selected objects are in the same collection. The full fix for the issue is in 'work in progress'.

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
