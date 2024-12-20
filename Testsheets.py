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


# ��ѡ��ť��,����ʵ�ֱ�ѡ�и�ѡ��id�Ĵ洢��ȫѡ�ȡ�pyqt���õ��а�ť�飬�����Ǹ���ť��İ�ťѡ�л��⣬���ʺ�check_box
class CheckBoxGroup:

    def __init__(self):
        self.__cb_list = list()
        self.__cb_id_list = list()
        self.__selected_list = list()
        self.__selected_id_list = list()

    @staticmethod
    def table_center_btn(btn):
        # ����һ��������ʾ��ť�Ĵ���

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return container

    def append(self, check_box, data_id):
        """��Ӹ�ѡ�򵽰�ť�飬��ѡ���󶨵���¼����洢����ť��"""
        if check_box in self.__cb_list:
            return
        if data_id in self.__cb_id_list:
            raise Exception(f"data_id {data_id} is Existed")

        check_box.data_id = data_id
        check_box.stateChanged.connect(lambda state, cb=check_box: self.__state_changed_func(state, cb))

        self.__cb_list.append(check_box)
        self.__cb_id_list.append(data_id)

    def select_all(self):
        """��ť��ĸ�ѡ��ȫ��ѡ��"""
        for i in self.__cb_list:
            i.setChecked(True)

    def cancel_all(self):
        for i in self.__cb_list:
            i.setChecked(False)

    def selected(self):
        """���ر�ѡ�еĸ�ѡ���б�"""
        return tuple(self.__selected_list)

    def selected_id(self):
        """���ر�ѡ�еĸ�ѡ��洢��data_id���б�"""
        return tuple(self.__selected_id_list)

    def selected_len(self):
        """��ѡ�е�����"""
        return len(self.__selected_list)

    def len(self):
        """��ť���а�ť����"""
        return len(self.__cb_list)

    def delete(self, check_box):
        self.__cb_list.remove(check_box)

    def clear(self):
        """��հ�ť��"""
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


# �ɵ����QFrame
class ClickFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=None)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


# �ɵ����QLabel
class ClickLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text=text, parent=parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


# ���Լ����س��¼���LineEdit
class EnterLineEdit(QLineEdit):

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        # �س��¼�����,�����Ҫ���Σ�Ҫ��lamda
        self.enter_func = ...

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            self.enter_func()
        else:
            super().keyPressEvent(event)


class TableWidget(QTableWidget):

    def __init__(self, max_row: int, header_list):
        super().__init__()

        # �����ʾ����������������Ҳ�Ƿ�ҳ����
        self.max_row = max_row
        self.col_num = len(header_list)

        # ����һ����ѡ��ť��
        self.check_box_group = CheckBoxGroup()

        # ����߼�2�����ڴ�Ÿ�ѡ������
        # ��ֱ�ӸĶ�header_list����������header_list���޸�
        self.headers = ["", "���"] + header_list

        # �洢����С��������ã������Stretch���ԣ����ÿ���޷���Ч
        self.headers_width = list()

        """
        # QHeaderView.ResizeMode.Interactive  �����ֶ���ק��Ĭ�ϵľ��ǣ��������������Ծ��������ֶ���ק
        # QHeaderView.ResizeMode.ResizeToContents  �п������������Ӧ
        # QHeaderView.ResizeMode.Fixed �̶����
        # QHeaderView.ResizeMode.Stretch  ����仯
        """
        # ��ͷĬ�ϳ��Ȳ��ԣ�Ҳ�ɵ�������ĳ1�еĳ��Ȳ���
        self.size_default_mode = QHeaderView.ResizeMode.Stretch

        # ��ͷ������ʽ
        # self.setStyleSheet("""
        #     QHeaderView::section {
        #         padding-left: 10px;
        #         padding-right: 10px;
        #     }
        # """)
        self.init_ui()

    def init_ui(self):
        self.setAlternatingRowColors(True)  # ʹ�����ɫ������ʾ
        self.verticalHeader().setVisible(False)  # ���ش�ֱ���� ���
        # self.horizontalHeader().setStretchLastSection(True)  # �������һ���Զ��������
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # ��ֹ�༭

        # ���ñ�ͷ
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

        # ��ʼ���г�����Ϣ
        for i in range(len(self.headers)):
            self.headers_width.append(
                {"min_width": 0, "max_width": 999}
            )

        """
        # QHeaderView.ResizeMode.Interactive  �����ֶ���ק��Ĭ�ϵľ��ǣ��������������Ծ��������ֶ���ק
        # QHeaderView.ResizeMode.ResizeToContents  �п������������Ӧ
        # QHeaderView.ResizeMode.Fixed �̶����
        # QHeaderView.ResizeMode.Stretch  ����仯
        """

        # ���ñ�ͷ�ĳ��Ȳ���
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
        ���������
        :param data_list: �����б�[[id],[],[]]��������ʽ,Ҫע�⣬��һ��һ����id�ֶ�
        :param page: ��ҳ����Żᰴ�����������
        :return:
        """

        self.check_box_group.clear()
        self.clearContents()  # �����Ԫ������
        row_num = len(data_list)
        if row_num > self.max_row:
            row_num = self.max_row
        self.setRowCount(row_num)

        page_num = (page - 1) * self.max_row

        for row in range(row_num):
            for col in range(self.col_num + 2):  # �����и���źͰ�ť
                # ��һ�и���ť
                if col == 0:
                    check_box = QCheckBox()
                    # ��ť��Ҫ��¼���ݵ�id������ѡ��ʱ��Ĳ���
                    self.check_box_group.append(check_box, data_list[row][0])
                    self.setCellWidget(row, 0, self.__center_cb(check_box))
                # �ڶ��и����
                elif col == 1:
                    self.setItem(row, 1, self.__center_item(page_num + row + 1))
                # ������������
                else:
                    data = data_list[row][col - 1]
                    self.setItem(row, col, self.__center_item(data))

        # ���������п�
        # self.__resize_col_width()

    # ���ر�ѡ�����ݵ�id�б�
    def selected_id(self):
        return self.check_box_group.selected_id()

    # ȫѡ
    def select_all(self):
        self.check_box_group.select_all()

    # ȡ��ȫѡ
    def cancel_select_all(self):
        self.check_box_group.cancel_all()

    # �����е���С��Ⱥ������
    def set_col_width(self, index: int, min_width: int = 0, max_width: int = 9999):
        self.headers_width[index]["min_width"] = min_width
        self.headers_width[index]["max_width"] = max_width

    @staticmethod
    def __center_cb(check_box):
        # ����һ��������ʾ��ť�Ĵ���

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
        # �����г����޸ĳɺ��ʴ�С
        self.resizeColumnsToContents()

        # ÿ1�и���set_col_width()���õ���С����������������
        for col in range(len(self.headers)):

            col_width = self.horizontalHeader().sectionSize(col)  # ��������ʵĿ��
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
            get_data_funcΪ���ݽӿں�������Ҫ���������б�
            ��ʽΪ[[id, name, age], [id, name, age]]
            ��һ�����ݱ���Ϊid��Ҫ�͸�ѡ��󶨣��޸�ɾ�����ݵ�ʱ����Ҫ
            ���� get_data_demo����
        """
        # get_data_func���ݽӿں���
        self.get_data_func = get_data_func

        self.table = table

        # �������ò���
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        ))

        # ���ô��ڸ߶�
        self.setFixedHeight(40)

        # ������Ӳ���
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(5)

        # ��ҳ��������Ϊ��ɫ
        self.setStyleSheet("background-color:#fff;")

        # page��ѡ�е���ʽ
        self.page_btn_selected_sheet = "border: 1px solid #E3E5E7"  # ѡ�е���ʽ

        # ��ҳpage��ʾ���ٸ���ֻ���ǵ�������С��7 �����7����ô���� < 1 ������ 3 4 5 ������ 999 >
        self.page_btn_num = 7

        # �Զ����������
        self.current_page = 1  # ��ǰҳ��
        self.page_into: QLabel = ...  # ��ҳ��Ϣ
        self.page_skip: QLineEdit = ...  # ��ת��
        self.page_btn_list = list()  # ��ҳpage��ţ�page_num��
        self.data_count = 0

        # ������
        self.init_ui()

        # ���ݳ�ʼ�������µ�1ҳ������
        self.update_table(self.current_page)

    def init_ui(self):

        # ������� �߶���䣬��ȹ̶�
        control_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # 1.���ȫѡ��
        select_all_btn = QCheckBox("ȫѡ", parent=self)
        select_all_btn.clicked.connect(self.__select_all_func)
        select_all_btn.setSizePolicy(control_policy)
        self.layout.addWidget(select_all_btn)

        # 2.��ӹ̶����ɵ���
        spacer1_item = QSpacerItem(130, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer1_item)

        # 3.�����չ����
        spacer2_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer2_item)

        # 4.��ӷ�ҳ���
        page_box = QFrame(parent=self)
        page_box.setSizePolicy(control_policy)
        page_box.setFixedHeight(25)
        self.layout.addWidget(page_box)

        page_box_layout = QHBoxLayout(page_box)
        page_box_layout.setContentsMargins(10, 0, 10, 0)
        page_box_layout.setSpacing(5)

        # 4.1 �����һҳ
        prior_btn = ClickLabel(parent=page_box)
        prior_btn.setStyleSheet("margin-right: 10px;")
        prior_btn.setObjectName("prior_btn")
        prior_btn.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        prior_btn.setPixmap(QPixmap("static/icon/prior.png"))
        prior_btn.setSizePolicy(control_policy)
        prior_btn.setMinimumWidth(20)
        prior_btn.clicked.connect(lambda: self.__page_func(prior_btn))
        page_box_layout.addWidget(prior_btn)

        # 4.2 ��ӷ�ҳ ��ʵ���԰���һҳ����һҳҲ�ӽ����������Ķ����벻ֱ��
        for i in range(self.page_btn_num):
            page_btn = ClickLabel(f"{i + 1}", parent=page_box)
            page_btn.setObjectName(f"page{i + 1}_btn")
            page_btn.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            page_btn.setSizePolicy(control_policy)
            page_btn.setMinimumWidth(20)
            page_box_layout.addWidget(page_btn)
            # ����������У���Ϊpage_btn�������һ��page7_btn
            # page_btn.clicked.connect(lambda: self.__page_func(page_btn))
            page_btn.clicked.connect(lambda pb=page_btn: self.__page_func(pb))
            self.page_btn_list.append(page_btn)

        # 4.3 �����һҳ
        next_btn = ClickLabel(parent=page_box)
        next_btn.setStyleSheet("margin-left: 10px")
        next_btn.setObjectName("next_btn")
        next_btn.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        next_btn.setPixmap(QPixmap("static/icon/next.png"))
        next_btn.setSizePolicy(control_policy)
        next_btn.setMinimumWidth(20)
        next_btn.clicked.connect(lambda: self.__page_func(next_btn))
        page_box_layout.addWidget(next_btn)

        # 5 �����չ����
        spacer3_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer3_item)

        # 6 ��ӷ�ҳ��Ϣ
        page_into = QLabel("181ҳ/3999��", parent=self)
        page_into.setSizePolicy(control_policy)
        self.layout.addWidget(page_into)
        self.page_into = page_into
        # print(page_into.widthMM())

        # 7.�����ת
        skip_box = QFrame(self)
        skip_box.setSizePolicy(control_policy)
        self.layout.addWidget(skip_box)

        skip_box_layout = QHBoxLayout(skip_box)
        skip_box_layout.setContentsMargins(10, 0, 0, 0)
        skip_box_layout.setSpacing(5)

        # ��� "��ת"
        skip_label1 = QLabel("��ת", parent=skip_box)
        skip_label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        skip_label1.setSizePolicy(control_policy)
        skip_box_layout.addWidget(skip_label1)

        # ��������
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

        # ��� "ҳ"
        skip_label1 = QLabel("ҳ", parent=skip_box)
        skip_label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        skip_label1.setSizePolicy(control_policy)
        skip_box_layout.addWidget(skip_label1)

    def __select_all_func(self, state):
        """ȫѡ��Ĳۺ���"""
        if state:
            self.table.select_all()
        else:
            self.table.cancel_select_all()

    def __page_func(self, page_btn):
        """pageҳ����һҳ����һҳ�Ĳۺ���"""
        # ��ȡ�����ҳ��
        # ��һҳ
        if page_btn.objectName() == "prior_btn":
            page_num = self.current_page - 1
            if page_num <= 0:
                return
        # ��һҳ
        elif page_btn.objectName() == "next_btn":
            page_num = self.current_page + 1
            if page_num > self.data_count / self.table.max_row:
                return
        # ����ҳ
        else:
            try:
                page_num = int(page_btn.text())
            except:
                return

        # ���±��
        self.update_table(page_num)

    def update_table(self, page_num):
        """����page������table.max_row�������ҳ����ȡ���������񣬸���page������"""

        # �����޸ĵ�ǰ����ҳ
        self.current_page = page_num

        # ������ �����
        offset = (page_num - 1) * self.table.max_row
        self.data_count, data_list = self.get_data_func(offset, self.table.max_row)
        self.table.fill_data(data_list, page_num)

        # ����page�� -------------

        # 1.����״̬��
        total_pages = math.ceil(self.data_count / self.table.max_row)
        self.page_into.setText(f"{total_pages}ҳ/{self.data_count}��")

        # 2.���·�ҳ
        self.page_skip.setText(f"{self.current_page}")

        # 3.����page��
        # ���С��7ҳ���ж���ҳ��ʾ����
        if total_pages <= self.page_btn_num:
            for i in self.page_btn_list[total_pages:]:
                i.hide()

        # �������7ҳ��page1_btn=1, page_end_btn=total_pages
        else:
            # ������β
            self.page_btn_list[0].setText("1")
            self.page_btn_list[self.page_btn_num - 1].setText(f"{total_pages}")

            """
                ���� page_num=7 (7��pageҳ)��������� 
                1. < 1 2 3 4 5 ... 10 > 
                2. < 1 ... 6 7 8 9 10 >
                3. < 1 ... 5 6 7 ... 10>

                ��1�֣���ת1 2 3 4��ʱ����Ҫ��ǰ��5����� 1 2 3 4 5
                ��2�֣���ת7 8 9 10��ʱ����Ҫ�Ѻ���5����� 6 7 8 9 10
                ��3�֣��������Ĳ��ǵ�1 2 �֣����ǵ�3���ˣ����߶�Ҫ��ʡ�Ժţ����ҵ����pageҳ���м䣬������������������

                Ϊʲô��ǰ4 ���ߺ�4�� ��Ϊȥ������3�����ܵ��(���˾ͻ�����������)��7-3=4 
                ����margin_num = 3 ,����page_num�Ƕ��٣�margin_num����3
            """
            margin_num = 3

            # ��1�֣����ǰ4��
            if self.current_page <= self.page_btn_num - margin_num:
                self.page_btn_list[self.page_btn_num - 2].setText("������")
                start_num = 2
                for i in self.page_btn_list[1:-2]:
                    i.setText(f"{start_num}")
                    start_num += 1
            # �ڶ��֣������4��
            elif self.current_page >= total_pages - margin_num:
                self.page_btn_list[1].setText("������")
                start_num = total_pages - 1
                for i in self.page_btn_list[-2:1:-1]:
                    i.setText(f"{start_num}")
                    start_num -= 1
            # �����֣�����м��
            else:
                self.page_btn_list[1].setText("������")
                self.page_btn_list[self.page_btn_num - 2].setText("������")

                center_page_num = self.page_btn_num - 4  # �м��������ʾ����pageҳ

                # �����7ҳ���м���ʾ3ҳ����ǰҳ��10����ô����9 10 11��9=��ǰҳ-��ȡ��(center_page_num/2)
                start_num = self.current_page - int(center_page_num / 2)
                for i in self.page_btn_list[2:-2]:
                    i.setText(f"{start_num}")
                    start_num += 1

        # 4.���ñ�ѡ�е�page��ʽ
        for i in self.page_btn_list:
            if i.text() == str(self.current_page):
                i.setStyleSheet(self.page_btn_selected_sheet)
            else:
                i.setStyleSheet("")

    @staticmethod
    def get_data_demo(offset, limit):
        """
        ����������
        ��������������������offset��limit��offset��limit���ڷ�ҳ
        ���뷵�����������������б������б��1�б���Ϊ����id(������ʾ)��ʣ�µĸ��ݱ�ͷ���Ⱦ���
        """

        # �������������ڷ�ҳʹ��
        total_count = 100

        # �����б����ݵ�����0һ��Ҫ������id��ɾ���޸ĵ�ʱ��Ϳ���֪������id��
        data_list = list()
        for i in range(offset, offset + limit, 1):
            data_list.append(
                [i + 1, f"��ͼͼ{i + 1}", "15555555555", '6', "����ʡ֣���н�ˮ��������ַ�����԰����¥1001��"]
            )

        return total_count, data_list


# ��׽pyqt6������
def handle_exception(*args, **kwargs):
    traceback.print_exception(*args)
    sys.exit()


if __name__ == '__main__':
    app = QApplication([])
    sys.excepthook = handle_exception

    # ����һ������
    widget = QWidget()
    widget.setGeometry(200, 200, 800, 500)

    # �������
    table_widget = TableWidget(10, ["����", "�绰", "����", "��ַ"])

    # ��������ҳ����
    table_page = TablePage(table_widget, TablePage.get_data_demo)

    v_layout = QVBoxLayout(widget)
    v_layout.setSpacing(0)
    v_layout.addWidget(table_widget)
    v_layout.addWidget(table_page)

    widget.show()

    app.exec()


