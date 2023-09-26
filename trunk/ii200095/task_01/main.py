import sys
from PyQt5.QtWidgets import QApplication
from widgets.Window import Window

def main():
	app = QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())

main() 
