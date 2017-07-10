import os, sys, shutil, stat
import tkinter as tk
import tkFileDialog
from functools import partial
import json
#import collections
import subprocess
from PyQt4 import QtGui as qg
from PyQt4 import QtCore as qc

class Main(qg.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.initUI()

    def initUI(self):

        #window title
        self.setWindowTitle("PMT")

        #global variable 
        self.projectsLocation = "C:\\Projects"

        #main widget
        self.centralWidget = qg.QWidget()
        self.centralWidget.setLayout(qg.QVBoxLayout())

        #widget for project name label and combobox
        self.projectWidget = qg.QWidget()
        self.projectWidget.setLayout(qg.QHBoxLayout())

        projectName_lbl = qg.QLabel("Current Studio Projects:")
        addProject = qg.QPushButton("+")
        removeProject = qg.QPushButton("x")

        width = addProject.fontMetrics().boundingRect("+").width() + 10
        addProject.setMaximumWidth(width)
        removeProject.setMaximumWidth(width)

        self.project_comboBox = qg.QComboBox()

        self.projectWidget.layout().layout().addWidget(projectName_lbl)
        self.projectWidget.layout().layout().addWidget(self.project_comboBox)
        self.projectWidget.layout().layout().addWidget(addProject)
        self.projectWidget.layout().layout().addWidget(removeProject)

        #tab widget to contain all the subset tools 
        self.softwareLaunch_tab_widget = qg.QWidget()
        self.softwareLaunch_tab_widget.setLayout(qg.QHBoxLayout())

        #art source widget
        self.sourceDirectory_widget = qg.QWidget()
        self.sourceDirectory_widget.setLayout(qg.QVBoxLayout())
        
        self.projectAssets_lbl = qg.QLabel("Available Assets")
        self.projectAssets_lbl.setAlignment(qc.Qt.AlignCenter)

        sourceAsset_ComboBox_widget = qg.QWidget()
        sourceAsset_ComboBox_widget.setLayout(qg.QHBoxLayout())       

        typeOfSourceAsset_widget = qg.QWidget()
        typeOfSourceAsset_widget.setLayout(qg.QVBoxLayout())

        typeOfSourceAsset_lbl = qg.QLabel("Asset Type:")
        typeOfSourceAsset_lbl.setAlignment(qc.Qt.AlignCenter)

        #comboBox to serve as drop down of the type of asset "character or environment"
        self.typeOfSourceAsset_comboBox = qg.QComboBox()      

        whichSourceAsset_widget = qg.QWidget()
        whichSourceAsset_widget.setLayout(qg.QVBoxLayout())

        whichSourceAsset_lbl = qg.QLabel("Asset Name:")
        whichSourceAsset_lbl.setAlignment(qc.Qt.AlignCenter)
        
        #comboBox to serve as drop down of the asset list for the type of asset
        self.whichSourceAsset_comboBox = qg.QComboBox()

        sourceAssetSoftware_widget = qg.QWidget()
        sourceAssetSoftware_widget.setLayout(qg.QVBoxLayout())

        sourceAssetSoftware_lbl = qg.QLabel("Software:")
        sourceAssetSoftware_lbl.setAlignment(qc.Qt.AlignCenter)
        
        #comboBox to serve as drop down of the asset list for the type of asset
        self.sourceAssetSoftware_comboBox = qg.QComboBox()

        listSourceAsset_widget = qg.QWidget()
        listSourceAsset_widget.setLayout(qg.QVBoxLayout())

        listSourceAsset_lbl = qg.QLabel("Available Assets:")
        listSourceAsset_lbl.setAlignment(qc.Qt.AlignCenter)
        
        #comboBox to serve as drop down of the asset list for the type of asset
        self.listSourceAsset_comboBox = qg.QComboBox()

        typeOfSourceAsset_widget.layout().addWidget(typeOfSourceAsset_lbl)
        typeOfSourceAsset_widget.layout().addWidget(self.typeOfSourceAsset_comboBox)

        whichSourceAsset_widget.layout().addWidget(whichSourceAsset_lbl)
        whichSourceAsset_widget.layout().addWidget(self.whichSourceAsset_comboBox)

        sourceAssetSoftware_widget.layout().addWidget(sourceAssetSoftware_lbl)
        sourceAssetSoftware_widget.layout().addWidget(self.sourceAssetSoftware_comboBox)

        listSourceAsset_widget.layout().addWidget(listSourceAsset_lbl)
        listSourceAsset_widget.layout().addWidget(self.listSourceAsset_comboBox)

        #button to open asset
        self.openSourceAsset_bttn = qg.QPushButton("Open Asset")

        sourceAsset_ComboBox_widget.layout().addWidget(typeOfSourceAsset_widget)
        sourceAsset_ComboBox_widget.layout().addWidget(whichSourceAsset_widget)
        sourceAsset_ComboBox_widget.layout().addWidget(sourceAssetSoftware_widget)        
        sourceAsset_ComboBox_widget.layout().addWidget(listSourceAsset_widget)      
        sourceAsset_ComboBox_widget.layout().addWidget(self.openSourceAsset_bttn)

        #seperator line between asset comboboxes and the action buttons
        sourceAsset_Seperator = qg.QFrame()
        sourceAsset_Seperator.setFrameShape(qg.QFrame.HLine)
        sourceAsset_Seperator.setFrameShadow(qg.QFrame.Sunken) 

        #tab widget to split up asset action buttons which is child to self.softwareLaunch_tab_widget
        self.assetActionsTabs_widget = qg.QTabWidget()
        self.assetActionsTabs_widget.addTab(sourceAssetButton_widget, "Asset Actions")
        self.assetActionsTabs_widget.addTab(sourceFolderButton_widget, "Asset Folder Actions")  

        sourceAssetButton_widget = qg.QWidget()
        sourceAssetButton_widget.setLayout(qg.QHBoxLayout())

        self.addNewAsset_bttn = qg.QPushButton("Add New Asset")
        self.deleteAsset_bttn = qg.QPushButton("Delete Asset")
        self.renameAsset_bttn = qg.QPushButton("Rename Asset")

        sourceAssetButton_widget.layout().addWidget(self.addNewAsset_bttn)
        sourceAssetButton_widget.layout().addWidget(self.deleteAsset_bttn)
        sourceAssetButton_widget.layout().addWidget(self.renameAsset_bttn)

        sourceFolderButton_widget = qg.QWidget()
        sourceFolderButton_widget.setLayout(qg.QHBoxLayout())

        self.openSourceAssetFolder_bttn = qg.QPushButton("Open Asset Folder")        
        self.openSoftwareFolder_bttn = qg.QPushButton("Open Software Folder")
        self.copySourceAssetPath_bttn = qg.QPushButton("Copy Asset Path")

        sourceFolderButton_widget.layout().addWidget(self.openSourceAssetFolder_bttn)
        sourceFolderButton_widget.layout().addWidget(self.openSoftwareFolder_bttn)
        sourceFolderButton_widget.layout().addWidget(self.copySourceAssetPath_bttn)

        #self.sourceDirectory_widget.layout().addWidget(self.projectAssets_lbl)
        self.sourceDirectory_widget.layout().addWidget(sourceAsset_ComboBox_widget)
        self.sourceDirectory_widget.layout().addWidget(sourceAsset_Seperator)
        self.sourceDirectory_widget.layout().addWidget(self.assetActionsTabs_widget)

        #widget for art export assets
        self.exportDirectory_widget = qg.QWidget()
        self.exportDirectory_widget.setLayout(qg.QVBoxLayout())

        exportAsset_ComboBox_widget = qg.QWidget()
        exportAsset_ComboBox_widget.setLayout(qg.QHBoxLayout()) 

        typeOfExportAsset_widget = qg.QWidget()
        typeOfExportAsset_widget.setLayout(qg.QVBoxLayout())

        typeOfExportAsset_lbl = qg.QLabel("Asset Type:")
        typeOfExportAsset_lbl.setAlignment(qc.Qt.AlignCenter)

        #comboBox to serve as drop down of the type of asset "character or environment"
        self.typeOfExportAsset_comboBox = qg.QComboBox()      

        whichExportAsset_widget = qg.QWidget()
        whichExportAsset_widget.setLayout(qg.QVBoxLayout())

        whichExportAsset_lbl = qg.QLabel("Asset Name:")
        whichExportAsset_lbl.setAlignment(qc.Qt.AlignCenter)
        
        #comboBox to serve as drop down of the asset list for the type of asset
        self.whichExportAsset_comboBox = qg.QComboBox()

        assetExportTypes_widget = qg.QWidget()
        assetExportTypes_widget.setLayout(qg.QVBoxLayout())

        assetExportTypes_lbl = qg.QLabel("Export Types:")
        assetExportTypes_lbl.setAlignment(qc.Qt.AlignCenter)

        self.assetExportTypes_comboBox = qg.QComboBox()

        listExportAsset_widget = qg.QWidget()
        listExportAsset_widget.setLayout(qg.QVBoxLayout())

        listExportAsset_lbl = qg.QLabel("Available Assets:")
        listExportAsset_lbl.setAlignment(qc.Qt.AlignCenter)
        
        #comboBox to serve as drop down of the asset list for the type of asset
        self.listExportAsset_comboBox = qg.QComboBox()

        typeOfExportAsset_widget.layout().addWidget(typeOfExportAsset_lbl)
        typeOfExportAsset_widget.layout().addWidget(self.typeOfExportAsset_comboBox)

        whichExportAsset_widget.layout().addWidget(whichExportAsset_lbl)
        whichExportAsset_widget.layout().addWidget(self.whichExportAsset_comboBox)

        assetExportTypes_widget.layout().addWidget(assetExportTypes_lbl)
        assetExportTypes_widget.layout().addWidget(self.assetExportTypes_comboBox)

        #listExportAsset_widget.layout().addWidget(listExportAsset_lbl)
        #listExportAsset_widget.layout().addWidget(self.listExportAsset_comboBox)

        exportAsset_ComboBox_widget.layout().addWidget(typeOfExportAsset_widget)
        exportAsset_ComboBox_widget.layout().addWidget(whichExportAsset_widget)
        exportAsset_ComboBox_widget.layout().addWidget(assetExportTypes_widget)        
        #exportAsset_ComboBox_widget.layout().addWidget(listExportAsset_widget)

        #seperator line between asset comboboxes and the action buttons
        exportAsset_Seperator = qg.QFrame()
        exportAsset_Seperator.setFrameShape(qg.QFrame.HLine)
        exportAsset_Seperator.setFrameShadow(qg.QFrame.Sunken)

        #tab widget to seperate art exports buttons
        self.toolTabs_widget = qg.QTabWidget()
        self.toolTabs_widget.addTab(self.softwareLaunch_tab_widget, "Project Software")
        self.toolTabs_widget.addTab(self.sourceDirectory_widget, "Project Source Assets")        
        self.toolTabs_widget.addTab(self.exportDirectory_widget, "Project Export Assets")  

        exportFolderButton_widget = qg.QWidget()
        exportFolderButton_widget.setLayout(qg.QHBoxLayout())

        self.openExportAssetFolder_bttn = qg.QPushButton("Open Asset Folder")        
        self.openExportExportTypesFolder_bttn = qg.QPushButton("Open Export Types Folder")        
        self.copyExportAssetPath_bttn = qg.QPushButton("Copy Asset Path")

        exportFolderButton_widget.layout().addWidget(self.openExportAssetFolder_bttn)
        exportFolderButton_widget.layout().addWidget(self.openExportExportTypesFolder_bttn)
        exportFolderButton_widget.layout().addWidget(self.copyExportAssetPath_bttn)

        self.exportDirectory_widget.layout().addWidget(exportAsset_ComboBox_widget)
        self.exportDirectory_widget.layout().addWidget(exportAsset_Seperator)
        self.exportDirectory_widget.layout().addWidget(exportFolderButton_widget)


        #adds project widget and tools widget to central widget
        self.centralWidget.layout().addWidget(self.projectWidget)
        self.centralWidget.layout().addWidget(self.toolTabs_widget)

        self.setCentralWidget(self.centralWidget)

        #intilizes tool
        self.fillProjectComboBox(self.project_comboBox, self.projectsLocation)
        
        #fills comboboxes if projects exist
        if self.project_comboBox.currentText() != "":
            currentJSON = "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Tools" + "\\" + "config.json"
            JSON = self.loadJSONConfig(currentJSON)
            self.loadSoftware(JSON, self.softwareLaunch_tab_widget, softwareButton)

            self.fillComboBox(self.typeOfSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source")
            self.fillComboBox(self.whichSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.itemText(self.typeOfSourceAsset_comboBox.currentIndex()))
            self.fillComboBox(self.sourceAssetSoftware_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.itemText(self.whichSourceAsset_comboBox.currentIndex()))            
            self.fillComboBox(self.listSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText() + "\\" + self.sourceAssetSoftware_comboBox.itemText(self.sourceAssetSoftware_comboBox.currentIndex()))
            
            self.fillComboBox(self.typeOfExportAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports")
            self.fillComboBox(self.whichExportAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.itemText(self.typeOfExportAsset_comboBox.currentIndex()))
            self.fillComboBox(self.assetExportTypes_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.itemText(self.whichExportAsset_comboBox.currentIndex()))            
            #self.fillComboBox(self.listExportAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.currentText() + "\\" + self.assetExportTypes_comboBox.itemText(self.assetExportTypes_comboBox.currentIndex()))
        

        #add and remove projects functionality calls
        addProject.clicked.connect(lambda: self.createProject())
        removeProject.clicked.connect(lambda: self.deleteProject())

        #index 0 of art source tab widget functionality calls
        self.addNewAsset_bttn.clicked.connect(lambda: self.createDirForNewAsset())
        self.openSourceAsset_bttn.clicked.connect(lambda: self.openSourceAsset())
        self.deleteAsset_bttn.clicked.connect(lambda: self.deleteAssetDir())
        self.renameAsset_bttn.clicked.connect(lambda: self.renameAsset(str("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText())))

        #index 1 of art source tab widget functionality calls
        self.openSourceAssetFolder_bttn.clicked.connect(lambda: self.openExplorerWindow("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText()))
        self.openSoftwareFolder_bttn.clicked.connect(lambda: self.openExplorerWindow("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText() + "\\" + self.sourceAssetSoftware_comboBox.currentText()))
        self.copySourceAssetPath_bttn.clicked.connect(lambda: self.copyAssetPath("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText() + "\\" + self.sourceAssetSoftware_comboBox.currentText()))

        #index 0 of art exports tab widget functionality calls
        self.openExportAssetFolder_bttn.clicked.connect(lambda: self.openExplorerWindow("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.currentText()))
        self.openExportExportTypesFolder_bttn.clicked.connect(lambda: self.openExplorerWindow("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.currentText() + "\\" + self.assetExportTypes_comboBox.currentText()))
        self.copyExportAssetPath_bttn.clicked.connect(lambda: self.copyAssetPath("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.currentText() + "\\" + self.assetExportTypes_comboBox.currentText()))

        #if project combobox index changes functionality calls
        self.project_comboBox.currentIndexChanged.connect(lambda: self.reloadLaunchSoftware(self.softwareLaunch_tab_widget))
        self.project_comboBox.currentIndexChanged.connect(lambda: self.reloadAssets())

        #if art source combobox index changes functionality calls
        self.typeOfSourceAsset_comboBox.currentIndexChanged.connect(self.fillWhichSourceAssetComboBox)
        self.whichSourceAsset_comboBox.currentIndexChanged.connect(self.fillsourceAssetSoftwareComboBox)
        self.sourceAssetSoftware_comboBox.currentIndexChanged.connect(self.fillListSourceAssetComboBox)

        #if art exports combobox index changes functionality calls
        self.typeOfExportAsset_comboBox.currentIndexChanged.connect(self.fillWhichExportAssetComboBox)
        self.whichExportAsset_comboBox.currentIndexChanged.connect(self.fillExportAssetExportTypesComboBox)
        self.listExportAsset_comboBox.currentIndexChanged.connect(self.fillListExportAssetComboBox)

    #function to open a windows explorer window
    def openExplorerWindow(self, path):
        
        if self.osPath(path):
            os.startfile(path)
        else:
            self.popupOkWindow("ASSET DOESN'T EXIST")

    #adds current asset path to clipboard
    def copyAssetPath(self, path):
        root = tk.Tk()
        # keep the window from showing
        
        root.clipboard_clear()
        # text to clipboard
        root.clipboard_append(path)
        self.popupOkWindow(path + "\n" + "was copied to your clipboard")

    #function to populate combobox with new itmes based on index selection
    def fillListExportAssetComboBox(self, index):
        
        #string for the object based on file path
        selection = "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.currentText() + "\\" + self.assetExportTypes_comboBox.itemText(index)
        
        if self.assetExportTypes_comboBox:
            self.listExportAsset_comboBox.clear()

        self.fillComboBox(self.listExportAsset_comboBox, selection)

    #function to populate combobox with new itmes based on index selection
    def fillExportAssetExportTypesComboBox(self, index):
        
        #string for the object based on file path
        selection = "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.itemText(index)
        
        if self.whichExportAsset_comboBox:
            self.assetExportTypes_comboBox.clear()
            self.listExportAsset_comboBox.clear()

        self.fillComboBox(self.assetExportTypes_comboBox, selection)

    #function to populate combobox with new itmes based on index selection
    def fillWhichExportAssetComboBox(self, index):
        
        #string for the object based on file path
        selection = "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.itemText(index)
                    
        if self.typeOfExportAsset_comboBox:
            self.whichExportAsset_comboBox.clear()
            self.assetExportTypes_comboBox.clear()
            self.listExportAsset_comboBox.clear()

        self.fillComboBox(self.whichExportAsset_comboBox, selection)

    #function to populate combobox with new itmes based on index selection
    def fillListSourceAssetComboBox(self, index):
        
        #string for the object based on file path
        selection = "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText() + "\\" + self.sourceAssetSoftware_comboBox.itemText(index)
        
        if self.sourceAssetSoftware_comboBox:
            self.listSourceAsset_comboBox.clear()

        self.fillComboBox(self.listSourceAsset_comboBox, selection)

    #function to populate combobox with new itmes based on index selection
    def fillsourceAssetSoftwareComboBox(self, index):
        
        #string for the object based on file path
        selection = "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.itemText(index)
        
        if self.whichSourceAsset_comboBox:
            self.sourceAssetSoftware_comboBox.clear()
            self.listSourceAsset_comboBox.clear()

        self.fillComboBox(self.sourceAssetSoftware_comboBox, selection)

    #function to populate combobox with new itmes based on index selection
    def fillWhichSourceAssetComboBox(self, index):
        
        #string for the object based on file path
        selection = "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.itemText(index)
                    
        if self.typeOfSourceAsset_comboBox:
            self.whichSourceAsset_comboBox.clear()
            self.sourceAssetSoftware_comboBox.clear()
            self.listSourceAsset_comboBox.clear()

        self.fillComboBox(self.whichSourceAsset_comboBox, selection)

    #function to open source asset based on designated program folder
    def openSourceAsset(self):
        
        if self.listSourceAsset_comboBox.currentText() != "":

            currentJSON = str("C:\Projects\\" + self.project_comboBox.currentText() + "\\" + "Tools" + "\\" + "config.json")
            jsonData = self.loadJSONConfig(currentJSON)

            assetToOpen = str("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText() + "\\" + self.sourceAssetSoftware_comboBox.currentText() + "\\" + self.listSourceAsset_comboBox.currentText())
            #print assetToOpen
            #subprocess.call([jsonData["DCC"][str(self.sourceAssetSoftware_comboBox.currentText())]["Exe"], assetToOpen])
            os.startfile(assetToOpen)
        else:
            self.popupOkWindow("No Asset Selected or Available")

    #loads the JSON file that the project tool references
    def loadJSONConfig(self, configFile="C:\\Projects\\Tools\\config.json"):
        configData = json.loads(self.readConfigFile(configFile))
        
        return configData

    #based on available software in the JSON file, the function will populate buttons into widget   
    def loadSoftware(self, jsonData, destinationWidget, classType):
        
        #this function serves a dual purpose to populate the software buttons and software checkboxes and determines that based on incoming parameter
        if classType is softwareButton:
            for x in jsonData["DCC"]:
                destinationWidget.layout().addWidget(softwareButton(str(jsonData["DCC"][x]["Icon"]), str(jsonData["DCC"][x]["Exe"]), str(x)))

        elif classType is softwareCheckBoxes:
            for x in jsonData["DCC"]:
                softwareNameVer = x + " " + str(jsonData["DCC"][x]["Version"])
                destinationWidget.layout().addWidget(softwareCheckBoxes(str(jsonData["DCC"][x]["Icon"]), softwareNameVer, str(x)))

    #if project combobox index were to change to repopulate list of available software
    def reloadLaunchSoftware(self, destinationWidget):
        
        currentJSON = "C:\Projects\\" + self.project_comboBox.currentText() + "\\" + "Tools" + "\\" + "config.json"
        jsonData = self.loadJSONConfig(currentJSON)

        #precuationary step to clear out current list of available software to make room for new list of software
        if len(destinationWidget.findChildren(qg.QPushButton)) > 0:

            for i in reversed(range(destinationWidget.layout().count())):                
                destinationWidget.layout().itemAt(i).widget().deleteLater()
                destinationWidget.layout().itemAt(i).widget().setParent(None)

        #loads new list of software
        for x in jsonData["DCC"]:
            destinationWidget.layout().addWidget(softwareButton(str(jsonData["DCC"][x]["Icon"]), str(jsonData["DCC"][x]["Exe"]), str(x)))

    #if project combobox changes, asset lists would be reloaded based on the project
    def reloadAssets(self):

        if str(self.project_comboBox.currentText()) == "":
            return
        else:
            
            #clears combobxes so they can be refilled
            self.typeOfSourceAsset_comboBox.clear()
            self.whichSourceAsset_comboBox.clear()
            self.sourceAssetSoftware_comboBox.clear()
            self.listSourceAsset_comboBox.clear()

            self.typeOfExportAsset_comboBox.clear()
            self.whichExportAsset_comboBox.clear()
            self.assetExportTypes_comboBox.clear()
            #self.listExportAsset_comboBox.clear()

            self.fillComboBox(self.typeOfSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source")
            self.fillComboBox(self.whichSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.itemText(self.typeOfSourceAsset_comboBox.currentIndex()))
            self.fillComboBox(self.sourceAssetSoftware_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.itemText(self.whichSourceAsset_comboBox.currentIndex()))            
            self.fillComboBox(self.listSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText() + "\\" + self.sourceAssetSoftware_comboBox.itemText(self.sourceAssetSoftware_comboBox.currentIndex()))
            
            self.fillComboBox(self.typeOfExportAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports")
            self.fillComboBox(self.whichExportAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.itemText(self.typeOfExportAsset_comboBox.currentIndex()))
            self.fillComboBox(self.assetExportTypes_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Exports" + "\\" + self.typeOfExportAsset_comboBox.currentText() + "\\" + self.whichExportAsset_comboBox.itemText(self.whichExportAsset_comboBox.currentIndex()))            
                    
    #intermediary function to test if there is the JSON file available
    def readConfigFile(self, configFile):
        print "Config File Location: ", configFile
        try:
            file = open(configFile, "r")
        except:
            print "Config file could not be opened"
            sys.exit(1)

        configData = file.read()
        file.close()

        return configData

    #generic popup window with an OK button and can display message based on use
    def popupOkWindow(self, message):

        popupWindow = qg.QMessageBox()
        
        popupWindow.setText(str(message))
        popupWindow.setStandardButtons(qg.QMessageBox.Ok)

        popupWindow.exec_()

    #generic popup window with an yes and no buttons and can display message based on use
    def popupYesNoWindow(self, message):
        msg = qg.QMessageBox()

        msg.setText(message)
        #msg.setWindowTitle("MessageBox demo")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(qg.QMessageBox.Yes | qg.QMessageBox.No)

        result = msg.exec_()

        if result == qg.QMessageBox.Yes:
            return True
        elif result == qg.QMessageBox.No:
            return False

    #function to create window to 
    def createProject(self):

        #this window is of type dialog so that is treated as a popup
        newProjectWindow = qg.QDialog()
        newProjectWindow.setLayout(qg.QVBoxLayout())

        newProjectWindow.setWindowTitle("Create Project")

        newProject_widget = qg.QWidget()
        newProject_widget.setLayout(qg.QHBoxLayout())
        
        nameOfProject_lbl = qg.QLabel("Name of Project:")
        nameOfProject_le = qg.QLineEdit()
        nameOfProject_le.setPlaceholderText("Enter Name Here...")

        typeOfProject_widget = qg.QWidget()
        typeOfProject_widget.setLayout(qg.QHBoxLayout())

        typeOfProject_lbl = qg.QLabel("Choose Project Type:")

        preRendered_radioBtn = qg.QRadioButton("Pre-Rendered")

        orProject_lbl = qg.QLabel("- OR -")

        realTime_radioBtn = qg.QRadioButton("Real-Time")

        typeOfProject_widget.layout().addWidget(typeOfProject_lbl)
        typeOfProject_widget.layout().addWidget(preRendered_radioBtn)        
        typeOfProject_widget.layout().addWidget(orProject_lbl)               
        typeOfProject_widget.layout().addWidget(realTime_radioBtn) 

        #incorporates regex into testing input of lineEdit
        #QRegExp in QtCore
        reg_ex = qc.QRegExp("[a-zA-Z0-9]+")

        #Validator in QtGui
        validNameForAsset = qg.QRegExpValidator(reg_ex, nameOfProject_le)
        nameOfProject_le.setValidator(validNameForAsset)

        software_widget = qg.QWidget()
        software_widget.setLayout(qg.QVBoxLayout())

        availableSoftware_lbl = qg.QLabel("Available Software:")

        software_widget.layout().addWidget(availableSoftware_lbl)

        #load JSON as dictionary into variable
        JSON = self.loadJSONConfig()

        #loads available software based on JSON file
        self.loadSoftware(JSON, software_widget, softwareCheckBoxes)

        newProjectButton_widget = qg.QWidget()
        newProjectButton_widget.setLayout(qg.QHBoxLayout())
        
        create_btn = qg.QPushButton("Create")
        create_btn.setCheckable(True)
        cancel_btn = qg.QPushButton("Cancel")
        cancel_btn.setCheckable(True)

        newProject_widget.layout().addWidget(nameOfProject_lbl)
        newProject_widget.layout().addWidget(nameOfProject_le)

        newProjectButton_widget.layout().addWidget(create_btn)        
        newProjectButton_widget.layout().addWidget(cancel_btn)

        newProjectWindow.layout().addWidget(newProject_widget)                
        newProjectWindow.layout().addWidget(typeOfProject_widget)        
        newProjectWindow.layout().addWidget(software_widget)
        newProjectWindow.layout().addWidget(newProjectButton_widget)

        create_btn.clicked.connect(newProjectWindow.close)
        cancel_btn.clicked.connect(newProjectWindow.close)
        newProjectWindow.exec_()

        #runs some if else statements to check what was clicked since buttons were set to checkable
        if create_btn.isChecked():
            if preRendered_radioBtn.isChecked() or realTime_radioBtn.isChecked():
                if not nameOfProject_le.text() == "":            

                    newPath = "C:\Projects" + "\\" + str(nameOfProject_le.text())
                    
                    #if path does not exist, the directory will be created based on JSON folder structure
                    if not os.path.exists(newPath):

                        os.mkdir(newPath)
                        self.createTxt(newPath)

                        for x in JSON["Real-Time Art Structure"]["Structure"]:
                            os.mkdir(newPath + "\\" + x)
                            self.createTxt(newPath + "\\" + x)

                            if x != "Tools":
                                for y in JSON["Real-Time Art Structure"]["Asset Type"]:
                                    os.mkdir(newPath + "\\" + x + "\\" + y)
                                    self.createTxt(newPath + "\\" + x + "\\" + y)

                        tempDCC = JSON["DCC"]

                        #if realtime or prerendered is checked it will remove the other's entry from the JSON dictory to be saved in a projects local JSON file
                        if preRendered_radioBtn.isChecked():
                            del JSON["Real-Time Art Structure"]
                            tempART = JSON["Pre-Rendered Art Structure"]

                            for checkBox in software_widget.findChildren(qg.QCheckBox):
                                if not checkBox.isChecked():

                                    softwareObjName = str(checkBox.objectName())

                                    del tempDCC[softwareObjName]                                                                               
                                    artSourceIndex = tempART["Source Asset"].index(softwareObjName)
                                    tempART["Source Asset"].pop(artSourceIndex)

                            JSON["Pre-Rendered Art Structure"] = tempART

                        elif realTime_radioBtn.isChecked():
                            del JSON["Pre-Rendered Art Structure"]
                            tempART = JSON["Real-Time Art Structure"]

                            for checkBox in software_widget.findChildren(qg.QCheckBox):
                                if not checkBox.isChecked():

                                    softwareObjName = str(checkBox.objectName())

                                    del tempDCC[softwareObjName]                                                                               
                                    artSourceIndex = tempART["Source Asset"].index(softwareObjName)
                                    tempART["Source Asset"].pop(artSourceIndex)

                            JSON["Real-Time Art Structure"] = tempART                        

                        JSON["DCC"] = tempDCC

                        jDict = json.dumps(JSON, indent = 4, separators = (',',':'))
                        with open(newPath + "\\" + x + "\\" + "config.json", "w") as jFile:
                            jFile.write(jDict)                        

                        self.popupOkWindow("Successfully Created Structure For: " + str(nameOfProject_le.text()))

                        if self.project_comboBox.currentText() != "":
                            self.project_comboBox.clear()

                        self.fillProjectComboBox(self.project_comboBox, self.projectsLocation)

                    else:
                        self.popupOkWindow("PATH EXISTS")
                else:
                    self.popupOkWindow("NAME WASN'T ENTERED")
            else:
                self.popupOkWindow("TYPE OF PROJECT WAS NOT CHOSEN")

    #function to delete selected project
    def deleteProject(self):

        if self.project_comboBox.currentText() != "":              

            delPath = "C:\Projects" + "\\" + str(self.project_comboBox.currentText())
            delBool = self.popupYesNoWindow("This will delete the entire project!" + "\n" + "Delete: " + self.project_comboBox.currentText() + " ?")

            # if user chooses to delete project tool will delete path and remove software buttons from window
            if delBool:

                os.access(delPath, os.W_OK)
                os.chmod(delPath, stat.S_IWRITE)
                shutil.rmtree(delPath)

                self.popupOkWindow("Successfully Deleted " + self.project_comboBox.currentText() + " !")

                self.project_comboBox.clear()
                self.fillProjectComboBox(self.project_comboBox, self.projectsLocation)

                if self.project_comboBox.currentText() == "":
                    for i in reversed(range(self.softwareLaunch_tab_widget.layout().count())):                
                        self.softwareLaunch_tab_widget.layout().itemAt(i).widget().deleteLater()
                        self.softwareLaunch_tab_widget.layout().itemAt(i).widget().setParent(None)

                self.reloadAssets()

        else:
            self.popupOkWindow("NO PROJECT AVAILABLE TO DELETE")

    #dialog for creation of new asset
    def createDirForNewAsset(self):

        selectedAssetType = ""

        newAssetWindow = qg.QDialog()
        newAssetWindow.setLayout(qg.QVBoxLayout())

        newAssetWindow.setWindowTitle("Create New Asset")
        
        typeOfSourceAsset_widget = qg.QWidget()
        typeOfSourceAsset_widget.setLayout(qg.QHBoxLayout())

        typeOfSourceAsset_lbl = qg.QLabel("Choose Asset Type:")

        character_radioBtn = qg.QRadioButton("Characters")

        orAsset_lbl = qg.QLabel("- OR -")

        environment_radioBtn = qg.QRadioButton("Environment")

        nameAsset_widget = qg.QWidget()
        nameAsset_widget.setLayout(qg.QHBoxLayout())

        nameOfAsset_lbl = qg.QLabel("Name of Asset:")
        nameOfAsset_le = qg.QLineEdit()
        nameOfAsset_le.setPlaceholderText("Enter Name Here...")

        #incorporates regex into testing input of lineEdit
        #QRegExp in QtCore
        reg_ex = qc.QRegExp("[a-zA-Z0-9]+")

        #Validator in QtGui
        validNameForAsset = qg.QRegExpValidator(reg_ex, nameOfAsset_le)
        nameOfAsset_le.setValidator(validNameForAsset)

        newProjectButton_widget = qg.QWidget()
        newProjectButton_widget.setLayout(qg.QHBoxLayout())
        
        create_btn = qg.QPushButton("Create")
        create_btn.setCheckable(True)
        cancel_btn = qg.QPushButton("Cancel")
        cancel_btn.setCheckable(True)

        typeOfSourceAsset_widget.layout().addWidget(typeOfSourceAsset_lbl)
        typeOfSourceAsset_widget.layout().addWidget(character_radioBtn)        
        typeOfSourceAsset_widget.layout().addWidget(orAsset_lbl)               
        typeOfSourceAsset_widget.layout().addWidget(environment_radioBtn) 

        nameAsset_widget.layout().addWidget(nameOfAsset_lbl)
        nameAsset_widget.layout().addWidget(nameOfAsset_le)        

        newProjectButton_widget.layout().addWidget(create_btn)        
        newProjectButton_widget.layout().addWidget(cancel_btn)

        newAssetWindow.layout().addWidget(typeOfSourceAsset_widget)
        newAssetWindow.layout().addWidget(nameAsset_widget)
        newAssetWindow.layout().addWidget(newProjectButton_widget)

        create_btn.clicked.connect(newAssetWindow.close)
        cancel_btn.clicked.connect(newAssetWindow.close)
        newAssetWindow.exec_()

        if create_btn.isChecked():            

            if nameOfAsset_le.text() != "" and character_radioBtn.isChecked() or environment_radioBtn.isChecked():

                if character_radioBtn.isChecked():
                    selectedAssetType = character_radioBtn.text()
                elif environment_radioBtn.isChecked():
                    selectedAssetType = environment_radioBtn.text()

                selectedProj = "C:\Projects\\" + self.project_comboBox.currentText()
                jsonData = self.loadJSONConfig("C:\Projects\\" + self.project_comboBox.currentText() + "\\" + "Tools" + "\\" + "config.json")

                if "Real-Time Art Structure" in jsonData:
                    newArtSourcePath = str(selectedProj + "\\" + "Art Source" + "\\" + selectedAssetType + "\\" + nameOfAsset_le.text())
                    newArtExportsPath = str(selectedProj + "\\" + "Art Exports" + "\\" + selectedAssetType + "\\" + nameOfAsset_le.text())

                    """
                    print "POOOP", newArtSourcePath
                    print type(newArtSourcePath)
                    print newArtExportsPath
                    """
                    
                    subSourceFolders = jsonData["Real-Time Art Structure"]["Source Asset"]
                    subExportFolders = jsonData["Real-Time Art Structure"]["Export Asset"]

                    #if asset doesn't exist, create directories based on JSON file for the asset
                    if not os.path.exists(newArtSourcePath) and not os.path.exists(newArtExportsPath):

                        os.makedirs(newArtSourcePath)
                        self.createTxt(newArtSourcePath)
                        os.makedirs(newArtExportsPath)
                        self.createTxt(newArtExportsPath)

                        for x in subSourceFolders:
                            os.makedirs(newArtSourcePath + "\\" + x)
                            self.createTxt(newArtSourcePath + "\\" + x)

                        for x in subExportFolders:
                            os.makedirs(newArtExportsPath + "\\" + x)
                            self.createTxt(newArtExportsPath + "\\" + x)                 

                        #gets current index of asset comboboxes
                        typeOfSourceAssetIndex = self.typeOfSourceAsset_comboBox.currentIndex()
                        whichSourceAssetIndex = self.whichSourceAsset_comboBox.currentIndex()
                        sourceAssetSoftwareIndex = self.sourceAssetSoftware_comboBox.currentIndex()
                        listSourceAssetIndex = self.listSourceAsset_comboBox.currentIndex()

                        #clears combobxes so they can be refilled
                        self.typeOfSourceAsset_comboBox.clear()
                        self.whichSourceAsset_comboBox.clear()
                        self.sourceAssetSoftware_comboBox.clear()
                        self.listSourceAsset_comboBox.clear()

                        self.fillComboBox(self.typeOfSourceAsset_comboBox, "C:\Projects\\" + self.project_comboBox.currentText() + "\\" + "Art Source")
                        self.typeOfSourceAsset_comboBox.setCurrentIndex(typeOfSourceAssetIndex)
                        self.fillComboBox(self.whichSourceAsset_comboBox, "C:\Projects\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.itemText(self.typeOfSourceAsset_comboBox.currentIndex()))
                        self.whichSourceAsset_comboBox.setCurrentIndex(whichSourceAssetIndex)
                        self.fillComboBox(self.sourceAssetSoftware_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.itemText(self.whichSourceAsset_comboBox.currentIndex()))                                
                        self.sourceAssetSoftware_comboBox.setCurrentIndex(sourceAssetSoftwareIndex)
                        self.fillComboBox(self.listSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.itemText(self.whichSourceAsset_comboBox.currentIndex()) + "\\" + self.sourceAssetSoftware_comboBox.itemText(self.sourceAssetSoftware_comboBox.currentIndex()))
                        self.listSourceAsset_comboBox.setCurrentIndex(listSourceAssetIndex)

                    self.popupOkWindow("Successfully Created New Asset Directory")

                else:
                    self.popupOkWindow("PATH EXISTS")
                    create_btn.setChecked(False)

            
            elif nameOfAsset_le.text() == "":
                self.popupOkWindow("NAME WASN'T ENTERED")
                create_btn.setChecked(False)
            elif not character_radioBtn.isChecked() or not environment_radioBtn.isChecked():
                self.popupOkWindow("DID NOT CHOOSE TYPE")
                create_btn.setChecked(False)

    #funciton to delete asset
    def deleteAssetDir(self):
        if self.whichSourceAsset_comboBox.currentText() != "":            

            delPath = str("C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText() + "\\" + self.whichSourceAsset_comboBox.currentText())
            delBool = self.popupYesNoWindow("This will delete the entire project!" + "\n" + "Delete: " + self.whichSourceAsset_comboBox.currentText() + " ?")

            #if user chooses to delete asset, set file to writable to ensure asset and its folder structure is deleted
            if delBool:

                os.chmod(delPath, stat.S_IWRITE)
                shutil.rmtree(delPath)

                self.popupOkWindow("Successfully Deleted " + self.whichSourceAsset_comboBox.currentText() + " !")

                self.whichSourceAsset_comboBox.clear()
                self.fillComboBox(self.whichSourceAsset_comboBox, "C:\\Projects" + "\\" + self.project_comboBox.currentText() + "\\" + "Art Source" + "\\" + self.typeOfSourceAsset_comboBox.currentText())

            else:
                self.popupOkWindow("PATH DOESN'T EXIST")
        else:
            self.popupOkWindow("NO PROJECT AVAILABLE TO DELETE")

    #function to rename asset
    def renameAsset(self, assetPath):

        #takes in assetPath
        if self.osPath(assetPath):
            renameAssetWindow = qg.QDialog()
            renameAssetWindow.setLayout(qg.QVBoxLayout())

            renameAssetWidget = qg.QWidget()
            renameAssetWidget.setLayout(qg.QHBoxLayout())

            #splits assetPath to get assetName
            sourceAssetPathList = assetPath.split("\\")
            print sourceAssetPathList
            print type(sourceAssetPathList)

            oldAssetName = sourceAssetPathList[-1]

            #uses last element in sourceAssetPathList which should be assetName
            renameAsset_lbl = qg.QLabel("Rename \"" + oldAssetName + "\" to ")

            newNameOfAsset_le = qg.QLineEdit()
            newNameOfAsset_le.setPlaceholderText("Enter Name Here...")

            reg_ex = qc.QRegExp("[a-zA-Z0-9]+")

            validNameForAsset = qg.QRegExpValidator(reg_ex, newNameOfAsset_le)
            newNameOfAsset_le.setValidator(validNameForAsset)

            renameAssetWidget.layout().addWidget(renameAsset_lbl)
            renameAssetWidget.layout().addWidget(newNameOfAsset_le)

            renamesourceAssetButton_widget = qg.QWidget()
            renamesourceAssetButton_widget.setLayout(qg.QHBoxLayout())

            rename_btn = qg.QPushButton("Rename")
            rename_btn.setCheckable(True)
            cancel_btn = qg.QPushButton("Cancel")
            cancel_btn.setCheckable(True)

            renamesourceAssetButton_widget.layout().addWidget(rename_btn)
            renamesourceAssetButton_widget.layout().addWidget(cancel_btn)

            renameAssetWindow.layout().addWidget(renameAssetWidget)
            renameAssetWindow.layout().addWidget(renamesourceAssetButton_widget)

            rename_btn.clicked.connect(renameAssetWindow.close)
            cancel_btn.clicked.connect(renameAssetWindow.close)
            renameAssetWindow.exec_()

            if rename_btn.isChecked():
                if not newNameOfAsset_le.text() == "":

                    selectedProj = "C:\Projects\\" + self.project_comboBox.currentText()
                    jsonData = self.loadJSONConfig("C:\Projects\\" + self.project_comboBox.currentText() + "\\" + "Tools" + "\\" + "config.json")

                    #if user inputs a new name, asset is created and added to folder path
                    if "Real-Time Art Structure" in jsonData:
                        #print "SOURCE LIST", sourceAssetPathList

                        #the [:] is needed to literally copy a list, not using this just copys the reference to the list
                        exportAssetPathList = sourceAssetPathList[:]
                        exportAssetPathList[3] = "Art Exports"

                        #print "SOURCE LIST2", sourceAssetPathList

                        #print "EXPORT LIST", exportAssetPathList

                        #removes old asset name from list
                        sourceAssetPathList.pop()
                        sourceAssetPathList.append(str(newNameOfAsset_le.text()))

                        newSourcePath = "\\".join(sourceAssetPathList)
                        #print "NEW SOURCE", newSourcePath

                        os.rename(assetPath, newSourcePath)

                        oldExportAssetPath = "\\".join(exportAssetPathList)

                        exportAssetPathList.pop()
                        exportAssetPathList.append(str(newNameOfAsset_le.text()))

                        newExportPath = "\\".join(exportAssetPathList)
                        #print "NEW EXPORT", newExportPath

                        os.rename(oldExportAssetPath, newExportPath)

                    self.popupOkWindow("SUCCESSFULLY RENAMED " + oldAssetName + " TO " + str(newNameOfAsset_le.text()))
                else:
                    self.popupOkWindow("A NEW NAME WAS NOT ENTERED")

        else:
            self.popupOkWindow("ASSET CAN'T BE RENAMED IF IT DOESN'T EXIST")

    #creates dummy file in each folder in case folder would be added to P4V
    def createTxt(self, filePath):
        if self.osPath(filePath):
            with open(filePath + "\\" + "dummy.txt", "w") as txtFile:
                txtFile.write("Dummy File for " + filePath)
        else:
            self.popupOkWindow(filePath + " NOT FOUND TO GENERATE DUMMY.TXT")

    #generic fill combobox function to be used when a combobox needs filling
    def fillComboBox(self, comboBox, filePath):
        currentJSON = "C:\\Projects" + "\\" + "Tools" + "\\" + "config.json"
        JSON = self.loadJSONConfig(currentJSON)            

        ignoreList = JSON["File Ignore List"]
        
        #clears default entry of comboBox
        if comboBox.currentText() == " ":
            comboBox.removeItem(comboBox.currentIndex())

        assetPaths = self.getPath(filePath)
        
        #print "Paths:", assetPaths
        
        foundInIgnoreList = False

        for x in assetPaths:
            for y in ignoreList:
                #print y
                if y in x:
                    foundInIgnoreList = True
                    #print foundInIgnoreList

            if not foundInIgnoreList:
                comboBox.addItem(x)

            foundInIgnoreList = False

    #identical function to previous fill combobox but specifically for filling project combobox to ensure only folders are populating it
    def fillProjectComboBox(self, comboBox, filePath):
        currentJSON = "C:\\Projects" + "\\" + "Tools" + "\\" + "config.json"
        JSON = self.loadJSONConfig(currentJSON)            

        ignoreList = JSON["File Ignore List"]
        
        #clears default entry of comboBox
        if comboBox.currentText() == " ":
            comboBox.removeItem(comboBox.currentIndex())

        assetPaths = self.getPath(filePath)

        #print "Paths:", assetPaths
        
        foundInIgnoreList = False

        for x in assetPaths:
            #print x
            if self.osPath(os.path.join(filePath, str(x))):
                print "Project", x
                for y in ignoreList:
                    #print y
                    if y in x:
                        foundInIgnoreList = True
                        #print foundInIgnoreList

                if not foundInIgnoreList:
                    comboBox.addItem(x)

                foundInIgnoreList = False

    #get list of directories if path exists
    def getPath(self, filePath):
        if self.osPath(filePath): 
            return os.listdir(filePath)

    #determine if path exists
    def osPath(self, filePath):
        #print filePath
        #print type(filePath)
        if os.path.isdir(filePath):
            return True
        else:
            return False

#button class used to populate software 
class softwareButton(qg.QPushButton):
    def __init__( self, icon = '', exe = '', objName = '', parent=None, ):
        super(softwareButton, self).__init__(parent )

        self.setCheckable(True)

        self.setIcon(qg.QIcon(icon))

        self.setObjectName(objName)
        self.setIconSize(qc.QSize(64,64))
        self.setMaximumWidth(74)

        #self.setText(softwareNameVer)
        #neat feature to delete button
        #self.clicked.connect(self.deleteLater)

        #calls function on click to change button color and add script name to list in Main class
        self.clicked.connect(lambda: self.buttonClicked(exe))
    
    #function called when button is clicked
    def buttonClicked(self, exe):
        if self.isChecked():
            self.setChecked(False)
            os.startfile(exe)

#checkbox class used in dialog to create a project
class softwareCheckBoxes(qg.QCheckBox):
    def __init__(self, icon = '', softwareNameVer = '', objName = '', parent = None):
        super(softwareCheckBoxes, self).__init__(parent)

        self.setIcon(qg.QIcon(icon))
        self.setText(softwareNameVer)
        self.setObjectName(objName)
        self.setIconSize(qc.QSize(64,64))


app = qg.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()