import os
import sys
import mdown_rc
from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
	super(MainWindow, self).__init__()

        self.initMenu()
        self.initToolBar()
        self.initCenterWidget()
        self.initStatusBar()
        
	self.setWindowTitle("download device")
	self.resize(800, 600)
	
    def initMenu(self):
        bar = self.menuBar()

        #File
        self.menuFile = QtGui.QMenu(self.tr("File(&F)"), bar)
        self.actNew = self.menuFile.addAction(self.tr("New(&N)"))
        self.actNew.setIcon(QtGui.QIcon(":/images/new.png"))
        self.actNew.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+n")))
        self.menuFile.addSeparator()
        self.actSetting = self.menuFile.addAction(self.tr("Settings(&S)"))
        self.actSetting.setIcon(QtGui.QIcon(":images/settings"))
        self.actSetting.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+s")))
        self.menuFile.addSeparator()
        self.actExit = self.menuFile.addAction(self.tr("Exit(&q)"))
        self.actExit.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+q")))
        bar.addMenu(self.menuFile)

        #Edit Start, Pause, Cancel
        self.menuEdit = QtGui.QMenu(self.tr("Edit(&E)"), bar)
        self.actStart = self.menuEdit.addAction(self.tr("Start(&S)"))
        self.actStart.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+s")))
        self.actStart.setIcon(QtGui.QIcon(":/images/start.png"))
        self.menuEdit.addSeparator()
        self.actPause = self.menuEdit.addAction(self.tr("Pause(&P)"))
        self.actPause.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+p")))
        self.actPause.setIcon(QtGui.QIcon(":/images/pause.png"))
        self.menuEdit.addSeparator()
        self.actCancel = self.menuEdit.addAction(self.tr("Cancel(&C)"))
        self.actCancel.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+c")))
        self.actCancel.setIcon(QtGui.QIcon(":/images/cancel.png"))
        bar.addMenu(self.menuEdit)

        #About
        self.menuAbout = QtGui.QMenu(self.tr("About(&A)"), bar)
        self.actAbout = self.menuAbout.addAction(self.tr("About(&A)"))
        bar.addMenu(self.menuAbout)

    def initToolBar(self):
        fileToolBar = QtGui.QToolBar(self.tr("file bar"), self)
        fileToolBar.addAction(self.actNew)

        editToolBar = QtGui.QToolBar(self.tr("edit bar"), self)
        editToolBar.addAction(self.actStart)
        editToolBar.addAction(self.actPause)
        editToolBar.addAction(self.actCancel)
        editToolBar.addAction(self.actSetting)

        self.addToolBar(fileToolBar)
        self.addToolBar(editToolBar)
        
    def initCenterWidget(self):
        self.centerWidget = QtGui.QTreeWidget(self)
        self.centerWidget.setRootIsDecorated(False) # no decoration
        self.setCentralWidget(self.centerWidget)
        strList = ("Download/Name", "Speed", "Percentage", "Size","Est.time", "Progress")
        self.centerWidget.setHeaderLabels(strList)

        strList = ("ubuntu.iso", "230kb/s", "60%", "4G", "3min", "------------------------------>==============")
        item = QtGui.QTreeWidgetItem(self.centerWidget, strList, 1)
        item.setIcon(0, QtGui.QIcon(":/images/down.png"))
        self.centerWidget.addTopLevelItem(item)
        strList = ("archlinux.iso", "300kb/s", "60%", "4G", "3min","------------------------------>==============")
        item = QtGui.QTreeWidgetItem(self.centerWidget, strList, 1)
        item.setIcon(0, QtGui.QIcon(":/images/down.png"))
        self.centerWidget.addTopLevelItem(item)

        
    def initStatusBar(self):
        statusBar = self.statusBar()
        downLabel = QtGui.QLabel("Downloads: %d of %d, %d running")
        downLabel.setMinimumSize(200, 25)
        
        speedLabel = QtGui.QLabel("% kb/s")
        speedLabel.setMinimumSize(200, 25)

        statusBar.addWidget(downLabel)
        statusBar.addWidget(speedLabel)
        

    def initLocSize():
	pass
    def initConnection():
	pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
