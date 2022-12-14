from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from SkyrimTools.abstractConverter import AbstractConverter
import SkyrimTools.configManager as ConfigManager

class NvidiaConverter(AbstractConverter):

    def buildCommand(self, texset, map):
        nvttPath = ConfigManager.global_config["nvtt_location"]
        suffix = ConfigManager.global_config[map + "_suffix"]
        codec = self.getCodec(map)
        return [nvttPath, 
                    #'-silent',
                    #'-fast' if config.quality == 'fast' else '-production',
                    '-{}'.format(codec),
                    '{}\{}{}.png'.format(ConfigManager.project_config["png_output"] ,texset, suffix),
                    '{}\{}{}.dds'.format(ConfigManager.project_config["dds_output"],texset, suffix)
                ]

    def getCodec(self, map):
        if map == "diffuse":
            return ('bc3' if ConfigManager.project_config["le_compability"] else 'bc7') if ConfigManager.project_config["alpha_blending"] else 'bc1a'
        if map == "normal":
            return ('bc3' if ConfigManager.project_config["le_compability"] else 'bc7')
        if map == "glow":
            return 'bc1a' if ConfigManager.project_config["glow"] else None
        if map == "reflective":
            return 'bc1a' if ConfigManager.project_config["reflection"] else None
