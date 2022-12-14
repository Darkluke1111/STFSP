import string
import substance_painter.export
import substance_painter.resource
import substance_painter.logging as l
import substance_painter
import SkyrimTools.configManager as ConfigManager
from SkyrimTools.constants import PLUGIN_NAME


def exportTextureSet(tset):
    outputDir = ConfigManager.project_config["png_output"]
    requiredTextures = ["$textureSet", "$textureSet_n"]
    if ConfigManager.project_config["glow"]:
        requiredTextures.append("$textureSet_g")
    if ConfigManager.project_config["reflection"]:
        requiredTextures.append("$textureSet_m")

    l.log(l.INFO, PLUGIN_NAME, "Exporting textures: " + " ".join(requiredTextures))
    l.log(l.INFO, PLUGIN_NAME, "Building config for " + tset.name())
    l.log(l.INFO, PLUGIN_NAME, "Exporting into " + outputDir)
    export_config = buildExportConfig(outputDir, tset, requiredTextures)

    # Actual export operation:
    export_result = substance_painter.export.export_project_textures(export_config)

    # In case of error, display a human readable message:
    if export_result.status != substance_painter.export.ExportStatus.Success:
        l.log(l.ERROR, PLUGIN_NAME, export_result.message)

    l.log(l.INFO, PLUGIN_NAME, "Finished expot operation")


def buildExportConfig(outputDir, textureSet, requiredTextures):
    return  {

        "exportPath" : outputDir,
        "exportShaderParams" : True,
        "defaultExportPreset" : "Custom_Skyrim_Export",
        "exportPresets" : [{
            "name" : "Custom_Skyrim_Export",
            "maps" : [{
                "fileName" : "$textureSet",
                "channels" : [{
                    "destChannel" : "R",
                    "srcChannel" : "R",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "diffuse"
                    },{
                    "destChannel" : "G",
                    "srcChannel" : "G",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "diffuse"
                    },{
                    "destChannel" : "B",
                    "srcChannel" : "B",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "diffuse"
                    },{
                    "destChannel" : "A",
                    "srcChannel" : "L",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "opacity"
                }],
                "parameters" : {
                    "fileFormat" : "png",
                    "bitDepth" : "8",
                    "dithering" : False,
                    # "sizeLog2" : 10,
                    "paddingAlgorithm" : "infinite"
                }
            },{
                "fileName" : "$textureSet_n",
                "channels" : [{
                    "destChannel" : "R",
                    "srcChannel" : "R",
                    "srcMapType" : "virtualMap",
                    "srcMapName" : "Normal_DirectX"
                    },{
                    "destChannel" : "G",
                    "srcChannel" : "G",
                    "srcMapType" : "virtualMap",
                    "srcMapName" : "Normal_DirectX"
                    },{
                    "destChannel" : "B",
                    "srcChannel" : "B",
                    "srcMapType" : "virtualMap",
                    "srcMapName" : "Normal_DirectX"
                    },{
                    "destChannel" : "A",
                    "srcChannel" : "L",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "specularlevel"
                    }
                ],
                "parameters" : {
                    "fileFormat" : "png",
                    "bitDepth" : "8",
                    "dithering" : False,
                    # "sizeLog2" : 10,
                    "paddingAlgorithm" : "infinite"
                }
            },{
                "fileName" : "$textureSet_g",
                "channels" : [{
                    "destChannel" : "R",
                    "srcChannel" : "R",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "emissive"
                },{
                    "destChannel" : "G",
                    "srcChannel" : "G",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "emissive"
                },{
                    "destChannel" : "B",
                    "srcChannel" : "B",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "emissive"
                }],
                "parameters" : {
                    "fileFormat" : "png",
                    "bitDepth" : "8",
                    "dithering" : False,
                    # "sizeLog2" : 10,
                    "paddingAlgorithm" : "infinite"
                }
            },{
                "fileName" : "$textureSet_m",
                "channels" : [{
                    "destChannel" : "R",
                    "srcChannel" : "L",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "reflection"
                },{
                    "destChannel" : "G",
                    "srcChannel" : "L",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "reflection"
                },{
                    "destChannel" : "B",
                    "srcChannel" : "L",
                    "srcMapType" : "documentMap",
                    "srcMapName" : "reflection"
                }],
                "parameters" : {
                    "fileFormat" : "png",
                    "bitDepth" : "8",
                    "dithering" : False,
                    # "sizeLog2" : 10,
                    "paddingAlgorithm" : "infinite"
                }
            }]
        }],
        "exportList": [{ 
            "rootPath": textureSet.name(),
            "filter": {
                "outputMaps" : requiredTextures,
                # "uvTiles" : [[1, 1]]
            }
        }]
    }   