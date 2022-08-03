from __future__ import print_function
from pyqtlibs import *
from PyQt5.QtCore import (Qt, pyqtSignal)
# import PyQt5
# from PyQt5 import Qt, QtGui, QtCore
# from PyQt5.QtCore import pyqtSignal
# from PyQt5.QtGui import QWidget
# from PyQt5.QtGui import QButtonGroup
# from PyQt5.QtGui import QRadioButton
# from PyQt5.QtGui import QVBoxLayout
# from PyQt5.QtGui import QLabel
# from PyQt5.QtGui import QGridLayout
# from PyQt5.QtGui import QLineEdit
# from PyQt5.QtGui import QDoubleValidator
# from PyQt5.QtGui import QComboBox
# from PyQt5.QtGui import QTabWidget
# from PyQt5.QtGui import QPushButton
# from PyQt5.QtGui import QColorDialog
# from PyQt5.QtGui import QColor
# from PyQt5.QtGui import QSizePolicy
import sys

class PreferencesView(QTabWidget):

    closed                  =  pyqtSignal()

    def __init__(self, parent = None):
        super(PreferencesView, self).__init__(parent)

        self.setWindowTitle("Preferences")
        # self.setFixedSize(self.maximumSize())
        # self.setMinimumSize(self.maximumSize())
        # self.setMaximumSize(self.maximumSize())

        # self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.chemicalSimulationDt               =   self.createFloatingPointEditor()
        self.chemicalDiffusionDt                =   self.createFloatingPointEditor()
        self.chemicalPlotUpdateInterval         =   self.createFloatingPointEditor()
        self.chemicalDefaultSimulationRuntime   =   self.createFloatingPointEditor()
        self.chemicalGuiUpdateInterval          =   self.createFloatingPointEditor()
        self.chemicalSolver                     =   QButtonGroup()
        self.chemicalSolvers                    =   {   "Exponential Euler" :  QRadioButton("Exponential Euler")
                                                      , "Gillespie"         :  QRadioButton("Gillespie")
                                                      , "Runge Kutta"       :  QRadioButton("Runge Kutta")
                                                    }
        self.chemicalSimulationApply                      =   QPushButton("Apply")
        self.chemicalSimulationCancel                     =   QPushButton("Cancel")
        self.electricalSimulationDt             =   self.createFloatingPointEditor()
        self.electricalPlotUpdateInterval       =   self.createFloatingPointEditor()
        self.electricalDefaultSimulationRuntime =   self.createFloatingPointEditor()
        self.electricalGuiUpdateInterval        =   self.createFloatingPointEditor()
        self.electricalSolver                   =   QButtonGroup()
        self.electricalSolvers                    = { "Gillespie"       :   QRadioButton("Gillespie")
                                                    , "Runge Kutta"     :   QRadioButton("Runge Kutta")
                                                    }
        self.electricalSimulationApply          =   QPushButton("Apply")
        self.electricalSimulationCancel         =   QPushButton("Cancel")
        self.electricalVisualizationApply       =   QPushButton("Apply")
        self.electricalVisualizationCancel      =   QPushButton("Cancel")
        self.electricalBaseColorButton          =   QPushButton()
        self.electricalBaseColorDialog          =   QColorDialog()
        self.electricalPeakColorButton          =   QPushButton()
        self.electricalPeakColorDialog          =   QColorDialog()
        self.electricalBackgroundColorButton    =   QPushButton()
        self.electricalBackgroundColorDialog    =   QColorDialog()
        self.electricalBaseMembraneVoltage      =   self.createFloatingPointEditor()
        self.electricalPeakMembraneVoltage      =   self.createFloatingPointEditor()

        self.create()

    def closeEvent(self, event):
        self.closed.emit()

    def create(self):
        # Set up the column titles
        self.setUsesScrollButtons(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.addTab( self.createChemicalSettingsTab(),"Chemical")
        self.addTab( self.createElectricalSettingsTab(),"Electrical")

    def createChemicalSettingsTab(self):
        chemicalSettingsTab = QWidget()
        layout = QGridLayout()
        chemicalSettingsTab.setLayout(layout)

        layout.addWidget(QLabel('Simulation dt'), 0, 0)
        layout.addWidget(self.chemicalSimulationDt, 0, 1)

        layout.addWidget(QLabel('Diffusion dt'), 1, 0)
        layout.addWidget(self.chemicalDiffusionDt, 1, 1)

        layout.addWidget(QLabel('Plot Update Interval'), 2, 0)
        layout.addWidget(self.chemicalPlotUpdateInterval, 2, 1)

        layout.addWidget(QLabel('GUI Update Interval'), 3, 0)
        layout.addWidget(self.chemicalGuiUpdateInterval, 3, 1)

        # layout.addWidget(QLabel('Default Runtime'), 4, 0)
        # layout.addWidget(self.chemicalDefaultSimulationRuntime, 4, 1)

        layout.addWidget(QLabel('Solver'), 5, 0)

        index = 0
        for solver in self.chemicalSolvers:
            layout.addWidget(self.chemicalSolvers[solver], 5 + index, 1)
            self.chemicalSolver.addButton(self.chemicalSolvers[solver], index)
            self.chemicalSolvers[solver].setFocusPolicy(QtCore.Qt.NoFocus)
            index += 1

        self.chemicalSolver.setExclusive(True)

        buttonLayout = QGridLayout()
        layout.addLayout(buttonLayout, 5 + index, 1)
        buttonLayout.addWidget(self.chemicalSimulationCancel, 0, 0, Qt.AlignRight)
        buttonLayout.addWidget(self.chemicalSimulationApply, 0, 1, Qt.AlignLeft)


        return chemicalSettingsTab

    def createElectricalSettingsTab(self):

        electricalSettingsTab = QTabWidget()
        electricalSettingsTab.addTab( self.createElectricalSimulationSettingsTab()
                                    , "Simulation"
                                    )
        electricalSettingsTab.addTab( self.createElectricalSimulationVisualizationTab()
                                    , "Visualization"
                                    )
        electricalSettingsTab.setTabPosition(QTabWidget.East)
        electricalSettingsTab.setTabShape(QTabWidget.Triangular)
        electricalSettingsTab.setDocumentMode(True)
        electricalSettingsTab.setUsesScrollButtons(True)
        electricalSettingsTab.setFocusPolicy(QtCore.Qt.NoFocus)
        return electricalSettingsTab

    def createElectricalSimulationSettingsTab(self):

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        layout.addWidget(QLabel('Simulation dt'), 0, 0)
        layout.addWidget(self.electricalSimulationDt, 0, 1)

        layout.addWidget(QLabel('Plot Update Interval'), 2, 0)
        layout.addWidget(self.electricalPlotUpdateInterval, 2, 1)

        layout.addWidget(QLabel('GUI Update Interval'), 3, 0)
        layout.addWidget(self.electricalGuiUpdateInterval, 3, 1)

        # layout.addWidget(QLabel('Default Runtime'), 4, 0)
        # layout.addWidget(self.electricalDefaultSimulationRuntime, 4, 1)

        # layout.addWidget(QLabel('Solver'), 5, 0)

        index = 0
        for solver in self.electricalSolvers:
            # layout.addWidget(self.electricalSolvers[solver], 5 + index, 1)
            self.electricalSolver.addButton(self.electricalSolvers[solver], index)
            self.electricalSolvers[solver].setFocusPolicy(QtCore.Qt.NoFocus)
            index += 1

        self.electricalSolver.setExclusive(True)
        buttonLayout = QGridLayout()
        layout.addLayout(buttonLayout, 5 + index, 1)
        buttonLayout.addWidget(self.electricalSimulationCancel, 0, 0, Qt.AlignRight)
        buttonLayout.addWidget(self.electricalSimulationApply, 0, 1, Qt.AlignLeft)

        return widget

    def createElectricalSimulationVisualizationTab(self):

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        layout.addWidget(QLabel('Base Membrane Voltage'), 1, 0)
        layout.addWidget(self.electricalBaseMembraneVoltage, 1, 1)

        layout.addWidget(QLabel('Base Compartment Color'), 2, 0)
        self.electricalBaseColorDialog.setOption(QColorDialog.ShowAlphaChannel, True)
        layout.addWidget(self.electricalBaseColorButton, 2, 1)
        self.electricalBaseColorButton.clicked.connect(self.electricalBaseColorDialog.show)
        self.electricalBaseColorButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.electricalBaseColorDialog.colorSelected.connect(
            lambda color: self.electricalBaseColorButton.setStyleSheet(
                        "QPushButton {"
                    +   "background-color: {0}; color: {0};".format(color.name())
                    +   "}"
                                                                         )
                                                                )

        layout.addWidget(QLabel('Peak Membrane Voltage'), 3, 0)
        layout.addWidget(self.electricalPeakMembraneVoltage, 3, 1)

        layout.addWidget(QLabel('Peak Compartment Color'), 4, 0)
        self.electricalPeakColorDialog.setOption(QColorDialog.ShowAlphaChannel, True)
        layout.addWidget(self.electricalPeakColorButton, 4, 1)
        self.electricalPeakColorButton.clicked.connect(self.electricalPeakColorDialog.show)
        self.electricalPeakColorButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.electricalPeakColorDialog.colorSelected.connect(
            lambda color: self.electricalPeakColorButton.setStyleSheet(
                        "QPushButton {"
                    +   "background-color: {0}; color: {0};".format(color.name())
                    +   "}"
                                                                         )
                                                                )

        layout.addWidget(QLabel('Background Color'), 5, 0)
        self.electricalBackgroundColorDialog.setOption(QColorDialog.ShowAlphaChannel, True)
        layout.addWidget(self.electricalBackgroundColorButton, 5, 1)
        self.electricalBackgroundColorButton.clicked.connect(self.electricalBackgroundColorDialog.show)
        self.electricalBackgroundColorButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.electricalBackgroundColorDialog.colorSelected.connect(
            lambda color: self.electricalBackgroundColorButton.setStyleSheet(
                        "QPushButton {"
                    +   "background-color: {0}; color: {0};".format(color.name())
                    +   "}"
                                                                         )
                                                                )
        buttonLayout = QGridLayout()
        layout.addLayout(buttonLayout, 6, 1)
        buttonLayout.addWidget(self.electricalVisualizationCancel, 0, 0, Qt.AlignRight)
        buttonLayout.addWidget(self.electricalVisualizationApply, 0, 1, Qt.AlignLeft)

        return widget

    def createFloatingPointEditor(self, value = 0.0, minValue = float("-inf"), maxValue = float("+inf"), decimals = 1000):
        floatingPointEditor = QLineEdit(str(value))
        floatingPointEditor.setValidator(QtGui.QDoubleValidator(minValue, maxValue, decimals))
        return floatingPointEditor

def main():
    app     = QApplication(sys.argv)
    widget  = PreferencesView()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
