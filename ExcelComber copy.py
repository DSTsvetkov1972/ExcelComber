from PySide6 import QtWidgets, QtCore, QtGui
from my_windows import main_window

import sys, os
import global_vars
from colorama import Fore
import resources_rc

from my_threads.functions import clean_process_folder
from my_threads.interface_thread import InterfaceThread

from my_threads.choose_project_folder import ChooseProjectFolderThread
from my_threads.xls_to_xlsx import XLS_TO_xlsxThread
from my_threads.headers_filler import HeadersFillerThread
from my_threads.processing import ProcessingThread
from my_threads.open_choosed_files import OpenChoosedFilesThread
from my_threads.del_choosed_md_files import DelChoosedMDFilesThread
from my_threads.concat import ConcatThread
from my_threads.make_files import MakeFilesThread

from my_threads.rename_column import RenameColumnThread
from my_threads.mark_empty_columns import MarkEmptyColumnsThread
from my_threads.clean_empty_columns import CleanEmptyColumnsThread
from my_threads.get_release import GetReleaseThread

from my_threads.change_rem import ChangeRemThread

class MyWindow(QtWidgets.QWidget):
    def __init__ (self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

####################################################################################
####################################################################################   

        self.choose_project_folder_thread = ChooseProjectFolderThread() 
        self.xls_to_xlsx_thread = XLS_TO_xlsxThread()
        self.interface_thread = InterfaceThread()
        #self.interface_thread.start()
        self.processing_thread = ProcessingThread()
        self.headers_filler_thread = HeadersFillerThread()     
        self.open_choosed_files_thread = OpenChoosedFilesThread(md_files = False)  
        self.open_choosed_mdfiles_thread = OpenChoosedFilesThread(md_files = True)      
        self.del_choosed_md_files_thread = DelChoosedMDFilesThread()
        self.concat_thread = ConcatThread()
        self.make_files_thread = MakeFilesThread()   
        self.change_rems_thread = ChangeRemThread()
        self.rename_column_thread = RenameColumnThread()
        self.mark_empty_columns_thread = MarkEmptyColumnsThread()
        self.clean_empty_columns_thread = CleanEmptyColumnsThread()
        self.get_release_thread = GetReleaseThread()
        #self.get_release_thread.start()



        global_vars.ui = main_window.Ui_MainWindow()
        global_vars.ui.setupUi(self)   

        self.open_choosed_files_thread.mysignal.connect(self.open_choosed_files_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
        self.open_choosed_mdfiles_thread.mysignal.connect(self.open_choosed_mdfiles_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)        
        self.processing_thread.mysignal.connect(self.processing_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
        self.headers_filler_thread.mysignal.connect(self.headers_filler_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)        
        self.concat_thread.mysignal.connect(self.processing_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
        self.make_files_thread.mysignal.connect(self.processing_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
        self.rename_column_thread.mysignal.connect(self.rename_column_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)  
        self.change_rems_thread.mysignal.connect(self.change_rems_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
        self.mark_empty_columns_thread.mysignal.connect(self.mark_empty_columns_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
        self.clean_empty_columns_thread.mysignal.connect(self.clean_empty_columns_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)
        self.get_release_thread.mysignal.connect(lambda: self.setWindowTitle(global_vars.title), QtCore.Qt.ConnectionType.QueuedConnection) 

        global_vars.ui.action_show_manual.triggered.connect(self.show_manual)   
        global_vars.ui.action_show_dev_info.triggered.connect(self.show_dev_info) 
            
        global_vars.ui.pushButtonChooseProjectFolder.clicked.connect(self.choose_project_folder_thread.on_clicked)
        self.choose_project_folder_thread.started.connect(self.choose_project_folder_thread.on_started)
        self.choose_project_folder_thread.finished.connect(self.choose_project_folder_thread.on_finished)
        
        global_vars.ui.pushButtonXLStoXLSX.clicked.connect(self.xls_to_xlsx_thread.on_clicked)
        self.xls_to_xlsx_thread.started.connect(self.xls_to_xlsx_thread.on_started)
        self.xls_to_xlsx_thread.finished.connect(self.xls_to_xlsx_thread.on_finished)         
         
        global_vars.ui.pushButtonProcessing.clicked.connect(self.processing_thread.on_clicked)
        self.processing_thread.started.connect(self.processing_thread.on_started)
        self.processing_thread.finished.connect(self.processing_thread.on_finished)  

        global_vars.ui.pushButtonOpenChoosedFiles.clicked.connect(self.open_choosed_files_thread.on_clicked)
        self.open_choosed_files_thread.started.connect(self.open_choosed_files_thread.on_started)
        self.open_choosed_files_thread.finished.connect(self.open_choosed_files_thread.on_finished)

        global_vars.ui.pushButtonOpenChoosedMDFiles.clicked.connect(self.open_choosed_mdfiles_thread.on_clicked)
        self.open_choosed_mdfiles_thread.started.connect(self.open_choosed_mdfiles_thread.on_started)
        self.open_choosed_mdfiles_thread.finished.connect(self.open_choosed_mdfiles_thread.on_finished)

        global_vars.ui.pushButtonDelChoosedMDFiles.clicked.connect(self.del_choosed_md_files_thread.on_clicked)
        self.del_choosed_md_files_thread.started.connect(self.del_choosed_md_files_thread.on_started)
        self.del_choosed_md_files_thread.finished.connect(self.del_choosed_md_files_thread.on_finished)

        global_vars.ui.pushButtonConcat.clicked.connect(self.concat_thread.on_clicked)
        self.concat_thread.started.connect(self.concat_thread.on_started)
        self.concat_thread.finished.connect(self.concat_thread.on_finished)

        
        global_vars.ui.pushButtonMakeFiles.clicked.connect(self.make_files_thread.on_clicked)
        self.make_files_thread.started.connect(self.make_files_thread.on_started)
        self.make_files_thread.finished.connect(self.make_files_thread.on_finished)

        
        global_vars.ui.pushButtonHeadersFiller.clicked.connect(self.headers_filler_thread.on_clicked)
        self.headers_filler_thread.started.connect(self.headers_filler_thread.on_started)
        self.headers_filler_thread.finished.connect(self.headers_filler_thread.on_finished)     


        global_vars.ui.pushButtonShowEmpty.clicked.connect(self.mark_empty_columns_thread.on_clicked)
        self.mark_empty_columns_thread.started.connect(self.mark_empty_columns_thread.on_started)
        self.mark_empty_columns_thread.finished.connect(self.mark_empty_columns_thread.on_finished)  

        
        global_vars.ui.pushButtonCleanEmpty.clicked.connect(self.clean_empty_columns_thread.on_clicked)
        self.clean_empty_columns_thread.started.connect(self.clean_empty_columns_thread.on_started)
        self.clean_empty_columns_thread.finished.connect(self.clean_empty_columns_thread.on_finished)

        global_vars.ui.pushButtonChangeRem.clicked.connect(self.change_rems_thread.on_clicked)      
        self.change_rems_thread.started.connect(self.change_rems_thread.on_started)
        self.change_rems_thread.finished.connect(self.change_rems_thread.on_finished)

        global_vars.ui.pushButtonRenameColumn.clicked.connect(self.rename_column_thread.on_clicked)      
        self.rename_column_thread.started.connect(self.rename_column_thread.on_started)
        self.rename_column_thread.finished.connect(self.rename_column_thread.on_finished)


    def show_dev_info(self):
        QtWidgets.QMessageBox.about(None, "Контакты разработчиков", global_vars.dev_info)

    def show_manual(self):
        try:
            # 1/0
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(global_vars.manual_url))
        except:
            QtWidgets.QMessageBox.critical(None, "Нет соединения с интернетом", f"Инструкция опубликована на сайте {global_vars.manual_url}")
            

    def closeEvent(self, event):
        for thread in (
            self.interface_thread,
            self.get_release_thread,
            # добавьте сюда остальные долгоживущие потоки, если нужно
        ):
            if thread.isRunning():
                thread.quit()
                thread.wait(3000)  # ждём до 3 секунд
        event.accept()

     

    

####################################################################################
####################################################################################         

if __name__ == "__main__":

    #global_vars.interface_enabled = False

    # подчищаем папку .Обработка из папки проекта
    # выбранной при предыдущем запуске программы
    if os.path.exists('.session_folder'):
        with open('.session_folder', encoding='utf-8') as f:
            precending_project_folder = f.readline()
    else:
        precending_project_folder = ''
    clean_process_folder(precending_project_folder)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.get_release_thread.start()
    window.interface_thread.start()
    window.show()

    sys.exit(app.exec())
  
    