# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'miasmod_data.ui'
#
# Created: Tue Apr 29 18:40:05 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, \
    QPushButton, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QTreeView, \
    QFormLayout, QComboBox, QGridLayout, QListView, QPlainTextEdit


class Ui_MiasmataData(object):
    def setupUi(self, MiasmataData):
        MiasmataData.setObjectName("MiasmataData")
        MiasmataData.setWindowIcon(QtGui.QIcon('imageformats/miasmod.ico'))
        MiasmataData.resize(713, 490)
        self.verticalLayout_3 = QVBoxLayout(MiasmataData)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.save = QPushButton(MiasmataData)
        self.save.setEnabled(False)
        self.save.setObjectName("save")
        self.horizontalLayout_2.addWidget(self.save)
        self.show_diff = QPushButton(MiasmataData)
        self.show_diff.setEnabled(False)
        self.show_diff.setObjectName("show_diff")
        self.horizontalLayout_2.addWidget(self.show_diff)
        self.lblVersion = QLabel(MiasmataData)
        self.lblVersion.setEnabled(False)
        self.lblVersion.setObjectName("lblVersion")
        self.horizontalLayout_2.addWidget(self.lblVersion)
        self.version = QLineEdit(MiasmataData)
        self.version.setEnabled(False)
        self.version.setMaximumSize(QtCore.QSize(84, 16777215))
        self.version.setObjectName("version")
        self.horizontalLayout_2.addWidget(self.version)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Expanding,
                                 QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QTreeView(MiasmataData)
        self.treeView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAllColumnsShowFocus(True)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QLabel(MiasmataData)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.search = QLineEdit(MiasmataData)
        self.search.setObjectName("search")
        self.horizontalLayout_3.addWidget(self.search)
        self.clear_search = QPushButton(MiasmataData)
        self.clear_search.setObjectName("clear_search")
        self.horizontalLayout_3.addWidget(self.clear_search)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QLabel(MiasmataData)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)
        self.name = QLineEdit(MiasmataData)
        self.name.setReadOnly(True)
        self.name.setObjectName("name")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.name)
        self.type = QComboBox(MiasmataData)
        self.type.setEnabled(False)
        self.type.setObjectName("type")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.type)
        self.label_2 = QLabel(MiasmataData)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)
        self.label_3 = QLabel(MiasmataData)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)
        self.value_line = QLineEdit(MiasmataData)
        self.value_line.setObjectName("value_line")
        self.formLayout.setWidget(3, QFormLayout.FieldRole,
                                  self.value_line)
        self.verticalLayout_2.addLayout(self.formLayout)
        spacerItem1 = QSpacerItem(20, 0, QSizePolicy.Minimum,
                                  QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.value_list = QListView(MiasmataData)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(
            self.value_list.sizePolicy().hasHeightForWidth())
        self.value_list.setSizePolicy(sizePolicy)
        self.value_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.value_list.setAlternatingRowColors(True)
        self.value_list.setUniformItemSizes(True)
        self.value_list.setObjectName("value_list")
        self.verticalLayout_2.addWidget(self.value_list)
        self.value_hex = QPlainTextEdit(MiasmataData)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(
            self.value_hex.sizePolicy().hasHeightForWidth())
        self.value_hex.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setWeight(QtGui.QFont.Weight.Thin)
        font.setBold(True)
        self.value_hex.setFont(font)
        self.value_hex.setReadOnly(True)
        self.value_hex.setObjectName("value_hex")
        self.verticalLayout_2.addWidget(self.value_hex)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 1, 1, 1)
        self.new_key = QPushButton(MiasmataData)
        self.new_key.setEnabled(False)
        self.new_key.setObjectName("new_key")
        self.gridLayout_2.addWidget(self.new_key, 1, 0, 1, 1)
        self.delete_node = QPushButton(MiasmataData)
        self.delete_node.setEnabled(False)
        self.delete_node.setObjectName("delete_node")
        self.gridLayout_2.addWidget(self.delete_node, 2, 2, 1, 1)
        self.new_value = QPushButton(MiasmataData)
        self.new_value.setEnabled(False)
        self.new_value.setObjectName("new_value")
        self.gridLayout_2.addWidget(self.new_value, 2, 0, 1, 1)
        self.undo = QPushButton(MiasmataData)
        self.undo.setEnabled(False)
        self.undo.setObjectName("undo")
        self.gridLayout_2.addWidget(self.undo, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.actionNew_Key = QtGui.QAction(MiasmataData)
        self.actionNew_Key.setObjectName("actionNew_Key")
        self.actionNew_Value = QtGui.QAction(MiasmataData)
        self.actionNew_Value.setObjectName("actionNew_Value")
        self.actionUndo_Changes = QtGui.QAction(MiasmataData)
        self.actionUndo_Changes.setObjectName("actionUndo_Changes")
        self.actionDelete = QtGui.QAction(MiasmataData)
        self.actionDelete.setObjectName("actionDelete")
        self.actionInsert_Row = QtGui.QAction(MiasmataData)
        self.actionInsert_Row.setObjectName("actionInsert_Row")
        self.actionRemove_Row = QtGui.QAction(MiasmataData)
        self.actionRemove_Row.setObjectName("actionRemove_Row")
        self.lblVersion.setBuddy(self.version)
        self.label_4.setBuddy(self.search)
        self.label.setBuddy(self.name)
        self.label_2.setBuddy(self.type)
        self.label_3.setBuddy(self.value_line)

        self.retranslateUi(MiasmataData)
        QtCore.QObject.connect(self.actionNew_Key, QtCore.SIGNAL("triggered()"),
                               MiasmataData.insert_key)
        QtCore.QObject.connect(self.actionNew_Value,
                               QtCore.SIGNAL("triggered()"),
                               MiasmataData.insert_value)
        QtCore.QObject.connect(self.new_key, QtCore.SIGNAL("clicked()"),
                               MiasmataData.insert_key)
        QtCore.QObject.connect(self.new_value, QtCore.SIGNAL("clicked()"),
                               MiasmataData.insert_value)
        QtCore.QObject.connect(self.delete_node, QtCore.SIGNAL("clicked()"),
                               MiasmataData.delete_node)
        QtCore.QObject.connect(self.undo, QtCore.SIGNAL("clicked()"),
                               MiasmataData.undo)
        QtCore.QObject.connect(self.actionUndo_Changes,
                               QtCore.SIGNAL("triggered()"), MiasmataData.undo)
        QtCore.QObject.connect(self.actionDelete, QtCore.SIGNAL("triggered()"),
                               MiasmataData.delete_node)
        QtCore.QObject.connect(self.clear_search, QtCore.SIGNAL("clicked()"),
                               self.search.clear)
        QtCore.QMetaObject.connectSlotsByName(MiasmataData)
        MiasmataData.setTabOrder(self.treeView, self.search)
        MiasmataData.setTabOrder(self.search, self.clear_search)
        MiasmataData.setTabOrder(self.clear_search, self.name)
        MiasmataData.setTabOrder(self.name, self.type)
        MiasmataData.setTabOrder(self.type, self.value_line)
        MiasmataData.setTabOrder(self.value_line, self.value_list)
        MiasmataData.setTabOrder(self.value_list, self.value_hex)
        MiasmataData.setTabOrder(self.value_hex, self.new_key)
        MiasmataData.setTabOrder(self.new_key, self.new_value)
        MiasmataData.setTabOrder(self.new_value, self.undo)
        MiasmataData.setTabOrder(self.undo, self.delete_node)
        MiasmataData.setTabOrder(self.delete_node, self.save)
        MiasmataData.setTabOrder(self.save, self.show_diff)
        MiasmataData.setTabOrder(self.show_diff, self.version)

    def retranslateUi(self, MiasmataData):
        self.save.setText(
            QApplication.translate("MiasmataData", "&Save...", None))
        self.show_diff.setText(
            QApplication.translate("MiasmataData", "Show &mod changes...",
                                   None))
        self.lblVersion.setText(
            QApplication.translate("MiasmataData", "&Version:", None))
        self.label_4.setText(
            QApplication.translate("MiasmataData", "&Search:", None))
        self.clear_search.setText(
            QApplication.translate("MiasmataData", "&Clear", None))
        self.label.setText(
            QApplication.translate("MiasmataData", "&Name:", None))
        self.label_2.setText(
            QApplication.translate("MiasmataData", "&Type:", None))
        self.label_3.setText(
            QApplication.translate("MiasmataData", "&Value:", None))
        self.new_key.setText(
            QApplication.translate("MiasmataData", "New &Key", None))
        self.delete_node.setText(
            QApplication.translate("MiasmataData", "&Delete Node...", None))
        self.new_value.setText(
            QApplication.translate("MiasmataData", "New V&alue", None))
        self.undo.setText(
            QApplication.translate("MiasmataData", "&Undo Changes to Node",
                                   None))
        self.actionNew_Key.setText(
            QApplication.translate("MiasmataData", "New Key", None))
        self.actionNew_Value.setText(
            QApplication.translate("MiasmataData", "New Value", None))
        self.actionUndo_Changes.setText(
            QApplication.translate("MiasmataData", "Undo Changes", None))
        self.actionDelete.setText(
            QApplication.translate("MiasmataData", "Delete", None))
        self.actionInsert_Row.setText(
            QApplication.translate("MiasmataData", "Insert Row", None))
        self.actionRemove_Row.setText(
            QApplication.translate("MiasmataData", "Remove Row", None))
