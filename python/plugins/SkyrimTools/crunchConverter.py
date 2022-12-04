from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from SkyrimTools.abstractConverter import AbstractConverter
import SkyrimTools.configManager as cm

class CrunchConverter(AbstractConverter):

    def buildCommand(self, texset, map, config:cm.Config):
        suffix = config.suffixes[map]
        codec = self.getCodec(map,config)
        print("running converter at {}".format(config.crunch_location))
        return [config.crunch_location, 
                    '-file', '{}/{}{}.png'.format(config.png_output,texset, suffix),
                    '-outdir', config.dds_output, 
                    '-fileformat', 'dds', '-{}'.format(codec), 
                    #'-quiet'
                ]

    def getCodec(self, map, config: cm.Config):
        if map == "diffuse":
            return 'DXT5' if config.alpha_blending else 'DXT1A'
        if map == "normal":
            return 'DXT5'
        if map == "glow":
            return 'DXT1A' if config.glow else None
        if map == "reflective":
            return 'DXT1A' if config.reflection else None
