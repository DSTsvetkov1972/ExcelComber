from PySide6 import QtWidgets, QtCore
from colorama import Fore
import global_vars 
import os
from my_threads.functions import check_excel_file_is_open, check_path_length, all_control_elements_off, all_control_elements_on, get_license_data
from colorama import Fore
from datetime import datetime
import pandas as pd
from time import sleep


class ChooseProjectFolderThread(QtCore.QThread):

    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Выбор папки проекта:"


    def run(self): 
        self.error_message = ""
        self.warning_message = ""

        print(Fore.YELLOW, os.path.exists(os.path.join(global_vars.project_folder,'.Исходники')), Fore.RESET)

        if not global_vars.project_folder:

            global_vars.ui.project_folder_label.setStyleSheet('color: red')  
            global_vars.ui.project_folder_label.setText('Папка проекта: не выбрана') 
          
            global_vars.ui.info_label.setStyleSheet('color: red')            
            global_vars.ui.info_label.setText('Выберите папку проекта')
                
            self.error_message = ('Папка проекта: не выбрана')
            return
 
        if os.path.exists(os.path.join(global_vars.project_folder,'.Исходники')):
            source_files_list = list(os.walk(os.path.join(global_vars.project_folder,'.Исходники')))[0][2]
            source_excels_list = [file for file in source_files_list if file[-4:].lower() == 'xlsx']            
            source_old_excels_list = [file for file in source_files_list if file[-4:].lower() in ['.xls', 'xlsm']]

        else:
            global_vars.ui.project_folder_label.setStyleSheet('color: red')  
            global_vars.ui.project_folder_label.setText(f'Папка проекта: {global_vars.project_folder}') 
          
            global_vars.ui.info_label.setStyleSheet('color: red')            
            global_vars.ui.info_label.setText(f'В папке проекта нет папки .Исходники/.')
                
            self.error_message = ('В папке проекта нет папки .Исходники!\n'
                                  'Создайте в папке проекта папку .Исходники\n'
                                  'и скопируйте в неё файлы, которые нужно обработать,\n'
                                  'затем снова нажмите кнопку "Выбирете папку проекта"!')

            #all_control_elements_off()
            #global_vars.ui.pushButtonChooseProjectFolder.setEnabled(True)                 
            return 
        
        if not source_files_list:

            global_vars.ui.project_folder_label.setStyleSheet('color: red')  
            global_vars.ui.project_folder_label.setText(f'Папка проекта: {global_vars.project_folder}') 
       
            global_vars.ui.info_label.setStyleSheet('color: red')            
            global_vars.ui.info_label.setText(f'В папке проекта есть папка .Исходники/, но она не содержит файлов.')
                             
            self.error_message = f'Папка .Исходники/ не содержит файлов!\nСкопируйте в папку .Исходники/ файлы для обработки и снова нажмите кнопку "Выберите папку проекта"!'

            #all_control_elements_off()
            #global_vars.ui.pushButtonChooseProjectFolder.setEnabled(True)     
            return                  

        if source_old_excels_list:       

            global_vars.ui.project_folder_label.setStyleSheet('color: red')  
            global_vars.ui.project_folder_label.setText(f'Папка проекта: {global_vars.project_folder}') 
       
            global_vars.ui.info_label.setStyleSheet('color: red')            
            global_vars.ui.info_label.setText('В папке проекта есть папка .Исходники/, но в ней некоторые файлы в формате .xls или .xlsm')
                             
            self.error_message = 'В папке проекта есть папка .Исходники/, но в ней некоторые файлы в формате .xls или .xlsm'
            print('Мы тут! Странно!')
            global_vars.ui.pushButtonXLStoXLSX.setEnabled(True)
            sleep(0.01)
            print('Мы тут! Странно!')
            return                


        if not source_excels_list:
            global_vars.ui.project_folder_label.setStyleSheet('color: red')  
            global_vars.ui.project_folder_label.setText(f'Папка проекта: {global_vars.project_folder}') 
       
            global_vars.ui.info_label.setStyleSheet('color: red')            
            global_vars.ui.info_label.setText('В папке проекта есть папка .Исходники/, но в ней нет файлов .xlsx')
                             
            self.error_message = 'В папке проекта есть папка .Исходники/, но в ней нет файлов .xlsx'

            return
        
        self.length_err_list = check_path_length()
        
        if self.length_err_list:
            self.warning_message = (
                f"Длина пути к размеченным файлам {len(global_vars.project_folder + '.Размеченные') + 2},\n"
                f"полная длина пути к некоторым размеченным файлам превышает 218 символов.\n"
                f"Переименуйте файлы с длинными названиями или перенесите проект в папку с более коротким путём!\n")

        global_vars.ui.project_folder_label.setStyleSheet('color: green')  
        global_vars.ui.project_folder_label.setText(f'Папка проекта: {global_vars.project_folder}') 


        license_data = get_license_data()
        trial_finish = license_data['trial_finish']

        if datetime.now()>datetime.strptime(trial_finish, "%Y-%m-%d %H:%M:%S"):
            global_vars.ui.info_label.setStyleSheet('color: red')          
            global_vars.ui.info_label.setText('Срок действия лицензии закончился!')  
        else:
            global_vars.ui.info_label.setStyleSheet('color: green')          
            global_vars.ui.info_label.setText('Папка проекта выбрана. Нажмите кнопку Просмотреть разметку')

        '''
        global_vars.ui.pushButtonXLStoXLSX.setEnabled(False)
        global_vars.ui.pushButtonProcessing.setEnabled(True)
        global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(True)      
        global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(True)
        global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(True)          
        sleep(0.01)
        '''

   
                      
        print(f'run {self.message_title}')   

    def on_clicked(self):
        
        if check_excel_file_is_open("markup.xlsx"):
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText('Закройте файл markup.xlsx перед тем как выбирать папку проекта.')   
            self.error_message ='Файл markup.xlsx уже открыт на рабочем столе.\nЗакройте его и заново нажмите кнопку "Выбрать папку проекта"'
            
            QtWidgets.QMessageBox.critical(None,
                self.message_title,
                self.error_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok)
            return 
         
        
        if os.path.exists('.session_folder'):
            with open('.session_folder', encoding='utf-8') as f:
                dir = f.readline()
        else:
            dir = ''
    
        global_vars.project_folder = QtWidgets.QFileDialog.getExistingDirectory(dir=dir) 


        if global_vars.project_folder:
            with open('.session_folder', 'w', encoding='utf-8') as f:
                    f.write(global_vars.project_folder)
        print('Запускаем поток  ')
        self.start() # Запускаем поток  
     
        
    def on_started(self): # Вызывается при запуске потока     
        print(f"on_started {self.message_title}")
        all_control_elements_off() 


    def on_finished(self): # Вызывается при завершении потока


        global_vars.ui.pushButtonChooseProjectFolder.setEnabled(True)

        if self.error_message == 'В папке проекта есть папка .Исходники/, но в ней некоторые файлы в формате .xls или .xlsm':
            global_vars.ui.pushButtonXLStoXLSX.setEnabled(True)
        
        if self.error_message:
            QtWidgets.QMessageBox.critical(None,
                self.message_title,
                self.error_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok)
            return 
        
        if self.warning_message:
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"{self.warning_message.replace('\n',' ')}")
            QtWidgets.QMessageBox.warning(None,
                self.message_title,
                self.warning_message,
                buttons=QtWidgets.QMessageBox.StandardButton.Ok)
            
            df = pd.DataFrame(self.length_err_list)
            df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None)
            os.startfile(os.path.join(global_vars.project_folder, 'markup.xlsx'))
            while True:
                sleep(0.1)
                if os.path.exists(os.path.join(global_vars.project_folder, f'{os.path.join(global_vars.project_folder, '~$markup.xlsx')}')):
                    break
            return
        
        all_control_elements_on()
 
