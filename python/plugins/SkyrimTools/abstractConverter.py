
import string
from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from abc import ABC, abstractmethod
import substance_painter
import substance_painter.logging as l
import SkyrimTools.configManager as ConfigManager
from SkyrimTools.constants import PLUGIN_NAME

class AbstractConverter(ABC):

    def convertTextureSet(self, tset):
        kwargs ={}
        if ConfigManager.global_config["hide_terminal"]:
            kwargs["creationflags"] = CREATE_NO_WINDOW

        self.convertTexture(tset, "diffuse", kwargs)
        self.convertTexture(tset, "normal", kwargs)

        if ConfigManager.project_config["glow"]:
            self.convertTexture(tset, "glow", kwargs)
        else:
            print("Skipping converting glowmap")

        if ConfigManager.project_config["reflection"]:
            self.convertTexture(tset, "reflective", kwargs)
        else:
            print("Skipping converting reflectionmap")


    def logIfPresent(self,msg, err):
        if(msg):
            try:
                l.log(l.INFO, PLUGIN_NAME, msg.decode("utf-8"))
            except:
                l.log(l.INFO, PLUGIN_NAME, msg.decode("latin-1"))
        if(err):
            l.log(l.ERROR, PLUGIN_NAME, err.decode("utf-8"))

    def convertTexture(self, tset, texture, kwargs):
        cmd =  self.buildCommand(tset, texture)
        l.log(l.INFO, PLUGIN_NAME, "Running: " + " ".join(cmd))
        p = Popen(cmd, stdout= PIPE, **kwargs)

        out, err = p.communicate()
        self.logIfPresent(out, err)


    @abstractmethod
    def buildCommand(self, texsetName):
        pass

    @abstractmethod
    def getCodec(self, map):
        pass

    @abstractmethod
    def getName(self):
        pass