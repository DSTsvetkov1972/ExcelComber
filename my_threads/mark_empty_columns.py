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
from my_threads.functions import value_searcher, marking_checker, get_files_and_sheets_from_pyperclip, all_control_elements_on, all_control_elements_off, check_files_modified, check_excel_file_is_open, on_finsh_change_thread
from time import sleep


class MarkEmptyColumnsThread(QtCore.QThread):
    def __init__ (self, md_files=False, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Помечаем непустые колонки."
        self.folder = '.Размеченные'
        self.md_files = md_files

    mysignal_info_label_blue = QtCore.Signal(str)

    def run(self):
        self.error_message = ""
        self.error_list = []
        self.warning_message = ""
        self.info_message = ""
        self.md_files_opened = []
        
        if check_excel_file_is_open("errors.xlsx"):
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText('Закройте файл markup.xlsx перед тем как запустить обработку.')   
            self.error_message ='Файл errors.xlsx уже открыт на рабочем столе.\nЗакройте его и заново нажмите кнопку "Пометить непустые колонки"'
            self.folder = ""
            self.md_files_opened = ["errors.xlsx"]
            return 
        

        self.is_src_files_modifyed = check_files_modified('.Исходники')


        if self.is_src_files_modifyed:
            self.error_message = ('В папку .Исходники были добавлены новые файлы или\n'
                                  'некоторые файлы в ней были пересохранены или удалены.\n'
                                  'Нажмите кнопку "Просмотерь разметку"!')

            # global_vars.ui.info_label.setText(self.error_message)
            return
        
       
        

        files_sheets_list = get_files_and_sheets_from_pyperclip()
        files_list = list({files_sheets[0] for files_sheets in files_sheets_list})
        files_list.sort()

        # self.md_files_opened = [file for file in files_list if check_excel_file_is_open(file)]
        self.md_files_opened = []
        
        for file_number, file in enumerate(files_list):
            self.mysignal_info_label_blue.emit(
                f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {file_number} из {len(files_list)}. "
                f"Маркировка непустых колонок. Проверяем не открыт ли на рабочем столе: {file}.")
            sleep(0.01)
            if check_excel_file_is_open(file):
                self.md_files_opened.append(file)



        if self.md_files_opened:
            self.warning_message = (
                f"Некоторые размеченные файлы открыты на рабочем столе!\n"
                f"{'\n'.join(self.md_files_opened)}"
                )
            self.folder = '.Размеченные'

            #for md_file in md_files_opened:
            #    os.startfile(os.path.join(global_vars.project_folder, '.Размеченные', md_file))
            return




        file_preceding = ""
        need_to_save = False
        file_sheets_qty = 0

        for file_sheet_number, file_sheet_list in enumerate(files_sheets_list, 1):
            # print(Fore.MAGENTA, file_sheet_list,  Fore.RESET)
            file = file_sheet_list[0]


            if file != file_preceding:

                if need_to_save:
                    self.mysignal_info_label_blue.emit(
                        f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                        f'{files_list.index(file)+1} из {len(files_list)}. '
                        f'Сохраняем с помеченными непустыми колонками: "{file}"')
                    # print(Fore.GREEN, 'Мы тут', Fore.RESET)
                    wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))

                file_preceding = file
                need_to_save = False

                self.mysignal_info_label_blue.emit(
                    f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {files_list.index(file)+1} из {len(files_list)}. '
                    f'Загружаем для поиска непустых колонок "{file}"')
                
                wb = load_workbook(os.path.join(global_vars.project_folder, '.Размеченные', file))

            
            sheet_name = file_sheet_list[1]


            self.mysignal_info_label_blue.emit(
                f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {file_sheet_number} из {len(files_sheets_list)}. '
                f'Ищем непустые колонки в книге: "{file}" в листе: "{file_sheet_list[0]}"')
            sleep(0.01)

            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
            else:
                self.info_message = f"Помечены заголовки для непустых колонок.\nУспешно обработано листов: {file_sheets_qty} из {len(files_sheets_list)}."
                continue
                
            col_0 = ws['A']
            col_values = list([cell.value for cell in col_0])
            
            s = value_searcher(pd.Series(col_values), 's')
            f = value_searcher(pd.Series(col_values), 'f')
                                    
            # print(Fore.MAGENTA, s, Fore.RESET)
            # print(Fore.MAGENTA, f, Fore.RESET)
            
                      
            errors = marking_checker(sheet_rem=[], s=s, f=f, header_rows=[], rem_and_headers_check = False)
            print(Fore.RED, errors, Fore.RESET)
            if errors != 'ok':
                if errors == '-':
                    self.error_list.append((file, sheet_name, 'Не заданы маркеры s и f'))
                else:
                    self.error_list.append((file, sheet_name, errors))
                continue

            s_index = int(s)
            f_index = int(f)
            
            for col_number, col in enumerate(list(ws.iter_cols())[2:], 3):
                col_values = list([cell.value for cell in col[s_index-1:f_index]])
                # print(col_number, col_values)

                if set(col_values) == {None}:
                    ws.cell(column=col_number, row=1).fill = styles.PatternFill(fill_type=None)
                else:
                    ws.cell(column=col_number, row=1).fill = styles.PatternFill(start_color='C6EFCE', fill_type='solid')
                    ws.cell(column=col_number, row=1).font = styles.Font(color='006100')
                    need_to_save = True

            if need_to_save:
                file_sheets_qty += 1
                
                self.info_message = f"Помечены заголовки для непустых колонок.\nУспешно обработано листов: {file_sheets_qty} из {len(files_sheets_list)}."


        if need_to_save:
            self.mysignal_info_label_blue.emit(
                f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}.  {files_list.index(file)+1} из {len(files_list)}. ' 
                f'Сохраняем с помеченными непустыми колонками: "{file}"')
            wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))
        else:
            wb.close()




    def on_clicked(self):
     
        self.start() # Запускаем поток  


    def on_finished(self): # Вызывается при завершении потока
        
        if self.error_list:
            
            if self.info_message:
                self.info_message += ("\nНа некоторых листах не удалось пометить пустые заголовки,\n"
                                    "из-за ошибок маркировки строк!")
            else:
                self.error_message = "Все выбранные Вами листы содержат ошибки маркировки."
            
        on_finsh_change_thread(self.message_title, self.error_message, self.warning_message, self.info_message, self.md_files_opened, folder=self.folder)
        
        if self.error_list:
            # print(Fore.RED, self.error_list, Fore.RESET)
            errors_df = pd.DataFrame(self.error_list, columns=['file', 'sheet', 'Ошибки маркировки строк'])
            errors_df.to_excel(os.path.join(global_vars.project_folder, 'errors.xlsx'), index=None)
            
            os.startfile(os.path.join(global_vars.project_folder, 'errors.xlsx'))
            while True:
                sleep(0.1)
                if os.path.exists(os.path.join(global_vars.project_folder, '~$errors.xlsx')):
                    break
            
                
        all_control_elements_on()
