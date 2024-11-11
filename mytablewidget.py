# coding=gbk
from PyQt5.QtWidgets import QApplication,QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import  QtWidgets
from PyQt5.Qt import QTableWidgetItem
 

# ����PYQT������
class MyTableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # ����QMenu�ź��¼�
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QMenu(self)
        
        self.CP = self.contextMenu.addAction('����')
        self.JQ = self.contextMenu.addAction('����')
        self.NT = self.contextMenu.addAction('ճ��')
        self.DE = self.contextMenu.addAction('ɾ��')
        self.ADD_col = self.contextMenu.addAction('�����')
        self.ADD_row = self.contextMenu.addAction('�����')
        self.CT = self.contextMenu.addAction('��Ϊ����(��һ��)')

        #����Function
        self.CP.triggered.connect(self.copy)
        self.JQ.triggered.connect(self.cut)
        self.NT.triggered.connect(self.paste)
        self.DE.triggered.connect(self.Delete)
        self.ADD_col.triggered.connect(self.ADD_COL)
        self.ADD_row.triggered.connect(self.ADD_ROW)
        self.CT.triggered.connect(self.changeColName)
        self.itemChanged.connect(self.on_item_changed)
        self.init='no'
    def on_item_changed(self, item):
        if self.init=='yes':
            self.fill_above_with_zeros(item)

    def fill_above_with_zeros(self,item):
        row = item.row()
        column = item.column()
        value = item.text()

        # ��������ֵ�Ƿ�Ϊ����
        if value.isdigit():
            pass  # ת��Ϊ����
        # ����Ϸ��������еĿ�ֵΪ0
        for r in range(row - 1, 0, -1):
            upper_item = self.item(r, column)
            if upper_item is None or upper_item.text() == "":
                self.setItem(r, column, QTableWidgetItem("0"))
        else:
            return  # ����������֣���ִ��������


    #ɾ��Table Text
    def del_tb_text(self):
        temp=self.init
        self.init = 'no'
        try:
            indexes = self.selectedIndexes()
            
            for index in indexes:
                row, column = index.row(), index.column()
                item = QTableWidgetItem()
                
                self.setItem(row, column, item)
        except BaseException as e:
            print(e)
            self.init = temp
            return
        finally:
            self.init = temp
        
    #ճ��Table Text
    def paste_tb_text(self):
        try:
            indexes = self.selectedIndexes()
            for index in indexes:
                
                index = index
                break
            r, c = index.row(), index.column()
            text = QApplication.clipboard().text()
            ls = text.split('\n')
            ls1 = []
            for row in ls:
                ls1.append(row.split('\t'))
            rows = len(ls)
            columns = len(ls1[0])
            for row in range(rows):
                for column in range(1, columns):
                    item = QTableWidgetItem()
                    item.setText((str(ls1[row][column])))
                    self.setItem(row + r, column + c-1, item)
        except Exception as e:
            print(e)
            return
    
    #���ѡ�и��ӵ�����
    def selected_tb_text(self):
        try:
            indexes = self.selectedIndexes()  # ��ȡ�������б�ѡ�е����������б�
            indexes_dict = {}
            for index in indexes:  # ����ÿ����Ԫ��
                row, column = index.row(), index.column()  # ��ȡ��Ԫ����кţ��к�
                if row in indexes_dict.keys():
                    indexes_dict[row].append(column)
                else:
                    indexes_dict[row] = [column]
 
            # �����ݱ��������Ʊ��(\t)�ͻ��з�(\n)���ӣ�ʹ����Ը��Ƶ�excel�ļ���
            text = ''
            for row, columns in indexes_dict.items():
                row_data = ''
                for column in columns:
                    data = self.item(row, column).text()
                    row_data = row_data + '\t' + data 

                if text:
                    text = text + '\n' + row_data
                else:
                    text = row_data
            # print(text)
            return text
        except BaseException as e:
            print(e)
            return ''
        
    #���Ƹ��ӵ�����
    def copy(self):
        text = self.selected_tb_text()  # ��ȡ��ǰ���ѡ�е�����
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    #�����
    def ADD_COL(self):
        try:
            col = set()
            indexes = self.selectedIndexes()
            for index in indexes:  # ����ÿ����Ԫ��
                column = index.column()
                col.add(column)
            
            self.setColumnCount(self.columnCount()+len(col))
        except Exception as e:
            print(e)
            return ''
        
    #�����
    def ADD_ROW(self):
        try:
            row_set = set()
            indexes = self.selectedIndexes()
            for index in indexes:  # ����ÿ����Ԫ��
                row = index.row()
                row_set.add(row)
            self.setRowCount(self.rowCount()+len(row_set))
        except Exception as e:
            print(e)
            return ''
    
    #�ı�����
    def changeColName(self):
        try:

            indexes = self.selectedIndexes()
            row_num = 0
            col_num = set()
            
            for index in indexes:
                
                index = index
                break
            c = index.column()

            for index in indexes:  # ����ÿ����Ԫ��
                Col = index.column()
                col_num.add(Col)
                
            #�ı���
              
            # print(col_num)
                
            for i in col_num:
                self.setHorizontalHeaderItem(i,QTableWidgetItem(self.item(row_num, i).text()))

            highest_row = 0
            for j in col_num:
                
                s = 0
                while self.item(s, j).text() != "":
                    s += 1
                highest_row = max(highest_row, s)
                    

            # print(highest_row)
            
            indexes_dict = {}
            for i in range(1,highest_row):  # ����ÿ����Ԫ��
                for j in col_num:
                    row, column = i, j  # ��ȡ��Ԫ����кţ��к�
                    if row in indexes_dict.keys():
                        indexes_dict[row].append(column)
                    else:
                        indexes_dict[row] = [column]
            print(indexes_dict)
            # �����ݱ��������Ʊ��(\t)�ͻ��з�(\n)���ӣ�ʹ����Ը��Ƶ�excel�ļ���
            text = ''
            for row, columns in indexes_dict.items():
                row_data = ''
                for column in columns:
                    data = self.item(row, column).text()
                    
                    row_data = row_data + '\t' + data 
                    

                if text:
                    text = text + '\n' + row_data
                else:
                    text = row_data
            
            # paste text
            ls = text.split('\n')
            ls1 = []
            for row in ls:
                ls1.append(row.split('\t'))
            rows = len(ls)
            columns = len(ls1[0])
            
            for row in range(rows):
                for column in range(1,columns):
                    item = QTableWidgetItem()
                    item.setText((str(ls1[row][column])))
                    self.setItem(row, column + c-1, item)

            for j in col_num:
                item = QTableWidgetItem()
                item.setText('')
                self.setItem(highest_row-1, j, item)
            
            
        except Exception as e:
            print(e)
            return ''
    
    #���ݴ���
    def transfer_data(self):
        #1106 Yedi ���´������¿��

        try:
            current_row = self.tableWidget.selectedItems()[0].row()
            current_col = self.tableWidget.selectedItems()[0].column()
            
            temp_row = 0
            temp_col = 0
            if current_row == 0 and current_col == 0:
                temp_row = 1
            self.tableWidget.setCurrentCell(temp_row, temp_col)
            
            self.tableWidget.setCurrentCell(current_row, current_col)
        except:
            pass


        # �Ѹ������ݴ���
        try:
            row_num = self.rowCount()
            col_num = self.columnCount()
            col_set = []
            for i in range(col_num): # ����ÿ�������޿���
                if self.item(1, i).text() == "":
                    continue
                else:
                    
                    if not self.horizontalHeaderItem(i):
                        col_set.append([i+1, i])
                    else:
                        title=self.item(0, i).text()
                        if title=="":
                            col_set.append([self.horizontalHeaderItem(i).text(), i])  # ����������λ�á�
                        else:
                            col_set.append([title, i]) #����������λ�á�
            
            col_item_set = {}
            for item in col_set: # ����ÿ����������
                if str(item[0]) not in col_item_set:
                    col_item_set[str(item[0])] = []
                for i in range(1,row_num):
                    if self.item(i, item[1]).text()== '':
                        break
                    else:
                        # print(self.item(i, item[1]).text())
                        col_item_set[str(item[0])].append(self.item(i,item[1]).text())
            

            # print(col_item_set) # Example {'C1': ['123', '24', '251'], 'C2': ['125', '16', '216']}
            return col_item_set

        except Exception as e:
            print(e)
            return ''

    #����
    def cut(self):
        self.copy()
        self.del_tb_text()
    
    #ճ��
    def paste(self):
        self.paste_tb_text()
    
    #ɾ��
    def Delete(self):
        self.del_tb_text()
    
    def showMenu(self, pos):
        # pos ���λ��
        # �˵���ʾǰ,�����ƶ����������λ��
        self.contextMenu.exec_(QCursor.pos())  # �����λ����ʾ



    def keyPressEvent(self, event):  # ��д���̼����¼�
        # ���� CTRL+C ��ϼ���ʵ�ָ������ݵ�ճ����
        if (event.key() == Qt.Key_C) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.copy()  # ��ȡ��ǰ���ѡ�е�����
        elif (event.key() == Qt.Key_X) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.cut()
        elif (event.key() == Qt.Key_V) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.paste()
        elif(event.key() == Qt.Key_Delete):
            self.Delete()
        # elif (event.key() == Qt.Key_Z) and QApplication.keyboardModifiers() == Qt.ControlModifier:
        #     self.paste()
        else:
            super().keyPressEvent(event)

    def random_col(self, name="C1", data=[]):

        c = self.columnCount()
        try:
            col = int(name.lower().strip("c ")) - 1
        except:
            for j in range(c):
                if self.horizontalHeaderItem(j).text() == name:
                    col = j
                    break

        r = self.rowCount()-1
        if len(data) > r:
            self.setRowCount(len(data)+1)

        for i in range(len(data)):
            item = QTableWidgetItem()
            item.setText(str(data[i]))
            self.setItem(i+1, col, item)