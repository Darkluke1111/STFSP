from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from SkyrimTools.abstractConverter import AbstractConverter
import SkyrimTools.configManager as ConfigManager

class TexConvConverter(AbstractConverter):

    def getName(self):
        return "TexConv"

    def buildCommand(self, texset, map):
        path = ConfigManager.global_config["executables"].get("{}_location".format(self.getName()))
        suffix = ConfigManager.global_config[map + "_suffix"]
        codec = self.getCodec(map)
        return ['{}'.format(path).replace('/','\\') ,
                    '-f', '{}'.format(codec),
                    '-y',
                    '-o', '{}'.format(ConfigManager.project_config["dds_output"]).replace('/','\\'),
                    '{}/{}{}.png'.format(ConfigManager.project_config["png_output"] ,texset, suffix).replace('/','\\'),
                ]

    def getCodec(self, map):
        if map == "diffuse":
            return ('BC3_UNORM' if ConfigManager.project_config["le_compability"] else 'BC7_UNORM') if ConfigManager.project_config["alpha_blending"] else 'BC1_UNORM'
        if map == "normal":
            return ('BC3_UNORM' if ConfigManager.project_config["le_compability"] else 'BC7_UNORM')
        if map == "glow":
            return 'BC1_UNORM' if ConfigManager.project_config["glow"] else None
        if map == "reflective":
            return 'BC1_UNORM' if ConfigManager.project_config["reflection"] else None
