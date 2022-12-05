import substance_painter
import substance_painter.logging as l
import json
import os
from SkyrimTools.constants import PLUGIN_NAME
from typing import TypedDict

class ProjectConfig(TypedDict):
    png_output: str
    dds_output: str
    alpha_blending: bool
    glow: bool
    reflection: bool
    le_compability: bool
    quality: bool
    diffuse_suffix: str
    normal_suffix: str
    glow_suffix: str
    reflective_suffix: str

project_default: ProjectConfig = {
    "png_output": "",
    "dds_output": "",
    "alpha_blending": False,
    "glow": False,
    "reflection": False,
    "le_compability": False,
    "quality": False,
    "diffuse_suffix": "",
    "normal_suffix": "_n",
    "glow_suffix": "_g",
    "reflective_suffix": "_m",
}

class GlobalConfig(TypedDict):
    crunch_location: str
    nvtt_location: str
    hide_terminal: bool

global_default : GlobalConfig = {
    "crunch_location": "",
    "nvtt_location": "",
    "hide_terminal": False,
}


def save_to_project(config: ProjectConfig) -> bool:
    if not substance_painter.project.is_open():
        return False
    l.log(l.INFO, PLUGIN_NAME, "saving project settings")

    localConfig = substance_painter.project.Metadata("skyrim_tools")
    for key, value in config.items():
        localConfig.set(key, value)
    return True

def load_from_project() -> ProjectConfig:
    if not substance_painter.project.is_open():
        return False
    localConfig = substance_painter.project.Metadata("skyrim_tools")
    l.log(l.INFO, PLUGIN_NAME, "loading project settings")
    
    project_config : ProjectConfig = project_default.copy()
    
    for key in project_config:
        project_config[key] = localConfig.get(key)

def save_to_global(config: GlobalConfig, path: str) -> bool:
    l.log(l.INFO, PLUGIN_NAME, "saving global settings to {}".format(path))
    with open(path,'w+', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def load_from_global(path: str) -> GlobalConfig:
    l.log(l.INFO, PLUGIN_NAME, "loading global settings from {}".format(path))
    global_config = global_default.copy()
    if not os.path.isfile(path):
        return global_config
        
    with open(path, 'r', encoding= 'utf_8') as f:
        data = json.load(f)
        for key in global_config.keys():
            if key in data:
                global_config[key] = data[key]
    return global_config
