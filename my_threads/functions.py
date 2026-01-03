import pandas as pd
import psutil
import os
from openpyxl.utils import range_boundaries, get_column_letter
from openpyxl.styles import borders, Side, Border

from colorama import Fore

from collections import Counter
import sqlite3
import json
from datetime import datetime

import global_vars
import pyperclip
import json
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PySide6.QtCore import QFile, QIODevice
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
from time import sleep 

import resources_rc

def read_resource(resource_path):
    """Читает данные из ресурса PySide6"""
    file = QFile(resource_path)
    
    if not file.exists():
        raise FileNotFoundError(f"Ресурс не найден: {resource_path}")
    
    if file.open(QIODevice.ReadOnly):
        data = bytes(file.readAll())
        file.close()
        return data
    else:
        raise IOError(f"Не удалось открыть ресурс: {resource_path}")
    

def decrypt_file_with_private_key(encrypted_file, private_key, output_file=None, password=None):
    """
    Расшифровывает файл, зашифрованный RSA публичным ключом
    
    Args:
        encrypted_file: путь к зашифрованному файлу
        private_key_file: путь к файлу с приватным ключом
        output_file: путь для сохранения расшифрованного файла (опционально)
        password: пароль для зашифрованного приватного ключа
    """
    
    
    
    # 2. Читаем зашифрованный файл
    print(f"Чтение зашифрованного файла {encrypted_file}...")
    with open(encrypted_file, "rb") as f:
        encrypted_data = f.read()
    
    print(f"✓ Прочитано {len(encrypted_data)} байт")
    
    # 3. Определяем формат зашифрованных данных
    try:
        # Пробуем декодировать как JSON (многоканковое шифрование)
        encrypted_str = encrypted_data.decode('utf-8')
        chunks = json.loads(encrypted_str)
        
        if isinstance(chunks, list):
            print(f"Обнаружено многоканковое шифрование: {len(chunks)} чанков")
            
            # Расшифровываем каждый чанк
            decrypted_chunks = []
            for i, chunk_b64 in enumerate(chunks, 1):
                print(f"  Расшифровка чанка {i}/{len(chunks)}...")
                chunk_data = base64.b64decode(chunk_b64)
                decrypted_chunk = private_key.decrypt(
                    chunk_data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                decrypted_chunks.append(decrypted_chunk)
            
            decrypted_data = b''.join(decrypted_chunks)
        else:
            raise ValueError("Неверный формат JSON")
            
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Если не JSON, то это single chunk в base64 или raw bytes
        print("Обнаружено одноканальное шифрование...")
        
        try:
            print('Пробуем декодировать как base64')
            encrypted_bytes = base64.b64decode(encrypted_data)
        except:
            print('Если не base64, используем как есть')
            encrypted_bytes = encrypted_data
        
        decrypted_data = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
   
    return json.loads(decrypted_data.decode('utf-8'))


def get_license_data():
    license_file = os.path.join(os.getcwd(),'license')
    private_key = serialization.load_pem_private_key(
        read_resource(":/keys_manager/private_key.pem"),
        password="Rostiks".encode(),  # Укажите пароль если ключ зашифрован
        backend=None    # default_backend будет использован автоматически
        )


    if not os.path.exists(license_file):
        license_dict = {
            'user': 'Файл лицензии отсутствует',
            'trial_finish': '1970-01-01 00:00:00'
            }
    else:
        try:
            license_dict = decrypt_file_with_private_key(
                license_file,
                private_key, output_file=None, password=None)
        except:
            license_dict = {
            'user':  'Файл лицензии повреждён',
            'trial_finish': '1970-01-01 00:00:00'
            }
    return license_dict

def init_project():
    if not os.path.exists(os.path.join(global_vars.project_folder, '.Обработка')):
        os.mkdir(os.path.join(global_vars.project_folder, '.Обработка'))
    
    if not os.path.exists(os.path.join(global_vars.project_folder, '.Размеченные')):
        os.mkdir(os.path.join(global_vars.project_folder, '.Размеченные'))

    conn = sqlite3.connect(os.path.join(global_vars.project_folder, "files_info.db"))
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS src_files_info (file TEXT, modifyed_time TEXT)")  
        # cur.execute("CREATE TABLE IF NOT EXISTS actual_src_files_info (file TEXT, modifyed_time TEXT)")  
        cur.execute("CREATE TABLE IF NOT EXISTS md_files_info (file TEXT, modifyed_time TEXT)")  
        # cur.execute("CREATE TABLE IF NOT EXISTS actual_md_files_info (file TEXT, modifyed_time TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS markup (file TEXT, modifyed_time TEXT, markup_json TEXT)")   

    with conn:

        cursor = conn.cursor()

        # Способ 1: Используем sqlite_master
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print("Список таблиц:")
        for table in tables:
            print(f"  - {table[0]}")                       


def value_searcher(col, value):
    #found = col[col==value]
    found = col.apply(lambda x: value in str(x))
    found = found[found]
    if found.size == 0:
        return "-"
    elif (len(found)) > 1:
        return "несколько"
    else:
        return str(found.index[0]+1)


def headers_checker(header_rows_df):
    i = 0
    errors_list = []
    for column in header_rows_df.columns:
        i += 1
        if i >= 3:
            if not pd.isna(header_rows_df[column].iloc[0]) and not pd.isna(header_rows_df[column].iloc[1]):
                errors_list.append(str(i))
    if errors_list != []:
        return 'Колонки: ' + ', '.join(errors_list) + ' промаркированы и "с заполнением" и "без"' 

    for column in header_rows_df.columns:
        i += 1
        if i >= 3:
            if not pd.isna(header_rows_df[column].iloc[0]) and not pd.isna(header_rows_df[column].iloc[1]):
                errors_list.append(str(i))
    if errors_list != []:
        return 'Колонки: ' + ', '.join(errors_list) + ' промаркированы и "с заполнением" и "без"'


def repeating_headers_checker(header_rows_df):

    headers_0 = [i for i in header_rows_df.loc[0][2:] if pd.notna(i)]
    headers_1 = [i for i in header_rows_df.loc[1][2:] if pd.notna(i)]
    if headers_0 == [] and headers_1 == []:
        return ("Не выбрано ни одного заголовка")    

    errors_list = [f"{k}-{v}" for k,v in Counter(headers_0 + headers_1).items() if v>1]
    if errors_list != []:
        return ("Повторяющиеся заголовки: " + ", ".join(errors_list))


def marking_checker(sheet_rem, s, f, header_rows):
    errors_list = []

    # if str(sheet_rem) != 'nan':
    if str(sheet_rem) != 'None' and str(sheet_rem) != 'nan':        
        return sheet_rem

    if s == "-" and f == "-":
        return "-"
    elif s == "-" and f != "-":
        errors_list.append('Маркер s не задан')
    elif s != "-" and f == "-":
        errors_list.append('Маркер f не задан')        

    if s == "несколько":
        errors_list.append("Маркер s проставлен в нескольких строках")
    elif s != "-":
        if int(s) < 3:
            errors_list.append('Маркер s расположен выше области таблицы')        
            
    if f == "несколько":
        errors_list.append("Маркер f проставлен в нескольких строках")
    elif f != "-":
        if int(f) < 2:
            errors_list.append('Маркер f расположен выше области таблицы') 

    if (s != "несколько" and f != "несколько" and
        s !="-" and f != "-" and
        int(s) > int(f)):
        errors_list.append('Маркер f расположен выше маркера s')  

    headers_errors =  headers_checker(header_rows)
    if headers_errors:
        errors_list.append(headers_errors) 

    repeating_headers_errors = repeating_headers_checker(header_rows)
    if repeating_headers_errors:
        errors_list.append(repeating_headers_errors)       

    if errors_list:        
        return ("; " + "\n").join(errors_list)
    else:
        return "ok"


def refresh_files_info (folder):
    if folder=='.Размеченные':
        table='md_files_info'
    elif folder=='.Исходники': 
        table='src_files_info'

    folder_path = os.path.join(global_vars.project_folder, folder)

    files = list(os.walk(folder_path))[0][2]    
    files = [(file, f"{os.path.getmtime(os.path.join(folder_path , file))}") for file in files if file[0] != "~"] 

    conn = sqlite3.connect(os.path.join(global_vars.project_folder, "files_info.db"))
    with conn:
        actual_files_info_df = pd.DataFrame(files, columns=['file','modifyed_time'])
        actual_files_info_df.to_sql(table, conn, index=False, if_exists='replace')


def check_files_modified(folder):
    print(f'check_files_modified {folder}')

    global_vars.ui.info_label.setStyleSheet('color: blue')
    global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}. Проверяем не менялись ли файлы в папке .Исходники")

    if folder=='.Размеченные':
        table='md_files_info'
    elif folder=='.Исходники': 
        table='src_files_info'

    folder_path = os.path.join(global_vars.project_folder, folder)  

    files = list(os.walk(folder_path))[0][2]    
    files = [(file, f"{os.path.getmtime(os.path.join(folder_path, file))}") for file in files if file[0] != "~"]

    conn = sqlite3.connect(os.path.join(global_vars.project_folder, "files_info.db"))
    with conn:
        cur = conn.cursor()


        actual_md_files_info_df = pd.DataFrame(files, columns=['file','modifyed_time'])
        actual_md_files_info_df.to_sql(f'actual_{table}', conn, index=False, if_exists='replace')

        files_in_table = list(cur.execute(f"SELECT * FROM {table}"))
        if  not files_in_table:
            print(Fore.RED, "Таблица БД не содержит записей", files_in_table, Fore.WHITE)
            return True
        
        cur.execute(f"SELECT t.file FROM {table} AS t INNER JOIN actual_{table} AS at ON t.file = at.file WHERE t.modifyed_time <> at.modifyed_time")
        
        files_modified = [file[0] for file in cur.fetchall()]
        #input('Ждем ввод')
        if  files_modified:
            print(Fore.RED, f"Файлы были пересохранены {files_modified}", Fore.WHITE)            
            return files_modified
        
        new_files = list(cur.execute(f"SELECT * FROM actual_{table} AS at LEFT JOIN {table} AS t ON t.file = at.file WHERE t.file IS NULL"))
        if  new_files:
            print(Fore.RED, f"Появились новые файлы {new_files}", Fore.RESET)           
            return True 

        deleted_files = list(cur.execute(f"SELECT * FROM {table} AS t LEFT JOIN actual_{table} AS at ON t.file = at.file WHERE at.file IS NULL"))
        if  deleted_files:
            print(Fore.RED, f"Некоторые файлы были удалены {deleted_files}", Fore.RESET)           
            return True 
    
        return False


def max_column(file, sheet_name):
    df = pd.read_excel(file, sheet_name = sheet_name)
    return (len(df.columns))


def clean_process_folder(project_folder):
    """
    Удаляет из папкпи .Обработка файлы, которые можно удалить
    """

    if not project_folder:
        return 
    
    try:
        processing_files = list(os.walk(os.path.join(project_folder,'.Обработка')))[0][2]
    except:
        print(Fore.RED, "Папка .Обработка не была очищенна. Или её нет или папка проекта не выбрана", Fore.RESET)
        return
    
    for pr_file_number, pr_file in enumerate(processing_files, 1):
        try:
            os.remove(os.path.join(project_folder, '.Обработка', pr_file))
        except PermissionError:
            print(Fore.RED, f"{pr_file_number} из {len(processing_files)} Файл {pr_file} не может быть удален из .Обработка", Fore.RESET)
            pass


def all_control_elements_off():
        global_vars.interface_enabled = False
        ##########################################################################################
        global_vars.ui.pushButtonChooseProjectFolder.setEnabled(False)
        global_vars.ui.pushButtonXLStoXLSX.setEnabled(False)
        global_vars.ui.pushButtonProcessing.setEnabled(False)

        global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(False)
        global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(False)
        global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(False)
        
        global_vars.ui.pushButtonConcat.setEnabled(False)
        ##########################################################################################
        global_vars.ui.pushButtonHeadersFiller.setEnabled(False)
        global_vars.ui.pushButtonShowEmpty.setEnabled(False) 
        global_vars.ui.pushButtonRenameColumn.setEnabled(False)

        global_vars.ui.radioButtonOldInTopHeader.setEnabled(False)
        global_vars.ui.radioButtonOldInBottomHeader.setEnabled(False)
        global_vars.ui.lineEditOldColumnNameInHeader.setEnabled(False)

        global_vars.ui.radioButtonNewInTopHeader.setEnabled(False)
        global_vars.ui.radioButtonNewInBottomHeader.setEnabled(False)
        global_vars.ui.lineEditNewColumnNameInHeader.setEnabled(False)
        ##########################################################################################
        global_vars.ui.pushButtonChangeRem.setEnabled(False)
        global_vars.ui.lineEditOldRem.setEnabled(False)
        global_vars.ui.lineEditNewRem.setEnabled(False)


def all_control_elements_on():
        print(Fore.BLUE, 'all_control_elements_on', Fore.RESET)
        license_data = get_license_data()
        print(Fore.GREEN, license_data, Fore.RESET)
        trial_finish = license_data['trial_finish']


        if datetime.now()<=datetime.strptime(trial_finish, "%Y-%m-%d %H:%M:%S"):
            global_vars.interface_enabled = True
            ##########################################################################################
            global_vars.ui.pushButtonChooseProjectFolder.setEnabled(True)

            if os.path.exists(os.path.join(global_vars.project_folder,'.Исходники')):
                source_files_list = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]
                source_old_excels_list = [file for file in source_files_list if file[-4:] in ['.xls', 'xlsm']]
            if source_old_excels_list:
                global_vars.ui.pushButtonXLStoXLSX.setEnabled(True)
                
            global_vars.ui.pushButtonProcessing.setEnabled(True)       
            # global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(True) 
            # global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(True)                
            # global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(True)
            ##########################################################################################
            # global_vars.ui.pushButtonHeadersFiller.setEnabled(True)
            
            #global_vars.ui.pushButtonShowEmpty.setEnabled(True)  

            global_vars.ui.radioButtonOldInTopHeader.setEnabled(True)
            global_vars.ui.radioButtonOldInBottomHeader.setEnabled(True)            

            global_vars.ui.lineEditOldColumnNameInHeader.setEnabled(True)

            global_vars.ui.radioButtonNewInTopHeader.setEnabled(True)
            global_vars.ui.radioButtonNewInBottomHeader.setEnabled(True)        

            global_vars.ui.lineEditNewColumnNameInHeader.setEnabled(True)
            ##########################################################################################
            # global_vars.ui.pushButtonChangeRem.setEnabled(True)

            global_vars.ui.lineEditOldRem.setEnabled(True)
            global_vars.ui.lineEditNewRem.setEnabled(True)
        else:
            print(Fore.RED, 'Просроченная лицензия', Fore.RESET)


def get_files_to_show():
    md_folder_info = list(os.walk(os.path.join(global_vars.project_folder, '.Размеченные')))

    if md_folder_info:
        md_files = md_folder_info[0][2]
    else:
        global_vars.ui.tableMDFilesInClipboard.clear()
        return []
    
    if not md_files:
        global_vars.ui.tableMDFilesInClipboard.clear()
        return []

    files_list_in_pyperclip = (set(pyperclip.paste().splitlines()))

    files_to_show = [
        file_in_pyperclip.split('\t')[0] for file_in_pyperclip in files_list_in_pyperclip if file_in_pyperclip.split('\t')[0] in md_files]
    
    files_to_show.sort()

    return files_to_show


def get_files_and_sheets_from_pyperclip():
    md_folder_info = list(os.walk(os.path.join(global_vars.project_folder, '.Размеченные')))

    if md_folder_info:
        md_files = md_folder_info[0][2]
    else:
        global_vars.ui.tableMDFilesInClipboard.clear()
        return []
    
    if not md_files:
        try:
            global_vars.ui.tableMDFilesInClipboard.clear()
            return []
        except AttributeError:
            pass
    
    try:
        in_clipboard = pyperclip.paste()
    except Exception as e: #pyperclip.PyperclipWindowsException:
        print(str(e))
        pyperclip.paste('')
        in_clipboard = ''
        
    if not in_clipboard:
        return []
    
    lines_in_pyperclip = in_clipboard.splitlines()
    file_sheet_list = [line_in_pyperclip.split('\t')[:2] for line_in_pyperclip in lines_in_pyperclip]

    # print(Fore.MAGENTA, file_sheet_list, Fore.RESET)

    if not file_sheet_list:
        return []

    if len(file_sheet_list[0]) == 2:
        # print(Fore.MAGENTA, 'Мы тут', Fore.RESET)

        file_sheet_to_run = list({(file_sheet[0], file_sheet[1]) for file_sheet in file_sheet_list if file_sheet[0] in md_files})
    
        file_sheet_to_run.sort()

        return file_sheet_to_run

    if len(file_sheet_list[0]) == 1:

        file_sheet_to_run = list({(file_sheet[0],) for file_sheet in file_sheet_list if file_sheet[0] in md_files})
    
        file_sheet_to_run.sort()

        return file_sheet_to_run

    else:
        return []




def get_range_info(cell_range):
    """
    Возвращает информацию о диапазоне ячеек
    Args:
        cell_range: строка диапазона (например, "B3:F10")
    Returns:
        словарь с информацией о диапазоне
    """
    # Используем встроенную функцию openpyxl
    min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    
    return {
        'min_row': min_row,
        'max_row': max_row,
        'min_col': min_col,
        'max_col': max_col,
        'min_col_letter': get_column_letter(min_col),
        'max_col_letter': get_column_letter(max_col),
        'start_cell': f"{get_column_letter(min_col)}{min_row}",
        'end_cell': f"{get_column_letter(max_col)}{max_row}",
        'range_string': cell_range
    }

def set_range_border(ws, min_row, max_row, min_col, max_col):


  
    suround_min_row = min_row - 1
    suround_max_row = max_row + 1
    suround_min_col = min_col - 1
    suround_max_col = min_row + 1

    """
    suround_border_style = borders.BORDER_SLANTDASHDOT
    # suround_border_style = borders.BORDER_NONE        

    for row in range(suround_min_row, suround_max_row+1):
        if row == 0 or row == 65536:
            continue

        for col in range(suround_min_col, suround_max_col+1):
            if col == 0 or col == 1048576:
                continue
            try:
                suround_cell = ws.cell(row=row, column=col)
                suround_border = Border()
                
                # Очищаем верхнюю границу (только для первой строки диапазона)
                if row == suround_min_row and col not in [suround_min_col, suround_max_col]:

                    suround_border.top = Side(style=suround_border_style, color='00FF00')
                
                # Очищаем нижнюю границу (только для последней строки диапазона)
                if row == suround_max_row and col not in [suround_min_col, suround_max_col]:

                    suround_border.bottom = Side(style=suround_border_style, color='00FF00')
                
                # Очищаем левую границу (только для первого столбца диапазона)
                if col == suround_min_col and row not in [suround_min_row, suround_max_row]:

                    suround_border.right =Side(style=suround_border_style, color='00FF00')
                
                # Очищаем правую границу (только для последнего столбца диапазона)
                if col == suround_max_col and row not in [suround_min_row, suround_max_row]:

                    suround_border.left = Side(style=suround_border_style, color='00FF00')

                suround_cell.border = suround_border

            except:
                pass    
    """

    # border_style = borders.BORDER_SLANTDASHDOT
    border_style = borders.BORDER_THICK

    for row in range(min_row, max_row+1):
        for col in range(min_col, max_col+1):            

            cell = ws.cell(row=row, column=col)
            border = Border()

            # Верхняя граница (только для первой строки диапазона)
            if row == min_row:
                #border.top = Side(style=border_style)
                border.top = Side(style=border_style, color="fe6072")
            
            # Нижняя граница (только для последней строки диапазона)
            if row == max_row:
                #border.bottom = Side(style=border_style)               
                border.bottom = Side(style=border_style, color='fe6072')
            
            # Левая граница (только для первого столбца диапазона)
            if col == min_col:
                #border.left = Side(style=border_style)           
                border.left = Side(style=border_style, color="fe6072")
            
            # Правая граница (только для последнего столбца диапазона)
            if col == max_col:
                #border.right = Side(style=border_style)
                border.right = Side(style=border_style, color="fe6072")
            
            cell.border = border


'''
def set_range_border(ws, min_row, max_row, min_col, max_col):
    """Устанавливает границу только по внешнему контуру диапазона"""
    
    thin = Side(border_style="thick", color="FFFFC7CE")
    
    # Верхняя граница
    for col in range(min_col, max_col + 1):
        cell = ws.cell(row=min_row, column=col)
        if not cell.border:
            cell.border = Border()
        cell.border = Border(top=thin, 
                           bottom=cell.border.bottom,
                           left=cell.border.left,
                           right=cell.border.right)
    
    # Нижняя граница
    for col in range(min_col, max_col + 1):
        cell = ws.cell(row=max_row, column=col)
        if not cell.border:
            cell.border = Border()
        cell.border = Border(bottom=thin,
                           top=cell.border.top,
                           left=cell.border.left,
                           right=cell.border.right)
    
    # Левая граница
    for row in range(min_row, max_row + 1):
        cell = ws.cell(row=row, column=min_col)
        if not cell.border:
            cell.border = Border()
        cell.border = Border(left=thin,
                           right=cell.border.right,
                           top=cell.border.top,
                           bottom=cell.border.bottom)
    
    # Правая граница
    for row in range(min_row, max_row + 1):
        cell = ws.cell(row=row, column=max_col)
        if not cell.border:
            cell.border = Border()
        cell.border = Border(right=thin,
                           left=cell.border.left,
                           top=cell.border.top,
                           bottom=cell.border.bottom)

'''

def set_markup_in_db(db, file, modifyed_time='', markup_dict={}):

    conn = sqlite3.connect(db)
    markup_json = json.dumps(markup_dict, ensure_ascii=False)
    
    with conn:
        cur = conn.cursor()
        
        cur.execute(
            f"DELETE FROM markup WHERE file = '{file}'")

        
        sql = (f"INSERT INTO markup (file , modifyed_time , markup_json) "
               f"VALUES ('{file}', '{modifyed_time}', '{markup_json.replace("'", "''")}');")
        
        # print(Fore.CYAN, sql, Fore.RESET)

        cur.execute(sql)

def get_markup_from_db(db, file):
    conn = sqlite3.connect(db)
    res = {}
    
    with conn:
        cur = conn.cursor()
        
        sql = (f"SELECT file , modifyed_time , markup_json "
               f"FROM markup WHERE file = '{file}';")
        
        # print(sql)

        cur.execute(sql)
        row = cur.fetchone()
        # print(row)
        if row:
            res['modifyed_time'] = row[1]

            markup_json = row[2]
            res['markup_dict'] = json.loads(markup_json)


        return res            

def check_excel_file_is_open(filename):
    """
    Проверяет, открыт ли файл Excel в системе
    """
    print(Fore.YELLOW,  f"Запускаем проверку открытости файла {filename}", Fore.RESET)
    # Получаем базовое имя файла без пути
    base_name = os.path.basename(filename)
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Проверяем процессы Excel (Windows)
            if proc.info['name'] and 'excel' in proc.info['name'].lower():
                # Для Windows можно проверить открытые файлы процесса
                try:
                    open_files = proc.open_files()
                    for f in open_files:
                        if base_name.lower() in f.path.lower():
                            return True, proc.info['pid']
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    continue
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    return False#, None


def pop_up_files(message_title, warning_message, md_files_opened, folder = ''):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle(message_title)
            msg_box.setText(warning_message)
            msg_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No )

            # Меняем стандартные подписи
            msg_box.button(QMessageBox.Yes).setText("Показать поверх других окон?")
            msg_box.button(QMessageBox.No).setText("Нет")
            result = msg_box.exec()
 
            print(result)
            if result == QMessageBox.StandardButton.Yes:

                for file in md_files_opened:
                    os.startfile(os.path.join(global_vars.project_folder, folder, file))

      
   


def open_or_show_file(file_name='markup.xlsx'):
    global_vars.ui.info_label.setStyleSheet('color: blue')             
    global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                        f"{file_name} открываем или помещаем поверх всех окон.")

    if os.path.exists(os.path.join(global_vars.project_folder, file_name)):
        os.startfile(os.path.join(global_vars.project_folder, file_name))

    while True:
        sleep(0.1)
        if os.path.exists(os.path.join(global_vars.project_folder, f'~${file_name}')):
            break

    global_vars.ui.info_label.setStyleSheet('color: green')             
    global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                        f"{file_name} открыт и помещён поверх всех окон.")    


def on_finsh_change_thread(message_title, error_message, warning_message, info_message, md_files_opened):
        if warning_message:
            global_vars.ui.info_label.setStyleSheet('color: red')
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} {warning_message.replace('\n',' ')}.")

            pop_up_files(message_title, warning_message, md_files_opened, '.Размеченные')



        elif error_message:
            global_vars.ui.info_label.setStyleSheet('color: red')            
            global_vars.ui.info_label.setText(error_message.replace('\n',' '))

            QMessageBox.critical(None,
                message_title,
                error_message,
                buttons=QMessageBox.StandardButton.Ok)
            


        else:
            global_vars.ui.info_label.setStyleSheet('color: green')
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} {message_title} {info_message}")

            QMessageBox.information(
                None,
                message_title,
                info_message,
                buttons=QMessageBox.StandardButton.Ok)