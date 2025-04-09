# coding=gbk
import sys
import traceback
import math

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QKeyEvent
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidget,
                             QAbstractItemView, QCheckBox, QTableWidgetItem, QHeaderView, QSizePolicy, QFrame,
                             QSpacerItem, QLineEdit)


# 复选框按钮组,用于实现被选中复选框id的存储、全选等。pyqt内置的有按钮组，但是那个按钮组的按钮选中互斥，不适合check_box
class CheckBoxGroup:

    def __init__(self):
        self.__cb_list = list()
        self.__cb_id_list = list()
        self.__selected_list = list()
        self.__selected_id_list = list()

    @staticmethod
    def table_center_btn(btn):
        # 返回一个居中显示按钮的窗体

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return container

    def append(self, check_box, data_id):
        """添加复选框到按钮组，复选框会绑定点击事件，存储进按钮组"""
        if check_box in self.__cb_list:
            return
        if data_id in self.__cb_id_list:
            raise Exception(f"data_id {data_id} is Existed")

        check_box.data_id = data_id
        check_box.stateChanged.connect(lambda state, cb=check_box: self.__state_changed_func(state, cb))

        self.__cb_list.append(check_box)
        self.__cb_id_list.append(data_id)

    def select_all(self):
        """按钮组的复选框，全部选中"""
        for i in self.__cb_list:
            i.setChecked(True)

    def cancel_all(self):
        for i in self.__cb_list:
            i.setChecked(False)

    def selected(self):
        """返回被选中的复选框列表"""
        return tuple(self.__selected_list)

    def selected_id(self):
        """返回被选中的复选框存储的data_id的列表"""
        return tuple(self.__selected_id_list)

    def selected_len(self):
        """被选中的数量"""
        return len(self.__selected_list)

    def len(self):
        """按钮组中按钮总数"""
        return len(self.__cb_list)

    def delete(self, check_box):
        self.__cb_list.remove(check_box)

    def clear(self):
        """清空按钮组"""
        self.__cb_list.clear()
        self.__cb_id_list.clear()
        self.__selected_list.clear()
        self.__selected_id_list.clear()

    def __state_changed_func(self, state, btn):
        if btn.isChecked():
            self.__selected_list.append(btn)
            self.__selected_id_list.append(btn.data_id)
        else:
            self.__selected_list.remove(btn)
            self.__selected_id_list.remove(btn.data_id)


# 可点击的QFrame
class ClickFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=None)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


# 可点击的QLabel
class ClickLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text=text, parent=parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


# 可以监听回车事件的LineEdit
class EnterLineEdit(QLineEdit):

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        # 回车事件函数,如果需要传参，要用lamda
        self.enter_func = ...

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            self.enter_func()
        else:
            super().keyPressEvent(event)


class TableWidget(QTableWidget):

    def __init__(self, max_row: int, header_list):
        super().__init__()

        # 表格显示最大行数，这个参数也是分页条数
        self.max_row = max_row
        self.col_num = len(header_list)

        # 创建一个复选框按钮组
        self.check_box_group = CheckBoxGroup()

        # 最左边加2列用于存放复选框和序号
        # 不直接改动header_list，免得外面的header_list被修改
        self.headers = ["", "序号"] + header_list

        # 存储列最小最大宽度设置，如果是Stretch策略，设置宽度无法生效
        self.headers_width = list()

        """
        # QHeaderView.ResizeMode.Interactive  可以手动拖拽，默认的就是，设置了其他策略均不可以手动拖拽
        # QHeaderView.ResizeMode.ResizeToContents  列宽根据内容自适应
        # QHeaderView.ResizeMode.Fixed 固定宽度
        # QHeaderView.ResizeMode.Stretch  随表格变化
        """
        # 表头默认长度策略，也可单独设置某1列的长度策略
        self.size_default_mode = QHeaderView.ResizeMode.Stretch

        # 表头设置样式
        # self.setStyleSheet("""
        #     QHeaderView::section {
        #         padding-left: 10px;
        #         padding-right: 10px;
        #     }
        # """)
        self.init_ui()

    def init_ui(self):
        self.setAlternatingRowColors(True)  # 使表格颜色交错显示
        self.verticalHeader().setVisible(False)  # 隐藏垂直标题 序号
        # self.horizontalHeader().setStretchLastSection(True)  # 设置最后一列自动填充容器
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 禁止编辑

        # 设置表头
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

        # 初始化列长度信息
        for i in range(len(self.headers)):
            self.headers_width.append(
                {"min_width": 0, "max_width": 999}
            )

        """
        # QHeaderView.ResizeMode.Interactive  可以手动拖拽，默认的就是，设置了其他策略均不可以手动拖拽
        # QHeaderView.ResizeMode.ResizeToContents  列宽根据内容自适应
        # QHeaderView.ResizeMode.Fixed 固定宽度
        # QHeaderView.ResizeMode.Stretch  随表格变化
        """

        # 设置表头的长度策略
        header_layout = self.horizontalHeader()
        for i in range(len(self.headers)):
            if i == 0:
                header_layout.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
                self.setColumnWidth(0, 40)
            else:
                header_layout.setSectionResizeMode(i, self.size_default_mode)
                # header_layout.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
                # header_layout.setSectionResizeMode(i, self.size_default_mode)

    def fill_data(self, data_list, page=1):
        """
        填充表格数据
        :param data_list: 数据列表，[[id],[],[]]这样的形式,要注意，第一列一定是id字段
        :param page: 分页，序号会按照这个来排序
        :return:
        """

        self.check_box_group.clear()
        self.clearContents()  # 清除单元格内容
        row_num = len(data_list)
        if row_num > self.max_row:
            row_num = self.max_row
        self.setRowCount(row_num)

        page_num = (page - 1) * self.max_row

        for row in range(row_num):
            for col in range(self.col_num + 2):  # 加两列给序号和按钮
                # 第一列给按钮
                if col == 0:
                    check_box = QCheckBox()
                    # 按钮需要记录数据的id，方便选择时候的操作
                    self.check_box_group.append(check_box, data_list[row][0])
                    self.setCellWidget(row, 0, self.__center_cb(check_box))
                # 第二列给序号
                elif col == 1:
                    self.setItem(row, 1, self.__center_item(page_num + row + 1))
                # 其他列是数据
                else:
                    data = data_list[row][col - 1]
                    self.setItem(row, col, self.__center_item(data))

        # 重新设置列宽
        # self.__resize_col_width()

    # 返回被选中数据的id列表
    def selected_id(self):
        return self.check_box_group.selected_id()

    # 全选
    def select_all(self):
        self.check_box_group.select_all()

    # 取消全选
    def cancel_select_all(self):
        self.check_box_group.cancel_all()

    # 设置列的最小宽度和最大宽度
    def set_col_width(self, index: int, min_width: int = 0, max_width: int = 9999):
        self.headers_width[index]["min_width"] = min_width
        self.headers_width[index]["max_width"] = max_width

    @staticmethod
    def __center_cb(check_box):
        # 返回一个居中显示按钮的窗体

        container = ClickFrame()
        container.clicked.connect(lambda cb=check_box: cb.setChecked(False) if cb.isChecked() else cb.setChecked(True))
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(check_box)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return container

    @staticmethod
    def __center_item(text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def __resize_col_width(self):
        # 所有列长度修改成合适大小
        self.resizeColumnsToContents()

        # 每1列根据set_col_width()设置的最小宽度最大宽度重新设置
        for col in range(len(self.headers)):

            col_width = self.horizontalHeader().sectionSize(col)  # 该列最合适的宽度
            min_width = self.headers_width[col]["min_width"]
            max_width = self.headers_width[col]["max_width"]

            if col_width < min_width:
                self.setColumnWidth(col, min_width)
            elif col_width > max_width:
                self.setColumnWidth(col, max_width)


class TablePage(QFrame):
    def __init__(self, table: TableWidget, get_data_func):

        super().__init__()

        """
            get_data_func为数据接口函数，需要返回数据列表
            格式为[[id, name, age], [id, name, age]]
            第一个数据必须为id，要和复选框绑定，修改删除数据的时候需要
            参照 get_data_demo函数
        """
        # get_data_func数据接口函数
        self.get_data_func = get_data_func

        self.table = table

        # 窗口设置策略
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        ))

        # 设置窗口高度
        self.setFixedHeight(40)

        # 窗口添加布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(5)

        # 分页栏背景改为白色
        self.setStyleSheet("background-color:#fff;")

        # page被选中的样式
        self.page_btn_selected_sheet = "border: 1px solid #E3E5E7"  # 选中的样式

        # 分页page显示多少个，只能是单数，最小是7 如果是7，那么就是 < 1 ··· 3 4 5 ··· 999 >
        self.page_btn_num = 7

        # 自定义参数，勿动
        self.current_page = 1  # 当前页数
        self.page_into: QLabel = ...  # 分页信息
        self.page_skip: QLineEdit = ...  # 跳转框
        self.page_btn_list = list()  # 分页page存放，page_num是
        self.data_count = 0

        # 添加组件
        self.init_ui()

        # 数据初始化，更新第1页的数据
        self.update_table(self.current_page)

    def init_ui(self):

        # 组件策略 高度填充，宽度固定
        control_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # 1.添加全选框
        select_all_btn = QCheckBox("全选", parent=self)
        select_all_btn.clicked.connect(self.__select_all_func)
        select_all_btn.setSizePolicy(control_policy)
        self.layout.addWidget(select_all_btn)

        # 2.添加固定弹簧弹簧
        spacer1_item = QSpacerItem(130, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer1_item)

        # 3.添加伸展弹簧
        spacer2_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer2_item)

        # 4.添加分页组件
        page_box = QFrame(parent=self)
        page_box.setSizePolicy(control_policy)
        page_box.setFixedHeight(25)
        self.layout.addWidget(page_box)

        page_box_layout = QHBoxLayout(page_box)
        page_box_layout.setContentsMargins(10, 0, 10, 0)
        page_box_layout.setSpacing(5)

        # 4.1 添加上一页
        prior_btn = ClickLabel(parent=page_box)
        prior_btn.setStyleSheet("margin-right: 10px;")
        prior_btn.setObjectName("prior_btn")
        prior_btn.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        prior_btn.setPixmap(QPixmap("static/icon/prior.png"))
        prior_btn.setSizePolicy(control_policy)
        prior_btn.setMinimumWidth(20)
        prior_btn.clicked.connect(lambda: self.__page_func(prior_btn))
        page_box_layout.addWidget(prior_btn)

        # 4.2 添加分页 其实可以把上一页和下一页也加进来，但是阅读代码不直观
        for i in range(self.page_btn_num):
            page_btn = ClickLabel(f"{i + 1}", parent=page_box)
            page_btn.setObjectName(f"page{i + 1}_btn")
            page_btn.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            page_btn.setSizePolicy(control_policy)
            page_btn.setMinimumWidth(20)
            page_box_layout.addWidget(page_btn)
            # 下面这个不行，因为page_btn会是最后一个page7_btn
            # page_btn.clicked.connect(lambda: self.__page_func(page_btn))
            page_btn.clicked.connect(lambda pb=page_btn: self.__page_func(pb))
            self.page_btn_list.append(page_btn)

        # 4.3 添加下一页
        next_btn = ClickLabel(parent=page_box)
        next_btn.setStyleSheet("margin-left: 10px")
        next_btn.setObjectName("next_btn")
        next_btn.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        next_btn.setPixmap(QPixmap("static/icon/next.png"))
        next_btn.setSizePolicy(control_policy)
        next_btn.setMinimumWidth(20)
        next_btn.clicked.connect(lambda: self.__page_func(next_btn))
        page_box_layout.addWidget(next_btn)

        # 5 添加伸展弹簧
        spacer3_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer3_item)

        # 6 添加分页信息
        page_into = QLabel("181页/3999条", parent=self)
        page_into.setSizePolicy(control_policy)
        self.layout.addWidget(page_into)
        self.page_into = page_into
        # print(page_into.widthMM())

        # 7.添加跳转
        skip_box = QFrame(self)
        skip_box.setSizePolicy(control_policy)
        self.layout.addWidget(skip_box)

        skip_box_layout = QHBoxLayout(skip_box)
        skip_box_layout.setContentsMargins(10, 0, 0, 0)
        skip_box_layout.setSpacing(5)

        # 添加 "跳转"
        skip_label1 = QLabel("跳转", parent=skip_box)
        skip_label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        skip_label1.setSizePolicy(control_policy)
        skip_box_layout.addWidget(skip_label1)

        # 添加输入框
        skip_line = EnterLineEdit(parent=skip_box)
        skip_line.setText("1")
        skip_line.text()
        skip_line.setObjectName("skip_line")
        skip_line.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        skip_line.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        skip_line.setFixedHeight(25)
        skip_line.setFixedWidth(35)
        skip_line.enter_func = lambda le=skip_line: self.update_table(int(le.text()))
        skip_box_layout.addWidget(skip_line)
        self.page_skip = skip_line

        # 添加 "页"
        skip_label1 = QLabel("页", parent=skip_box)
        skip_label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        skip_label1.setSizePolicy(control_policy)
        skip_box_layout.addWidget(skip_label1)

    def __select_all_func(self, state):
        """全选框的槽函数"""
        if state:
            self.table.select_all()
        else:
            self.table.cancel_select_all()

    def __page_func(self, page_btn):
        """page页、上一页、下一页的槽函数"""
        # 获取点击的页数
        # 上一页
        if page_btn.objectName() == "prior_btn":
            page_num = self.current_page - 1
            if page_num <= 0:
                return
        # 下一页
        elif page_btn.objectName() == "next_btn":
            page_num = self.current_page + 1
            if page_num > self.data_count / self.table.max_row:
                return
        # 数字页
        else:
            try:
                page_num = int(page_btn.text())
            except:
                return

        # 更新表格
        self.update_table(page_num)

    def update_table(self, page_num):
        """传入page，根据table.max_row，计算分页，获取数据填入表格，更新page栏内容"""

        # 首先修改当前索引页
        self.current_page = page_num

        # 找数据 填充表格
        offset = (page_num - 1) * self.table.max_row
        self.data_count, data_list = self.get_data_func(offset, self.table.max_row)
        self.table.fill_data(data_list, page_num)

        # 更新page栏 -------------

        # 1.更新状态栏
        total_pages = math.ceil(self.data_count / self.table.max_row)
        self.page_into.setText(f"{total_pages}页/{self.data_count}条")

        # 2.更新分页
        self.page_skip.setText(f"{self.current_page}")

        # 3.更新page栏
        # 如果小于7页，有多少页显示多少
        if total_pages <= self.page_btn_num:
            for i in self.page_btn_list[total_pages:]:
                i.hide()

        # 如果大于7页，page1_btn=1, page_end_btn=total_pages
        else:
            # 设置首尾
            self.page_btn_list[0].setText("1")
            self.page_btn_list[self.page_btn_num - 1].setText(f"{total_pages}")

            """
                举例 page_num=7 (7个page页)，三种情况 
                1. < 1 2 3 4 5 ... 10 > 
                2. < 1 ... 6 7 8 9 10 >
                3. < 1 ... 5 6 7 ... 10>

                第1种，跳转1 2 3 4的时候，需要把前面5个变成 1 2 3 4 5
                第2种，跳转7 8 9 10的时候，需要把后面5个变成 6 7 8 9 10
                第3种，如果点击的不是第1 2 种，就是第3种了，两边都要有省略号，并且点击的page页在中间，左右两个是他的相邻

                为什么是前4 或者后4， 因为去掉边上3个不能点的(点了就会变成其他种类)，7-3=4 
                所以margin_num = 3 ,无论page_num是多少，margin_num都是3
            """
            margin_num = 3

            # 第1种，点击前4个
            if self.current_page <= self.page_btn_num - margin_num:
                self.page_btn_list[self.page_btn_num - 2].setText("···")
                start_num = 2
                for i in self.page_btn_list[1:-2]:
                    i.setText(f"{start_num}")
                    start_num += 1
            # 第二种，点击后4个
            elif self.current_page >= total_pages - margin_num:
                self.page_btn_list[1].setText("···")
                start_num = total_pages - 1
                for i in self.page_btn_list[-2:1:-1]:
                    i.setText(f"{start_num}")
                    start_num -= 1
            # 第三种，点击中间的
            else:
                self.page_btn_list[1].setText("···")
                self.page_btn_list[self.page_btn_num - 2].setText("···")

                center_page_num = self.page_btn_num - 4  # 中间最多能显示多少page页

                # 如果是7页，中间显示3页，当前页是10，那么就是9 10 11，9=当前页-下取整(center_page_num/2)
                start_num = self.current_page - int(center_page_num / 2)
                for i in self.page_btn_list[2:-2]:
                    i.setText(f"{start_num}")
                    start_num += 1

        # 4.设置被选中的page样式
        for i in self.page_btn_list:
            if i.text() == str(self.current_page):
                i.setStyleSheet(self.page_btn_selected_sheet)
            else:
                i.setStyleSheet("")

    @staticmethod
    def get_data_demo(offset, limit):
        """
        测试用例子
        函数必须有两个参数，offset和limit，offset和limit用于分页
        必须返回数据总数和数据列表，数据列表第1列必须为数据id(不会显示)，剩下的根据表头长度决定
        """

        # 数据总数，用于分页使用
        total_count = 100

        # 数据列表，数据的索引0一定要是数据id，删除修改的时候就可以知道数据id了
        data_list = list()
        for i in range(offset, offset + limit, 1):
            data_list.append(
                [i + 1, f"胡图图{i + 1}", "15555555555", '6', "河南省郑州市金水区翻斗大街翻斗花园二号楼1001室"]
            )

        return total_count, data_list


# 捕捉pyqt6报错函数
def handle_exception(*args, **kwargs):
    traceback.print_exception(*args)
    sys.exit()


if __name__ == '__main__':
    app = QApplication([])
    sys.excepthook = handle_exception

    # 创建一个窗体
    widget = QWidget()
    widget.setGeometry(200, 200, 800, 500)

    # 创建表格
    table_widget = TableWidget(10, ["姓名", "电话", "年龄", "地址"])

    # 创建表格分页导航
    table_page = TablePage(table_widget, TablePage.get_data_demo)

    v_layout = QVBoxLayout(widget)
    v_layout.setSpacing(0)
    v_layout.addWidget(table_widget)
    v_layout.addWidget(table_page)

    widget.show()

    app.exec()


