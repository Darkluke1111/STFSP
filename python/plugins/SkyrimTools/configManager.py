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

project_default: ProjectConfig = {
    "png_output": "",
    "dds_output": "",
    "alpha_blending": False,
    "glow": False,
    "reflection": False,
    "le_compability": False,
    "quality": False,
}

class GlobalConfig(TypedDict):
    crunch_location: str
    nvtt_location: str
    hide_terminal: bool
    diffuse_suffix: str
    normal_suffix: str
    glow_suffix: str
    reflective_suffix: str

global_default : GlobalConfig = {
    "crunch_location": "",
    "nvtt_location": "",
    "hide_terminal": False,
    "diffuse_suffix": "",
    "normal_suffix": "_n",
    "glow_suffix": "_g",
    "reflective_suffix": "_m",
}


global_config_path: str
global_config: GlobalConfig
project_config: ProjectConfig

     
def init(_global_config_path: str) -> None:
    global global_config_path
    global_config_path = _global_config_path + "/config.json"
    substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectOpened, on_project_opened)
    substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectCreated, on_project_opened)
    load_global_config()

def on_project_opened(e):
    load_project_config()


def save_project_config() -> None:
    global project_config
    if not substance_painter.project.is_open():
        return
    l.log(l.INFO, PLUGIN_NAME, "saving project settings")

    localConfig = substance_painter.project.Metadata("skyrim_tools")
    for key, value in project_config.items():
        localConfig.set(key, value)


def load_project_config() -> None:
    l.log(l.INFO, PLUGIN_NAME, "Loading prject config")
    global project_config
    if not substance_painter.project.is_open():
        return
    localConfig = substance_painter.project.Metadata("skyrim_tools")
    l.log(l.INFO, PLUGIN_NAME, "loading project settings")
    
    project_config = project_default.copy()
    
    for key in project_config:
        project_config[key] = localConfig.get(key)


def save_global_config() -> None:
    global global_config
    global global_config_path
    l.log(l.INFO, PLUGIN_NAME, "saving global settings to {}".format(global_config_path))
    with open(global_config_path,'w+', encoding='utf-8') as f:
        json.dump(global_config, f, ensure_ascii=False, indent=4)

def load_global_config() -> None:
    global global_config
    global global_config_path
    l.log(l.INFO, PLUGIN_NAME, "loading global settings from {}".format(global_config_path))
    global_config = global_default.copy()
    if not os.path.isfile(global_config_path):
        return
        
    with open(global_config_path, 'r', encoding= 'utf_8') as f:
        data = json.load(f)
        for key in global_config.keys():
            if key in data:
                global_config[key] = data[key]

def set_global_option(name, value) -> None:
    global_config[name] = value

def set_project_option(name, value) -> None:
    project_config[name] = value
