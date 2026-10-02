from PySide6 import QtWidgets, QtCore
from colorama import Fore
from datetime import datetime
from time import sleep
import global_vars 
import os
import pandas as pd
from my_threads.functions import check_files_modified
from openpyxl import load_workbook, styles
from my_threads.functions import all_control_elements_off, all_control_elements_on, get_files_and_sheets_from_pyperclip, check_excel_file_is_open, on_finsh_change_thread, get_merged_range_headers_from_db
class HeadersFillerThread(QtCore.QThread):
 
    # mysignal = QtCore.Signal(str)

    mysignal_info_label_blue = QtCore.Signal(str)
    
    # def on_signal(self,mysignal):          
    #     global_vars.ui.info_label.setText(mysignal)


    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Заполнение заголовков на выбранных листах."         

       

    def run(self):
        self.error_message = ""
        self.warning_message = ""
        self.info_message = ""
        self.md_files_opened = []
        self.err_list = []

        if check_excel_file_is_open("errors.xlsx"):
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText('Закройте файл errors.xlsx перед тем как запустить обработку.')   
            self.error_message =('Файл errors.xlsx открыт на рабочем столе.\n'
                                   'Закройте его и снова попробуйте удалить файлы!')
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
                f"Заполнение заголовков. Проверяем не открыт ли на рабочем столе: {file}.")
            sleep(0.01)
            if check_excel_file_is_open(file):
                self.md_files_opened.append(file)

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

            print(file)

            file = file_sheet_list[0]

            if file != file_preceding:

                if need_to_save:
                    self.mysignal_info_label_blue.emit(
                        f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                        f'{files_list.index(file)} из {len(files_list)}. '
                        f'Сохраняем с заполненными заголовками: "{file}"')
                    sleep(0.01)

                    wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))

                file_preceding = file
                need_to_save = False

                self.mysignal_info_label_blue.emit(
                    f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                    f'{files_list.index(file)+1} из {len(files_list)}. '
                    f'Загружаем для заполнения заголовков: "{file}"')
                sleep(0.01)
                
                wb = load_workbook(os.path.join(global_vars.project_folder, '.Размеченные', file))
        

            sheet_name = file_sheet_list[1]

            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
            else:
                self.info_message = "Заголовки заполнены."
                continue

            self.mysignal_info_label_blue.emit(
                f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {file_sheet_number} из {len(files_sheets_list)}. "
                f"Заполняем заголовки в: {file} в листе: {file_sheet_list[0]}.")
            sleep(0.01)

            # Загружаем данные с листа в датафрейм
            data = []
            for row in ws.iter_rows(values_only=True):
                data.append(list(row))
            df = pd.DataFrame(data)
            # df = df.map(str)

            # print(df[[20,21,22,23,24,25,26,27,28]])

            # Если лист пустой, то пропускаем
            if df.empty:
                continue

            # Если заголовок уже есть, то пропускаем
            """ 
            header_df = df.iloc[:2, 2:]
            header_df = header_df.fillna("")

            отключаем незаполнение заголовков если они есть
            for t in header_df.itertuples():
                print(t)
                not_empty_header = [i for i in t[1:] if i!='' and not pd.isnull(i)]
                print(not_empty_header)
                if not_empty_header:
                    break


            if not_empty_header:
                print("Заголовок уже есть!")
                continue
            """

       
            # получаем номер строки с заголовком
            # print(Fore.GREEN, df, Fore.RESET)
            header_df = df[df[0]=='h']

            if header_df.empty:
                self.err_list.append((file, f'Не выбраны строки заголовков на листе "{sheet_name}"'))
                self.error_message = (
                    f"У некоторых выбранных листов не была промаркированы строки заголовков!\n"
                    )
            else:
                header_rows = [i-2 for i in header_df.index]
                print(header_rows)


                source_file_df = pd.read_excel(
                    os.path.join(global_vars.project_folder, '.Исходники', file[3:]),
                    sheet_name=sheet_name,
                    nrows=header_rows[-1]+1,
                    header=None)
                
                source_file_df = source_file_df.loc[header_rows]
                source_file_df = source_file_df.fillna('') 
                
                header_cells = []
                merged_range_headers = get_merged_range_headers_from_db(file[3:], sheet_name)

                for column_number, column in enumerate(source_file_df.columns, 1):
                    header = []
                    for row in header_rows:
                        if str(row+1) in merged_range_headers:
                            if str(column_number) in merged_range_headers[str(row+1)]:
                                header.append(merged_range_headers[str(row+1)][str(column_number)]) 
                            elif source_file_df[column].loc[row]:
                                header.append(source_file_df[column].loc[row])
                            else:
                                pass
                                #header.append('')
                        elif source_file_df[column].loc[row]:
                            header.append(source_file_df[column].loc[row])

                    if header:
                        header = [str(x) for x in header]
                        print(Fore.MAGENTA, header, Fore.RESET)
                        header_cells.append('>>>'.join(header))
                    else:
                        header_cells.append('')


                if not header_cells:
                #    header_cells = header_df.iloc[0][2:]
                #else:
                    continue

                col = 3
                for header_cell in header_cells:
                    ws.cell(row=1, column=col, value=header_cell)
                    ws.cell(row=1, column=col).alignment = styles.Alignment(wrap_text=True, horizontal="left", vertical="center")
                    col += 1
                need_to_save = True

                # wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))                      

        if need_to_save:
            self.mysignal_info_label_blue.emit(
                f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. '
                f'{files_list.index(file)+1} из {len(files_list)}. '
                f'Сохраняем с заполненными заголовками: "{file}"')
            wb.save(os.path.join(global_vars.project_folder, '.Размеченные', file_preceding))
        else:
            wb.close()

        self.info_message = "Заголовки заполнены."    

           


    def on_clicked(self):
        self.start() # Запускаем поток  


    def on_finished(self): # Вызывается при завершении потока
        on_finsh_change_thread(self.message_title, self.error_message, self.warning_message, self.info_message, self.md_files_opened)

        if self.err_list:
            df = pd.DataFrame(self.err_list, index=None)
            df.to_excel(os.path.join(global_vars.project_folder, 'errors.xlsx'), index=None, header=None)

            os.startfile(os.path.join(global_vars.project_folder, "errors.xlsx"))
            
        all_control_elements_on()
