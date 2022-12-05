from PySide2.QtWidgets import QMenu, QFileDialog, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QCheckBox, QComboBox, QVBoxLayout, QMessageBox, QTabWidget
from SkyrimTools.configManager import Config
from PySide2.QtCore import QObject, Signal, Slot 
import substance_painter
import substance_painter.logging as l
from SkyrimTools.constants import PLUGIN_NAME


class Settings_Dialog(QDialog):
    def __init__(self, config: Config, parent=None):
        super(Settings_Dialog, self).__init__(parent)

        self.config = config
        self.tabs = QTabWidget()

        self.tab1 = GlobalConfigTab(config)
        self.tabs.addTab(self.tab1,"Global Settings")
        
        if substance_painter.project.is_open():
            self.tab2 = LocalConfigTab(config)
            self.tabs.addTab(self.tab2,"Project Settings")

        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()


        self.okButton = QPushButton("Save Settings")
        self.okButton.clicked.connect(self.saveSettings)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancel)
        
        self.buttonLayout.addWidget(self.okButton)
        self.buttonLayout.addWidget(self.cancelButton)
        
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

        self.setWindowTitle("Settings")

    def cancel(self):
        self.reject()

    def saveSettings(self):
        self.config.saveSettings()
        self.accept()

class FileSelectField(QWidget):

    fileSelected = Signal(str)

    def __init__(self, default = "", parent = None):
        super(FileSelectField, self).__init__(parent)

        self.textBox = QLineEdit()
        self.textBox.setText(default)
        self.browseButton = QPushButton("browse")
        self.browseButton.clicked.connect(self.selectFile)

        layout = QHBoxLayout(self)
        layout.addWidget(self.textBox)
        layout.addWidget(self.browseButton)

    def selectFile(self):
        file = QFileDialog.getExistingDirectory(parent=None, caption='Select Directory', dir=self.textBox.text())
        self.fileSelected.emit(file)
        self.textBox.setText(file)

    def text(self):
        return self.textBox.text()

class LocalConfigTab(QWidget):
    def __init__(self, config: Config, parent=None):
        super(LocalConfigTab, self).__init__(parent)

        self.config = config
        self.pngExportLabel = QLabel("png export folder")
        self.pngExportLabel.setToolTip("Your textures will be exported as png into this directory")
        self.pngExportField = FileSelectField(default = config.png_output,parent = self)
        self.pngExportField.fileSelected.connect(config.set_png_output)

        self.ddsExportLabel = QLabel("dds export folder")
        self.ddsExportLabel.setToolTip("Your textures will be converted to dds and saved into this directory")
        self.ddsExportField = FileSelectField(default = config.dds_output, parent = self)
        self.ddsExportField.fileSelected.connect(config.set_dds_output)

        self.alphaBlendingLabel = QLabel("Apha Blending is used")
        self.alphaBlendingLabel.setToolTip("Whether you want to use alpha blending for this texture set. (Textures without blending can be compressed even more)")
        self.alphaBlendingBox = QCheckBox()
        self.alphaBlendingBox.setChecked(config.alpha_blending)
        self.alphaBlendingBox.clicked.connect(config.set_alpha_blending)

        self.glowLabel = QLabel("Glow is used")
        self.glowLabel.setToolTip("Whether you want to use a glow map for this texture set. (Prevents glow map from being converted entirely when unchecked)")
        self.glowBox = QCheckBox()
        self.glowBox.setChecked(config.glow)
        self.glowBox.clicked.connect(config.set_glow)

        self.reflectionLabel = QLabel("Cubemap Reflections are used")
        self.reflectionLabel.setToolTip("Whether you want to use cubemap stuff for this texture set. (Prevents reflection map from being converted entirely when unchecked)")
        self.reflectionBox = QCheckBox()
        self.reflectionBox.setChecked(config.reflection)
        self.reflectionBox.clicked.connect(config.set_reflection)

        self.leCompabilityLabel = QLabel("Compatibility with LE required")
        self.leCompabilityLabel.setToolTip("Whether you want to use this texture in a LE mod (Prevents comressing into the newest DXT10 (BC7) format which LE can't handle))")
        self.leCompabilityBox = QCheckBox()
        self.leCompabilityBox.setChecked(config.le_compability)
        self.leCompabilityBox.clicked.connect(config.set_le_compability)

        # self.qualityOptions = ["fast", "good"]
        # self.qualityLabel = QLabel("Compression Quality")
        # self.qualityLabel.setToolTip("Fast option is fast and nice when you are still working on the textures. Good is only recommended for you final release to squeeze out tha last bit of quality and can take a !LONG! time")
        # self.qualityBox = QComboBox()
        # self.qualityBox.insertItems(0,self.qualityOptions)
        # default = default = config.quality
        # if not default:
        #     default = "good"
        # else:
        #     default = str(default)
        # self.qualityBox.setCurrentIndex(self.qualityOptions.index(default))

        self.layout = QFormLayout()

        self.layout.addRow(self.pngExportLabel, self.pngExportField)
        self.layout.addRow(self.ddsExportLabel, self.ddsExportField)
        self.layout.addRow(self.alphaBlendingLabel, self.alphaBlendingBox)
        self.layout.addRow(self.glowLabel, self.glowBox)
        self.layout.addRow(self.reflectionLabel, self.reflectionBox)
        self.layout.addRow(self.leCompabilityLabel, self.leCompabilityBox)

        self.setLayout(self.layout)

class GlobalConfigTab(QWidget):
    def __init__(self, config: Config, parent=None):
        super(GlobalConfigTab, self).__init__(parent)

        self.config = config

        self.nvttLabel = QLabel("NVTT location (if available)")
        self.nvttLabel.setToolTip("The path of the Nvidia Texture Tools folder. This is only required if you want to use BS7 compression. If nothing is set here it will fall back to crunch compression")

        self.nvttField = FileSelectField(default = config.nvtt_location, parent = self)
        self.nvttField.fileSelected.connect(config.set_nvtt_location)

        self.hideTerminalWindowsLabel = QLabel("Hide Terminal Windows")
        self.hideTerminalWindowsLabel.setToolTip("By default Terminal Windows will open when textures are converted and close when everything has finished. You can hide them but then you won't be sure when the processes have finished their work")
        self.hideTerminalWindowsBox = QCheckBox()
        self.hideTerminalWindowsBox.setChecked(config.hide_terminal)
        self.hideTerminalWindowsBox.clicked.connect(config.set_hide_terminal)

        self.layout = QFormLayout()

        self.layout.addRow(self.nvttLabel, self.nvttField)
        self.layout.addRow(self.hideTerminalWindowsLabel, self.hideTerminalWindowsBox)

        self.setLayout(self.layout)