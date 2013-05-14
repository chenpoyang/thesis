'''
Created on May 14, 2013

@author: young
'''

from PyQt4 import QtCore

class DThread(QtCore.QThread):
    
    url = None
    pause = True
    mutex = None
    startCond = None
    started = None
    
    def __init__(self, parent = None, _url):
        super(DThread, self).__init__(parent)
        
        self.url = _url
        self.pause = False
        self.mutex = QtCore.QMutex()
        self.startCond = QtCore.QWaitCondition()
        self.started = True
    
    def run(self):
        while (self.started):
            self.mutex.lock()
            if self.pause:
                self.storeInfoForPause()
                self.startCond.wait(self.mutex)
                self.restoreInfoForPause()
            self.mutex.unlock()
            
            
        
    def storeInfoForPause(self):
        pass
    
    def restoreInfoForPause(self):
        pass