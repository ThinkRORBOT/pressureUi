import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtChart import QChart, QLineSeries, QChartView
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QBrush
import dummy_pressure
from detect_pressure_drop import leak_check
import time
import email_warning
import threading


class getDataObject(QObject):
    def __init__(self, samplingRate):
        self.samplingRate = samplingRate
        self.gotPressure = pyqtSignal(int, float)
        self.keepRunning = True
        
    def __del__(self):
        self.wait()

    def stop(self):
        self.keepRunning = False
        
    def run(self):
        time_passed = 0
        while self.keepRunning:
            cur_pressure = dummy_pressure.get_pressure()
            self.gotPressure.emit(time_passed, cur_pressure)
            time.sleep(1/samplingRate)
            


class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.samplingRate = 0
        self.continueLoop = True
        self.chart = QChart()
        
        self.series = QLineSeries()
        
        self.chart.setTitle('pressureGraph')
        
        self.chartView = QChartView(self.chart)
        self.ui.verticalLayout.addWidget(self.chartView)

        self.ui.samplingButton.clicked.connect(self.getSamplingRate)
        self.ui.resetButton.clicked.connect(self.startCollection)
        self.ui.stopButton.clicked.connect(self.stopLoop)
        

    def getSamplingRate(self):
        self.samplingRate = float(self.ui.frequencyEdit.text())
        print(self.samplingRate)

    def stopLoop(self):
        self.continueLoop = False

    def setAxis(self, time_passed, yList):
        horAxis = self.chart.axes(orientation=Qt.Horizontal)
        verAxis = self.chart.axes(orientation=Qt.Vertical)
        
        max_time = time_passed/self.samplingRate
        # set axis limits
        horAxis[0].setMax(max_time)
        horAxis[0].setMin(max(max_time-10, 0))
        verAxis[0].setMax(max(yList))
        verAxis[0].setMin(min(yList))
            
    def process(self, time_passed, cur_pressure):
        pList = list()
        print(cur_pressure)
            
        if len(self.series) != 0:
            self.chart.removeSeries(self.series)
        if len(self.series) > 10:
            # remove the first index after certain number of data
            self.series.remove(0)
            pList = pList[1:]
        self.series.append(time_passed/self.samplingRate, cur_pressure)
        pList.append(cur_pressure)
        self.chart.addSeries(self.series)

        # only create new axes in first instance to avoid clipping of labels.
        if len(self.series) < 2:
            self.chart.createDefaultAxes()
        
        self.ui.pressureDisplay.setText('{:.4f}'.format(cur_pressure))
        leak = False
        leakO = leak_check()
        leak = leakO.check_leak(cur_pressure)
        if not leak:
            self.ui.leakStatusBox.setText("No Pressure Drop detected")
        else:
            self.ui.leakStatusBox.setText("Pressure drop detected. Email sent")
            email_warning.send_message(pList)
            return
            
        self.setAxis(time_passed, pList)
        time.sleep(1/self.samplingRate)
        #self.chart.removeAxis(horAxis[0])
        #self.chart.removeAxis(verAxis[0])
        time_passed += 1
        return

    def startCollection(self):
        if self.samplingRate == 0:
            msgBox = QMessageBox()
            msgBox.setText('Set Sampling rate first')
            msgBox.exec()
            return
        self.continueLoop = True
        objThread = QThread()
        dataObj = getDataObject(self.samplingRate)
        dataObj.moveToThread(objThread)
        dataObj.gotPressure.connect(self.process)
        objThread.started.connect(dataObj.run)
        objThread.start()
        self.ui.stopButton.setEnabled(True)
        self.ui.stopButton.clicked.connect(objThread.stop)
        # t1 = threading.Thread(target=self.process, args = (series))
        print('stopped')
        return
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = StartWindow()
    main.show()
    sys.exit(app.exec_())
