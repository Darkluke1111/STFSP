import substance_painter
import substance_painter.logging as l
import json
import os
from SkyrimTools.constants import PLUGIN_NAME


class Config():
    def __init__(self, pluginPath) -> None:
        self.globalConfigPath = "{}/config.json".format(pluginPath)
        self.crunch_location = "{}/crunch_x64.exe".format(pluginPath)
        self.nvtt_location = ""
        self.hide_terminal =  False
        self.png_output = ""
        self.dds_output = ""
        self.alpha_blending =  False
        self.glow = False
        self.reflection =  False
        self.le_compability = False
        self.quality = "fast"
        self.suffixes = {"diffuse": "", "normal": "_n", "glow": "_g", "reflective": "_m"}

        l.log(l.INFO, PLUGIN_NAME, "finished initializing configManager")

    def set_nvtt_location(self, nvtt_location):
        self.nvtt_location = nvtt_location

    def set_hide_terminal(self, hide_terminal):
        self.hide_terminal = hide_terminal

    def set_png_output(self, png_output):
        self.png_output = png_output

    def set_dds_output(self, dds_output):
        self.dds_output = dds_output

    def set_alpha_blending(self, alpha_blending):
        self.alpha_blending = alpha_blending

    def set_glow(self, glow):
        self.glow = glow

    def set_reflection(self,reflection):
        self.reflection = reflection

    def set_le_compability(self, le_compability):
        self.le_compability = le_compability

    def set_quality(self, quality):
        self.quality = quality

    def saveSettings(self):
        self.saveGlobalConfigs()
        self.saveLocalConfigs()

    def saveGlobalConfigs(self):
        l.log(l.INFO, PLUGIN_NAME, "saving global settings to {}".format(self.globalConfigPath))
        with open(self.globalConfigPath,'w+', encoding='utf-8') as f:
            json.dump({'nvtt_location': self.nvtt_location, 'hide_terminal': self.hide_terminal}, f, ensure_ascii=False, indent=4)

    def saveLocalConfigs(self):
        if substance_painter.project.is_open():
            l.log(l.INFO, PLUGIN_NAME, "saving project settings")
            self.localConfig = substance_painter.project.Metadata("skyrim_tools")
            self.localConfig.set("png_output",      self.png_output)
            self.localConfig.set("dds_output",      self.dds_output)
            self.localConfig.set("alpha_blending",  self.alpha_blending)
            self.localConfig.set("glow",            self.glow)
            self.localConfig.set("reflection",      self.reflection)
            self.localConfig.set("le_compability",  self.le_compability)
            self.localConfig.set("quality",         self.quality)

    def loadSettings(self):
        self.loadGlobalConfigs()
        self.loadLocalConfigs()



    def loadGlobalConfigs(self):
        l.log(l.INFO, PLUGIN_NAME, "loading global settings from {}".format(self.globalConfigPath))
        if not os.path.isfile(self.globalConfigPath):
            self.saveGlobalConfigs()
        
        with open(self.globalConfigPath, 'r', encoding= 'utf_8') as f:
            data = json.load(f)
            if 'nvtt_location' in data:
                self.nvtt_location = data['nvtt_location']
            if 'hide_terminal' in data:
                self.hide_terminal = data['hide_terminal']

    def loadLocalConfigs(self):
        if substance_painter.project.is_open():
            self.localConfig = substance_painter.project.Metadata("skyrim_tools")
            l.log(l.INFO, PLUGIN_NAME, "loading project settings")
            
            self.png_output        = self.localConfig.get("png_output")
            self.dds_output        = self.localConfig.get("dds_output")
            self.alpha_blending    = bool(self.localConfig.get("alpha_blending"))
            self.glow              = bool(self.localConfig.get("glow"))
            self.reflection        = bool(self.localConfig.get("reflection"))
            self.le_compability    = bool(self.localConfig.get("le_compability"))
            self.quality           = self.localConfig.get("quality")

            projectPath = substance_painter.project.file_path()
            projectPath = os.path.dirname(projectPath) + "/"
            if not self.png_output or self.png_output == "":
                self.png_output = projectPath
            if not self.dds_output or self.dds_output == "":
                self.dds_output = projectPath
