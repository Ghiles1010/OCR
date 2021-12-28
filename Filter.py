from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QHBoxLayout, QGroupBox


class Filter(QGroupBox):

    def __init__(self, ui, function, name, var_name, min_value, max_value, init_value=0, step=1):
        super().__init__(name)

        self.ui = ui
        self.function = function
        self.name = name
        self.var_name = var_name
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.init_value = init_value

        self.current_value = init_value

        self.isApplied = False
        self.label = None
        self.slider = None
        self.up_button = None
        self.down_button = None
        self.check_box = None

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.add_entete()
        self.add_body()

        self.setFixedHeight(150)

    def on_up(self):
        index = self.ui.filter_list.indexOf(self)
        if index != 0:
            self.setParent(None)
            self.ui.filter_list.insertWidget(index-1, self)
            self.ui.modify_image()


    def on_down(self):
        index = self.ui.filter_list.indexOf(self)
        if index != self.ui.filter_list.count()-1:
            self.setParent(None)
            self.ui.filter_list.insertWidget(index + 1, self)
            self.ui.modify_image()

    def on_check(self):
        self.isApplied = self.check_box.isChecked()
        self.ui.modify_image()

    def add_entete(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        self.check_box = QCheckBox("Apply")
        self.check_box.setChecked(self.isApplied)
        self.check_box.setFixedHeight(30)
        self.check_box.clicked.connect(lambda: self.on_check())
        hbox.addWidget(self.check_box)

        self.up_button = QtWidgets.QPushButton("^")
        self.up_button.setFixedSize(50, 40)
        self.up_button.clicked.connect(lambda: self.on_up())
        hbox.addWidget(self.up_button)

        self.down_button = QtWidgets.QPushButton("v")
        self.down_button.setFixedSize(50, 40)
        self.down_button.clicked.connect(lambda: self.on_down())
        hbox.addWidget(self.down_button)

        self.vbox.addLayout(hbox)
        self.setFixedHeight(200)

    def on_drag(self):
        self.current_value = self.slider.value()
        text = "{var_name} : {value}".format(var_name=self.var_name, value=str(self.current_value))
        self.label.setText(text)
        self.ui.modify_image()

    def add_body(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(
            "{var_name} : {value}".format(var_name=self.var_name, value=self.init_value))
        self.label.setFixedHeight(25)
        vbox.addWidget(self.label)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(self.min_value)
        self.slider.setMaximum(self.max_value)
        self.slider.setSingleStep(self.step)
        self.slider.setTickInterval(self.step)
        self.slider.setValue(self.init_value)

        self.slider.valueChanged.connect(lambda: self.on_drag())

        vbox.addWidget(self.slider)
        self.vbox.addLayout(vbox)
