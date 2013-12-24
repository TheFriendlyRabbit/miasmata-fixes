# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'miasmod_data.ui'
#
# Created: Wed Dec 25 01:13:04 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MiasmataData(object):
    def setupUi(self, MiasmataData):
        MiasmataData.setObjectName("MiasmataData")
        MiasmataData.resize(713, 490)
        self.horizontalLayout = QtGui.QHBoxLayout(MiasmataData)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeView = QtGui.QTreeView(MiasmataData)
        self.treeView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAllColumnsShowFocus(True)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(MiasmataData)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.name = QtGui.QLineEdit(MiasmataData)
        self.name.setReadOnly(True)
        self.name.setObjectName("name")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.name)
        self.type = QtGui.QComboBox(MiasmataData)
        self.type.setEnabled(False)
        self.type.setObjectName("type")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.type)
        self.label_2 = QtGui.QLabel(MiasmataData)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(MiasmataData)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.value_line = QtGui.QLineEdit(MiasmataData)
        self.value_line.setObjectName("value_line")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.value_line)
        self.verticalLayout_2.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.value_list = QtGui.QListView(MiasmataData)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.value_list.sizePolicy().hasHeightForWidth())
        self.value_list.setSizePolicy(sizePolicy)
        self.value_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.value_list.setAlternatingRowColors(True)
        self.value_list.setUniformItemSizes(True)
        self.value_list.setObjectName("value_list")
        self.verticalLayout_2.addWidget(self.value_list)
        self.value_hex = QtGui.QPlainTextEdit(MiasmataData)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.value_hex.sizePolicy().hasHeightForWidth())
        self.value_hex.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setWeight(75)
        font.setBold(True)
        self.value_hex.setFont(font)
        self.value_hex.setReadOnly(True)
        self.value_hex.setObjectName("value_hex")
        self.verticalLayout_2.addWidget(self.value_hex)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 1, 1, 1)
        self.new_key = QtGui.QPushButton(MiasmataData)
        self.new_key.setEnabled(False)
        self.new_key.setObjectName("new_key")
        self.gridLayout_2.addWidget(self.new_key, 1, 0, 1, 1)
        self.delete_node = QtGui.QPushButton(MiasmataData)
        self.delete_node.setEnabled(False)
        self.delete_node.setObjectName("delete_node")
        self.gridLayout_2.addWidget(self.delete_node, 2, 2, 1, 1)
        self.new_value = QtGui.QPushButton(MiasmataData)
        self.new_value.setEnabled(False)
        self.new_value.setObjectName("new_value")
        self.gridLayout_2.addWidget(self.new_value, 2, 0, 1, 1)
        self.undo = QtGui.QPushButton(MiasmataData)
        self.undo.setEnabled(False)
        self.undo.setObjectName("undo")
        self.gridLayout_2.addWidget(self.undo, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 2)
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
        self.label.setBuddy(self.name)
        self.label_2.setBuddy(self.type)
        self.label_3.setBuddy(self.value_line)

        self.retranslateUi(MiasmataData)
        QtCore.QObject.connect(self.actionNew_Key, QtCore.SIGNAL("triggered()"), MiasmataData.insert_key)
        QtCore.QObject.connect(self.actionNew_Value, QtCore.SIGNAL("triggered()"), MiasmataData.insert_value)
        QtCore.QObject.connect(self.new_key, QtCore.SIGNAL("clicked()"), MiasmataData.insert_key)
        QtCore.QObject.connect(self.new_value, QtCore.SIGNAL("clicked()"), MiasmataData.insert_value)
        QtCore.QObject.connect(self.delete_node, QtCore.SIGNAL("clicked()"), MiasmataData.delete_node)
        QtCore.QObject.connect(self.undo, QtCore.SIGNAL("clicked()"), MiasmataData.undo)
        QtCore.QObject.connect(self.actionUndo_Changes, QtCore.SIGNAL("triggered()"), MiasmataData.undo)
        QtCore.QObject.connect(self.actionDelete, QtCore.SIGNAL("triggered()"), MiasmataData.delete_node)
        QtCore.QMetaObject.connectSlotsByName(MiasmataData)
        MiasmataData.setTabOrder(self.treeView, self.name)
        MiasmataData.setTabOrder(self.name, self.type)
        MiasmataData.setTabOrder(self.type, self.value_line)
        MiasmataData.setTabOrder(self.value_line, self.value_list)
        MiasmataData.setTabOrder(self.value_list, self.value_hex)
        MiasmataData.setTabOrder(self.value_hex, self.new_key)
        MiasmataData.setTabOrder(self.new_key, self.new_value)
        MiasmataData.setTabOrder(self.new_value, self.undo)
        MiasmataData.setTabOrder(self.undo, self.delete_node)

    def retranslateUi(self, MiasmataData):
        self.label.setText(QtGui.QApplication.translate("MiasmataData", "&Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MiasmataData", "&Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MiasmataData", "&Value:", None, QtGui.QApplication.UnicodeUTF8))
        self.new_key.setText(QtGui.QApplication.translate("MiasmataData", "New &Key", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_node.setText(QtGui.QApplication.translate("MiasmataData", "&Delete Node...", None, QtGui.QApplication.UnicodeUTF8))
        self.new_value.setText(QtGui.QApplication.translate("MiasmataData", "New V&alue", None, QtGui.QApplication.UnicodeUTF8))
        self.undo.setText(QtGui.QApplication.translate("MiasmataData", "&Undo Changes to Node", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Key.setText(QtGui.QApplication.translate("MiasmataData", "New Key", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Value.setText(QtGui.QApplication.translate("MiasmataData", "New Value", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo_Changes.setText(QtGui.QApplication.translate("MiasmataData", "Undo Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MiasmataData", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInsert_Row.setText(QtGui.QApplication.translate("MiasmataData", "Insert Row", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Row.setText(QtGui.QApplication.translate("MiasmataData", "Remove Row", None, QtGui.QApplication.UnicodeUTF8))

