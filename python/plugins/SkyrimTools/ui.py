from PySide2.QtWidgets import QMenu, QFileDialog, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QCheckBox, QComboBox, QVBoxLayout, QMessageBox, QTabWidget
import SkyrimTools.configManager as ConfigManager
from PySide2.QtCore import QObject, Signal, Slot 
import substance_painter
import substance_painter.logging as l
import substance_painter.project
from SkyrimTools.constants import PLUGIN_NAME


class Settings_Dialog(QDialog):
    def __init__(self, parent=None):
        super(Settings_Dialog, self).__init__(parent)

        self.tabs = QTabWidget()

        self.tab1 = GlobalConfigTab()
        self.tabs.addTab(self.tab1,"Global Settings")
        
        if substance_painter.project.is_open():
            self.tab2 = ProjectConfigTab()
            self.tabs.addTab(self.tab2,"Project Settings")

        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()


        self.okButton = QPushButton("Save Settings")
        self.okButton.clicked.connect(self.saveSettings)
        self.buttonLayout.addWidget(self.okButton)

        #self.cancelButton = QPushButton("Cancel")
        #self.cancelButton.clicked.connect(self.cancel)
        #self.buttonLayout.addWidget(self.cancelButton)
        
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

        self.setWindowTitle("Settings")

    def cancel(self):
        self.reject()

    def saveSettings(self):
        ConfigManager.save_global_config()
        ConfigManager.save_project_config()
        self.accept()



class ProjectConfigTab(QWidget):
    def __init__(self, parent=None):
        super(ProjectConfigTab, self).__init__(parent)

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.add_path_select_option(
            name = "png export folder",
            description = "Your textures will be exported as png into this directory",
            var_name = "png_output"
        )

        self.add_path_select_option(
            name = "dds export folder",
            description = "Your textures will be converted to dds and saved into this directory",
            var_name = "dds_output"
        )

        self.add_checkbox_option(
            name = "alpha blending used",
            description = "Whether you want to use alpha blending for this texture set. (Textures without blending can be compressed even more)",
            var_name = "alpha_blending"
        )

        self.add_checkbox_option(
            name = "Glow is used",
            description = "Whether you want to use a glow map for this texture set. (Prevents glow map from being converted entirely when unchecked)",
            var_name = "glow"
        )

        self.add_checkbox_option(
            name = "Cubemap Reflections are used",
            description = "Whether you want to use cubemap stuff for this texture set. (Prevents reflection map from being converted entirely when unchecked)",
            var_name = "reflection"
        )

        self.add_checkbox_option(
            name = "Compatibility with LE required",
            description = "Whether you want to use this texture in a LE mod (Prevents comressing into the newest DXT10 (BC7) format which LE can't handle))",
            var_name = "le_compability"
        )

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

        

    def add_path_select_option(self, name: str, description: str, var_name: str):
        label = QLabel(name)
        label.setToolTip(description)
        field = FileSelectField("Select " + name, True, ConfigManager.project_config[var_name],parent = self)
        field.fileSelected.connect(lambda value: ConfigManager.set_project_option(var_name, value))
        self.layout.addRow(label, field)    

    def add_checkbox_option(self, name: str, description: str, var_name: str):
        label = QLabel(name)
        label.setToolTip(description)
        box = QCheckBox()
        box.setChecked(ConfigManager.project_config[var_name])
        box.stateChanged.connect(lambda value: ConfigManager.set_project_option(var_name, value))
        self.layout.addRow(label, box)

class GlobalConfigTab(QWidget):
    def __init__(self, parent=None):
        super(GlobalConfigTab, self).__init__(parent)



        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.add_path_select_option(
            name = "crunch_64 location",
            description = "The path of the crunch_64 executable.",
            var_name = "crunch_location"
        )

        self.add_path_select_option(
            name = "NVTT location (if available)",
            description = "The path of the Nvidia Texture Tools folder. This is only required if you want to use BS7 compression. If nothing is set here it will fall back to crunch compression",
            var_name = "nvtt_location"
        )

        self.add_checkbox_option(
            name = "Hide Terminal Windows",
            description = "By default Terminal Windows will open when textures are converted and close when everything has finished. You can hide them but then you won't be sure when the processes have finished their work",
            var_name = "hide_terminal"
        )

        self.add_text_select_option(
            name = "Diffuse texture suffix",
            description = "The suffix that the exported diffuse texture will have",
            var_name = "diffuse_suffix"
        )

        self.add_text_select_option(
            name = "Normal texture suffix",
            description = "The suffix that the exported normal texture will have",
            var_name = "normal_suffix"
        )

        self.add_text_select_option(
            name = "Glow texture suffix",
            description = "The suffix that the exported glow texture will have",
            var_name = "glow_suffix"
        )

        self.add_text_select_option(
            name = "Reflective texture suffix",
            description = "The suffix that the exported reflective texture will have",
            var_name = "reflective_suffix"
        )

    def add_path_select_option(self, name: str, description: str, var_name: str):
        label = QLabel(name)
        label.setToolTip(description)
        field = FileSelectField("Select " + name, False, ConfigManager.global_config[var_name],parent = self)
        field.fileSelected.connect(lambda value: ConfigManager.set_global_option(var_name, value))
        self.layout.addRow(label, field)    

    def add_checkbox_option(self, name: str, description: str, var_name: str):
        label = QLabel(name)
        label.setToolTip(description)
        box = QCheckBox()
        box.setChecked(ConfigManager.global_config[var_name])
        box.stateChanged.connect(lambda value: ConfigManager.set_global_option(var_name, value))
        self.layout.addRow(label, box)

    def add_text_select_option(self, name: str, description: str, var_name: str):
        label = QLabel(name)
        label.setToolTip(description)
        textBox = QLineEdit()
        textBox.setText(ConfigManager.global_config[var_name])
        textBox.editingFinished.connect(lambda: ConfigManager.set_global_option(var_name, textBox.text()))
        self.layout.addRow(label, textBox)


class FileSelectField(QWidget):

    fileSelected = Signal(str)

    def __init__(self, caption: str, dir_select: bool, default = "", parent = None):
        super(FileSelectField, self).__init__(parent)

        self.caption = caption
        self.dir_select = dir_select

        self.textBox = QLineEdit()
        self.textBox.setText(default)
        self.textBox.editingFinished.connect(lambda: self.fileSelected.emit(self.textBox.text()))
        self.browseButton = QPushButton("browse")
        self.browseButton.clicked.connect(self.selectFile)

        layout = QHBoxLayout(self)
        layout.addWidget(self.textBox)
        layout.addWidget(self.browseButton)

    def selectFile(self):
        if self.dir_select:
            file = QFileDialog.getExistingDirectory(parent=None, caption=self.caption, dir=self.textBox.text())
        else: 
            file,_ = QFileDialog.getOpenFileName(parent=None, caption=self.caption, dir=self.textBox.text())
        l.log(l.INFO,PLUGIN_NAME, "Selected file: " + str(file))
        if file:
            self.fileSelected.emit(file)
            self.textBox.setText(file)

    def text(self):
        return self.textBox.text()