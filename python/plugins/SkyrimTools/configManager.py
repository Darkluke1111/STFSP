import substance_painter
import substance_painter.logging as l
import json
import os
from SkyrimTools.constants import PLUGIN_NAME
from typing import TypedDict
import skyrim_tools

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
    executables: dict
    compression_tool: str
    hide_terminal: bool
    diffuse_suffix: str
    normal_suffix: str
    glow_suffix: str
    reflective_suffix: str

global_default : GlobalConfig = {
    "executables": {},
    "compression_tool": "Crunch",
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
        #l.log(l.INFO, PLUGIN_NAME, "saving {} = {}".format(key, value))
        localConfig.set(key, value)
    substance_painter.project.save(substance_painter.project.ProjectSaveMode.Incremental)


def load_project_config() -> None:
    l.log(l.INFO, PLUGIN_NAME, "Loading project config")
    global project_config
    if not substance_painter.project.is_open():
        return
    localConfig = substance_painter.project.Metadata("skyrim_tools")
    
    project_config = project_default.copy()
    
    for key in project_config:
        if localConfig.get(key) is not None:
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
    if value is not None:
        l.log(l.INFO, PLUGIN_NAME, "setting global option {} to {}".format(name, value))
        global_config[name] = value

def add_executable(name, path) -> None:
    global global_config
    if name is not None and path is not None:
        l.log(l.INFO, PLUGIN_NAME, "adding executable {} at {}".format(name, path))
        global_config["executables"][name] = path

def set_project_option(name, value) -> None:
    if value is not None:
        l.log(l.INFO, PLUGIN_NAME, "setting project option {} to {}".format(name, value))
        project_config[name] = value
