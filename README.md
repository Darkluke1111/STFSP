# STFSP

Github Project for STFSP (Skyrim Tools for Substance Painter), a collection of tools, assets and shaders that make creating textures for Skyrim models easier and faster.

## Setting up SP for development

1. Link the assets directory to SP
   > While it is possible to just copy the contents of the assets folder into the default assets folder of SP, it's much easier to just link the assets folder of the git repo into SP. To do this, open SP and follow Edit -> Settings -> Libraries and add a new library location with a name of your choice and the path of the assets folder in this git repository
  
2.  Link the plugins directory to SP
    > I recommend to add the python folder in this repository to the Substance Painter plugins path environment variable. Documenation on how to do this, can be found [here](https://substance3d.adobe.com/documentation/ptpy/tutorials/loading-external-python-plugins).
  
3.  Add aditional resources that are not provided within this repository if needed
    > I want to avoid adding to many binary files to this git repository. This means you might want to download resources like environment HDRIs for shader testing from the [Nexus page](https://www.nexusmods.com/skyrimspecialedition/mods/44400)
