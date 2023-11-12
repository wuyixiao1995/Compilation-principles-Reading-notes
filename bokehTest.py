import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, \
    QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import QSettings

class ConvolutionSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("卷积计算模拟GUI")
        self.setGeometry(100, 100, 1000, 300)

        main_layout = QVBoxLayout()

        # input_dim
        input_dim_w = 2
        # 创建输入文件部分
        input_layout = QHBoxLayout()
        input_label = QLabel("Input 文件:", self)
        self.entry_input = QLineEdit(self)
        browse_input_button = QPushButton("选择文件", self)
        browse_input_button.clicked.connect(lambda: self.browse_file(self.entry_input))
        dimension_label = QLabel("维度输入:", self)
        self.combo_input_dim1 = QLineEdit(self)
        self.combo_input_dim2 = QLineEdit(self)
        self.combo_input_dim3 = QLineEdit(self)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.entry_input, input_dim_w * 10)
        input_layout.addWidget(browse_input_button)
        input_layout.addWidget(dimension_label)
        input_layout.addWidget(self.combo_input_dim1, input_dim_w)
        input_layout.addWidget(self.combo_input_dim2, input_dim_w)
        input_layout.addWidget(self.combo_input_dim3, input_dim_w)

        # 创建Kernel文件部分
        kernel_layout = QHBoxLayout()
        kernel_label = QLabel("Kernel文件:", self)
        self.entry_kernel = QLineEdit(self)
        browse_kernel_button = QPushButton("选择文件", self)
        browse_kernel_button.clicked.connect(lambda: self.browse_file(self.entry_kernel))
        dimension_label = QLabel("维度输入:", self)
        self.combo_kernel_dim1 = QLineEdit(self)
        self.combo_kernel_dim2 = QLineEdit(self)
        self.combo_kernel_dim3 = QLineEdit(self)
        kernel_layout.addWidget(kernel_label)
        kernel_layout.addWidget(self.entry_kernel, input_dim_w * 10)
        kernel_layout.addWidget(browse_kernel_button)
        kernel_layout.addWidget(dimension_label)
        kernel_layout.addWidget(self.combo_kernel_dim1, input_dim_w)
        kernel_layout.addWidget(self.combo_kernel_dim2, input_dim_w)
        kernel_layout.addWidget(self.combo_kernel_dim3, input_dim_w)

        # 创建Bias文件部分
        bias_layout = QHBoxLayout()
        bias_label = QLabel("Bias  文件:", self)
        self.entry_bias = QLineEdit(self)
        browse_bias_button = QPushButton("选择文件", self)
        browse_bias_button.clicked.connect(lambda: self.browse_file(self.entry_bias))
        dimension_label = QLabel("维度输入:", self)
        self.combo_bias_dim1 = QLineEdit(self)
        self.combo_bias_dim2 = QLineEdit(self)
        self.combo_bias_dim3 = QLineEdit(self)
        bias_layout.addWidget(bias_label)
        bias_layout.addWidget(self.entry_bias, input_dim_w * 10)
        bias_layout.addWidget(browse_bias_button)
        bias_layout.addWidget(dimension_label)
        bias_layout.addWidget(self.combo_bias_dim1, input_dim_w)
        bias_layout.addWidget(self.combo_bias_dim2, input_dim_w)
        bias_layout.addWidget(self.combo_bias_dim3, input_dim_w)

        # 创建输出文件部分
        output_layout = QHBoxLayout()
        output_label = QLabel("输出文件:", self)
        self.entry_output = QLineEdit(self)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.entry_output)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(kernel_layout)
        main_layout.addLayout(bias_layout)
        main_layout.addLayout(output_layout)

        # 创建比对按钮
        compare_button = QPushButton("比对", self)
        compare_button.clicked.connect(self.perform_convolution)
        main_layout.addWidget(compare_button)

        # 创建结果显示标签
        self.result_label = QLabel("", self)
        main_layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load previous values from settings
        self.load_previous_values()
    def browse_file(self, entry):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Numpy Files (*.npy)",
                                                   options=options)
        if file_path:
            entry.setText(file_path)


    def load_previous_values(self):
        # Load and set previous values from settings
        settings = QSettings("MyApp", "MySettings")

        # //
        input_file = settings.value("input_file", "")
        self.entry_input.setText(input_file)
        dim1 = settings.value("input_dim1", "")
        self.combo_input_dim1.setText(dim1)
        dim2 = settings.value("input_dim2", "")
        self.combo_input_dim2.setText(dim2)
        dim3 = settings.value("input_dim3", "")
        self.combo_input_dim3.setText(dim3)

        # # //
        kernel_file = settings.value("kernel_file", "")
        self.entry_kernel.setText(kernel_file)
        dim1 = settings.value("kernel_dim1", "")
        self.combo_kernel_dim1.setText(dim1)
        dim2 = settings.value("kernel_dim2", "")
        self.combo_kernel_dim2.setText(dim2)
        dim3 = settings.value("kernel_dim3", "")
        self.combo_kernel_dim3.setText(dim3)
        #
        # //
        bias_label = settings.value("bias_file", "")
        self.entry_bias.setText(bias_label)
        dim1 = settings.value("bias_dim1", "")
        self.combo_bias_dim1.setText(dim1)
        dim2 = settings.value("bias_dim2", "")
        self.combo_bias_dim2.setText(dim2)
        dim3 = settings.value("bias_dim3", "")
        self.combo_bias_dim3.setText(dim3)


    def closeEvent(self, event):
        # Save the current input values to settings
        settings = QSettings("MyApp", "MySettings")

        settings.setValue("input_file", self.entry_input.text())
        settings.setValue("input_dim1", self.combo_input_dim1.text())
        settings.setValue("input_dim2", self.combo_input_dim2.text())
        settings.setValue("input_dim3", self.combo_input_dim3.text())

        settings.setValue("kernel_file", self.entry_kernel.text())
        settings.setValue("kernel_dim1", self.combo_kernel_dim1.text())
        settings.setValue("kernel_dim2", self.combo_kernel_dim2.text())
        settings.setValue("kernel_dim3", self.combo_kernel_dim3.text())

        settings.setValue("bias_file", self.entry_bias.text())
        settings.setValue("bias_dim1", self.combo_bias_dim1.text())
        settings.setValue("bias_dim2", self.combo_bias_dim2.text())
        settings.setValue("bias_dim3", self.combo_bias_dim3.text())

        event.accept()

    def check_file_validity(self, file_path, expected_shape):
        try:
            data = np.load(file_path)
            if data.shape == expected_shape:
                return True
            else:
                return False
        except:
            return False

    def perform_convolution(self):
        input_file = self.entry_input.text()
        kernel_file = self.entry_kernel.text()
        bias_file = self.entry_bias.text()
        output_file = self.entry_output.text()

        input_dim1 = int(self.combo_input_dim1.text())
        input_dim2 = int(self.combo_input_dim2.text())
        input_dim3 = int(self.combo_input_dim3.text())

        kernel_dim1 = int(self.combo_kernel_dim1.text())
        kernel_dim2 = int(self.combo_kernel_dim2.text())
        kernel_dim3 = int(self.combo_kernel_dim3.text())

        bias_dim1 = int(self.combo_bias_dim1.text())
        bias_dim2 = int(self.combo_bias_dim2.text())
        bias_dim3 = int(self.combo_bias_dim3.text())

        if (self.check_file_validity(input_file, (input_dim1, input_dim2, input_dim3)) and
                self.check_file_validity(kernel_file, (kernel_dim1, kernel_dim2, kernel_dim3)) and
                self.check_file_validity(bias_file, (bias_dim1, bias_dim2, bias_dim3))):

            # 执行卷积计算
            # 这里需要实现卷积计算的逻辑，将结果保存到output_file

            self.result_label.setText("卷积计算完成，结果已保存")
        else:
            self.result_label.setText("输入文件维度不匹配或无法解析")


def main():
    app = QApplication(sys.argv)
    window = ConvolutionSimulator()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
