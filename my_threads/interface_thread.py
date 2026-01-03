from PySide6 import QtWidgets, QtCore, QtGui
from colorama import Fore
import global_vars 
import os
import pyperclip
from time import sleep
from my_threads.functions import get_files_and_sheets_from_pyperclip


class InterfaceThread(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Открываем выбранные файлы:"

    def fill_in_md_files_table_title(self, files_sheet_to_show):
        # print(Fore.MAGENTA, files_sheet_to_show, len(files_sheet_to_show), Fore.RESET)

        if files_sheet_to_show:

            if len(files_sheet_to_show[0]) == 2:
                files_qty = len({file[0] for file in files_sheet_to_show })
                global_vars.ui.lineEditInClipboardTitle.setText(f'Выбрано файлов: {files_qty}. Выбрано листов: { len(files_sheet_to_show) }.')

            if len(files_sheet_to_show[0]) == 1:
                global_vars.ui.lineEditInClipboardTitle.setText(f'Выбрано файлов: { len(files_sheet_to_show) }')
  
        else:
            global_vars.ui.lineEditInClipboardTitle.setText('')



    def fill_in_md_files_table(self, files_sheet_to_show):
        # print(Fore.MAGENTA, files_sheet_to_show, len(files_sheet_to_show), Fore.RESET)

        if files_sheet_to_show:
            # global_vars.ui.tableMDFilesInClipboard.setVisible(True)
            if len(files_sheet_to_show[0]) == 2:
                global_vars.ui.tableMDFilesInClipboard.setColumnCount(2)
                global_vars.ui.tableMDFilesInClipboard.setRowCount(len(files_sheet_to_show))
                sleep(0.01)               
                

                for file_sheet_to_show_number,  file_sheet_to_show in enumerate(files_sheet_to_show, 0):

                    md_file_name = QtWidgets.QTableWidgetItem(file_sheet_to_show[0])
                    md_file_name.setForeground(QtGui.QColor(128,128,128))
                    md_file_sheet = QtWidgets.QTableWidgetItem(file_sheet_to_show[1])
                    md_file_sheet.setForeground(QtGui.QColor(128,128,128))

                    global_vars.ui.tableMDFilesInClipboard.setItem(file_sheet_to_show_number, 0, md_file_name)
                    global_vars.ui.tableMDFilesInClipboard.setItem(file_sheet_to_show_number, 1, md_file_sheet)

                global_vars.ui.tableMDFilesInClipboard.setColumnWidth(0, 240)
                global_vars.ui.tableMDFilesInClipboard.setColumnWidth(1, 60)

                global_vars.ui.lineEditInClipboardTitle.setText(f'Выбрано листов для редактирования: { len(files_sheet_to_show) }')
                sleep(0.0051)
                # global_vars.ui.tableMDFilesInClipboard.resizeColumnsToContents()

            if len(files_sheet_to_show[0]) == 1:
                global_vars.ui.tableMDFilesInClipboard.setColumnCount(1)
                global_vars.ui.tableMDFilesInClipboard.setRowCount(len(files_sheet_to_show))
                sleep(0.01)        
            
                

                for file_sheet_to_show_number,  file_sheet_to_show in enumerate(files_sheet_to_show, 0):
                    md_file_name = QtWidgets.QTableWidgetItem(file_sheet_to_show[0])
                    md_file_name.setForeground(QtGui.QColor(128,128,128))

                    global_vars.ui.tableMDFilesInClipboard.setItem(file_sheet_to_show_number, 0, md_file_name)

                global_vars.ui.tableMDFilesInClipboard.setColumnWidth(0, 240)
                global_vars.ui.lineEditInClipboardTitle.setText(f'Выбрано файлов для показа/удаления: { len(files_sheet_to_show) }')
  

        else:
            # global_vars.ui.tableMDFilesInClipboard.setVisible(False)
            global_vars.ui.lineEditInClipboardTitle.setText('')
            global_vars.ui.tableMDFilesInClipboard.setRowCount(0)


    def run(self):
        # clipboard_preceding = ''
        # project_folder_preceding = ''

        while True:
            sleep(0.5)
            #if not global_vars.interface_enabled:
            #    continue

            files_sheet_to_show = get_files_and_sheets_from_pyperclip()

            self.fill_in_md_files_table(files_sheet_to_show)
            self.fill_in_md_files_table_title(files_sheet_to_show)

            if files_sheet_to_show and global_vars.interface_enabled:

                if len(files_sheet_to_show[0]) == 2:

                    global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(True) 
                    global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(True)                
                    global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(True)

                    global_vars.ui.pushButtonHeadersFiller.setEnabled(True)
                    global_vars.ui.pushButtonShowEmpty.setEnabled(True)
                    global_vars.ui.pushButtonRenameColumn.setEnabled(True)
                    global_vars.ui.pushButtonChangeRem.setEnabled(True)

                elif len(files_sheet_to_show[0]) == 1:
                    global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(True) 
                    global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(True)                
                    global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(True)

                    global_vars.ui.pushButtonHeadersFiller.setEnabled(False)
                    global_vars.ui.pushButtonShowEmpty.setEnabled(False)
                    global_vars.ui.pushButtonRenameColumn.setEnabled(False)
                    global_vars.ui.pushButtonChangeRem.setEnabled(False)
                    
            else:
                #global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(False)

                #if os.path.exists(os.path.join(global_vars.project_folder, 'markup.xlsx')):
                #    global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(True)
                #    global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(True)                      
                #    global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(True)
                #else:

                global_vars.ui.pushButtonOpenChoosedFiles.setEnabled(False)
                global_vars.ui.pushButtonOpenChoosedMDFiles.setEnabled(False)
                global_vars.ui.pushButtonDelChoosedMDFiles.setEnabled(False)  
                


                global_vars.ui.pushButtonHeadersFiller.setEnabled(False)                    
                global_vars.ui.pushButtonShowEmpty.setEnabled(False)
                global_vars.ui.pushButtonRenameColumn.setEnabled(False)
                global_vars.ui.pushButtonChangeRem.setEnabled(False)

