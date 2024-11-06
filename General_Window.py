
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QColor, QBrush


class general_window(object):
    def __init__(self,type):
        if type=='Time_series_plot':
            from general_plot_window import Ui_Dialog as plot_window
            self.plot = plot_window(type)

        elif type=='Scatter_plot':
            from scatter_plot_window import Ui_Dialog as plot_window
            self.plot = plot_window()
        elif type=='Histogram':
            from general_plot_window import Ui_Dialog as plot_window
            self.plot = plot_window(type)
        super().__init__()
        self.new_window = QtWidgets.QWidget()

        self.plot.setupUi(self.new_window)
        self.new_window.show()
        self.table_raw_data = None
        self.model = None
        self.plot.cancel_btn.clicked.connect(self.quit)
        self.plot.clear_btn.clicked.connect(self.clear_input)
        # self.plot.setting_btn.clicked.connect(self.test1)
        self.new_window.show()

    def quit(self):
        self.new_window.close()

    def msgbox_info(self, title, text):
        QMessageBox.about(self.new_window, title, text)

    def load_data(self,data):
        self.table_raw_data = data
        self.model = QStandardItemModel()
        for col in self.table_raw_data.columns:
            self.model.appendRow(QStandardItem(str(col)))
        self.plot.listView.setModel(self.model)
        self.plot.listView.show()

    def add_to_column_list(self):
        selected = self.model.item(self.plot.listView.currentIndex().row()).text()
        text = self.plot.text_input.toPlainText()
        if text != "":
            text += " "
        self.plot.text_input.setText(text + str(selected))

    def clear_input(self):
        self.plot.text_input.setText('')

    def test1(self):
        print('gener')
        pass