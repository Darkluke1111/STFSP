Installation:

Move skyrim_tools.py and the SKyrimTools folder into the python plugins folder of Substance Painter. This is probably located under .../Documents/Allegorithmic/Substance Painter/python/plugins or .../Documents/Adobe/Substance Painter/python/plugins depending on your Substance Painter version. The final file structure should look like this:

...
Substance Painter
  |
  L python
    |
    L plugins
      |
      L skyrim_tools.py
      L SkyrimTools
        |
        L config.json
        L crunch_x64.exe
...

Start Substance Painter and there should be a new Menu Option in the top bar called Skyrim.

Usage:

If you click Export DDS it will export your textures and convert them to dds according to the settings you selected by clicking the Settings option.
All Settings have tooltips when you hover over their labels that explain what they do.
Everything should work out of the box when you selected the export folders in the settings. By default the crunch dds encoder that is redistributed with this plugin is used for the conversion process (https://github.com/Unity-Technologies/crunch/tree/unity). If you need better performance and access to the BC7 codec you can install the Nvidia Texture Tools Standalone version (https://developer.nvidia.com/nvidia-texture-tools-exporter).
This will require a signup (which is free). After you installed it you need to fill in the path to the "Nvidia Texture Tools" folder (containing nvcompress.exe) and it will be used instead of crunch.

A note on the settings: There are several checkboxes where you can check or uncheck which features are used by your texture set. This information will be used for deciding which dds codec is the best for your textures (or whether to convert certain textures at all. If you don't use glow, you won't need a glow map...). You can read on how these decisions are made on these pages: (https://wiki.beyondskyrim.org/wiki/Arcane_University:DDS_Data_Format) (https://w3dhub.com/forum/topic/417101-dds-files-and-dxt-compression/?tab=comments#comment-671198)
Also the quality setting only impacts conversions done by Nvidia Texture Tool (yet).

If you encounter any bugs or have further questions you can contact me via discord by joining this server: https://discord.gg/DaQYPKsSf5