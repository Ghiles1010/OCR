from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QTabWidget

from Filter import Filter
import cv2
import numpy as np
import sys


class UI:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()

        self.origin_image = np.zeros((600, 600, 3), dtype=np.uint16)
        self.result_image = np.zeros((600, 600, 3), dtype=np.uint16)
        pixmap = self.cv2_to_pixmap(self.result_image)

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1300, 650)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 20, 1137, 583))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.image = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setMaximumSize(QtCore.QSize(600, 600))
        self.image.setAutoFillBackground(True)
        self.image.setText("")
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setWordWrap(False)
        self.image.setObjectName("image")
        self.gridLayout.addWidget(self.image, 0, 0, 3, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.browse_input = QtWidgets.QLineEdit(self.widget)
        self.browse_input.setObjectName("browse_input")
        self.browse_input.setReadOnly(True)
        self.horizontalLayout.addWidget(self.browse_input)
        self.browse_btn = QtWidgets.QPushButton(self.widget)
        self.browse_btn.setObjectName("browse_btn")
        self.browse_btn.clicked.connect(lambda: self.on_browse())
        self.horizontalLayout.addWidget(self.browse_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.tabs = QTabWidget()
        self.filter_list = self.__setup_tab("Filters")
        # self.binar_list = self.__setup_tab("Binarisation")

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 962, 24))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.browse_btn.setText(_translate("MainWindow", "Browse"))
        self.label.setText(_translate("MainWindow", "Choose an image"))

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def __setup_tab(self, tab_name):

        scroll = QtWidgets.QScrollArea(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(scroll.sizePolicy().hasHeightForWidth())
        scroll.setSizePolicy(sizePolicy)
        scroll.setMaximumSize(QtCore.QSize(900, 900))
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea_"+tab_name)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 527, 528))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents_"+tab_name)
        scroll.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.tabs, 2, 1, 1, 1)
        scroll.setWidgetResizable(True)
        widget = QWidget()
        tab_list = QVBoxLayout()
        widget.setLayout(tab_list)
        scroll.setWidget(widget)
        self.tabs.addTab(scroll, tab_name)
        return tab_list
    def __setup_binarisation_tab(self):
        pass


    def on_browse(self):
        image_path, _ = QFileDialog.getOpenFileName(filter='Image Files(*.png *.jpg *.bmp)')
        image = cv2.imread(image_path)
        self.origin_image = image
        self.result_image = image
        pixmap = self.cv2_to_pixmap(image)
        self.image.setPixmap(pixmap)
        self.modify_image()

    def cv2_to_pixmap(self, image):
        image = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                             image.strides[0], QImage.Format_RGB888)
        image = image.rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        return pixmap

    def modify_image(self):
        self.result_image = self.origin_image

        for i in range(self.filter_list.count()-1, -1, -1):
            f = self.filter_list.itemAt(i).widget()
            if f.isApplied:
                self.result_image = f.function(self.result_image, f.current_value)

        pixmap = self.cv2_to_pixmap(self.result_image)
        self.image.setPixmap(pixmap)

    def add_filter(self, name, function, var_name, min_value, max_value, init_value=0, step=1):
        f = Filter(self, function, name, var_name, min_value, max_value,
                   init_value, step)

        self.filter_list.insertWidget(0, f)
        self.result_image = function(self.result_image, init_value)
        pixmap = self.cv2_to_pixmap(self.result_image)
        self.image.setPixmap(pixmap)

    # def add_binarisation():
    #     pass

    def set_image(self, image):
        self.origin_image = image
        self.result_image = image
        pixmap = self.cv2_to_pixmap(image)
        self.image.setPixmap(pixmap)

    def show(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    ui = UI()

