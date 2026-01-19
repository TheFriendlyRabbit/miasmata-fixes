# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'miaschiev.ui'
#
# Created: Wed Aug 06 17:13:17 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QWidget, QLabel, \
    QVBoxLayout, QGridLayout, QLineEdit, QFormLayout, QPushButton, \
    QSpacerItem, QSizePolicy, QScrollArea, QStatusBar, QHBoxLayout


class Ui_Miaschiev():
    def setupUi(self, Miaschiev):
        Miaschiev.setObjectName("Miaschiev")
        Miaschiev.setWindowIcon(QtGui.QIcon('imageformats/miasmod.ico'))
        Miaschiev.resize(1333, 860)
        self.centralwidget = QWidget(Miaschiev)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.install_path = QLineEdit(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Minimum,
                                  QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.install_path.sizePolicy().hasHeightForWidth())
        self.install_path.setSizePolicy(size_policy)
        self.install_path.setObjectName("install_path")
        self.gridLayout.addWidget(self.install_path, 2, 0, 1, 1)
        self.save_browse = QPushButton(self.centralwidget)
        self.save_browse.setObjectName("save_browse")
        self.gridLayout.addWidget(self.save_browse, 4, 1, 1, 1)
        self.install_browse = QPushButton(self.centralwidget)
        self.install_browse.setObjectName("install_browse")
        self.gridLayout.addWidget(self.install_browse, 2, 1, 1, 1)
        self.save_path = QLineEdit(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Minimum,
                                  QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.save_path.sizePolicy().hasHeightForWidth())
        self.save_path.setSizePolicy(size_policy)
        self.save_path.setObjectName("save_path")
        self.gridLayout.addWidget(self.save_path, 4, 0, 1, 1)
        self.label_2 = QLabel(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Minimum,
                                  QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(size_policy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 2)
        self.label = QLabel(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Minimum,
                                  QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(size_policy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        spacer_item = QSpacerItem(20, 32, QSizePolicy.Minimum,
                                  QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacer_item)
        self.save0 = QPushButton(self.centralwidget)
        self.save0.setEnabled(False)
        self.save0.setMinimumSize(QtCore.QSize(0, 38))
        self.save0.setMaximumSize(QtCore.QSize(416, 16777215))
        self.save0.setObjectName("save0")
        self.verticalLayout.addWidget(self.save0)
        self.save1 = QPushButton(self.centralwidget)
        self.save1.setEnabled(False)
        self.save1.setMinimumSize(QtCore.QSize(0, 38))
        self.save1.setMaximumSize(QtCore.QSize(416, 16777215))
        self.save1.setObjectName("save1")
        self.verticalLayout.addWidget(self.save1)
        self.save2 = QPushButton(self.centralwidget)
        self.save2.setEnabled(False)
        self.save2.setMinimumSize(QtCore.QSize(0, 38))
        self.save2.setMaximumSize(QtCore.QSize(416, 16777215))
        self.save2.setObjectName("save2")
        self.verticalLayout.addWidget(self.save2)
        spacer_item1 = QSpacerItem(20, 32, QSizePolicy.Minimum,
                                   QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacer_item1)
        self.formLayout = QFormLayout()
        self.formLayout.setFieldGrowthPolicy(
            QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.lbl_coast = QLabel(self.centralwidget)
        self.lbl_coast.setEnabled(False)
        self.lbl_coast.setObjectName("lbl_coast")
        self.formLayout.setWidget(1, QFormLayout.LabelRole,
                                  self.lbl_coast)
        self.show_coast = QPushButton(self.centralwidget)
        self.show_coast.setEnabled(False)
        self.show_coast.setObjectName("show_coast")
        self.formLayout.setWidget(2, QFormLayout.SpanningRole,
                                  self.show_coast)
        spacer_item2 = QSpacerItem(20, 16, QSizePolicy.Minimum,
                                   QSizePolicy.Maximum)
        self.formLayout.setItem(3, QFormLayout.SpanningRole, spacer_item2)
        self.lbl_urns = QLabel(self.centralwidget)
        self.lbl_urns.setEnabled(False)
        self.lbl_urns.setObjectName("lbl_urns")
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lbl_urns)
        self.urns = QLabel(self.centralwidget)
        self.urns.setText("")
        self.urns.setObjectName("urns")
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.urns)
        self.show_urns = QPushButton(self.centralwidget)
        self.show_urns.setEnabled(False)
        self.show_urns.setObjectName("show_urns")
        self.formLayout.setWidget(5, QFormLayout.SpanningRole,
                                  self.show_urns)
        spacer_item3 = QSpacerItem(20, 16, QSizePolicy.Minimum,
                                   QSizePolicy.Maximum)
        self.formLayout.setItem(6, QFormLayout.SpanningRole, spacer_item3)
        self.lbl_heads = QLabel(self.centralwidget)
        self.lbl_heads.setEnabled(False)
        self.lbl_heads.setObjectName("lbl_heads")
        self.formLayout.setWidget(7, QFormLayout.LabelRole,
                                  self.lbl_heads)
        self.heads = QLabel(self.centralwidget)
        self.heads.setObjectName("heads")
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.heads)
        self.show_heads = QPushButton(self.centralwidget)
        self.show_heads.setEnabled(False)
        self.show_heads.setObjectName("show_heads")
        self.formLayout.setWidget(8, QFormLayout.LabelRole,
                                  self.show_heads)
        self.reset_head = QPushButton(self.centralwidget)
        self.reset_head.setEnabled(False)
        self.reset_head.setObjectName("reset_head")
        self.formLayout.setWidget(8, QFormLayout.FieldRole,
                                  self.reset_head)
        spacer_item4 = QSpacerItem(20, 16, QSizePolicy.Minimum,
                                   QSizePolicy.Maximum)
        self.formLayout.setItem(9, QFormLayout.SpanningRole, spacer_item4)
        self.lbl_notes = QLabel(self.centralwidget)
        self.lbl_notes.setEnabled(False)
        self.lbl_notes.setObjectName("lbl_notes")
        self.formLayout.setWidget(10, QFormLayout.LabelRole,
                                  self.lbl_notes)
        self.notes = QLabel(self.centralwidget)
        self.notes.setText("")
        self.notes.setObjectName("notes")
        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.notes)
        self.reset_notezz = QPushButton(self.centralwidget)
        self.reset_notezz.setEnabled(False)
        self.reset_notezz.setObjectName("reset_notezz")
        self.formLayout.setWidget(11, QFormLayout.SpanningRole,
                                  self.reset_notezz)
        spacer_item5 = QSpacerItem(20, 16, QSizePolicy.Minimum,
                                   QSizePolicy.Maximum)
        self.formLayout.setItem(12, QFormLayout.SpanningRole,
                                spacer_item5)
        self.lbl_plants = QLabel(self.centralwidget)
        self.lbl_plants.setEnabled(False)
        self.lbl_plants.setObjectName("lbl_plants")
        self.formLayout.setWidget(13, QFormLayout.LabelRole,
                                  self.lbl_plants)
        self.plants = QLabel(self.centralwidget)
        self.plants.setText("")
        self.plants.setObjectName("plants")
        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.plants)
        self.coast = QLabel(self.centralwidget)
        self.coast.setText("")
        self.coast.setObjectName("coast")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.coast)
        self.verticalLayout.addLayout(self.formLayout)
        spacer_item6 = QSpacerItem(20, 32, QSizePolicy.Minimum,
                                   QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacer_item6)
        self.save_map = QPushButton(self.centralwidget)
        self.save_map.setEnabled(False)
        self.save_map.setObjectName("save_map")
        self.verticalLayout.addWidget(self.save_map)
        spacer_item7 = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                   QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item7)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(768, 0))
        self.scrollArea.setBaseSize(QtCore.QSize(1024, 1024))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(
            QtCore.QRect(0, 0, 1024, 1024))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(1024, 1024))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        Miaschiev.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(Miaschiev)
        self.statusBar.setObjectName("statusBar")
        Miaschiev.setStatusBar(self.statusBar)

        self.retranslate_ui(Miaschiev)
        QtCore.QMetaObject.connectSlotsByName(Miaschiev)
        Miaschiev.setTabOrder(self.install_path, self.install_browse)
        Miaschiev.setTabOrder(self.install_browse, self.save_path)
        Miaschiev.setTabOrder(self.save_path, self.save_browse)
        Miaschiev.setTabOrder(self.save_browse, self.save0)
        Miaschiev.setTabOrder(self.save0, self.save1)
        Miaschiev.setTabOrder(self.save1, self.save2)
        Miaschiev.setTabOrder(self.save2, self.show_coast)
        Miaschiev.setTabOrder(self.show_coast, self.show_urns)
        Miaschiev.setTabOrder(self.show_urns, self.show_heads)
        Miaschiev.setTabOrder(self.show_heads, self.reset_head)
        Miaschiev.setTabOrder(self.reset_head, self.reset_notezz)
        Miaschiev.setTabOrder(self.reset_notezz, self.scrollArea)

    def retranslate_ui(self, Miaschiev):
        Miaschiev.setWindowTitle(
            QApplication.translate("Miaschiev", "Mias(Achievement)mata", None))
        self.save_browse.setText(
            QApplication.translate("Miaschiev", "Browse...", None))
        self.install_browse.setText(
            QApplication.translate("Miaschiev", "Browse...", None))
        self.label_2.setText(QApplication.translate("Miaschiev",
                                                    "Miasmata Saved Games "
                                                    "Location:",
                                                    None))
        self.label.setText(
            QApplication.translate("Miaschiev", "Miasmata Install Location:",
                                   None))
        self.save0.setText(
            QApplication.translate("Miaschiev", "Load Save Slot 1", None))
        self.save1.setText(
            QApplication.translate("Miaschiev", "Load Save Slot 2", None))
        self.save2.setText(
            QApplication.translate("Miaschiev", "Load Save Slot 3", None))
        self.lbl_coast.setText(
            QApplication.translate("Miaschiev", "Coastline Mapped:", None))
        self.show_coast.setText(
            QApplication.translate("Miaschiev", "Show Mapped Coastline", None))
        self.lbl_urns.setText(
            QApplication.translate("Miaschiev", "Urns Lit:", None))
        self.show_urns.setText(
            QApplication.translate("Miaschiev", "Show Lit Urns", None))
        self.lbl_heads.setText(
            QApplication.translate("Miaschiev", "Head Statues Located:", None))
        self.show_heads.setText(
            QApplication.translate("Miaschiev", "Show", None))
        self.reset_head.setText(
            QApplication.translate("Miaschiev", "Reset one statue...", None))
        self.lbl_notes.setText(
            QApplication.translate("Miaschiev", "Notes Found:", None))
        self.reset_notezz.setText(QApplication.translate("Miaschiev",
                                                         "Reset missing "
                                                         "Sanchez #1 note...",
                                                         None))
        self.lbl_plants.setText(
            QApplication.translate("Miaschiev", "Plants Found:", None))
        self.save_map.setText(
            QApplication.translate("Miaschiev", "Save current map to file...",
                                   None))
