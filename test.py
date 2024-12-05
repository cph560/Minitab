
# -*- coding: GBK -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time

 
class MyTable(QTableWidget):
    def __init__(self, parent=None):
        super(MyTable, self).__init__(parent)
        self.setWindowTitle("�����г����ر�ʵʱ����")  # ���ñ�������
        self.setWindowIcon(QIcon("ok.png"))  # ����ͼ�꣨ͼƬҪ���ڣ�
        self.resize(600, 200)  # ���ñ���ߴ磨�����С��
        self.setColumnCount(5)  # ��������
        self.setRowCount(5)  # ��������
        # self.setColumnWidth(0, 200)  # �����п�(�ڼ��У� ����)
        # self.setRowHeight(0, 100)  # �����и�(�ڼ��У� �и�)
     
        column_name = [
            'ETH/BIC',
            'column1',
            'column2',
            'column3',
            'column4',
        ]
        self.setHorizontalHeaderLabels(column_name)  # ����������
        row_name = [
            'binance',
            'okex',
            'bitfinex',
            'bittrex',
            'bithumb',
        ]
        self.setVerticalHeaderLabels(row_name)  # ����������
 
    def update_item_data(self, data):
        """��������"""
        self.setItem(0, 1, QTableWidgetItem(data)) # ���ñ�������(�У� ��) ����
 
 
class UpdateData(QThread):
    """����������"""
    update_date = pyqtSignal(str)  # pyqt5 ֧��python3��str��û��Qstring


    def run(self):
        
        while True:
            localtime = time.localtime(time.time())
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
            self.update_date.emit(localtime)  # �����ź�
            time.sleep(1)
 
 
if __name__ == '__main__':
    expr = '2 ** (3 + 5) / 2'
    result = eval(expr)
    print("C23+C56".lower())
    
    print(result)  # �����8.5
    # ʵ��������
    app = QApplication(sys.argv)
    myTable = MyTable()
    # ���������߳�
    update_data_thread = UpdateData()
    update_data_thread.update_date.connect(myTable.update_item_data)  # �����ź�
    update_data_thread.start()

    # ��ʾ����Ļ����
    desktop = QApplication.desktop()  # ��ȡ����
    x = (desktop.width() - myTable.width()) // 2
    y = (desktop.height() - myTable.height()) // 2
    myTable.move(x, y)  # �ƶ�
 
    # ��ʾ����
    myTable.show()
    app.exit(app.exec_())

