import sys
from PyQt5.QtWidgets import QApplication
from widgets.Window import Window

def mainFunc():
	application = QApplication(sys.argv)
	window_setter = Window()
	window_setter.show()
	system.exit(app.exec_())


mainFunc()