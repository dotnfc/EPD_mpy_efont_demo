import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from mpy_efont_ui import *
from mpy_serial import *
import logging
import subprocess
import esptool

logger = logging.getLogger(__name__)

class CustomExceptionHandler:
    def __init__(self, widget):
        self.text_edit = widget

    def __call__(self, exc_type, exc_value, traceback):
        error_message = f"Exception Type: {exc_type.__name__}\n"
        error_message += f"Exception Value: {exc_value}\n"
        self.text_edit.appendPlainText(error_message)
        
class QPlainTextEditLogger(logging.Handler):
    '''Helper class for logging redirection.'''
    
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        log_message = self.format(record)
        self.widget.appendPlainText(log_message)

class QLineEditDropHandler(QObject):
    '''Helper class for QLineEdit to Handle Drag and Drop.'''
    
    def eventFilter(self, widget, event):
        if event.type() == QEvent.DragEnter:
            event.accept()
        if event.type() == QEvent.Drop:
            md = event.mimeData()
            if md.hasUrls():
                url = md.urls()[0]
                widget.setText(url.toLocalFile())
                return True
        return super().eventFilter(widget, event)

class MyMainForm(QMainWindow, Ui_MainWindow):
    '''Main form'''
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        
        # com port refresh button
        self.reloadBtn.clicked.connect(self.refreshPorts)
        self.btnFWUpd.clicked.connect(self.uploadFW)
        self.btnFSUpd.clicked.connect(self.uploadFS)
        
        # button for browsing for upload file
        self.btnSelFW.clicked.connect(self.browseFW)
        self.btnSelVFS.clicked.connect(self.browseFS)
        
        # Setup Firmware Control
        self.textFW.installEventFilter(QLineEditDropHandler(self))
        self.textFW.setPlaceholderText("Firmware File")
        self.textFW.setAcceptDrops(True)
        
        # Setup Filesystem Control
        self.textFS.installEventFilter(QLineEditDropHandler(self))
        self.textFS.setPlaceholderText("FileSystem File")
        self.textFS.setAcceptDrops(True)
        
        # Setup Log
        log_handler = QPlainTextEditLogger(self.textLog)
        formatter = logging.Formatter('%(asctime)s [%(name)s]: %(message)s')
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)
        
        # Combbox dropdown handler
        self.portBox.showPopup = self.onCombboxDropdown
        
        # Hook Exception Logging
        sys.excepthook = CustomExceptionHandler(self.textLog)
        
        logger.info("eFont Tool Started")
    
    def onCombboxDropdown(self):
        lastSel = self.portBox.currentText()
        self.refreshPorts()
        index = self.portBox.findText(lastSel)
        if index >= 0:
            self.portBox.setCurrentIndex(index)
    
        QComboBox.showPopup(self.portBox)

    def refreshPorts(self):
        '''refresh COM port.'''
        
        ports_list = list_serial_ports()# list(serial.tools.list_ports.comports())

        if len(ports_list) <= 0:
            logger.info("No ports found")
        else:
            logger.info(f"found {len(ports_list)} port(s)")
            
            self.portBox.clear()
            for comport in ports_list:
                if comport.interface is not None:
                    content = "%s(%s)" % (comport.interface, comport.device)
                else:
                    content = "%s" % (comport.description)
                    
                self.portBox.addItem(content, comport.device)
                print(content)

    def getPortBaud(self):
        self.portBox: QComboBox
        self.baudBox: QComboBox
        strPort = self.portBox.currentData()
        strBaud = self.baudBox.currentText()
        
        if strPort == "":
            raise Exception("Com Port not found")
        if strBaud == "":
            raise Exception("Baud rate is invalid")
        
        return (strPort, strBaud)
        
    def uploadFW(self):
        self.textFW: QLineEdit
        port, baud = self.getPortBaud()
        fw = self.textFW.text()
        if fw == "":
            raise Exception("invalid firmware file to upload")
        
        self.launchESPTool(port, baud, fw)        
        
    def uploadFS(self):
        self.textFS.text: QLineEdit
        port, baud = self.getPortBaud()
        fs = self.textFS.text()
        if fs == "":
            raise Exception("invalid file system image to upload")
        
        self.launchESPTool(port, baud, fs, 0x290000)
    
    def updateSubprocessMsg(self, msg):
        self.textLog: QPlainTextEdit
        
        if msg.endswith('\n'):
            msg = msg[:-1]

        self.textLog.appendPlainText(msg)
        QApplication.processEvents()    # update UI
        
    def launchESPTool(self, port, baud, fw, address = 0):
        cmd = [self.getSubprocessApp(), "-u", "-m", "esptool"]
        command = cmd + [
            "--port", port,
            "--baud", baud,
            "--before", "default_reset",
            "--after", "hard_reset",
            "--chip", "esp32s3",
            "write_flash",
            "-z", hex(address),
            fw
        ]
        
        sCmdl = subprocess.list2cmdline(command)
        self.updateSubprocessMsg(sCmdl)
                
        self._proc = self._create_subprocess(command)
        try:
            while True:
                line = self._proc.stdout.readline()
                if not line:
                    break
                self.updateSubprocessMsg(line)
                
            returncode = self._proc.wait()
        finally:
            self._proc = None

        if returncode:
            logger.info("\nCommand returned with error code %s" % returncode)
        else:
            logger.info("Done!")
            
    def _create_subprocess(self, cmd) -> subprocess.Popen:
        return subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        )
        
    def getSubprocessApp(self):
        candidate = sys.executable
        
        rtPath = os.environ.get("PYSTAND_RUNTIME")
        if rtPath is not None:
            candidate = os.path.join(rtPath, "python.exe")

        pythonw = candidate.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw):
            return pythonw
        else:
            return candidate.replace("pythonw.exe", "python.exe")
    
    def fileBrowse(self):
        '''Browse for upload file.'''
        
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("upload file (*.bin);;All File (*)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            for file in selected_files:
                return file

        return None
    
    def browseFW(self):
        uploadFile = self.fileBrowse()
        if uploadFile is not None:
            self.textFW.setText(uploadFile)
        
    def browseFS(self):
        uploadFile = self.fileBrowse()
        if uploadFile is not None:
            self.textFS.setText(uploadFile)

def main():
    app = QApplication(sys.argv)
    
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
