import sys, os
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

PROJECT_TYPE = [
    "Обычный",
    "Промежуточный",
    "Встроенный"
]

TYPE = {
    'C1': [3.2, 3.0, 2.8],
    'p1': [1.05, 1.12, 1.2],
    'C2': [2.5, 2.5, 2.5],
    'p2': [0.38, 0.35, 0.32]
}

ATTRIBUTES = {
    'RELY': [0.75, 0.86, 1.0, 1.15, 1.40],
    'DATA': [0.94, 1.0, 1.08, 1.16],
    'CPLX': [0.70, 0.85, 1.0, 1.15, 1.30],

    'TIME': [1.0, 1.11, 1.50],
    'STOR': [1.0, 1.06, 1.21],
    'VIRT': [0.87, 1.0, 1.15, 1.30],
    'TURN': [0.87, 1.0, 1.07, 1.15],

    'ACAP': [1.46, 1.19, 1.0, 0.86, 0.71],
    'AEXP': [1.29, 1.15, 1.0, 0.91, 0.82],
    'PCAP': [1.42, 1.17, 1.0, 0.86, 0.70],
    'VEXP': [1.21, 1.10, 1.0, 0.90],
    'LEXP': [1.14, 1.07, 1.0, 0.95],

    'MODP': [1.24, 1.10, 1.0, 0.91, 0.82],
    'TOOL': [1.24, 1.10, 1.0, 0.91, 0.82],
    'SCED': [1.23, 1.08, 1.0, 1.04, 1.10]
}

PERCENTAGE = {
    'PM': [0.08, 0.18, 0.25, 0.26, 0.31],
    'TM': [0.36, 0.36, 0.18, 0.18, 0.28]
}

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi('widget.ui', self)

        self.RELY: QComboBox = self.ui.comboBox_1
        self.DATA: QComboBox = self.ui.comboBox_2
        self.CPLX: QComboBox = self.ui.comboBox_3
        self.TIME: QComboBox = self.ui.comboBox_4
        self.STOR: QComboBox = self.ui.comboBox_5
        self.VIRT: QComboBox = self.ui.comboBox_6
        self.TURN: QComboBox = self.ui.comboBox_7
        self.ACAP: QComboBox = self.ui.comboBox_8
        self.AEXP: QComboBox = self.ui.comboBox_9
        self.PCAP: QComboBox = self.ui.comboBox_10
        self.VEXP: QComboBox = self.ui.comboBox_11
        self.LEXP: QComboBox = self.ui.comboBox_12
        self.MODP: QComboBox = self.ui.comboBox_13
        self.TOOL: QComboBox = self.ui.comboBox_14
        self.SCED: QComboBox = self.ui.comboBox_15
        
        self.size: QLineEdit = self.ui.sizeEdit
        self.type: QComboBox = self.ui.comboBox_16

        self.ui.wbsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.classicTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def fill_table(self, pm, tm, pm_clean, tm_clean):
        for i in range(8):
            self.ui.wbsTable.setItem(i, 1, QTableWidgetItem(
                str(round(pm * int(self.ui.wbsTable.item(i, 0).text()) / 100.0, 2))))
        self.ui.wbsTable.setItem(8, 1, QTableWidgetItem(str(pm)))

        self.ui.classicTable.setItem(0, 0, QTableWidgetItem(str(round(pm_clean * PERCENTAGE['PM'][0], 2))))
        self.ui.classicTable.setItem(1, 0, QTableWidgetItem(str(round(pm_clean * PERCENTAGE['PM'][1], 2))))
        self.ui.classicTable.setItem(2, 0, QTableWidgetItem(str(round(pm_clean * PERCENTAGE['PM'][2], 2))))
        self.ui.classicTable.setItem(3, 0, QTableWidgetItem(str(round(pm_clean * PERCENTAGE['PM'][3], 2))))
        self.ui.classicTable.setItem(4, 0, QTableWidgetItem(str(round(pm_clean * PERCENTAGE['PM'][4], 2))))
        self.ui.classicTable.setItem(5, 0, QTableWidgetItem(str(round(pm_clean, 2))))
        self.ui.classicTable.setItem(6, 0, QTableWidgetItem(str(round(pm, 2))))
        self.ui.classicTable.setItem(0, 1, QTableWidgetItem(str(round(tm_clean * PERCENTAGE['TM'][0], 2))))
        self.ui.classicTable.setItem(1, 1, QTableWidgetItem(str(round(tm_clean * PERCENTAGE['TM'][1], 2))))
        self.ui.classicTable.setItem(2, 1, QTableWidgetItem(str(round(tm_clean * PERCENTAGE['TM'][2], 2))))
        self.ui.classicTable.setItem(3, 1, QTableWidgetItem(str(round(tm_clean * PERCENTAGE['TM'][3], 2))))
        self.ui.classicTable.setItem(4, 1, QTableWidgetItem(str(round(tm_clean * PERCENTAGE['TM'][4], 2))))
        self.ui.classicTable.setItem(5, 1, QTableWidgetItem(str(round(tm_clean, 2))))
        self.ui.classicTable.setItem(6, 1, QTableWidgetItem(str(round(tm, 2))))


    def eaf(self):
        RELY = ATTRIBUTES['RELY'][self.RELY.currentIndex()]
        DATA = ATTRIBUTES['DATA'][self.DATA.currentIndex()]
        CPLX = ATTRIBUTES['CPLX'][self.CPLX.currentIndex()]
        TIME = ATTRIBUTES['TIME'][self.TIME.currentIndex()]
        STOR = ATTRIBUTES['STOR'][self.STOR.currentIndex()]
        VIRT = ATTRIBUTES['VIRT'][self.VIRT.currentIndex()]
        TURN = ATTRIBUTES['TURN'][self.TURN.currentIndex()]
        ACAP = ATTRIBUTES['ACAP'][self.ACAP.currentIndex()]
        AEXP = ATTRIBUTES['AEXP'][self.AEXP.currentIndex()]
        PCAP = ATTRIBUTES['PCAP'][self.PCAP.currentIndex()]
        VEXP = ATTRIBUTES['VEXP'][self.VEXP.currentIndex()]
        LEXP = ATTRIBUTES['LEXP'][self.LEXP.currentIndex()]
        MODP = ATTRIBUTES['MODP'][self.MODP.currentIndex()]
        TOOL = ATTRIBUTES['TOOL'][self.TOOL.currentIndex()]
        SCED = ATTRIBUTES['SCED'][self.SCED.currentIndex()]

        return RELY * DATA * CPLX * TIME * STOR * VIRT * TURN * ACAP * AEXP * PCAP * VEXP * LEXP * MODP * TOOL * SCED

    #Обычный вариант
    def PM(self, C1, p1, EAF, SIZE):
        return C1 * EAF * (SIZE ** p1)

    def TM(self, C2, p2, PM):
        return C2 * (PM ** p2)

    def calc_EAF(self, params: list):
        return np.prod(params)


    def plot_bar(self, table):
        y = []
        for i in range(5):
            t = round(float(table.item(i, 1).text()))
            for j in range(t):
                y.append(round(round(float(table.item(i, 0).text())) / t))

        x = [i + 1 for i in range(len(y))]

        plt.bar(x, y)
        plt.grid()
        plt.show()


    def plot(self, t, MODP, TOOL):
        y_modp_pm = []
        y_modp_tm = []

        y_tool_pm = []
        y_tool_tm = []

        y_sced_pm = []
        y_sced_tm = []

        x = [1, 2, 3]
        sced = ATTRIBUTES['SCED'][self.SCED.currentIndex()]
        for i in range(1, 4):
            y_modp_pm.append(self.PM(TYPE['C1'][t], TYPE['p1'][t], self.calc_EAF([
                ATTRIBUTES['MODP'][i], sced
            ]), 50))
            y_modp_tm.append(self.TM(TYPE['C2'][t], TYPE['p2'][t], y_modp_pm[-1]))

            y_tool_pm.append(self.PM(TYPE['C1'][t], TYPE['p1'][t], self.calc_EAF([
                ATTRIBUTES['TOOL'][i], sced
            ]), 50))
            y_tool_tm.append(self.TM(TYPE['C2'][t], TYPE['p2'][t], y_tool_pm[-1]))

            y_sced_pm.append(self.PM(TYPE['C1'][t], TYPE['p1'][t], self.calc_EAF([
                ATTRIBUTES['SCED'][i]
            ]), 50))
            y_sced_tm.append(self.TM(TYPE['C2'][t], TYPE['p2'][t], y_sced_pm[-1]))

        mpl.style.use('seaborn')
        plt.suptitle(f'Режим проекта: {PROJECT_TYPE[t]}')

        plt.subplot(121)
        plt.title('Трудоемкость')
        line1, = plt.plot(x, y_modp_pm, 'r', label='MODP')
        line2, = plt.plot(x, y_tool_pm, 'g', label='TOOL')
        #line3, = plt.plot(x, y_sced_pm, 'b', label='SCED')
        #plt.legend(handles=[line1, line2, line3])
        #plt.legend(handles=[line1, line2])


        plt.subplot(122)
        plt.title('Время разработки')
        line4, = plt.plot(x, y_modp_tm, 'r', label='MODP')
        line5, = plt.plot(x, y_tool_tm, 'g', label='TOOL')
        #line6, = plt.plot(x, y_sced_tm, 'b', label='SCED')
        #plt.legend(handles=[line4, line5, line6])
        plt.legend(handles=[line4, line5,])

        plt.show()

    
    @pyqtSlot(name="on_calculateButton_clicked")
    def calculate_project(self):
        pm, tm, pm_clean, tm_clean = self.calculate()

        self.ui.pmLine.setText(str(pm))
        self.ui.tmLine.setText(str(tm))
        self.fill_table(pm, tm, pm_clean, tm_clean)

        self.plot(self.type.currentIndex(), self.MODP.currentIndex(), self.TOOL.currentIndex())


    def calculate(self):
        try:
            mode = self.type.currentIndex()
            size = float(self.size.text())
        except:
            return

        PM = TYPE['C1'][mode] * self.eaf() * (size ** TYPE['p1'][mode])
        TM = TYPE['C2'][mode] * (PM ** TYPE['p2'][mode])

        pm_clean = round(PM, 2)
        tm_clean = round(TM, 2)
        pm = round(pm_clean * 1.08, 2)
        tm = round(tm_clean * 1.36, 2)

        return pm, tm, pm_clean, tm_clean


    @pyqtSlot(name="on_barButton_clicked")
    def bar_clicked(self):
        self.plot_bar(self.ui.classicTable)    

    