'''
Created on May 13, 2013

@author: young
'''

import sip
#sip.setapi('QString', 2)
from PyQt4 import QtCore, QtGui

class UrlDlg(QtGui.QDialog):
    
    downloadSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, parent = None):
        super(UrlDlg, self).__init__(parent)
        
        self.initWidget()
        self.initConnection()
        
    def initWidget(self):
        self.urlLabel = QtGui.QLabel("&URL:")
        self.urlLineEdit = QtGui.QLineEdit()
        self.urlLabel.setBuddy(self.urlLineEdit)
        
        self.statusLabel = QtGui.QLabel("Please Enter the URL of a file "
            "you want to download!")
        
        self.downloadBtn = QtGui.QPushButton("Download")
        self.downloadBtn.setDefault(True)
        self.cancelBtn = QtGui.QPushButton("Cancel")
        self.cancelBtn.setAutoDefault(False)
        btnBox = QtGui.QDialogButtonBox()
        btnBox.addButton(self.downloadBtn, QtGui.QDialogButtonBox.ActionRole)
        btnBox.addButton(self.cancelBtn, QtGui.QDialogButtonBox.RejectRole)
        
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.urlLabel)
        topLayout.addWidget(self.urlLineEdit)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.statusLabel)
        
        mainLayout.addWidget(btnBox)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Download")
    
    def sendNewUrl(self):
        self.downloadSignal.emit(self.urlLineEdit.text())
        self.hide()
    
    def initConnection(self):
        self.cancelBtn.clicked.connect(self.close)
        self.downloadBtn.clicked.connect(self.sendNewUrl)
        print "called!"