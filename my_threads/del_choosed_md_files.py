from PySide6 import QtWidgets, QtCore
from colorama import Fore
import global_vars 
import os
import pyperclip
import pandas as pd
from datetime import datetime
from my_threads.functions import get_files_and_sheets_from_pyperclip, all_control_elements_on, all_control_elements_off, is_excel_file_open



class DelChoosedMDFilesThread(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Удаляем выбранные md-файлы:"

    def run(self): 
        self.error_message = ""
        self.warning_message = ""
        self.info_message = ""   

        if is_excel_file_open("markup.xlsx"):
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText('Закройте файл markup.xlsx перед тем как запустить обработку.')   
            self.warning_message =('Файл markup.xlsx уже открыт на рабочем столе.\n'
                                   'Закройте его и снова попробуйте удалить файлы!')
            return 

        df = pd.DataFrame(['что-то пошло не так'])
        df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None)

    

        self.err_list = []
        
        folder = os.path.join(global_vars.project_folder,'.Размеченные')

        get_files_and_sheets_from_pyperclip

        for file in self.files_list_in_pyperclip:
            file_to_del = os.path.join(folder, file)     

            if not os.path.exists(file_to_del):
                self.error_message = ("Некоторые файлы не могут быть удалены")
                self.err_list.append((file, 'Не можем удалить этот файл, потому что его нет в папке .Размеченные'))
                continue
            try:
                os.remove(file_to_del) 
            except:     
                self.error_message = ("Некоторые файлы не могут быть удалены")                

                self.err_list.append((file, 'Не можем удалить этот файл, потому что он открыт на рабочем столе'))                

        if self.err_list:

            df = pd.DataFrame(self.err_list, index=None)
            df.to_excel(os.path.join(global_vars.project_folder, 'markup.xlsx'), index=None, header=None)

            

    def on_clicked(self): 
        self.files_list_in_pyperclip = get_files_and_sheets_from_pyperclip()

        files_sheet_to_show = get_files_and_sheets_from_pyperclip()
        # print(Fore.GREEN, files_sheet_to_show, Fore.RESET)
        self.files_list_in_pyperclip= list({file_sheet[0] for file_sheet in files_sheet_to_show})
        self.files_list_in_pyperclip.sort()


        confirm = QtWidgets.QMessageBox(None, self.message_title, None)
        confirm.setText(f'Подтвердите удаление файлов:\n'
                        f'{'\n'.join(self.files_list_in_pyperclip)}')
        confirm.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel) 
        confirm.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        button = confirm.exec()
        if button == 1024:  
            self.start() # Запускаем поток  

    def on_started(self):
        global_vars.ui.pushButtonChooseProjectFolder.setEnabled(False)  
        global_vars.ui.pushButtonXLStoXLSX.setEnabled(False)     
        global_vars.ui.pushButtonProcessing.setEnabled(False)
        global_vars.ui.pushButtonHeadersFiller.setEnabled(False)          
        global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(False) 
        global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(False)                
        global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(False)
     

    def on_finished(self): # Вызывается при завершении потока
        all_control_elements_on()

        # print(Fore.MAGENTA, self.error_message, Fore.RESET)
        if self.error_message:
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"{self.error_message.replace('\n',' ')}")
            QtWidgets.QMessageBox.critical(None,
                                           self.message_title,
                                           self.error_message,
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok)
            os.startfile(os.path.join(global_vars.project_folder, "markup.xlsx"))
        elif self.warning_message:
            global_vars.ui.info_label.setStyleSheet('color: red')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"{self.warning_message.replace('\n',' ')}")
            
            QtWidgets.QMessageBox.warning(None,
                                           self.message_title,
                                           self.warning_message,
                                           buttons=QtWidgets.QMessageBox.StandardButton.Ok)    
        else:
            global_vars.ui.info_label.setStyleSheet('color: green')             
            global_vars.ui.info_label.setText(f"{datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")} "
                                              f"Файлы удалены.")



        # if os.path.exists(os.path.join(global_vars.project_folder, "markup.xlsx")):
           
