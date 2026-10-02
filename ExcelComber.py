from PySide6 import QtWidgets, QtCore, QtGui
from my_windows import main_window

import sys, os
import global_vars
from colorama import Fore
import resources_rc

from my_threads.functions import clean_process_folder, get_files_and_sheets_from_pyperclip, fill_in_md_files_table, fill_in_md_files_table_title, toggle_buttons, all_control_elements_off
# from my_threads.interface_thread import InterfaceThread

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
        #elf.interface_thread = InterfaceThread()
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

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)  # 0.5 сек
        self.timer.timeout.connect(self.poll_clipboard)  # без декоратора
        self.timer.start()

        global_vars.ui = main_window.Ui_MainWindow()
        global_vars.ui.setupUi(self)   

        
        self.get_release_thread.mysignal.connect(lambda: self.setWindowTitle(global_vars.title), QtCore.Qt.ConnectionType.QueuedConnection) 
        
        # Инструкция on-line, Связь с разработчиками
        global_vars.ui.action_show_manual.triggered.connect(self.show_manual)   
        global_vars.ui.action_show_dev_info.triggered.connect(self.show_dev_info) 

        # Выберите папку проекта    
        global_vars.ui.pushButtonChooseProjectFolder.clicked.connect(self.choose_project_folder_thread.on_clicked)
        self.choose_project_folder_thread.started.connect(all_control_elements_off)
        self.choose_project_folder_thread.finished.connect(self.choose_project_folder_thread.on_finished)
        #
        self.choose_project_folder_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)
        self.choose_project_folder_thread.mysignal_info_label_red.connect(self.info_label_red, QtCore.Qt.ConnectionType.QueuedConnection)
        self.choose_project_folder_thread.mysignal_info_label_green.connect(self.info_label_green, QtCore.Qt.ConnectionType.QueuedConnection)
        #
        self.choose_project_folder_thread.mysignal_project_folder_label_blue.connect(self.project_folder_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)
        self.choose_project_folder_thread.mysignal_project_folder_label_red.connect(self.project_folder_label_red, QtCore.Qt.ConnectionType.QueuedConnection)
        self.choose_project_folder_thread.mysignal_project_folder_label_green.connect(self.project_folder_label_green, QtCore.Qt.ConnectionType.QueuedConnection)                       

        # Конвертировать xls и xlsm в xlsx
        global_vars.ui.pushButtonXLStoXLSX.clicked.connect(self.xls_to_xlsx_thread.on_clicked)
        self.xls_to_xlsx_thread.started.connect(self.xls_to_xlsx_thread.on_started)
        self.xls_to_xlsx_thread.finished.connect(self.xls_to_xlsx_thread.on_finished)         

        # Просмотреть разметку 
        global_vars.ui.pushButtonProcessing.clicked.connect(self.processing_thread.on_clicked)
        self.processing_thread.started.connect(all_control_elements_off)
        self.processing_thread.finished.connect(self.processing_thread.on_finished)
        self.processing_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)

        # Открыть выбранные файлы из папки .Исходники
        global_vars.ui.pushButtonOpenChoosedFiles.clicked.connect(self.open_choosed_files_thread.on_clicked)
        self.open_choosed_files_thread.started.connect(all_control_elements_off)
        self.open_choosed_files_thread.finished.connect(self.open_choosed_files_thread.on_finished)
        self.open_choosed_files_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)
 
        # Открыть выбранные файлы из папки .Размеченные
        global_vars.ui.pushButtonOpenChoosedMDFiles.clicked.connect(self.open_choosed_mdfiles_thread.on_clicked)
        self.open_choosed_mdfiles_thread.started.connect(all_control_elements_off)
        self.open_choosed_mdfiles_thread.finished.connect(self.open_choosed_mdfiles_thread.on_finished)
        self.open_choosed_mdfiles_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)  

        # Удалить выбранные файлы из папки .Размеченные
        global_vars.ui.pushButtonDelChoosedMDFiles.clicked.connect(self.del_choosed_md_files_thread.on_clicked)
        self.del_choosed_md_files_thread.started.connect(all_control_elements_off)
        self.del_choosed_md_files_thread.finished.connect(self.del_choosed_md_files_thread.on_finished)
        # self.del_choosed_mdfiles_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)          

        # Объединить
        global_vars.ui.pushButtonConcat.clicked.connect(self.concat_thread.on_clicked)
        self.concat_thread.started.connect(all_control_elements_off)
        self.concat_thread.finished.connect(self.concat_thread.on_finished)
        self.concat_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)

        # Созадать файлы
        global_vars.ui.pushButtonMakeFiles.clicked.connect(self.make_files_thread.on_clicked)
        self.make_files_thread.started.connect(all_control_elements_off)
        self.make_files_thread.finished.connect(self.make_files_thread.on_finished)
        # self.make_files_thread.mysignal.connect(self.processing_thread.on_signal, QtCore.Qt.ConnectionType.QueuedConnection)

        # Заполнить заголовки        
        global_vars.ui.pushButtonHeadersFiller.clicked.connect(self.headers_filler_thread.on_clicked)
        self.headers_filler_thread.started.connect(all_control_elements_off)
        self.headers_filler_thread.finished.connect(self.headers_filler_thread.on_finished)
        self.headers_filler_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)   

        # Пометить непустые колонки
        global_vars.ui.pushButtonShowEmpty.clicked.connect(self.mark_empty_columns_thread.on_clicked)
        self.mark_empty_columns_thread.started.connect(all_control_elements_off)
        self.mark_empty_columns_thread.finished.connect(self.mark_empty_columns_thread.on_finished) 
        self.mark_empty_columns_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection) 

        # Удалить заголовки пустых колонок
        global_vars.ui.pushButtonCleanEmpty.clicked.connect(self.clean_empty_columns_thread.on_clicked)
        self.clean_empty_columns_thread.started.connect(all_control_elements_off)
        self.clean_empty_columns_thread.finished.connect(self.clean_empty_columns_thread.on_finished)
        self.clean_empty_columns_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)

        # Переименовать заголовки
        global_vars.ui.pushButtonRenameColumn.clicked.connect(self.rename_column_thread.on_clicked)      
        self.rename_column_thread.started.connect(all_control_elements_off)
        self.rename_column_thread.finished.connect(self.rename_column_thread.on_finished)
        self.rename_column_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection) 

        # Изменить примечание
        global_vars.ui.pushButtonChangeRem.clicked.connect(self.change_rems_thread.on_clicked)      
        self.change_rems_thread.started.connect(all_control_elements_off)
        self.change_rems_thread.finished.connect(self.change_rems_thread.on_finished)
        self.change_rems_thread.mysignal_info_label_blue.connect(self.info_label_blue, QtCore.Qt.ConnectionType.QueuedConnection)
 

    def on_clipboard_updated(self, files_sheet_to_show):
        """
        Выполняется в ГЛАВНОМ потоке. Здесь можно безопасно трогать GUI.
        """
        self.fill_in_md_files_table(files_sheet_to_show)
        self.fill_in_md_files_table_title(files_sheet_to_show)
        self.update_buttons_state(files_sheet_to_show)


    def fill_in_md_files_table_title(self, files_sheet_to_show):
        ui = global_vars.ui
        if files_sheet_to_show:
            if len(files_sheet_to_show[0]) == 2:
                files_qty = len({file[0] for file in files_sheet_to_show})
                ui.lineEditInClipboardTitle.setText(
                    f'Выбрано файлов: {files_qty}. Выбрано листов: {len(files_sheet_to_show)}.'
                )
            if len(files_sheet_to_show[0]) == 1:
                ui.lineEditInClipboardTitle.setText(
                    f'Выбрано файлов: {len(files_sheet_to_show)}'
                )
        else:
            ui.lineEditInClipboardTitle.setText('')


    def fill_in_md_files_table(self, files_sheet_to_show):

        ui = global_vars.ui 
        table = ui.tableMDFilesInClipboard

        if files_sheet_to_show:
            if len(files_sheet_to_show[0]) == 2:
                table.setColumnCount(2)
                table.setRowCount(len(files_sheet_to_show))

                for row, (file_name, sheet_name) in enumerate(files_sheet_to_show):
                    item_file = QtWidgets.QTableWidgetItem(file_name)
                    item_file.setForeground(QtGui.QColor(128, 128, 128))
                    item_sheet = QtWidgets.QTableWidgetItem(sheet_name)
                    item_sheet.setForeground(QtGui.QColor(128, 128, 128))

                    table.setItem(row, 0, item_file)
                    table.setItem(row, 1, item_sheet)

                table.setColumnWidth(0, 240)
                table.setColumnWidth(1, 60)

            elif len(files_sheet_to_show[0]) == 1:
                table.setColumnCount(1)
                table.setRowCount(len(files_sheet_to_show))

                for row, (file_name,) in enumerate(files_sheet_to_show):
                    item_file = QtWidgets.QTableWidgetItem(file_name)
                    item_file.setForeground(QtGui.QColor(128, 128, 128))
                    table.setItem(row, 0, item_file)
        else:
            ui.lineEditInClipboardTitle.setText('')
            table.setRowCount(0)


    def update_buttons_state(self, files_sheet_to_show):
        ui = global_vars.ui

        if files_sheet_to_show and global_vars.interface_enabled:
            if len(files_sheet_to_show[0]) == 2:
                ui.pushButtonOpenChoosedFiles.setEnabled(True)
                ui.pushButtonDelChoosedMDFiles.setEnabled(True)
                ui.pushButtonOpenChoosedMDFiles.setEnabled(True)
                ui.pushButtonHeadersFiller.setEnabled(True)
                ui.pushButtonShowEmpty.setEnabled(True)
                ui.pushButtonCleanEmpty.setEnabled(True)
                ui.pushButtonRenameColumn.setEnabled(True)
                ui.pushButtonChangeRem.setEnabled(True)
            elif len(files_sheet_to_show[0]) == 1:
                ui.pushButtonOpenChoosedFiles.setEnabled(True)
                ui.pushButtonDelChoosedMDFiles.setEnabled(True)
                ui.pushButtonOpenChoosedMDFiles.setEnabled(True)
                ui.pushButtonHeadersFiller.setEnabled(False)
                ui.pushButtonShowEmpty.setEnabled(False)
                ui.pushButtonCleanEmpty.setEnabled(False)
                ui.pushButtonRenameColumn.setEnabled(False)
                ui.pushButtonChangeRem.setEnabled(False)
        else:
            ui.pushButtonOpenChoosedFiles.setEnabled(False)
            ui.pushButtonOpenChoosedMDFiles.setEnabled(False)
            ui.pushButtonDelChoosedMDFiles.setEnabled(False)
            ui.pushButtonHeadersFiller.setEnabled(False)
            ui.pushButtonShowEmpty.setEnabled(False)
            ui.pushButtonCleanEmpty.setEnabled(False)
            ui.pushButtonRenameColumn.setEnabled(False)
            ui.pushButtonChangeRem.setEnabled(False)



    def info_label_blue (self, value):
        global_vars.ui.info_label.setStyleSheet('color: blue')   
        global_vars.ui.info_label.setText(value)

    def info_label_red (self, value):
        global_vars.ui.info_label.setStyleSheet('color: red')   
        global_vars.ui.info_label.setText(value) 

    def info_label_green (self, value):
        global_vars.ui.info_label.setStyleSheet('color: green')   
        global_vars.ui.info_label.setText(value)                 

    def project_folder_label_blue (self, value):
        global_vars.ui.project_folder_label.setStyleSheet('color: blue')   
        global_vars.ui.project_folder_label.setText(value) 

    def project_folder_label_red (self, value):
        global_vars.ui.project_folder_label.setStyleSheet('color: red')   
        global_vars.ui.project_folder_label.setText(value)         

    def project_folder_label_green (self, value):
        global_vars.ui.project_folder_label.setStyleSheet('color: green')   
        global_vars.ui.project_folder_label.setText(value) 


    def show_dev_info(self):
        QtWidgets.QMessageBox.about(None, "Контакты разработчиков", global_vars.dev_info)


    def show_manual(self):
        try:
            # 1/0
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(global_vars.manual_url))
        except:
            QtWidgets.QMessageBox.critical(None, "Нет соединения с интернетом", f"Инструкция опубликована на сайте {global_vars.manual_url}")

            
    def poll_clipboard(self):
        files_sheet_to_show = get_files_and_sheets_from_pyperclip()
        fill_in_md_files_table(files_sheet_to_show)
        fill_in_md_files_table_title(files_sheet_to_show)
        toggle_buttons(files_sheet_to_show)

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
    window.show()

    sys.exit(app.exec())
  
