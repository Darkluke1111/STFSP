#    Substance Painter plugin to export texture sets in dds format for Skyrim
#    Copyright (C) 2022  Darkluke1111 (https://www.nexusmods.com/users/8086919)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from asyncio.log import logger
import json
import os
import SkyrimTools.amdCompressonatorConverter as amdCompressonatorConverter
import substance_painter.export
import substance_painter.resource
import substance_painter
import substance_painter_plugins
from PySide2.QtWidgets import QMenu, QFileDialog, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QCheckBox, QComboBox, QVBoxLayout, QMessageBox
import substance_painter.ui
import substance_painter.logging as l
from subprocess import Popen, PIPE, CREATE_NO_WINDOW
import SkyrimTools.ui  as ui
import SkyrimTools.exporter as exporter
import SkyrimTools.configManager as ConfigManager
import SkyrimTools.crunchConverter as crunchConverter
import SkyrimTools.nvidiaConverter as nvidiaConverter
import SkyrimTools.texconvConverter as texconvConverter
from SkyrimTools.constants import PLUGIN_NAME


plugin_widgets = []
pluginDirPath = None
export_one_menu = None

converters = [amdCompressonatorConverter.AmdCompressonatorConverter(), crunchConverter.CrunchConverter(), nvidiaConverter.NvidiaConverter(), texconvConverter.TexConvConverter()]

def start_plugin():
    setPluginPath()
    ConfigManager.init(pluginDirPath)

    substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectOpened, onProjectOpened)
    substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectCreated, onProjectOpened)
    setupMenu()

    if substance_painter.project.is_open():
        onProjectOpened(None)

def close_plugin():
    substance_painter.event.DISPATCHER.disconnect(substance_painter.event.ProjectOpened, onProjectOpened)
    substance_painter.event.DISPATCHER.disconnect(substance_painter.event.ProjectCreated, onProjectOpened)

def onProjectOpened(e):
    l.log(l.INFO,PLUGIN_NAME, "Project Opened")
    removeAllActions(export_one_menu)
    for tset in substance_painter.textureset.all_texture_sets():
        export_one_menu.addAction(tset.name(),lambda n = tset: exportAndConvertTextureSet(n), "member")

def removeAllActions(menu: QMenu):
    #Quick and dirty way to prevent a Qt related error message (which is harmless as far as I know) from showing up. There is probably a better way but this works for now...
    try:
        for action in menu.actions():
            menu.removeAction(action)
    except RuntimeError:
        pass

def setPluginPath():
    global pluginDirPath
    for p in substance_painter_plugins.path:
        path = p + "/plugins/SkyrimTools"
        if os.path.isdir(path):
            pluginDirPath = path
            l.log(l.INFO,PLUGIN_NAME, "Plugin Directory set to {}".format(path))

            return        
    if not pluginDirPath:
        l.log(l.ERROR, PLUGIN_NAME, "Plugin Directory not found! Can't activate plugin")
        close_plugin()
        return

def setupMenu():
    global export_one_menu
    l.log(l.INFO, PLUGIN_NAME, "Setup Menu")
    export_widget = QMenu()
    export_widget.setTitle("Skyrim")
    export_widget.addAction("Export All", exportAndConvert, "member")
    export_one_menu = export_widget.addMenu("Export One")
    export_widget.addAction("Settings", show_settings_dialog , "member")
    # Add this widget as a dock to the interface
    substance_painter.ui.add_menu(export_widget)
    # Store added widget for proper cleanup when stopping the plugin
    plugin_widgets.append(export_widget)


def close_plugin():
    l.log(l.INFO, PLUGIN_NAME, "Disabling Plugin")
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    plugin_widgets.clear()


def exportAndConvert():
    for tset in substance_painter.textureset.all_texture_sets():
        exportAndConvertTextureSet(tset)

def exportAndConvertTextureSet(textureSet):
    if not isExportValid():
        return
    exporter.exportTextureSet(textureSet)

    compression_tool = ConfigManager.global_config["compression_tool"]

    for converter in converters:
        if converter.getName() == compression_tool:
            converter.convertTextureSet(textureSet)
    

def isExportValid():
    if not substance_painter.project.is_open():
        l.log(l.ERROR, PLUGIN_NAME, "No project to export")
        return False

    if not ("png_output" in ConfigManager.project_config.keys()  and "dds_output" in ConfigManager.project_config.keys()):
        l.log(l.ERROR, PLUGIN_NAME, "You need to set the png and dds output paths before you can export")
        return False
    return True

def show_settings_dialog():
    l.log(l.INFO, PLUGIN_NAME, "Show Settings")
    ui.Settings_Dialog(parent = plugin_widgets[0]).show()
    

if __name__ == "__main__":
    start_plugin()