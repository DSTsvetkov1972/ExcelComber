import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment 
import os

from PySide6 import QtWidgets, QtCore
from colorama import Fore
from openpyxl import load_workbook, styles
import openpyxl
import os
import pyperclip
from PySide6 import QtWidgets, QtCore
from colorama import Fore
import global_vars 
import os
import pyperclip
import pandas as pd
from datetime import datetime
from my_threads.functions import get_files_and_sheets_from_pyperclip, all_control_elements_on, all_control_elements_off, check_files_modified, check_excel_file_is_open, on_finsh_change_thread
from time import sleep


class MarkEmptyColumnsThread(QtCore.QThread):
    def __init__ (self, md_files=False, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Помечаем непустые колонки"
        self.md_files = md_files

    mysignal = QtCore.Signal(str)

    def on_signal(self, mysignal):
        global_vars.ui.info_label.setStyleSheet('color: blue')            
        global_vars.ui.info_label.setText(mysignal)

    def run(self):
        self.error_message = ""
        self.warning_message = ""
        self.info_message = "" 

        self.is_src_files_modifyed = check_files_modified('.Исходники')
        self.is_md_files_modifyed = check_files_modified('.Размеченные')

        if self.is_src_files_modifyed:
            global_vars.ui.info_label.setStyleSheet('color: red')
            self.error_message = ('В папку .Исходники были добавлены новые файлы или\n'
                                  'некоторые файлы в ней были пересохранены или удалены.\n'
                                  'Нажмите кнопку "Просмотерь разметку"!')

            # global_vars.ui.info_label.setText(self.error_message)
            return
        
        #if self.is_md_files_modifyed:
        #    global_vars.ui.info_label.setStyleSheet('color: red')
        #    self.error_message = ('Файлы в папке .Размеченные были изменены.\n'
        #                          'Нажмите кнопку "Просмотерь разметку"!!')
        #    return
        
        

        files_sheets_list = get_files_and_sheets_from_pyperclip()
        files_list = list({files_sheets[0] for files_sheets in files_sheets_list})
        files_list.sort()

        self.md_files_opened = [file for file in files_list if check_excel_file_is_open(file)]
        if self.md_files_opened:
            self.warning_message = (
                f"Некоторые размеченные файлы открыты на рабочем столе!\n"
                f"{'\n'.join(self.md_files_opened)}"
                )

            #for md_file in md_files_opened:
            #    os.startfile(os.path.join(global_vars.project_folder, '.Размеченные', md_file))
            return




        file_preceding = ""
        need_to_save = False

        for file_sheet_number, file_sheet_list in enumerate(files_sheets_list, 1):
            # print(Fore.MAGENTA, file_sheet_list,  Fore.RESET)
            file = file_sheet_list[0]


            if file != file_preceding:

                if need_to_save:
                    self.mysignal.emit(
                        f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                        f'{files_list.index(file)+1} из {len(files_list)}. '
                        f'Сохраняем с помеченными не пустыми колонками: "{file}"')
                    # print(Fore.GREEN, 'Мы тут', Fore.RESET)
                    wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))

                file_preceding = file
                need_to_save = False

                self.mysignal.emit(
                    f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {files_list.index(file)+1} из {len(files_list)}. '
                    f'Загружаем для поиска не пустых колонок "{file}"')
                
                wb = load_workbook(os.path.join(global_vars.project_folder, '.Размеченные', file))

            
            sheet_name = file_sheet_list[1]


            self.mysignal.emit(
                f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {file_sheet_number} из {len(files_sheets_list)}. '
                f'Ищем не пустые колонки в книге: "{file}" в листе: "{file_sheet_list[0]}"')
            sleep(0.01)

            ws = wb[sheet_name]
                
            col_0 = ws['A']
            col_values = list([cell.value for cell in col_0])
            # print(Fore.MAGENTA, col_values , Fore.RESET)
            try:
                s_index = col_values.index('s')
                # print(s_index)                
            except ValueError:
                try:
                    s_index = col_values.index('sf')
                    f_index = col_values.index('sf')                           
                except ValueError:
                    continue

            try:
                f_index = col_values.index('f')
                # print(f_index) 
            except ValueError:
                try:
                    s_index = col_values.index('sf')
                    f_index = col_values.index('sf')                           
                except ValueError:
                    continue


            # print(s_index, f_index, s_index<=f_index)

            if not s_index<=f_index:
                continue


            for col_number, col in enumerate(list(ws.iter_cols())[2:], 3):
                col_values = list([cell.value for cell in col[s_index:f_index+1]])
                # print(col_number, col_values)

                if set(col_values) == {None}:
                    ws.cell(column=col_number, row=1).fill = styles.PatternFill(fill_type=None)
                else:
                    ws.cell(column=col_number, row=1).fill = styles.PatternFill(start_color='C6EFCE', fill_type='solid')
                    ws.cell(column=col_number, row=1).font = styles.Font(color='006100')
                    need_to_save = True


        if need_to_save:
            self.mysignal.emit(
                f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}.  {files_list.index(file)+1} из {len(files_list)}. ' 
                f'Сохраняем с помеченными не пустыми колонками: "{file}"')
            wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))
        else:
            wb.close()



    def on_clicked(self):
     
        self.start() # Запускаем поток  
     
        
    def on_started(self): # Вызывается при запуске потока
        all_control_elements_off()


    def on_finished(self): # Вызывается при завершении потока
        on_finsh_change_thread(self.message_title, self.error_message, self.warning_message, self.info_message, self.md_files_opened)
            
        all_control_elements_on()
