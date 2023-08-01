#!/usr/bin/python3
# Made By Sina Meysami
# Black-Notepad v1.0
#


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
import sys,platform
width = 1000
height = 700


class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        self.file = False
        self.file_path = ""
        self.setWindowTitle("Notepad")
        self.setWindowIcon(QIcon("./Icon/black-notepad-icon.ico"))
        self.setGeometry(500,150,width,height)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        
        self.text = QTextEdit(self)
        self.text.setFont(font)
        self.setCentralWidget(self.text)
        self.key_shortcut()
        self.menu()
    def menu(self):
        self.menu_ = self.menuBar()
        self.file = self.menu_.addMenu("&File")
        self.edit = self.menu_.addMenu("&Edit")
        self.font = self.menu_.addMenu("&Font")
        self.theme = self.menu_.addMenu("&Theme")
        self.help = self.menu_.addMenu("&Help")
        
        self.file.addAction("New File",self.new_file)
        self.file.addAction("Open File",self.open_file)
        self.file.addAction("Save File",self.save_file)
        self.file.addAction("Save As",self.save_as)
        self.file.addSeparator()
        self.file.addAction("Print",self.print_dialog)
        self.file.addSeparator()
        self.file.addAction("&Exit",self.close)
        self.font.addAction("Set Font",self.font_dialog)
        self.theme.addAction("Light",self.light)
        self.theme.addAction("Dark",self.dark)
        self.theme.addAction("Matrix",self.matrix)
        self.theme.addAction("Sky",self.sky)
        self.edit.addAction("Undo",self.undo)
        self.edit.addAction("Redo",self.redo)
        self.edit.addSeparator()
        self.edit.addAction("Cut",self.cut)
        self.edit.addAction("Copy",self.copy)
        self.edit.addAction("Paste",self.paste)
        
        self.help.addAction("Help",self.help_)
        self.help.addAction("About",self.about_)
        self.statusbar_()
        self.set_toolbar()
    def key_shortcut(self):
        exit_key = QShortcut(QKeySequence("Ctrl+Q"),self)
        exit_key.activated.connect(self.close)
        exit_key_2 = QShortcut(QKeySequence("Ctrl+E"),self)
        exit_key_2.activated.connect(self.close)
        open_key = QShortcut(QKeySequence("Ctrl+O"),self)
        open_key.activated.connect(self.open_file)
        save_key = QShortcut(QKeySequence("Ctrl+S"),self)
        save_key.activated.connect(self.save_file)
        save_as_key = QShortcut(QKeySequence("Ctrl+Shift+S"),self)
        save_as_key.activated.connect(self.save_as)
        
    def set_toolbar(self):
        tools = QToolBar()
        tools.setMovable(False)
        self.addToolBar(tools)
        tools.addAction(QIcon("./Icon/new_file.png"),"New File",self.new_file)
        tools.addAction(QIcon("./Icon/open_file.png"),"Open File",self.open_file)
        tools.addAction(QIcon("./Icon/save_file.jpg"),"Save File",self.save_file)
        tools.addAction(QIcon("./Icon/help_icon.png"),"Help",self.help_)
        tools.addAction(QIcon("./Icon/exit_icon.png"),"Exit",self.close)
    def undo(self):
        self.text.undo()
    def redo(self):
        self.text.redo()
    def copy(self):
        self.text.copy()
    def paste(self):
        self.text.paste()
    def cut(self):
        self.text.cut()
    def new_file(self):
        self.text.clear()
        self.file = False
        self.file_path = ""
        self.setWindowTitle("Notepad")
    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
        self.file_path = fileName
        self.setWindowTitle(f"Notepad - {self.file_path}")
        self.file = True
        if fileName:
            f = open(fileName).read()
            self.text.setText(f)
    def save_file(self):
        if self.file == True:
            file = open(self.file_path,'w')
            text = self.text.toPlainText()
            file.write(text)
        else:
            try:
                self.file = True
                name = QFileDialog.getSaveFileName(self, 'Save File')
                self.file_path = name[0]
                self.setWindowTitle(f"Notepad - {name[0]}")
                file = open(self.file_path,'w')
                text = self.text.toPlainText()
                file.write(text)
            
                file.close()
            except (Exception,FileNotFoundError,):
                pass
    def save_as(self):
        if self.file:
            f = open(self.file_path,"w")
            f.write(self.text.toPlainText())
            f.close()
        else:
            try:
                name = QFileDialog.getSaveFileName(self, 'Save File')
                self.setWindowTitle(f"Notepad - {name[0]}")
                file = open(name[0],'w')
                text = self.text.toPlainText()
                file.write(text)
                file.close()
                self.file = True
            except (Exception,FileNotFoundError,):
                pass
    def print_page(self):
        pass
    def print_dialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer,self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.text.print_printer
    def help_(self):
        width = 500
        height = 400
        text = """ Developer: Sina Meysami
Version: v1.0
Ctrl + Q = QUIT
Ctrl + E = Exit
Ctrl + P = Print
Ctrl + O = Open File
Ctrl + S = Save File
"""
        dlg = QDialog()
        dlg.setWindowTitle("Black-Notepad/About")
        dlg.setGeometry(600,300,width,height)
        t = QTextEdit(dlg)
        t.setReadOnly(True)
        t.setText(text)
        t.resize(width,height)
        
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        t.setFont(font)
        res = dlg.exec_()
    def about_(self):
        width = 500
        height = 400
        text = """
Developer: Sina Meysami
Version: v1.0
Instagram: https://instagram.com/sina.coder
Twitter: https://twitter.com/Sinameysami
Github: https://github.com/mrprogrammer2938
"""
        dlg = QDialog()
        dlg.setWindowTitle("Black-Notepad/About")
        dlg.setGeometry(600,300,width,height)
        t = QTextEdit(dlg)
        t.setReadOnly(True)
        t.setText(text)
        t.resize(width,height)
        
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        t.setFont(font)
        res = dlg.exec_()
        
    
    def font_dialog(self):
        font,ok = QFontDialog.getFont()
        if ok:
            self.text.setFont(font)
            
    # ----- Theme -----
    def light(self):
        self.text.setStyleSheet("""
QTextEdit {
    color: black;
    background-color: white;    
        
}
                                
""")
    def dark(self):
        self.text.setStyleSheet("""
QTextEdit {
    color: white;
    background-color: black;     
}                                
                                
""")
    def matrix(self):
        self.text.setStyleSheet("""
QTextEdit {
    color: lightgreen;
    background-color: black;    
        
}
                                
""")
    def sky(self):
        self.text.setStyleSheet("""
QTextEdit {
    color: lightblue;
    background-color: blue;
    
}
                                
""")
    
    def statusbar_(self):
        status = QStatusBar(self)
        status.showMessage("Notepad v1.0")
        self.setStatusBar(status)
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Notepad")
    app.setApplicationDisplayName("Notepad")
    app.setApplicationVersion("v1.0")
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Black Notepad v1.0
    if platform.system() == "Windows" or platform.system() == "Linux" or platform.system() == "Mac":
        main()
    else:
        print("Sorry Please Run This App On Windows,Linux Or Mac OS!")
        sys.exit()
    