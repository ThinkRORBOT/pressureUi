# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 30, 781, 491))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.topHorizonal = QtWidgets.QHBoxLayout()
        self.topHorizonal.setObjectName("topHorizonal")
        self.pressureLabel = QtWidgets.QLabel(self.widget)
        self.pressureLabel.setObjectName("pressureLabel")
        self.topHorizonal.addWidget(self.pressureLabel)
        self.pressureDisplay = QtWidgets.QLineEdit(self.widget)
        self.pressureDisplay.setReadOnly(True)
        self.pressureDisplay.setObjectName("pressureDisplay")
        self.topHorizonal.addWidget(self.pressureDisplay)
        self.mpaLabel = QtWidgets.QLabel(self.widget)
        self.mpaLabel.setObjectName("mpaLabel")
        self.topHorizonal.addWidget(self.mpaLabel)
        self.verticalLayout.addLayout(self.topHorizonal)
        self.leakStatusBox = QtWidgets.QLineEdit(self.widget)
        self.leakStatusBox.setReadOnly(True)
        self.leakStatusBox.setObjectName("leakStatusBox")
        self.verticalLayout.addWidget(self.leakStatusBox)
        self.bottomHorizonal = QtWidgets.QHBoxLayout()
        self.bottomHorizonal.setObjectName("bottomHorizonal")
        self.samplingLabel = QtWidgets.QLabel(self.widget)
        self.samplingLabel.setObjectName("samplingLabel")
        self.bottomHorizonal.addWidget(self.samplingLabel)
        self.frequencyEdit = QtWidgets.QLineEdit(self.widget)
        self.frequencyEdit.setInputMask("")
        self.frequencyEdit.setText("")
        self.frequencyEdit.setObjectName("frequencyEdit")
        self.bottomHorizonal.addWidget(self.frequencyEdit)
        self.samplingButton = QtWidgets.QPushButton(self.widget)
        self.samplingButton.setObjectName("samplingButton")
        self.bottomHorizonal.addWidget(self.samplingButton)
        self.stopButton = QtWidgets.QPushButton(self.widget)
        self.stopButton.setObjectName("stopButton")
        self.bottomHorizonal.addWidget(self.stopButton)
        self.resetButton = QtWidgets.QPushButton(self.widget)
        self.resetButton.setObjectName("resetButton")
        self.bottomHorizonal.addWidget(self.resetButton)
        self.verticalLayout.addLayout(self.bottomHorizonal)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pressureLabel.setText(_translate("MainWindow", "Current Pressure: "))
        self.mpaLabel.setText(_translate("MainWindow", "Mpa"))
        self.samplingLabel.setText(_translate("MainWindow", "Sampling Frequency"))
        self.frequencyEdit.setPlaceholderText(_translate("MainWindow", "Hz"))
        self.samplingButton.setText(_translate("MainWindow", "Ok"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.resetButton.setText(_translate("MainWindow", "Begin/Reset"))
