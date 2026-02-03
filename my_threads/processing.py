from PySide6 import QtWidgets, QtCore
from colorama import Fore
from time import sleep

from pprint import pprint

import global_vars 
import os, shutil
import pandas as pd

from openpyxl.utils.cell import get_column_letter
from openpyxl import load_workbook, styles
from openpyxl.utils import range_boundaries
from openpyxl.worksheet.datavalidation import DataValidationList
from openpyxl.workbook.views import BookView  

from datetime import datetime
from my_threads.functions import all_control_elements_off, all_control_elements_on
from my_threads.functions import value_searcher, marking_checker
from my_threads.functions import init_project, refresh_files_info, clean_process_folder, check_files_modified, check_excel_file_is_open, open_or_show_file
from my_threads.functions import get_range_info, set_range_border
from my_threads.functions import set_markup_in_db, get_markup_from_db, set_merged_range_headers_in_db


horizontal_offset = 2
vertical_offset = 2
sep_cell_style = styles.PatternFill(start_color='FFFFC7CE', fill_type='solid')
no_fill = styles.PatternFill(fill_type=None)
side = styles.Side(border_style=None)
no_border = styles.borders.Border(
    left=side,
    right=side,
    top=side,
    bottom=side,
)


class ProcessingThread(QtCore.QThread):
 
    mysignal = QtCore.Signal(str)


    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent) 

    def check_path_length(self):
        """
        Перед началом обработки проверяем чтобы не было 
        полный путь к любому md_ файлу не првышал 218 символов
        """

        self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                            f"проверяем чтобы длина пути к самому длинному файлу не превышала 218 символолв")

        project_folder_len = len(global_vars.project_folder + '.Размеченные') + 2

        src_files = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]

        src_files_and_lens = [(file, len(file)+3) for file in src_files]

        self.check_path_length_err_list = [(f'{global_vars.project_folder}/.Размеченные/md_{file[0]}',
                                            f'Длина полного пути { file[1] + project_folder_len } символов '
                                            f'(длина пути к папке { project_folder_len } + длина имени файла {file[1]}). '
                                            f'Не должна превышать 218 символов, иначе Эксель не сможет открыть этот файл!') for file in src_files_and_lens if file[1]+project_folder_len > 218]

        if self.check_path_length_err_list:
            self.check_path_length_error_message = (
                f"Длина пути к размеченным файлам {project_folder_len},\n"
                f"полная длина пути к некоторым размеченным файлам превышает 218 символов.\n"
                f"Переименуйте файлы с длинными названиями или перенесите проект в папку с более коротким путём!\n")
        else:
            self.check_path_length_error_message = ''
           
    def check_src_files_available(self):
        """
        Перед началом обработки проверяем чтобы не было 
        открытых исходных файлов
        """

        self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                            f"Проверяем не изменилось ли содержимое папки .Исходники")

        src_files = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]
        self.check_src_files_available_err_list = [(f'md_{file}', 'Файл из папки .Исходники открыт на рабочем столе. Его нужно закрыть!') for file in src_files if os.path.exists(os.path.join(global_vars.project_folder, '.Исходники', f'~${file}'))]

        if self.check_src_files_available_err_list:
            self.check_src_files_available_error_message = (
                "Некоторые файлы из папки .Исходники,\n"
                "открыты на рабочем столе.\n")
        else:
            self.check_src_files_available_error_message =  ''  


    def clean_md_folder(self):
        """
        Удаляет файл из папки .Размеченные, если его нет в папке .Исходники.
        Если файл не удаётся удалить, т.к. он открыть в другой программе,
        информация о нем добавляется в список ошибок.
        """

        self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                            f"проверяем соответствует ли содержимое папки .Размеченные содержимому папки .Исходники")

        source_files = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]
        marked_files = [file for file in list(os.walk(os.path.join(global_vars.project_folder,'.Размеченные')))[0][2] if file[0:2] != '~$']
        
        for md_file in marked_files:
                        
            if md_file[3:] not in source_files: # file[3:] чтобы откусить приставку md_ в начале
                try:
                    os.remove(os.path.join(global_vars.project_folder, '.Размеченные', md_file))
                except PermissionError:
                    # os.startfile(os.path.join(global_vars.project_folder, '.Размеченные', md_file))
                    self.error_message = (
                        "Некоторых файлов нет в папке .Исходники,\n"
                        "но соответствующие md-файлы не могут быть удалены,\n"
                        "т.к. открыты в другой программе")
                    self.err_list.append((md_file, 'файла нет в .Исходники, но md файл не может быть удален, т.к. открыт в другой программе'))

    
    def check_md_book_sheet(self, wb):
        """
        Прверяем можем ли мы сдвинуть содержимое листа вниз и вправо
        или размер данных не позволяет это сделать
        """
        sheets_exceeding_dict = {}
        for sheet_number, sheet in enumerate(wb.sheetnames, 1): 
            sheets_exceeding_dict[sheet] = ''   
            ws = wb[sheet]

            # проверяем на размер листа
            ws_max_column = ws.max_column
            ws_max_row = ws.max_row

            ws_max_rows = 1048574-vertical_offset-1
            ws_mas_columns = 16384-horizontal_offset-1

            if ws_max_column > ws_mas_columns:
                sheets_exceeding_dict[sheet] += f' колонок больше {ws_mas_columns}'

            if ws_max_row > ws_max_rows:               
                sheets_exceeding_dict[sheet] += f'строк больше {ws_max_rows}'                    

            if not sheets_exceeding_dict[sheet]:
                sheets_exceeding_dict.pop(sheet)

        return sheets_exceeding_dict


    def check_md_book(self, md_file, prc_file):
        """
        Почемуто некоторые Экселевские файлы не могут быть открыты в openpyxl если их
        не пересохранить.
        Проверяем файл на эту ошибку.
        """

        # пытаемся удалить файл-костыль если он образовался на предыдущем шаге
        if os.path.exists(os.path.join(global_vars.project_folder, '.Обработка', '~~~if_accident.xlsx')):
            try:
                os.remove(os.path.join(global_vars.project_folder, '.Обработка', '~~~if_accident.xlsx'))
            except:
                print(Fore.RED, 'Не удалось удалить ~~~if_accident.xlsx', Fore.RESET)


        try:

            wb = load_workbook(os.path.join(global_vars.project_folder, '.Обработка', prc_file),
                               data_only=True)

            size_check = self.check_md_book_sheet(wb) # если удалось книгу открыть, проверяем на размер данных на листах

            if size_check:
                self.error_message = "Некоторые файлы в папке .Исходники не могут быть обработаны."
                self.err_list.append((md_file, str(size_check)))
                os.remove(os.path.join(global_vars.project_folder, '.Обработка', prc_file))
                return False
            else:
                return wb
            #return wb
        except Exception:
            print(f'Авария 1 {prc_file}')            
            self.error_message = "Некоторые файлы в папке .Исходники не могут быть обработаны."
            self.err_list.append((md_file, 'Возможно файл повреждён. Попробуйте пересохранить исходный файл.'))


        # костыль, чтобы освободить файл, который не удалось загрузить 
        # в предыдущем try except блоке
        try:
            print('Авария 2')
            # shutil.copy(os.path.join(global_vars.project_folder, '.Размеченные', file), os.path.join(global_vars.project_folder, '.Аварийные', file))
            shutil.copy(os.path.join(global_vars.project_folder, '.Обработка', prc_file),
                        os.path.join(global_vars.project_folder, '.Обработка', '~~~if_accident.xlsx'))           
            print('Авария 3')                
            # wb = load_workbook(os.path.join(global_vars.project_folder, '.Аварийные', file), data_only=True)
            wb = load_workbook(os.path.join(global_vars.project_folder, '.Обработка', '~~~if_accident.xlsx'), data_only=True)            
        except Exception as e:
            print(f'Авария 3\n {e}')
            pass

        try:
            print('Авария 4') 
            os.remove(os.path.join(global_vars.project_folder, '.Обработка', prc_file))
            print('Авария 5') 
        except:
            print('Авария 666') 

        return False


    def premarker(self, project_folder):
        global_vars.ui.info_label.setStyleSheet('color: blue')  

        source_files = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]
        prc_files = list(os.walk(os.path.join(global_vars.project_folder,'.Обработка')))[0][2]
        md_files = list(os.walk(os.path.join(global_vars.project_folder,'.Размеченные')))[0][2]        
        
        for source_file_number, source_file in enumerate(source_files, 1):

            merged_range_headers = {}

            md_file = 'md_' + source_file

            if md_file in md_files: 
                continue

            self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                    f"Книга {source_file_number} из {len(source_files)}. Создаём размеченную книгу для {source_file}")

            prc_file = 'prc_' + source_file

            # бывало что prc файл блокировался при проверке и его не 
            # получалось удалить
            # на этот случай придуман костыль создающий prc файл с другим 
            # именем
            while True:
                if not prc_file in prc_files:
                    break
                else:
                    prc_file = "~" + prc_file

            shutil.copy(os.path.join(global_vars.project_folder, '.Исходники', source_file), os.path.join(global_vars.project_folder, '.Обработка', prc_file))

            self.mysignal.emit(f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} '
                               f'Книга {source_file_number} из {len(source_files)}. Открываем чтобы разметить книгу "{prc_file}"')
            
            # проверяем возможно ли открыть файл и позволяют ли размер данных на листе сдвигать столбцы и строки
            wb = self.check_md_book(md_file, prc_file)

            if not wb:
                continue                      

            # обрабатываем листы
            for sheet_number, sheet in enumerate(wb.sheetnames, 1):
                print(Fore.GREEN, f'Размечаем {source_file} лист {sheet}') 
                merged_range_headers[sheet]={}

                ws = wb[sheet]

                ws_max_column = ws.max_column
                ws_max_row = ws.max_row

                # Делаем лист видимым
                ws.sheet_state = 'visible'

                # Записываем ширины колонок
                self.mysignal.emit(f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Записываем ширины колонок {prc_file} {sheet}")

                columns_width = []
                for i in range(1, ws_max_column + 1):
                    letter = get_column_letter(i) # преобразовываем индекс столбца в его букву
                    # получаем ширину столбца и добавляем в список
                    cw = ws.column_dimensions[letter].width
                    if not cw:
                        columns_width.append(16)
                    elif cw<2:
                        columns_width.append(16)
                    elif cw>36:
                        columns_width.append(24)
                    else:
                        columns_width.append(cw)        

                # Записываем высоты строк
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Записываем высоты строк {prc_file} {sheet}")

                rows_height = []
                for i in range(1, ws_max_row + 1):
                    # получаем высоту столбца и добавляем в список
                    rh = ws.row_dimensions[i].height
                    if not rh:
                        rows_height.append(rh)                          
                    elif rh<10:                        
                        rows_height.append(10) 
                    elif rh>50:                        
                        rows_height.append(50)  
                    else:
                        rows_height.append(rh)

                # Снимаем пароль с листа
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Снимаем пароль с листа {prc_file} {sheet}")

                ws.protection.disable()

                # Показываем скрытые столбцы и строки
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Показываем скрытые столбцы и строки {prc_file} {sheet}")     
                    
                ws.column_dimensions.group(start='A', end=get_column_letter(ws_max_column), hidden=False)
                ws.row_dimensions.group(start=1, end=ws_max_row, hidden=False)

                # Удаляем проверку данных с листа
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Удаляем проверку данных с листа {prc_file} {sheet}")   

                ws.data_validations = DataValidationList()

                # Снимаем группировку колонок и столбцов
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Снимаем группировку колонок и столбцов {md_file} {sheet}")     

                ws.row_dimensions.group(1, ws_max_row, outline_level=0) # for entire sheet
                ws.column_dimensions.group('A', get_column_letter(ws_max_column), outline_level=0) # for entire sheet

                # Убираем фильтр
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. убираем фильтр {prc_file} {sheet}")   
                
                # ws.auto_filter.ref = None
                # ws.auto_filter.add_filter_column(None)
                ws.auto_filter.ref = ws.dimensions


                # Отменяем объединение ячеек
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Отменяем объединение ячеек {prc_file} {sheet}")
                
                merged_cells_info_list = [get_range_info(str(merged_cell_info)) for merged_cell_info in ws.merged_cells.ranges]

                if merged_cells_info_list:

                    # отменяем объединение ячеек
                    for merged_range in list(ws.merged_cells.ranges):

                        min_col, min_row, max_col, max_row = range_boundaries(str(merged_range))
                        ws.unmerge_cells(str(merged_range)) 

                        # получаем значение первой ячейки
                        first_cell_value = ws.cell(row=min_row, column=min_col).value
                        first_cell_alignment = ws.cell(row=min_row, column=min_col).alignment
                        
                        

                        # заполняем диапазон значением первой ячейки
                        for row in range(min_row, max_row + 1):
                            for col in range(min_col, max_col + 1):
                                if row == min_row:
                                    if row not in merged_range_headers[sheet]: 
                                        merged_range_headers[sheet][row]={}
                                    merged_range_headers[sheet][row][col] = str(first_cell_value)
                                    #print(str(merged_range), source_file, sheet, first_cell_value, row, col)
                                
                                if row != min_row or col != min_col:
                                    merged_range_cell = ws.cell(row=row, column=col, value=first_cell_value)
                                    merged_range_cell.alignment = styles.Alignment(
                                        vertical=first_cell_alignment.vertical,
                                        horizontal=first_cell_alignment.horizontal,
                                        wrap_text=first_cell_alignment.wrap_text)
                                    
                                    # merged_range_cell.alignment = styles.Alignment(
                                    #     vertical='top',
                                    #     horizontal='center',
                                    #     wrap_text=True)
                                    merged_range_cell.font = styles.Font(color="FFCCCC")

                    for merged_cells_info in merged_cells_info_list: # помечаем красной розовой линией ранее объединенные ячейки
                        set_range_border(
                            ws,
                            min_row=merged_cells_info['min_row'],
                            max_row=merged_cells_info['max_row'],
                            min_col=merged_cells_info['min_col'],
                            max_col=merged_cells_info['max_col']
                            )
                    # self.mysignal.emit(
                    #     f'{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} '
                    #     f'Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. '
                    #     f'Сохраняем после отмены объединения ячеек. Книга: "{prc_file}", лист: "{sheet}"')
                    # wb.save(os.path.join(project_folder,'.Обработка', prc_file)) 

                # Сохраняем текст, но удаляем ссылку
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Удаляем гиперссылки {prc_file} {sheet}")   

                for row in ws.iter_rows():
                    for cell in row:
                        if cell.hyperlink:
                            # Сохраняем значение ячейки (текст)
                            text = cell.value
                            # Удаляем гиперссылку
                            cell.hyperlink = None
                            # Восстанавливаем текст (если он был равен URL)
                            if cell.value == cell.hyperlink.target if cell.hyperlink else None:
                                cell.value = text    

 
                # Сдвигаем вниз
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Сдвигаем вниз {prc_file} {sheet}")   

                ws.insert_rows(idx=1, amount=2)
                
                # Сдвигаем вправо
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Сдвигаем вправо {prc_file} {sheet}")  

                ws.insert_cols(idx=1, amount=2)

                # Делаем ширины столбцов как в исходнике
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Сдвигаем вправо {prc_file} {sheet}")  

                ws.column_dimensions['A'].width = 5
                ws.column_dimensions['B'].width = 5
                ws.column_dimensions[get_column_letter(ws_max_column + horizontal_offset + 1)].width = 5  

                for i, column_width in enumerate(columns_width, vertical_offset + 1):
                    letter = get_column_letter(i) 
                    ws.column_dimensions[letter].width = column_width

                ws.row_dimensions[1].height = 15 
                ws.row_dimensions[2].height = 15

                for i, row_height in enumerate(rows_height, vertical_offset + 1):
                    ws.row_dimensions[i].height = row_height                   


                # Очищаем от форматирования верхний ряд и левую колонку
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Сдвигаем вправо {prc_file} {sheet}")            
                for col in range(1, ws_max_column + 12):
                  
                    cell = ws.cell(column=col, row = 1)

                    cell.fill = no_fill
                    cell.border = no_border 
                    cell.alignment = styles.Alignment(wrap_text=True,vertical='center', horizontal='center')                  

                for row in range(1, ws_max_row + horizontal_offset + 1):
              
                    cell = ws.cell(column=1, row=row)
                    cell.fill = no_fill
                    cell.border = no_border

                # Отключаем условное форматирование
                ws.conditional_formatting = {}    

                # Размечаем разделители
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Размечаем разделители {prc_file} {sheet}")   
            
                for col in range(1, ws_max_column + 12):
                    separator_cell = ws.cell(column=col, row = vertical_offset)
                    separator_cell.fill = sep_cell_style

              
                for col in range(1, ws_max_column + 4):
                    separator_cell = ws.cell(column=col, row = ws_max_row + vertical_offset + 1)
                    separator_cell.fill = sep_cell_style

                for row in range(1, ws_max_row + horizontal_offset + 1):
                    separator_cell = ws.cell(column=2, row = row)
                    separator_cell.fill = sep_cell_style

                
                for row in range(1, ws_max_row + horizontal_offset + 1):
                   
                    separator_cell = ws.cell(column=ws_max_column+3, row = row)
                    separator_cell.fill = sep_cell_style
                    
                # Замораживаем ячейки
                self.mysignal.emit(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                   f"Книга {source_file_number} из {len(source_files)} лист {sheet_number} из {len(wb.sheetnames)}. Закрепляем диапазон {prc_file} {sheet}") 
                ws.sheet_view.topLeftCell = 'A1'                
                freeze_cell = ws['C3']             
                ws.freeze_panes = freeze_cell


            pprint(merged_range_headers)

            # Сохраняем размеченную книгу.'
            self.mysignal.emit(f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} '
                               f'Книга {source_file_number} из {len(source_files)}. Сохраняем после разметки книгу "{prc_file}"')  
            
            
            view = BookView ()
            view.showHorizontalScroll = True  # скрыть горизонтальный ползунок
            view.showVerticalScroll = True    # скрыть вертикальный ползунок
            view.showSheetTabs = True         # скрыть вкладки листов


            wb.views = [view]
            
            set_merged_range_headers_in_db(source_file, merged_range_headers)

            wb.save(os.path.join(project_folder,'.Обработка', prc_file))            
            wb.close()
            shutil.move(os.path.join(project_folder,'.Обработка', prc_file), os.path.join(project_folder,'.Размеченные', md_file))


    def all_columns(self, project_folder):
        global_vars.ui.info_label.setStyleSheet('color: blue')          

        marked_folder = os.path.join(project_folder,'.Размеченные')

        
        files = [file for file in list(os.walk(os.path.join(project_folder, '.Размеченные')))[0][2] if file[0] != "~"]

        result_s_f_check_df = pd.DataFrame()

        result_first_and_second_line_df = pd.DataFrame()

        for file_number, file in enumerate(files, 1):

            markup_dict = get_markup_from_db(file)

            # print(markup_dict)

            if markup_dict:
                if markup_dict['modifyed_time'] != str(os.path.getmtime(os.path.join(global_vars.project_folder, '.Размеченные',file))):
                    set_markup_in_db(file)
                    markup_dict = {}


            if markup_dict:
                
                for sheet, sheet_dicts in markup_dict['markup_dict'].items():

                    first_and_second_line_dict = sheet_dicts['first_and_second_line_dict']
                    first_and_second_line_df = pd.DataFrame([first_and_second_line_dict])
                    result_first_and_second_line_df = pd.concat([result_first_and_second_line_df, first_and_second_line_df])

                    s_f_check_dict = sheet_dicts['s_f_check_dict']
                    s_f_check_df = pd.DataFrame([s_f_check_dict])
                    result_s_f_check_df = pd.concat([result_s_f_check_df, s_f_check_df])

                    errors_list=[]

            else:    
                #try:
                xlsx_file = load_workbook(os.path.join(marked_folder, file))
                sheets = xlsx_file.sheetnames
                #except:
                #    os.remove(os.path.join(marked_folder, file))
                #    self.error_message = (
                #        f"Файл {file}\n"
                #        "был испорчен и его пришлось удалить.\n"
                #        "Нажмите кнопку Просмотерь разметку еще раз,\n"
                #        "Файл будет создан вновь, но с ним снова \n"
                #        "придётся поработать!"
                #        )
                #    self.err_list.append((file, 'Файл был испорчен и его пришлось удалить.'))
                #    return

                for sheet_number, sheet in enumerate(sheets, 1):        
                    self.mysignal.emit(f'{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} '
                                    f'Книга {file_number} из {len(files)} лист {sheet_number} из {len(sheets)}. '
                                    f'Считываем разметку файла "{file}" из листа "{sheet}"') 

                    errors_list = []

                    # sheet_df =  pd.read_excel(marked_file, sheet_name = sheet, dtype = str, header=None, engine='calamine')
                    ws = xlsx_file[sheet]

                    data = []
                    for row in ws.iter_rows(values_only=True): 
                        data.append(row)

                    sheet_df = pd.DataFrame(data)
                    sheet_df_to_check_is_empty = sheet_df.copy()
                    sheet_df_to_check_is_empty = sheet_df_to_check_is_empty.dropna(axis=1, how='all')

                    print(sheet_df)

                    if sheet_df_to_check_is_empty.empty:
                        headers_df = pd.DataFrame([None, None])                    
                        s_f_check_dict = {
                            '_file_': file,
                            '_sheet_': sheet,
                            '_s_': '-',
                            '_f_': '-',
                            'Ошибки маркировки':'Пустой лист'}
                        # continue 

                    
                    else:
                        sheet_rem = (sheet_df[0].iloc[0])

                        errors_list.append(sheet_rem) # считываем комментарий если есть и добавляем в список
                        s = value_searcher(sheet_df[0], 's')
                        f = value_searcher(sheet_df[0], 'f')
                        # s = f = value_searcher(sheet_df[0], 'sf')

                        print('s, f', s, f) 
                        header_rows = sheet_df.iloc[0:2]
                        headers_df = sheet_df[sheet_df.columns[2:]].iloc[0:2] 

                        marking_errors = marking_checker(sheet_rem, s, f, header_rows)                   
                        s_f_check_dict = {
                            '_file_': file,
                            '_sheet_':sheet,
                            '_s_': s,
                            '_f_': f,
                            'Ошибки маркировки': marking_errors
                            }   
                                
                    
                    s_f_check_df = pd.DataFrame([s_f_check_dict])
                    result_s_f_check_df = pd.concat([result_s_f_check_df, s_f_check_df])

                    ###################################################################################################

                    first_and_second_line_dict = {}

                    for column in headers_df.columns:                

                        cell_in_first_line = headers_df.iloc[0].loc[column] 
                        cell_in_second_line = headers_df.iloc[1].loc[column]

                        if pd.notna(cell_in_first_line):
                            if cell_in_first_line in ('_file_', '_sheet_','_s_','_f_'):
                                first_and_second_line_dict[f"<<< колонка md-файла >>> { cell_in_first_line }"] = cell_in_first_line
                            else:
                                first_and_second_line_dict[cell_in_first_line] = cell_in_first_line
                        if pd.notna(cell_in_second_line):
                            first_and_second_line_dict[f"<<< с заполнением >>> { cell_in_second_line }"] = cell_in_second_line


                    first_and_second_line_df = pd.DataFrame([first_and_second_line_dict])
                    result_first_and_second_line_df = pd.concat([result_first_and_second_line_df, first_and_second_line_df]) 

                    ###################################################################################################

                    markup_dict[sheet] = {
                        'first_and_second_line_dict': first_and_second_line_dict,
                        's_f_check_dict': s_f_check_dict
                        }

                set_markup_in_db(
                    file,
                    modifyed_time=str(os.path.getmtime(os.path.join(global_vars.project_folder, '.Размеченные',file))),
                    markup_dict=markup_dict)
                

             # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            
            result_first_and_second_line_df.fillna("-", inplace=True)

        
        result_df = pd.concat([result_s_f_check_df, result_first_and_second_line_df], axis=1)  
        result_df_columns = list(dict.fromkeys(list(result_s_f_check_df.columns) +
                                               list(result_first_and_second_line_df.columns)))
        
        result_df = result_df[result_df_columns]        

        errors_list = list(map(str, errors_list))


        result_df.to_excel(os.path.join(project_folder, "markup.xlsx"), index=False)   
        
        wb = load_workbook(os.path.join(project_folder, "markup.xlsx"))
        ws = wb.active

        # Ширину столбцов A, B задаём по содержимому
        column_a = ws['A']
        max_a = 0
        for i in column_a:
            max_a=max(max_a, len(str(i.value)))

        ws.column_dimensions["A"].width = max_a+2


        column_b = ws['B']
        max_b = 0
        for i in column_b:
            max_b=max(max_b, len(str(i.value)))                

        ws.column_dimensions["B"].width = max_b+2

        # Закрепляем области
        freeze_cell = ws.cell(column=3, row=2)
        ws.freeze_panes = freeze_cell

        ws.auto_filter.ref = ws.dimensions

        wb.save(os.path.join(project_folder, "markup.xlsx"))
        global_vars.ui.info_label.setStyleSheet('color: green')  


    def on_signal(self,mysignal):          
        global_vars.ui.info_label.setText(mysignal)


    def run(self): 
        self.message_title = "Разметка"
        self.error_message = ""
        self.warning_message = ""
        global_vars.ui.info_label.setStyleSheet('color: blue')
        sleep(0.01) 

        if (not os.path.exists(os.path.join(global_vars.project_folder, "markup.xlsx")) and
            os.path.exists(os.path.join(global_vars.project_folder, "~$markup.xlsx"))):
            os.remove(os.path.join(global_vars.project_folder, "~$markup.xlsx"))

        if check_excel_file_is_open("markup.xlsx"):
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText('Закройте файл markup.xlsx перед тем как запустить обработку.')   
            self.warning_message ='Файл markup.xlsx уже открыт на рабочем столе.\nЗакройте его и заново нажмите кнопку "Просмотреть разметку"'
            return 
        # else:
        #     df = pd.DataFrame(['Что-то пошло не так'], index=None)
        #     df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None) 
           
        self.err_list = [] 

        clean_process_folder(global_vars.project_folder)  
        self.clean_md_folder()
        
        is_files_modified = check_files_modified('.Исходники')
        if type(is_files_modified) == type([]):

            # если файлы в .Исходниках поменялись и они есть в .Размеченных
            # то нужно спросить нужно ли его переразметить или оставить как есть
            md_files = list(os.walk(os.path.join(global_vars.project_folder, '.Размеченные')))[0][2] 
            self.wrn_list = []
            for file_modified in is_files_modified:
                if f"md_{file_modified}" in md_files:
                    self.warning_message = ('Некоторые файлы в папке .Исходники\n'
                                            'были пересохранены.\n'
                                            'Если их нужно переразметить,\n'
                                            'удалите md-файлы из папки .Размеченные!'
                                            )
                          
                    self.wrn_list.append((f"md_{file_modified}", 'Файл в .Исходниках поменялся, если его нужно переразметить, удалите md-файл из папки .Размеченные'))

            if self.wrn_list:
                df = pd.DataFrame(self.wrn_list)
                df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None)
                
            refresh_files_info('.Исходники')        
            refresh_files_info('.Размеченные')  

        if not self.warning_message:
            self.check_path_length()
            self.check_src_files_available()     

            self.err_list = self.check_path_length_err_list + self.check_src_files_available_err_list
            self.error_message = self.check_path_length_error_message + self.check_src_files_available_error_message
    
        else:
            if self.err_list:
                df = pd.DataFrame(self.err_list)
                df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None)

                        

        if not self.error_message and not self.warning_message:
            self.premarker(global_vars.project_folder)
        else:
            if self.err_list:
                df = pd.DataFrame(self.err_list)
                df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None)

        if not self.error_message and not self.warning_message:            
            self.all_columns(global_vars.project_folder)
        else:
            if self.err_list:
                df = pd.DataFrame(self.err_list)
                df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None)            

                  


    def on_clicked(self):
        init_project()

              
        self.start() # Запускаем поток  
     


    def on_started(self): # Вызывается при запуске потока
        global_vars.ui.pushButtonChooseProjectFolder.setEnabled(False)   
        all_control_elements_off()

       


    def on_finished(self): # Вызывается при завершении потока

        if self.error_message:
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"{self.error_message.replace('\n',' ')}")
            
            QtWidgets.QMessageBox.critical(
                None,
                self.message_title,
                self.error_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok
                )
            
            refresh_files_info('.Исходники')        
            refresh_files_info('.Размеченные')

            global_vars.ui.info_label.setStyleSheet('color: blue')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"Поднимаем markup.xlsx поверх всех окон.")

            open_or_show_file(file_name='markup.xlsx')
            

        elif self.warning_message:
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"{self.warning_message.replace('\n',' ')}")
            
            QtWidgets.QMessageBox.warning(
                None,
                self.message_title,
                self.warning_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok
                )  
            
            open_or_show_file(file_name='markup.xlsx')


            # if 'Некоторые файлы в папке .Исходники' in self.warning_message:
            #     msg = QtWidgets.QMessageBox.warning(
            #         None,
            #         self.message_title,
            #         'Открыть папку .Размеченные?',
            #         buttons=QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            #         )
            #     
            #     if  msg == 16384:  
            #         os.startfile(os.path.join(global_vars.project_folder, '.Размеченные'))    

             

        else:
            open_or_show_file(file_name='markup.xlsx')

            global_vars.ui.pushButtonConcat.setEnabled(True)
            global_vars.ui.pushButtonMakeFiles.setEnabled(True)  


            global_vars.ui.info_label.setStyleSheet('color: green')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"Обработка завершена. Файл markup.xlsx открыт на рабочем столе.")
            refresh_files_info('.Исходники')        
            refresh_files_info('.Размеченные')  



        all_control_elements_on()       
