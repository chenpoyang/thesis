'''
Created on May 14, 2013

@author: young
'''

from PyQt4 import QtCore
from ftplib import FTP
import os
import sys
import socket
import httplib

class DThread(QtCore.QThread):
    
    url = None
    pause = False
    mutex = None
    startCond = None
    started = None
    localFileName = None
    dstHost = None
    dstPort = None
    remoteFile = None
    isFtp = None
    conn = None
    #filename, speed, percentage, Size, Est.time, Progress
    strList = None
    fsize = None
    
    def __init__(self, parent = None, _url = None):
        super(DThread, self).__init__()
        self.url = str(_url)
        self.pause = False
        self.mutex = QtCore.QMutex()
        self.startCond = QtCore.QWaitCondition()
        self.started = True
        self.setHostInfo()
    
    def run(self):
        lsize = 0L
        idx = self.url.rfind("/")
        self.localFileName = self.url[idx+1:]
        if os.path.exists(self.localFileName):
            lsize = os.stat(self.localFileName).st_size
            
        
        if self.isFtp:
            print "ftp"
            self.conn = self.connectToFTPHost(self.dstHost, self.dstPort, "", "")
        else:
            print "http"
            self.conn = self.connectToHTTPHost(self.dstHost)
        
        if self.isFtp:
            self.conn.set_pasv(0)
            dirs = self.remoteFile.strip().split("/")
            for dir in dirs:
                if dir != dirs[-1]:
                    self.conn.cwd(dir)
            
            self.conn.voidcmd("TYPE I")
            self.fsize = self.conn.size(dirs[-1])
            if os.path.exists(self.localFileName):
                lsize = os.stat(self.localFileName).st_size
            else:
                lsize = 0
                
            if lsize >= self.fsize:
                return
                
            res = self.conn.transfercmd("RETR " + dirs[-1], lsize)
            fd = open(self.localFileName, "ab")
            while True:
                data = res.recv(1024)
                if not data:
                    break
                fd.write(data)
            
            fd.close()
            self.conn.voidcmd("NOOP")
            self.conn.voidresp()
            res.close()
            self.conn.close()
            self.conn.quit()
            
        else:
            #get file size
            self.conn.request('HEAD', self.remoteFile)
            res = self.conn.getresponse()
            self.fsize = int(res.getheader('content-length'))
            
            self.conn.request('GET', self.remoteFile)
            res = self.conn.getresponse()
            fd = open(self.localFileName, "ab")
            while True:
                data = res.read(10)
                if not data:
                    break
                fd.write(data)
            
            fd.close()
            res.close()
            self.conn.close()
        
        while (self.started):
            self.mutex.lock()
            if self.pause:
                self.storeInfoForPause()
                self.startCond.wait(self.mutex)
                self.restoreInfoForPause()
            self.mutex.unlock()
            print "run"
            break
            
    def connectToFTPHost(self, remoteIP, remotePort, username, password):
        ftp = FTP()
        print "remote ip:" + str(remoteIP) + ", remotePort:" + str(remotePort)
        try:
            ftp.connect(remoteIP, remotePort)
            print "connect FTP success!"
        except:
            print "connect failed!"
            return None
        else:
            try:
                ftp.login(username, password)
                print "login success!"
            except:
                print "login failed!"
                return None
            else:
                return ftp
    
    def connectToHTTPHost(self, remoteHostName):
        try:
            conn = httplib.HTTPConnection(remoteHostName)
            print "connect HTTP success!"
        except:
            print "connect HTTP failed!"
        
        return conn
    
    # set Host Info
    def setHostInfo(self):
        tmpHostName = None
        self.isFtp = False
        if self.url.lower().find("ftp") != -1:
            self.isFtp = True
        
        idx = self.url.find("//")
        if idx != -1:
            tmpHost = self.url[idx + 2:]
        else:
            tmpHost = self.url
            
        idx = tmpHost.find("/")
        # eg:/pub/find/findutil.tar.bz2
        self.remoteFile = tmpHost[idx:]
        if idx >= 0 and idx < len(tmpHost):
            tmpHostName = tmpHost[:idx]
        else:
            tmpHostName = tmpHost
            
        if self.isFtp:
            print "ftp:" + tmpHostName
            self.dstHost = socket.getaddrinfo(tmpHostName, 'ftp')[0][4][0]
            self.dstPort = 21
        else:
            print "http:" + tmpHostName
            self.dstHost = socket.getaddrinfo(tmpHostName, 'http')[0][4][0]
            self.dstPort = 80
        
    def storeInfoForPause(self):
        print "pause"
    
    def restoreInfoForPause(self):
        print "restore"
