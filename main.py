import os
import sys
import time

from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from qfluentwidgets import StateToolTip


from MainWindow import Ui_MainWindow  # 导入生成的窗口类
from convert import process_images


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.PushButton_md.clicked.connect(lambda: self.open_file_dialog("source_file_path"))
        self.ui.PushButton_output.clicked.connect(lambda: self.open_file_dialog("target_folder_path"))
        self.ui.SwitchButton.checkedChanged.connect(self.on_switch_changed)
        self.ui.PrimaryPushButton_Export.clicked.connect(self.convert)
        self.ui.IndeterminateProgressBar.setVisible(False)
        self.ui.IndeterminateProgressBar.pause()

    def resizeEvent(self, event):
        # 调用父类的 resizeEvent 方法
        super().resizeEvent(event)

        # 检查 stateTooltip 是否存在，并且窗口大小已经初始化
        if hasattr(self, 'ui') and hasattr(self.ui, 'stateTooltip'):
            # 获取窗口的右上角点坐标
            window_top_right = self.rect().topRight()
            # 计算提示框应该放置的位置（右上角对齐）
            tooltip_position = window_top_right - QPoint(300, -60)
            self.ui.stateTooltip.move(tooltip_position)

    def open_file_dialog(self, path_type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        if path_type == "source_file_path":
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Markdown Files (*.md);;All Files (*)",
                                                       options=options)
            if file_path:
                self.ui.LineEdit_md.setText(file_path)

        elif path_type == "target_folder_path":
            folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
            if folder_path:
                self.ui.LineEdit_output.setText(folder_path)

    def on_switch_changed(self):
        if self.ui.SwitchButton.isChecked():
            self.ui.BodyLabel_output.setVisible(False)
            self.ui.PushButton_output.setVisible(False)
            self.ui.LineEdit_output.setVisible(False)
        else:
            self.ui.BodyLabel_output.setVisible(True)
            self.ui.PushButton_output.setVisible(True)
            self.ui.LineEdit_output.setVisible(True)
            # 在这里可以添加其他控件的显示或隐藏逻辑

    def convert(self):
        modify_source_file_flag = self.ui.SwitchButton.isChecked()
        source_file_path = os.path.normpath(self.ui.LineEdit_md.text())
        # 获取文件名（带扩展名）
        file_name_with_extension = os.path.basename(source_file_path)
        # 获取不带扩展名的文件名
        file_name_without_extension, file_extension = os.path.splitext(file_name_with_extension)
        target_file_path = None
        asset_folder_path = None
        target_folder_path = None
        convert_validity = False
        if source_file_path == '.':
            print("Please pick source markdown file")

        else:
            if modify_source_file_flag:  # modify source file
                target_folder_path = os.path.dirname(source_file_path)
                asset_folder_path = os.path.normpath(os.path.join(target_folder_path, "assets"))
                target_file_path = source_file_path
                convert_validity = True

            else:  # modify new file
                asset_folder_path = os.path.normpath(self.ui.LineEdit_output.text())
                if asset_folder_path == '.':
                    print("Please fill assets output folder")
                else:
                    target_folder_path = os.path.dirname(asset_folder_path)
                    target_file_path = os.path.join(target_folder_path, f"{file_name_without_extension}_modify.md")
                    convert_validity = True

        if convert_validity:
            self.ui.stateTooltip = StateToolTip('正在转换', '客官请耐心等待哦~~', self)
            # 获取窗口的右上角点坐标
            window_top_right = self.rect().topRight()
            # 计算提示框应该放置的位置（右上角对齐）
            tooltip_position = window_top_right - QPoint(300, -60)
            self.ui.stateTooltip.move(tooltip_position)
            self.ui.stateTooltip.show()
            self.ui.IndeterminateProgressBar.setVisible(True)
            self.ui.IndeterminateProgressBar.resume()

            print(f"Source Markdown File Path : {source_file_path} \n"
                  f"Target Assets Folder Path : {asset_folder_path} \n"
                  f"Target Markdown File Path : {target_file_path}")

            if not os.path.exists(asset_folder_path):
                os.makedirs(asset_folder_path)  # 如果目标文件夹不存在，创建它

            process_images(source_file_path, target_file_path, asset_folder_path)
            self.ui.IndeterminateProgressBar.setVisible(False)
            self.ui.IndeterminateProgressBar.pause()
            self.ui.stateTooltip.setTitle("Finished")
            self.ui.stateTooltip.setContent('转换完成啦！')
            self.ui.stateTooltip.setState(True)
            self.ui.stateTooltip = None



def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
