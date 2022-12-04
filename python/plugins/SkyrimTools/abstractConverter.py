
import string
from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from abc import ABC, abstractmethod
import substance_painter
import SkyrimTools.configManager as cm
import SkyrimTools.logger

l = SkyrimTools.logger.INSTANCE()

class AbstractConverter(ABC):

    def convert(self, config: cm.Config):

        sets = substance_painter.textureset.all_texture_sets()

        kwargs ={}
        if config.hide_terminal:
            kwargs["creationflags"] = CREATE_NO_WINDOW
        
        for tset in sets:


            self.convertTexture(tset, "diffuse", config, kwargs)
            self.convertTexture(tset, "normal", config, kwargs)

            if config.glow:
                self.convertTexture(tset, "glow", config, kwargs)
            else:
                print("Skipping converting glowmap")

            if config.reflection:
                self.convertTexture(tset, "reflective", config, kwargs)
            else:
                print("Skipping converting reflectionmap")

    def convertTextureSet(self, config: cm.Config, tset):
        kwargs ={}
        if config.hide_terminal:
            kwargs["creationflags"] = CREATE_NO_WINDOW

        self.convertTexture(tset, "diffuse", config, kwargs)
        self.convertTexture(tset, "normal", config, kwargs)

        if config.glow:
            self.convertTexture(tset, "glow", config, kwargs)
        else:
            print("Skipping converting glowmap")

        if config.reflection:
            self.convertTexture(tset, "reflective", config, kwargs)
        else:
            print("Skipping converting reflectionmap")


    def logIfPresent(self,msg, err):
        if(msg):
            l.logDebug(msg.decode("utf-8"))
        if(err):
            l.logError(err.decode("utf-8"))

    def convertTexture(self, tset, texture, config, kwargs):
        cmd =  self.buildCommand(tset, texture, config)
        l.logDebug("Running: " + " ".join(cmd))
        p = Popen(cmd, stdout= PIPE, **kwargs)
        if l.mode == "DEBUG" :
            out, err = p.communicate()
            self.logIfPresent(out, err)


    @abstractmethod
    def buildCommand(self, texsetName, config):
        pass

    @abstractmethod
    def getCodec(self, map, config: cm.Config):
        pass