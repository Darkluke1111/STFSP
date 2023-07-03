from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from SkyrimTools.abstractConverter import AbstractConverter
import SkyrimTools.configManager as ConfigManager

class CrunchConverter(AbstractConverter):

    def getName(self):
        return "Crunch"

    def buildCommand(self, texset, map):
        suffix = ConfigManager.global_config[map + "_suffix"]
        codec = self.getCodec(map)
        path = ConfigManager.global_config["executables"].get("{}_location".format(self.getName()))
        print("running converter at {}".format(path))
        return [path, 
                    '-file', '{}/{}{}.png'.format(ConfigManager.project_config["png_output"],texset, suffix),
                    '-outdir', ConfigManager.project_config["dds_output"], 
                    '-fileformat', 'dds', '-{}'.format(codec), 
                    #'-quiet'
                ]

    def getCodec(self, map):
        if map == "diffuse":
            return 'DXT5' if ConfigManager.project_config["alpha_blending"] else 'DXT1A'
        if map == "normal":
            return 'DXT5'
        if map == "glow":
            return 'DXT1A' if ConfigManager.project_config["glow"] else None
        if map == "reflective":
            return 'DXT1A' if ConfigManager.project_config["reflection"] else None
