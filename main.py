import sys
from PyQt6.QtWidgets import QApplication
from ui.mainwindow import MainWindow
from PyQt6.QtCore import QFile, QTextStream

def main():
    app = QApplication(sys.argv)

    style_file = QFile("style/theme.qss")
    if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()