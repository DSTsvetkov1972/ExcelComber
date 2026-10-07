from PySide6 import QtWidgets, QtCore
from colorama import Fore
import global_vars 
import os
import pandas as pd
from time import sleep
from datetime import datetime
from my_threads.functions import get_files_and_sheets_from_pyperclip, all_control_elements_on, all_control_elements_off, check_excel_file_is_open


class OpenChoosedFilesThread(QtCore.QThread):

    def __init__ (self, md_files=False, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Открываем выбранные файлы:"
        self.md_files = md_files

    mysignal_info_label = QtCore.Signal(str, str)
    
    
    def run(self):
        self.error_message = ""
        self.warning_message = ""
        self.info_message = "" 

        md_files = list(os.walk(os.path.join(global_vars.project_folder, '.Размеченные')))
        
        if not md_files:
            self.error_message = "Нет папки .Размеченные"
            return
        
        if not md_files[0][2]:
            self.error_message = "Нет файлов в папке .Размеченные"
            return

        files_sheet_to_show = get_files_and_sheets_from_pyperclip()
        # print(Fore.GREEN, files_sheet_to_show, Fore.RESET)
        self.files_to_show = list({file_sheet[0] for file_sheet in files_sheet_to_show})

        if self.files_to_show:
            self.files_to_show.sort()
            
            folder = os.path.join(global_vars.project_folder,'.Размеченные') if self.md_files \
                else os.path.join(global_vars.project_folder,'.Исходники')

            for file_number, file in enumerate(self.files_to_show, 1):
                file = file if self.md_files else file[3:]
                file_to_start = os.path.join(folder, file)     
                if not os.path.exists(file_to_start):
                    self.error_message = f"Файл {file_to_start} не найден в папке .Размеченные/"
                    return
                print(len(global_vars.project_folder), len(file_to_start))

                self.mysignal_info_label.emit(
                    f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                    f'{file_number} из {len(self.files_to_show)}. '
                    f'Открываем из папки {'.Размеченные' if self.md_files else '.Исходники'}: "{file}"',
                    'color: blue')
                #sleep(0.01)
                os.startfile(file_to_start)
                
                while True:
                    sleep(0.05)
                    # print('Открываем', os.path.join(folder, f"~${file}"))
                    # print(os.path.exists(os.path.join(folder, f"~${file}")))
                    if os.path.exists(os.path.join(folder, f"~${file}")):
                        break
        else:
            self.error_message = "Файлы которые нужно открыть не были выбраны"

        self.on_finished()    


    def on_clicked(self):      
        self.start() # Запускаем поток  
     

    def on_finished(self): # Вызывается при завершении потока


        if self.error_message:       
            self.mysignal_info_label.emit(
                self.error_message.replace('\n',' '),
                'color: red')

            QtWidgets.QMessageBox.critical(None,
                self.message_title,
                self.error_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok)
        else:         
            self.mysignal_info_label.emit(
                f'Из папки {".Размеченные" if self.md_files else ".Исходники"} на рабочем столе открыли файлов: {len(self.files_to_show)}.',
                'color: green')
            
        if self.warning_message:
            QtWidgets.QMessageBox.warning(None,
                self.message_title,
                self.warning_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok)
            
        if self.info_message:
            QtWidgets.QMessageBox.information(None,
                self.message_title,
                self.info_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok)    
