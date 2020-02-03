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
    gotPressure = pyqtSignal(float, float)
    keepRunning = True
    finished = pyqtSignal()
    @pyqtSlot()
    def __del__(self):
        self.wait()

    def stop(self):
        print('button clicked')
        
        self.keepRunning = False
        
    def run(self, samplingRate):
        time_passed = 0
        print(QThread.currentThreadId())
        while self.keepRunning:
            QApplication.processEvents()
            cur_pressure = dummy_pressure.get_pressure()
            self.gotPressure.emit(time_passed, cur_pressure)
            time_passed += 1
            time.sleep(1/samplingRate)
        self.finished.emit()


class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.samplingRate = 0
        self.continueLoop = True
        self.chart = QChart()
        
        self.series = QLineSeries()
        self.thread = QThread()
        self.dataObj = getDataObject()
        
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
        # self.thread.exit()
        self.dataObj.stop()
        

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
        return

    def startCollection(self):
        print(QThread.currentThreadId())
        if self.samplingRate == 0:
            msgBox = QMessageBox()
            msgBox.setText('Set Sampling rate first')
            msgBox.exec()
            return
        self.continueLoop = True
        self.dataObj.gotPressure.connect(self.process)
        self.dataObj.moveToThread(self.thread)
        self.dataObj.finished.connect(self.thread.quit)
        try:
            # find a better way to handle an exception where I think dataObj doesn't exist
            self.thread.started.connect(self.dataObj.run(self.samplingRate))
            self.thread.start()
        except TypeError as e:
            print(e)
            print('thread stopped')
        # self.ui.stopButton.clicked.connect(dataObj.stop)
        # t1 = threading.Thread(target=self.process, args = (series))
        print('stopped')
        return
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = StartWindow()
    main.show()
    sys.exit(app.exec_())
