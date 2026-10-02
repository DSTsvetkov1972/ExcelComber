from PySide6 import QtWidgets, QtCore
from colorama import Fore
from datetime import datetime
import global_vars 
import os, random
import pandas as pd
from time import sleep
from my_threads.functions import check_files_modified, pop_up_files
from openpyxl import load_workbook, styles
from openpyxl.utils.cell import get_column_letter
from my_threads.functions import all_control_elements_off, all_control_elements_on, check_excel_file_is_open

class MakeFilesThread(QtCore.QThread):
 
    mysignal = QtCore.Signal(str)


    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent) 
        self.message_title = "Объединение"
        
        

    def clean_folder_marked(self, project_folder):

        errors_list = []


        source_files = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]
        marked_files = [file for file in list(os.walk(os.path.join(global_vars.project_folder,'.Размеченные')))[0][2] if file[0] != '~']
     
        for file in marked_files:
            sleep(0.0001)
            self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                               f"Проверяем наличие файла {file} из ./Размеченные в .Исходники/")             
            if file[3:] not in source_files: # file[3:] чтобы откусить приставку md_ в начале
                try:
                    os.remove(os.path.join(global_vars.project_folder, '.Размеченные', file))
                except PermissionError:
                    errors_list.append("Книга {file} есть в папке .Размеченные/,\
                            но ей нет соответствия в папке ./Исходники.\nНе можем удалить эту книгу из ./Размеченные,\
                                       потому что она открыта в Эксель!")

        return ("\n" + ">" + "\n").join(errors_list)

    def make_files(self):
        global_vars.ui.info_label.setStyleSheet('color: blue')

        marked_folder = os.path.join(global_vars.project_folder, r".Размеченные")
        files = [file for file in list(os.walk(os.path.join(global_vars.project_folder, '.Размеченные')))[0][2] if file[0] != "~"]
        columns_info_df = pd.read_excel(os.path.join(global_vars.project_folder,'markup.xlsx'), dtype=str)

        self.res_folder_files_qty = 0
        for file_number, file in enumerate(files, 1):
            with pd.ExcelFile(os.path.join(marked_folder, file)) as xlsx_file:
                sheets = xlsx_file.sheet_names
                    
            for sheet_number, sheet in enumerate(sheets, 1):
                # sleep(0.0001)
                print(file, sheet)
                
                self.mysignal.emit(f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} '
                                   f'Книга {file_number} из {len(files)} лист {sheet_number} из {len(sheets)}. ' 
                                   f'Подготавливаем к созданию файл "{file}" лист "{sheet}"')
                 
                file_info = columns_info_df[(columns_info_df['_file_'] == file) &
                                            (columns_info_df['_sheet_'] == sheet) &
                                            (columns_info_df['Ошибки маркировки'] == 'ok')]
                
                # print(file_info)
                
                if not file_info.empty:
                    s = int(file_info['_s_'].iloc[0])-1
                    f = int(file_info['_f_'].iloc[0])
                    print(Fore.YELLOW,  os.path.join(marked_folder,file), Fore.RESET)
                    file_df = pd.read_excel(os.path.join(marked_folder, file), sheet_name=sheet, header=None).iloc[:,2:]

        
                    file_df_without_ffill = file_df.iloc[s:f]
                    file_df_without_ffill.columns = file_df.iloc[0]
                    column_names_without_ffill = [column_name for column_name in file_df.iloc[0] if pd.notna(column_name)]
                    file_df_without_ffill = file_df_without_ffill[column_names_without_ffill]

                    # file_df_with_ffill = file_df.fillna(method='ffill')     
                    file_df_with_ffill = file_df.ffill()                       
                    file_df_with_ffill = file_df_with_ffill.iloc[s:f]
                    file_df_with_ffill.columns = file_df.iloc[1]
                    column_names_with_ffill = [column_name for column_name in file_df.iloc[1] if pd.notna(column_name)]
                    file_df_with_ffill = file_df_with_ffill[column_names_with_ffill]           

                    file_df = pd.concat([file_df_without_ffill, file_df_with_ffill], axis=1)


                    res_file_name = os.path.join(global_vars.project_folder, '.Результат', f"{file[3:-4]}_{sheet}.xlsx")
                    file_df.to_excel(res_file_name, index=None)


      
                    # задаём ширину столбцов по размеру заголовка
                    wb = load_workbook(res_file_name)
                    ws = wb.active

                    self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                    f"Подгоняем ширину столбцов под длины заголовков")

                    for n, column in enumerate(list(file_df .columns), 1):
                        ws.column_dimensions[get_column_letter(n)].width = len(str(column))*1.1 + 5

                    self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                    f"Замораживаем строку заголовков")
                    ws.auto_filter.ref = ws.dimensions    
                    
                    ws.freeze_panes = ws.cell(column=1, row=2)

                    self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                    f"Задаём цвет строки заголовков")
                    for col, column in enumerate(list(file_df .columns), start=1):
                        cell = ws.cell(column=col, row = 1)
                        # cell.fill = styles.PatternFill(start_color='FFFFC7CE', fill_type='solid')
                        cell.fill = styles.PatternFill(start_color='E9FDD9', fill_type='solid')
                        cell.font = styles.Font(color='974706', bold=True)
                        cell.alignment = styles.Alignment(wrap_text=True,
                                                        vertical='top',
                                                        horizontal='center') 
                        #cell.style.alignment.wrap_text=True

                    self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                        f"Сохраняем файл")    
                    wb.save(res_file_name)
                    self.res_folder_files_qty += 1

        os.startfile(os.path.join(global_vars.project_folder,'.Результат'))                

    def on_signal(self,mysignal):
        global_vars.ui.info_label.setStyleSheet('color: blue')            
        global_vars.ui.info_label.setText(mysignal)


    def run(self): 
        self.message_title = "Создаём файлы"
        self.error_message = ""
        self.warning_message = ""
        self.result_df_len = 0

        self.is_src_files_modifyed = check_files_modified('.Исходники')
        self.is_md_files_modifyed = check_files_modified('.Размеченные')

        # проверяем, чтобы если существует папка .Результат, чтобы не было открытых файлов на рабочем столе
        result_folder = os.path.join(global_vars.project_folder, '.Результат')
        if os.path.exists(result_folder):

            files_list = list(os.walk(result_folder))[0][2]
            files_list = [file for file in files_list if file[:2] != '~$']
            
            if files_list:
            
                files_list.sort()

                self.res_folder_files_opened = []
            
                for file_number, file in enumerate(files_list):
                    self.mysignal.emit(
                        f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. {file_number} из {len(files_list)}. "
                        f"Создание файлов. Проверяем не открыт ли на рабочем столе: {file}.")
                    sleep(0.01)
                    if check_excel_file_is_open(file):
                        self.res_folder_files_opened.append(file)
                    else:
                        os.remove(os.path.join(result_folder, file))

                if self.res_folder_files_opened:
                    self.warning_message = (
                        f"Некоторые файлы из папки .Результат открыты на рабочем столе!\n"
                        f"{'\n'.join(self.res_folder_files_opened)}"
                        )

                    #for md_file in md_files_opened:
                    #    os.startfile(os.path.join(global_vars.project_folder, '.Размеченные', md_file))
                    #    while True:
                    #        sleep(0.05)
                    #        if os.path.exists(os.path.join(global_vars.project_folder, '.Размеченные', f"~${md_file}")):
                    #            break                                     
                    return
                
        else:

            os.mkdir(result_folder)




        if self.is_src_files_modifyed:
            global_vars.ui.info_label.setStyleSheet('color: red')
            self.error_message = ('В папку .Исходники были добавлены новые файлы или\n'
                                  'некоторые файлы в ней были пересохранены или удалены.\n'
                                  'Нажмите кнопку "Просмотерь разметку"!')

            # global_vars.ui.info_label.setText(self.error_message)
            return
        if self.is_md_files_modifyed:
            global_vars.ui.info_label.setStyleSheet('color: red')
            self.error_message = ('Файлы в папке .Размеченные были изменены.\n'
                                  'Нажмите кнопку "Просмотерь разметку"!!')  
            # global_vars.ui.info_label.setText(self.error_message)
            return


        self.error_message = ""
        self.warning_message = ""        
        self.error_message = self.clean_folder_marked(global_vars.project_folder)
        if not self.error_message:  
            self.make_files()


    def on_clicked(self):     
        self.start() # Запускаем поток  
    

    def on_finished(self): # Вызывается при завершении потока

        #global_vars.interface_enabled = True
        all_control_elements_on()

        """
        global_vars.ui.pushButtonChooseProjectFolder.setEnabled(True)

        if os.path.exists(os.path.join(global_vars.project_folder,'.Исходники')):
            source_files_list = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]
            source_old_excels_list = [file for file in source_files_list if file[-4:] in ['.xls', 'xlsm']]
        if source_old_excels_list:
            global_vars.ui.pushButtonXLStoXLSX.setEnabled(True)        
        global_vars.ui.pushButtonProcessing.setEnabled(True)
        global_vars.ui.pushButtonHeadersFiller.setEnabled(True)          
        global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(True)        
        global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(True)
        global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(True)           

        if self.is_src_files_modifyed or self.is_md_files_modifyed:
            global_vars.ui.pushButtonConcat.setEnabled(False)      
        else:
            global_vars.ui.pushButtonConcat.setEnabled(True) 

        """

        if self.error_message:
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText(self.error_message.replace('\n',' '))
            QtWidgets.QMessageBox.critical(None,
                                           self.message_title,
                                           self.error_message,
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok)
            return
        
        elif self.warning_message:
            pop_up_files(self.message_title, self.warning_message, self.res_folder_files_opened, folder = '.Результат')
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText(self.warning_message.replace('\n',' '))
           
        else:
            #print('AAAA')
            #sleep(0.1)
            global_vars.ui.info_label.setStyleSheet('color: green')          
            global_vars.ui.info_label.setText(f'В папке .Результат создано { self.res_folder_files_qty } файлов.')

        
        global_vars.ui.pushButtonConcat.setEnabled(True)
        global_vars.ui.pushButtonMakeFiles.setEnabled(True)        

