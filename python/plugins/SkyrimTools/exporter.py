import string
import substance_painter.export
import substance_painter.resource
import substance_painter
from SkyrimTools.configManager import Config
import SkyrimTools.logger as logger

l = logger.INSTANCE()

def export(config: Config):

    outputDir = config.png_output
    requiredTextures = ["$textureSet", "$textureSet_n"]
    if config.glow:
        requiredTextures.append("$textureSet_g")
    if config.reflection:
        requiredTextures.append("$textureSet_m")

    l.logDebug("Exporting textures: " + " ".join(requiredTextures))

    sets = substance_painter.textureset.all_texture_sets()
    l.logDebug("Exporting texture sets: " + " ".join(map(lambda x: x.name(),sets)))
    for tset in sets:

        l.logDebug("Exporting into " + outputDir)
        export_config = buildExportConfig(outputDir, tset, requiredTextures)

        # Actual export operation:
        export_result = substance_painter.export.export_project_textures(export_config)

        # In case of error, display a human readable message:
        if export_result.status != substance_painter.export.ExportStatus.Success:
            l.logError(export_result.message)
    l.logDebug("Finished expot operation")

def exportTextureSet(config: Config, tset):
    outputDir = config.png_output
    requiredTextures = ["$textureSet", "$textureSet_n"]
    if config.glow:
        requiredTextures.append("$textureSet_g")
    if config.reflection:
        requiredTextures.append("$textureSet_m")

    l.logDebug("Exporting textures: " + " ".join(requiredTextures))
    l.logDebug("Building config for " + tset.name())
    l.logDebug("Exporting into " + outputDir)
    export_config = buildExportConfig(outputDir, tset, requiredTextures)

    # Actual export operation:
    export_result = substance_painter.export.export_project_textures(export_config)

    # In case of error, display a human readable message:
    if export_result.status != substance_painter.export.ExportStatus.Success:
        l.logError(export_result.message)

    l.logDebug("Finished expot operation")


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