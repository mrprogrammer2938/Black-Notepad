#!/usr/bin/python3
# Made By Sina Meysami
# Black-Notepad v1.0
#


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from colorama import init,Fore,Back,Style
import qdarktheme
import sys,platform,datetime
init()
width = 1000
height = 700


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        qdarktheme.setup_theme("dark")
        self.file = False
        self.file_path = ""
        self.setWindowTitle("Black Notepad")
        self.setWindowIcon(QIcon("black-notepad-icon.ico"))
        self.setGeometry(500,150,width,height)
    
        
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        
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
        self.view = self.menu_.addMenu("&View")
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
        self.font.addAction("Set Font Size",self.font_size)
        self.font.addAction("Set Font Color",self.font_color)

        
        self.edit.addAction("Undo",self.text.undo)
        self.edit.addAction("Redo",self.text.redo)
        self.edit.addSeparator()
        self.edit.addAction("Cut",self.text.cut)
        self.edit.addAction("Copy",self.text.copy)
        self.edit.addAction("Paste",self.text.paste)
        self.edit.addSeparator()
        self.edit.addAction("Select All",self.text.selectAll)
        self.edit.addAction("Clear All",self.text.clear)
        self.view.addAction("Fullscreen",lambda: self.showFullScreen())
        self.view.addAction("Normal",lambda: self.showNormal())
        self.view.addAction("Minimize",lambda: self.showMinimized())
        self.help.addAction("Help",self.help_)
        self.help.addAction("About",self.about_)
        self.help.addAction("Donate",self.donate)
        self.help.addSeparator()
        self.help.addAction("Send Feedback",self.send_feedback)
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
        history_key = QShortcut(QKeySequence("Ctrl+H"),self)
        history_key.activated.connect(self.help_)
        
        
    def set_toolbar(self):
        tools = QToolBar()
        tools.setStatusTip("Tools")
        tools.setMovable(False)
        self.addToolBar(tools)
        tools.addAction(QIcon("new_file.png"),"New File",self.new_file)
        tools.addAction(QIcon("open_file.png"),"Open File",self.open_file)
        tools.addAction(QIcon("save_file.jpg"),"Save File",self.save_file)
        tools.addAction(QIcon("save_as.png"),"Save As",self.save_as)
        tools.addAction(QIcon("help_icon.png"),"Help",self.help_)
        tools.addAction(QIcon("exit_icon.png"),"Exit",self.close)
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
        self.setWindowTitle("Notepad - New File")
    
    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","All Files (*)", options=options)
        self.file_path = fileName
        
        if self.file_path != "":
            self.file = True
        if fileName:
            f = open(fileName).read()
            self.text.setText(f)
            self.setWindowTitle(f"Black Notepad - {fileName}")
    
    def save_file(self):
        if self.file == True:
            file = open(self.file_path,'w')
            text = self.text.toPlainText()
            file.write(text)
        else:
            try:
                
                name = QFileDialog.getSaveFileName(self, 'Save File')
                self.file_path = name[0]
                self.setWindowTitle(f"Black Notepad - {name[0]}")
                file = open(self.file_path,'w')
                text = self.text.toPlainText()
                file.write(text)
            
                file.close()
                if self.file_path != "":
                    self.file = True
            except (Exception,FileNotFoundError,):
                self.file = False
    def save_as(self):
        if self.file == True and self.file_path != "":
            f = open(self.file_path,"w")
            f.write(self.text.toPlainText())
            f.close()
        else:
            try:
                name = QFileDialog.getSaveFileName(self, 'Save As')
                self.setWindowTitle(f"Black Notepad - {name[0]}")
                
                file = open(name[0],'w')
                text = self.text.toPlainText()
                file.write(text)
                file.close()
                if name[0] != "":
                    self.file = True
                    self.file_path = name[0]
            except (Exception,FileNotFoundError,):
                self.file = False
    def print_dialog(self):
        print = QPrintDialog()
        if print.exec_():
            self.text.print_(print.printer())
    def help_(self):
        width = 500
        height = 400
        text = """Developer: Sina Meysami
Version: v1.0
Ctrl + Q = QUIT
Ctrl + E = Exit
Ctrl + P = Print
Ctrl + O = Open File
Ctrl + S = Save File
Ctrl + Shift + S = Save As
Ctrl + H = Help
"""
        dlg = QDialog()
        dlg.setWindowTitle("Black-Notepad/Help")
        dlg.setWindowIcon(QIcon("./Icon/black-notepad-icon"))
        
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
        text = """Developer: Sina Meysami
Version: v1

Instagram: https://instagram.com/sina.coder
Twitter: https://twitter.com/Sinameysami
Github: https://github.com/mrprogrammer2938
Weblog: sinameysami.blogfa.com
"""
        dlg = QDialog()
        dlg.setWindowTitle("Black-Notepad/About")
        dlg.setWindowIcon(QIcon("./Icon/black-notepad-icon.png"))
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
        
    def donate(self):
        #webbrowser.open_new_tab("https://google.com")
        pass
    def send_feedback(self):
        #webbrowser.open_new_tab("")
        pass
    def font_dialog(self):
        font,ok = QFontDialog.getFont()
        if ok:
            self.text.setFont(font)
            
    def font_size(self):
        dlg = QDialog()
        dlg.setWindowTitle("Set Font Size")
        dlg.setWindowIcon(QIcon("./Icon/black-notepad-icon"))
        dlg.setFixedSize(122,64)
        
        self.spinbox = QSpinBox(dlg)
        self.spinbox.resize(121,22)
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(72)
        self.spinbox.valueChanged.connect(self.set_font_size)
        
        set_btn = QPushButton("Set",dlg)
        set_btn.setGeometry(0,20,121,24)
        set_btn.clicked.connect(self.set_font_size)
        
        close_btn = QPushButton("Close",dlg)
        close_btn.setGeometry(0,40,121,24)
        close_btn.clicked.connect(dlg.close)
        
        rev = dlg.exec_()
    def set_font_size(self):
        self.text.setFontPointSize(self.spinbox.value())
    def font_color(self):
        font_color = QColorDialog().getColor()
        self.text.setTextColor(font_color)
    def statusbar_(self):
        status = QStatusBar(self)
        status.showMessage(f"Black-Notepad  {self.file_path}")
        self.setStatusBar(status)
    def get_error(self):
        error = QErrorMessage(self)
        error.showMessage("Error, Please Try Again!")
        error.show()
def main():
    date_now = datetime.datetime.now()
    print(f"\n{Fore.GREEN}Start Black-Notepad At: {Fore.BLUE}{date_now}{Fore.WHITE}\n")
    app = QApplication(sys.argv)
    app.setApplicationName("Black-Notepad")
    app.setApplicationVersion('1')
    win = Window()  
    win.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    # Black Notepad v1.0
    if platform.system() == "Windows" or platform.system() == "Linux" or platform.system() == "Darwin":
        main()
    else:
        print(f"{Back.BLACK}{Fore.GREEN}Sorry Please Run This App On Windows,Linux Or Mac OS!")
        Style.RESET_ALL()
        sys.exit()
    
