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
import substance_painter.export
import substance_painter.resource
import substance_painter
import substance_painter_plugins
from PySide2.QtWidgets import QMenu, QFileDialog, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QCheckBox, QComboBox, QVBoxLayout, QMessageBox
import substance_painter.ui
from subprocess import Popen, PIPE, CREATE_NO_WINDOW
import SkyrimTools.ui  as ui
import SkyrimTools.exporter as exporter
import SkyrimTools.configManager as configManager
import SkyrimTools.crunchConverter as crunchConverter
import SkyrimTools.nvidiaConverter as nvidiaConverter
import SkyrimTools.logger as logger

plugin_widgets = []
pluginDirPath = None
config: configManager.Config = None
export_one_menu = None



def start_plugin():
    """This method is called when the plugin is started."""
    global l 
    global config
    l = logger.INSTANCE()
    l.setMode("DEBUG")
    l.setPrefix("[SkyrimTools] ")
    setPluginPath()
    config = configManager.Config(pluginDirPath)
    config.loadSettings()
    l.setMode(config.logging_level)

    substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectOpened, onProjectOpened)
    substance_painter.event.DISPATCHER.connect(substance_painter.event.ProjectCreated, onProjectOpened)
    setupMenu()

def onProjectOpened(e):
    l.logDebug("Project Opened")
    config.loadSettings()
    removeAllActions(export_one_menu)
    for tset in substance_painter.textureset.all_texture_sets():
        export_one_menu.addAction(tset.name(),lambda n = tset: exportAndConvertTextureSet(n), "member")

def removeAllActions(menu: QMenu):
    for action in menu.actions():
        menu.removeAction(action)

def setPluginPath():
    global pluginDirPath
    for p in substance_painter_plugins.path:
        path = p + "/plugins/SkyrimTools"
        if os.path.isdir(path):
            pluginDirPath = path
            l.logInfo("Plugin Directory set to {}".format(path))
            return        
    if not pluginDirPath:
        l.logError("Plugin Directory not found! Can't activate plugin")
        close_plugin()
        return

def setupMenu():
    global export_one_menu
    l.logDebug("Setup Menu")
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
    l.logDebug("Disabling Plugin")
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    plugin_widgets.clear()


def exportAndConvert():
    if not isExportValid():
        return

    exporter.export(config)
    if config.nvtt_location and config.nvtt_location != "":
        converter = nvidiaConverter.NvidiaConverter()
    else:
        converter = crunchConverter.CrunchConverter()
    converter.convert(config)

def exportAndConvertTextureSet(textureSet):
    if not isExportValid():
        return
    exporter.exportTextureSet(config, textureSet)
    if config.nvtt_location and config.nvtt_location != "":
        converter = nvidiaConverter.NvidiaConverter()
    else:
        converter = crunchConverter.CrunchConverter()
    converter.convertTextureSet(config, textureSet)

def isExportValid():
    if not substance_painter.project.is_open():
        l.logError("No project to export")
        return False
    if (not config.png_output) or (not config.dds_output):
        l.logError("You need to set the png and dds output paths before you can export")
        return False
    return True

def show_settings_dialog():
    l.logDebug("Show Settings")
    ui.Settings_Dialog(config, parent = plugin_widgets[0]).show()
    

if __name__ == "__main__":
    start_plugin()