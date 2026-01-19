from PySide6 import QtWidgets, QtCore
from colorama import Fore
from datetime import datetime
from time import sleep
import global_vars 
import os
import pandas as pd
from my_threads.functions import check_files_modified
from openpyxl import load_workbook, styles
from my_threads.functions import all_control_elements_off, all_control_elements_on, get_files_and_sheets_from_pyperclip, check_excel_file_is_open, on_finsh_change_thread
class HeadersFillerThread(QtCore.QThread):
 
    mysignal = QtCore.Signal(str)
    def on_signal(self,mysignal):          
        global_vars.ui.info_label.setText(mysignal)


    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Заполнение заголовков на выбранных листах."         

       

    def run(self):
        self.error_message = ""
        self.warning_message = ""
        self.info_message = ""
        self.md_files_opened = []


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

        self.md_files_opened = [file for file in files_list if check_excel_file_is_open(file)]
        if self.md_files_opened:
            self.warning_message = (
                f"Некоторые размеченные файлы открыты на рабочем столе!\n"
                f"{'\n'.join(self.md_files_opened)}"
                )

            #for md_file in md_files_opened:
            #    os.startfile(os.path.join(global_vars.project_folder, '.Размеченные', md_file))
            #    while True:
            #        sleep(0.05)
            #        if os.path.exists(os.path.join(global_vars.project_folder, '.Размеченные', f"~${md_file}")):
            #            break                                     
            return


        file_preceding = ""
        need_to_save = False

        for file_sheet_number, file_sheet_list in enumerate(files_sheets_list, 1):
            print(Fore.MAGENTA, file_sheet_list,  Fore.RESET)
            file = file_sheet_list[0]

            if file != file_preceding:

                if need_to_save:
                    self.mysignal.emit(
                        f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                        f'{files_list.index(file)} из {len(files_list)}. '
                        f'Сохраняем с заполненными заголовками: "{file}"')
                    sleep(0.01)

                    # print(Fore.GREEN, 'Мы тут', Fore.RESET)
                    wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))

                file_preceding = file
                need_to_save = False

                self.mysignal.emit(
                    f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                    f'{files_list.index(file)+1} из {len(files_list)}. '
                    f'Загружаем для заполнения заголовков: "{file}"')
                sleep(0.01)
                
                wb = load_workbook(os.path.join(global_vars.project_folder, '.Размеченные', file))
        

            sheet_name = file_sheet_list[1]

            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
            else:
                continue

            self.mysignal.emit(
                f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {file_sheet_number} из {len(files_sheets_list)}. "
                f"Заполняем заголовки в: {file} в листе: {file_sheet_list[0]}.")
            sleep(0.01)

            # Загружаем данные с листа в датафрейм
            data = []
            for row in ws.iter_rows(values_only=True):
                data.append(list(row))
            df = pd.DataFrame(data)


            # Если лист пустой, то пропускаем
            if df.empty:
                continue

            # Если заголовок уже есть, то пропускаем
            header_df = df.iloc[:2, 2:]
            header_df = header_df.fillna("")
            if not (header_df.applymap(lambda x: isinstance(x, str) and len(x) == 0)).all().all():
                print('Заголовок уже есть!')
                continue
                
            print(f"Файл {file} лист {file_sheet_list} Заголовка нет. будем заполнять")          
            # получаем номер строки с заголовком
            header_df = df[df[0]=='h']


            if not header_df.empty:
                header_cells = header_df.iloc[0][2:]
            else:
                continue

            col = 3
            # print(Fore.YELLOW, header_cells, Fore.RESET)
            for header_cell in header_cells:
                ws.cell(row=1, column=col, value=header_cell)
                ws.cell(row=1, column=col).alignment = styles.Alignment(wrap_text=False, horizontal="center", vertical="center")
                col += 1
            need_to_save = True

            # wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))                      

        if need_to_save:
            self.mysignal.emit(
                f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                f'{files_list.index(file)+1} из {len(files_list)}. '
                f'Сохраняем с заполненными заголовками: "{file}"')
            wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))
        else:
            wb.close()

        self.info_message = "Заголовки заполнены."    

           


    def on_clicked(self):
        self.start() # Запускаем поток  
     


    def on_started(self): # Вызывается при запуске потока
        all_control_elements_off()
        # global_vars.ui.pushButtonChooseProjectFolder.setEnabled(False)   
        global_vars.ui.info_label.setStyleSheet('color: blue')        


    def on_finished(self): # Вызывается при завершении потока
        on_finsh_change_thread(self.message_title, self.error_message, self.warning_message, self.info_message, self.md_files_opened)
            
        all_control_elements_on()
