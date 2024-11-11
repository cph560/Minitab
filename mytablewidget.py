# coding=gbk
from PyQt5.QtWidgets import QApplication,QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5 import  QtWidgets
from PyQt5.Qt import QTableWidgetItem
 

# 定义PYQT表格操作
class MyTableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QMenu(self)
        
        self.CP = self.contextMenu.addAction('复制')
        self.JQ = self.contextMenu.addAction('剪切')
        self.NT = self.contextMenu.addAction('粘贴')
        self.DE = self.contextMenu.addAction('删除')
        self.ADD_col = self.contextMenu.addAction('添加列')
        self.ADD_row = self.contextMenu.addAction('添加行')
        self.CT = self.contextMenu.addAction('设为标题(第一行)')

        #链接Function
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

        # 检查输入的值是否为数字
        if value.isdigit():
            pass  # 转换为整数
        # 填充上方所有列中的空值为0
        for r in range(row - 1, 0, -1):
            upper_item = self.item(r, column)
            if upper_item is None or upper_item.text() == "":
                self.setItem(r, column, QTableWidgetItem("0"))
        else:
            return  # 如果不是数字，不执行填充操作


    #删除Table Text
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
        
    #粘贴Table Text
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
    
    #获得选中格子的内容
    def selected_tb_text(self):
        try:
            indexes = self.selectedIndexes()  # 获取表格对象中被选中的数据索引列表
            indexes_dict = {}
            for index in indexes:  # 遍历每个单元格
                row, column = index.row(), index.column()  # 获取单元格的行号，列号
                if row in indexes_dict.keys():
                    indexes_dict[row].append(column)
                else:
                    indexes_dict[row] = [column]
 
            # 将数据表数据用制表符(\t)和换行符(\n)连接，使其可以复制到excel文件中
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
        
    #复制格子的内容
    def copy(self):
        text = self.selected_tb_text()  # 获取当前表格选中的数据
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    #添加列
    def ADD_COL(self):
        try:
            col = set()
            indexes = self.selectedIndexes()
            for index in indexes:  # 遍历每个单元格
                column = index.column()
                col.add(column)
            
            self.setColumnCount(self.columnCount()+len(col))
        except Exception as e:
            print(e)
            return ''
        
    #添加行
    def ADD_ROW(self):
        try:
            row_set = set()
            indexes = self.selectedIndexes()
            for index in indexes:  # 遍历每个单元格
                row = index.row()
                row_set.add(row)
            self.setRowCount(self.rowCount()+len(row_set))
        except Exception as e:
            print(e)
            return ''
    
    #改变列名
    def changeColName(self):
        try:

            indexes = self.selectedIndexes()
            row_num = 0
            col_num = set()
            
            for index in indexes:
                
                index = index
                break
            c = index.column()

            for index in indexes:  # 遍历每个单元格
                Col = index.column()
                col_num.add(Col)
                
            #改标题
              
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
            for i in range(1,highest_row):  # 遍历每个单元格
                for j in col_num:
                    row, column = i, j  # 获取单元格的行号，列号
                    if row in indexes_dict.keys():
                        indexes_dict[row].append(column)
                    else:
                        indexes_dict[row] = [column]
            print(indexes_dict)
            # 将数据表数据用制表符(\t)和换行符(\n)连接，使其可以复制到excel文件中
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
    
    #数据传输
    def transfer_data(self):
        #1106 Yedi 更新传输至新框架

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


        # 已更新数据传输
        try:
            row_num = self.rowCount()
            col_num = self.columnCount()
            col_set = []
            for i in range(col_num): # 遍历每个列有无空列
                if self.item(1, i).text() == "":
                    continue
                else:
                    
                    if not self.horizontalHeaderItem(i):
                        col_set.append([i+1, i])
                    else:
                        title=self.item(0, i).text()
                        if title=="":
                            col_set.append([self.horizontalHeaderItem(i).text(), i])  # 【列名，列位置】
                        else:
                            col_set.append([title, i]) #【列名，列位置】
            
            col_item_set = {}
            for item in col_set: # 遍历每个有内容行
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

    #剪切
    def cut(self):
        self.copy()
        self.del_tb_text()
    
    #粘贴
    def paste(self):
        self.paste_tb_text()
    
    #删除
    def Delete(self):
        self.del_tb_text()
    
    def showMenu(self, pos):
        # pos 鼠标位置
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示



    def keyPressEvent(self, event):  # 重写键盘监听事件
        # 监听 CTRL+C 组合键，实现复制数据到粘贴板
        if (event.key() == Qt.Key_C) and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.copy()  # 获取当前表格选中的数据
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