# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'miasmod.ui'
#
# Created: Sat May  3 20:45:52 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(935, 621)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.mods_tab = QtGui.QWidget()
        self.mods_tab.setObjectName("mods_tab")
        self.gridLayout_2 = QtGui.QGridLayout(self.mods_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rs5_mod_list = QtGui.QTableView(self.mods_tab)
        self.rs5_mod_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.rs5_mod_list.setAlternatingRowColors(True)
        self.rs5_mod_list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.rs5_mod_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.rs5_mod_list.setShowGrid(False)
        self.rs5_mod_list.setObjectName("rs5_mod_list")
        self.rs5_mod_list.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.rs5_mod_list, 2, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.open_environment = QtGui.QPushButton(self.mods_tab)
        self.open_environment.setObjectName("open_environment")
        self.verticalLayout.addWidget(self.open_environment)
        self.new_mod = QtGui.QPushButton(self.mods_tab)
        self.new_mod.setObjectName("new_mod")
        self.verticalLayout.addWidget(self.new_mod)
        self.open_saves_dat = QtGui.QPushButton(self.mods_tab)
        self.open_saves_dat.setObjectName("open_saves_dat")
        self.verticalLayout.addWidget(self.open_saves_dat)
        self.refresh_mod_list = QtGui.QPushButton(self.mods_tab)
        self.refresh_mod_list.setObjectName("refresh_mod_list")
        self.verticalLayout.addWidget(self.refresh_mod_list)
        self.synchronise_local_mod = QtGui.QPushButton(self.mods_tab)
        self.synchronise_local_mod.setObjectName("synchronise_local_mod")
        self.verticalLayout.addWidget(self.synchronise_local_mod)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.mod_list = QtGui.QTableView(self.mods_tab)
        self.mod_list.setAlternatingRowColors(True)
        self.mod_list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.mod_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.mod_list.setShowGrid(False)
        self.mod_list.setObjectName("mod_list")
        self.mod_list.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.mod_list, 0, 1, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.install_rs5mod = QtGui.QPushButton(self.mods_tab)
        self.install_rs5mod.setObjectName("install_rs5mod")
        self.verticalLayout_4.addWidget(self.install_rs5mod)
        self.revert_main_rs5 = QtGui.QPushButton(self.mods_tab)
        self.revert_main_rs5.setObjectName("revert_main_rs5")
        self.verticalLayout_4.addWidget(self.revert_main_rs5)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 2, 0, 1, 1)
        self.line = QtGui.QFrame(self.mods_tab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 1, 1, 1)
        self.line_2 = QtGui.QFrame(self.mods_tab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.mods_tab, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 935, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Remove_Mod = QtGui.QAction(MainWindow)
        self.action_Remove_Mod.setObjectName("action_Remove_Mod")
        self.actionSet_Lowest_Priority = QtGui.QAction(MainWindow)
        self.actionSet_Lowest_Priority.setObjectName("actionSet_Lowest_Priority")
        self.actionSet_Highest_Priority = QtGui.QAction(MainWindow)
        self.actionSet_Highest_Priority.setObjectName("actionSet_Highest_Priority")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.refresh_mod_list, QtCore.SIGNAL("clicked()"), MainWindow.refresh_mod_list)
        QtCore.QObject.connect(self.open_environment, QtCore.SIGNAL("clicked()"), MainWindow.open_alocalmod)
        QtCore.QObject.connect(self.synchronise_local_mod, QtCore.SIGNAL("clicked()"), MainWindow.synchronise_alocalmod)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.open_environment)
        MainWindow.setTabOrder(self.open_environment, self.new_mod)
        MainWindow.setTabOrder(self.new_mod, self.open_saves_dat)
        MainWindow.setTabOrder(self.open_saves_dat, self.refresh_mod_list)
        MainWindow.setTabOrder(self.refresh_mod_list, self.synchronise_local_mod)
        MainWindow.setTabOrder(self.synchronise_local_mod, self.mod_list)
        MainWindow.setTabOrder(self.mod_list, self.install_rs5mod)
        MainWindow.setTabOrder(self.install_rs5mod, self.revert_main_rs5)
        MainWindow.setTabOrder(self.revert_main_rs5, self.rs5_mod_list)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Miasmod - Miasmata Advanced Configuration and Modding Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.open_environment.setText(QtGui.QApplication.translate("MainWindow", "Open local &environment...", None, QtGui.QApplication.UnicodeUTF8))
        self.new_mod.setText(QtGui.QApplication.translate("MainWindow", "&New Mod...", None, QtGui.QApplication.UnicodeUTF8))
        self.open_saves_dat.setText(QtGui.QApplication.translate("MainWindow", "Open &saves.dat...", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_mod_list.setText(QtGui.QApplication.translate("MainWindow", "&Refresh Mod List", None, QtGui.QApplication.UnicodeUTF8))
        self.synchronise_local_mod.setText(QtGui.QApplication.translate("MainWindow", "S&ynchronise alocalmod.rs5", None, QtGui.QApplication.UnicodeUTF8))
        self.install_rs5mod.setText(QtGui.QApplication.translate("MainWindow", "&Install main.rs5 mod...", None, QtGui.QApplication.UnicodeUTF8))
        self.revert_main_rs5.setText(QtGui.QApplication.translate("MainWindow", "Restore original main.rs5", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mods_tab), QtGui.QApplication.translate("MainWindow", "Mod List", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Remove_Mod.setText(QtGui.QApplication.translate("MainWindow", "&Remove Mod", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_Lowest_Priority.setText(QtGui.QApplication.translate("MainWindow", "Set &Lowest Priority", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_Highest_Priority.setText(QtGui.QApplication.translate("MainWindow", "Set &Highest Priority", None, QtGui.QApplication.UnicodeUTF8))

