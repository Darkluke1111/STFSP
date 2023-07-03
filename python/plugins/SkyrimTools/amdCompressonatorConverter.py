from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from SkyrimTools.abstractConverter import AbstractConverter
import SkyrimTools.configManager as ConfigManager

class AmdCompressonatorConverter(AbstractConverter):

    def getName(self):
        return "AMD Compressonator"

    def buildCommand(self, texset, map):
        path = ConfigManager.global_config["executables"].get("{}_location".format(self.getName()))
        suffix = ConfigManager.global_config[map + "_suffix"]
        codec = self.getCodec(map)
        quality = 1.0  # Set the quality level to a constant value of 1.0
        return [path, 
                    '-fd', codec,  # Specify the compression format based on the codec
                    '-Quality', str(quality),  # Set the quality level
                    '-EncodeWith', 'GPU', # Use the GPU to encode
                    '-mipsize', '1', #Generate mip map down to 1 pixel
                    '{}\{}{}.png'.format(ConfigManager.project_config["png_output"], texset, suffix),
                    '{}\{}{}.dds'.format(ConfigManager.project_config["dds_output"], texset, suffix)
                ]

    def getCodec(self, map):
        # Adjust the codec based on the texture map and configuration
        if map == "diffuse":
            return "BC3" if ConfigManager.project_config["le_compability"] else "BC7"
        if map == "normal":
            return "BC3" if ConfigManager.project_config["le_compability"] else "BC7"
        if map == "glow":
            return "BC7" if ConfigManager.project_config["glow"] else None
        if map == "reflective":
            return "BC7" if ConfigManager.project_config["reflection"] else None
