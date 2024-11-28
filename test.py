import sys
import numpy as np
from scipy.stats import norm
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
from io import BytesIO


# 假设这是你的类的一部分
class YourClass:
    def __init__(self):
        self.distribution_set = True
        self.textBrowser = QTextBrowser()  # 假设你已经初始化了这个控件
        self.column_list = ['column1', 'column2']  # 示例列名
        self.plot_data = {
            'column1': np.random.normal(5, 2, 100),
            'column2': np.random.normal(3, 1, 100)
        }
        self.min_val = 0
        self.max_val = 10
        self.colormap2 = lambda i: f'color{i}'  # 示例颜色映射函数

    def plot_and_show_equations(self):
        if self.distribution_set:
            fit_equations = {}
            for i, column in enumerate(self.column_list):
                plot_data_drop = self.plot_data[column].dropna()
                mu, std = norm.fit(plot_data_drop)
                x = np.linspace(self.min_val, self.max_val, 100)
                y = norm.pdf(x, mu, std)
                ax.plot(x, y, '-.', color=self.colormap2(i), linewidth=2, label=f'{column}-Fit')

                # 保存拟合线方程（LaTeX 格式）
                fit_equation = f"f(x) = \\frac{{1}}{{{std:.2f} \\sqrt{{2\\pi}}}} e^{{-\\frac{{(x - {mu:.2f})^2}}{{2 {std:.2f}^2}}}}"
                fit_equations[column] = fit_equation

            # 将所有列的拟合线方程显示在 QTextBrowser 中
            for column, equation in fit_equations.items():
                self.textBrowser.append(f"拟合线方程 ({column}): ")
                self.textBrowser.append(self.latex_to_image(equation))

    def latex_to_image(self, equation):
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f'${equation}$', fontsize=20, ha='center', va='center')
        ax.axis('off')

        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        return f'<img src="data:image/png;base64,{buf.getvalue().hex()}">'


# 示例应用
app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
text_browser = QTextBrowser()
layout.addWidget(text_browser)

your_class_instance = YourClass()
your_class_instance.textBrowser = text_browser
your_class_instance.plot_and_show_equations()

window.setLayout(layout)
window.show()
sys.exit(app.exec_())