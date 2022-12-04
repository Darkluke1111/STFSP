from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from SkyrimTools.abstractConverter import AbstractConverter
import SkyrimTools.configManager as cm

class NvidiaConverter(AbstractConverter):

    def buildCommand(self, texset, map, config : cm.Config):
        nvttPath = config.nvtt_location + "/nvcompress.exe"
        suffix = config.suffixes[map]
        codec = self.getCodec(map, config)
        return [nvttPath, 
                    #'-silent',
                    #'-fast' if config.quality == 'fast' else '-production',
                    '-{}'.format(codec),
                    '{}\{}{}.png'.format(config.png_output ,texset, suffix),
                    '{}\{}{}.dds'.format(config.dds_output,texset, suffix)
                ]

    def getCodec(self, map, config: cm.Config):
        if map == "diffuse":
            return ('bc3' if config.le_compability else 'bc7') if config.alpha_blending else 'bc1a'
        if map == "normal":
            return ('bc3' if config.le_compability else 'bc7')
        if map == "glow":
            return 'bc1a' if config.glow else None
        if map == "reflective":
            return 'bc1a' if config.reflection else None
