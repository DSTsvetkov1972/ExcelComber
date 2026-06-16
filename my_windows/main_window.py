# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,Qt,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient, QCursor, QDesktopServices,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,QLineEdit, QComboBox,  QInputDialog,  QRadioButton,
    QTableView, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout)
import global_vars 

# import icons_rc
import resources_rc

# from my_threads.show_result_table_sheet import ShowResultTableThread
# from my_threads.open_files_from_marked_folder import OpenFilesFromMarkedFolderThread


class Ui_MainWindow(object):

    def headers_check(self):

        if self.lineEditOldColumnNameInHeader.text() == '' and self.lineEditNewColumnNameInHeader.text() == '':
            # self.lineEditOldColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500')
            # self.lineEditOldColumnNameInHeaderTitle.setText("В каком заголовке что заменяем:")

            # self.lineEditNewColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500')
            # self.lineEditNewColumnNameInHeaderTitle.setText("В каком заголовке на что заменяем:")

            print('aaa')
            self.radioButtonOldInTopHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )
            self.radioButtonOldInBottomHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )                   
            self.radioButtonNewInTopHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )
            self.radioButtonNewInBottomHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )
                       
            return


        elif (
            (self.lineEditOldColumnNameInHeader.text() != '' or self.lineEditNewColumnNameInHeader.text() != '') and
            self.lineEditOldColumnNameInHeader.text() == self.lineEditNewColumnNameInHeader.text() and
            self.radioButtonOldInTopHeader.isChecked() == self.radioButtonNewInTopHeader.isChecked()
            ):
            
            print('bbb')
            # self.lineEditOldColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500')
            # self.lineEditOldColumnNameInHeaderTitle.setText("Заменяемое значение такое же как новое!")

            # self.lineEditNewColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500')
            # self.lineEditNewColumnNameInHeaderTitle.setText("Новый значение такое же как заменяемое")

            self.radioButtonOldInTopHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )
            self.radioButtonOldInBottomHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )                   
            self.radioButtonNewInTopHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )
            self.radioButtonNewInBottomHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )            
            return

        else:
        #elif (
        #    (self.lineEditOldColumnNameInHeader.text() != '' or self.lineEditNewColumnNameInHeader.text() != '') and
        #    self.lineEditOldColumnNameInHeader.text() != self.lineEditNewColumnNameInHeader.text() or
        #    self.radioButtonOldInTopHeader.isChecked() != self.radioButtonNewInTopHeader.isChecked()
        #    ):
            # self.lineEditOldColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500')
            # self.lineEditOldColumnNameInHeaderTitle.setText("Заменяемое значение:")

            # self.lineEditNewColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500')
            # self.lineEditNewColumnNameInHeaderTitle.setText("Новый значение:")   
            
            print('ccc')

            self.radioButtonOldInTopHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )
            self.radioButtonOldInBottomHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )                   
            self.radioButtonNewInTopHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )
            self.radioButtonNewInBottomHeader.setStyleSheet(
                '''
                QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500;}
                QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
                '''
                )            
 


    def rems_check(self):
        if global_vars.ui.lineEditOldRem.text() == '' and global_vars.ui.lineEditNewRem.text() == '':
            global_vars.ui.lineEditOldRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500')
            global_vars.ui.lineEditOldRemTitle.setText("Какое примечание нужно заменить:")

            global_vars.ui.lineEditNewRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500')
            global_vars.ui.lineEditNewRemTitle.setText("Новое примечание:")




        elif global_vars.ui.lineEditOldRem.text() == global_vars.ui.lineEditNewRem.text():
            
            global_vars.ui.lineEditOldRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500')
            global_vars.ui.lineEditOldRemTitle.setText("Старый примечание (совпадает с новым):")

            global_vars.ui.lineEditNewRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: red; font-weight: 500')
            global_vars.ui.lineEditNewRemTitle.setText("Новое примечание (совпадает со старым):")


        else:
            
            global_vars.ui.lineEditOldRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500')
            global_vars.ui.lineEditOldRemTitle.setText("Примечание которое нужно заменить:")

            global_vars.ui.lineEditNewRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500')
            global_vars.ui.lineEditNewRemTitle.setText("Новое примечание:")



    def setupUi(self, MainWindow):
        #MainWindow.setFixedWidth(1366) 
        #MainWindow.setFixedHeight(768) 
        MainWindow.resize(1100, 380)
        MainWindow.setMaximumSize(1500, 380)
        MainWindow.setMinimumSize(350, 380)    
        MainWindow.setWindowTitle(f"ExcelComber {global_vars.version}")

        icon = QIcon(":/icons/app_icon.png")
        MainWindow.setWindowIcon(icon)
       

        self.centralWidget = QWidget(MainWindow)


        # MENU
        
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 860, 28))
     
        self.action_show_manual = QAction(self.menubar)
        self.action_show_manual.setText("Инструкция on-line") 
        self.menubar.addAction(self.action_show_manual)


        self.action_show_dev_info = QAction(self.menubar)
        self.action_show_dev_info.setText("Связь с разработчиками") 
        self.menubar.addAction(self.action_show_dev_info) 

        # LEFT

        self.verticalLayoutWidgetLeft = QWidget(self.centralWidget)
        self.verticalLayoutWidgetLeft.setGeometry(QRect(10, 41, 320, 266))
        self.verticalLayoutButtonsLeft = QVBoxLayout(self.verticalLayoutWidgetLeft)
        self.verticalLayoutButtonsLeft.setContentsMargins(10, 0, 0, 0)    
             
        self.pushButtonChooseProjectFolder = QPushButton("Выберите папку проекта")
        self.pushButtonChooseProjectFolder.setEnabled(True)
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonChooseProjectFolder)
        
        self.pushButtonXLStoXLSX = QPushButton("Конвертировать xls и xlsm в xlsx")
        self.pushButtonXLStoXLSX.setEnabled(False)
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonXLStoXLSX)

        self.pushButtonProcessing = QPushButton("Просмотреть разметку")
        self.pushButtonProcessing.setEnabled(False)
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonProcessing)

        self.pushButtonOpenChoosedFiles = QPushButton("Открыть выбранные файлы из папки .Исходники")
        self.pushButtonOpenChoosedFiles.setEnabled(False)        
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonOpenChoosedFiles)
 
        self.pushButtonOpenChoosedMDFiles = QPushButton("Открыть выбранные файлы из папки .Размеченные")
        self.pushButtonOpenChoosedMDFiles.setEnabled(False)        
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonOpenChoosedMDFiles)
 
        self.pushButtonDelChoosedMDFiles = QPushButton("Удалить выбранные файлы из папки .Размеченные")
        self.pushButtonDelChoosedMDFiles.setEnabled(False)
        self.pushButtonDelChoosedMDFiles.setStyleSheet("color: red")        
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonDelChoosedMDFiles)
 
        self.pushButtonConcat = QPushButton("Объединить")
        self.pushButtonConcat.setEnabled(False)        
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonConcat)

        self.pushButtonMakeFiles = QPushButton("Создать файлы")
        self.pushButtonMakeFiles.setEnabled(False)        
        self.verticalLayoutButtonsLeft.addWidget(self.pushButtonMakeFiles)

        # **********************************************************************************************
        # CENTER-TOP
        # **********************************************************************************************

        self.verticalLayoutWidgetCenterTop = QWidget(self.centralWidget)
        self.verticalLayoutWidgetCenterTop.setGeometry(QRect(368, 42, 320, 128))
        #self.verticalLayoutWidgetCenterTop.setStyleSheet("border: 2px solid blue; border-radius: 8px; background-color: #f0f0f0;")

        self.verticalLayoutCenterTop = QVBoxLayout(self.verticalLayoutWidgetCenterTop)
        self.verticalLayoutCenterTop.setContentsMargins(10, 0, 0, 0)
        # ---------------------------------------------------------------------------------------------- 
        # CENTER-TOP
        # ----------------------------------------------------------------------------------------------

        
        self.pushButtonHeadersFiller = QPushButton("Заполнить заголовки")
        self.pushButtonHeadersFiller.setEnabled(False)
        self.verticalLayoutCenterTop.addWidget(self.pushButtonHeadersFiller)

        self.pushButtonShowEmpty = QPushButton("Пометить непустые колонки")
        self.pushButtonShowEmpty.setEnabled(False)
        self.verticalLayoutCenterTop.addWidget(self.pushButtonShowEmpty)

        self.pushButtonCleanEmpty = QPushButton("Удалить заголовки пустых колонок")
        self.pushButtonCleanEmpty.setEnabled(False)
        self.verticalLayoutCenterTop.addWidget(self.pushButtonCleanEmpty)


        self.pushButtonRenameColumn = QPushButton("Переименовать заголовки")
        self.pushButtonRenameColumn.setEnabled(False)
        self.verticalLayoutCenterTop.addWidget(self.pushButtonRenameColumn)


        # self.lineEditOldColumnNameInHeaderTitle = QLineEdit(self.centralWidget)
        # self.lineEditOldColumnNameInHeaderTitle.setEnabled(False)
        # self.lineEditOldColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); font-weight: 500')
        # self.lineEditOldColumnNameInHeaderTitle.setText("В каком заголовке что заменяем:")
        # self.lineEditOldColumnNameInHeaderTitle.setAlignment(Qt.AlignLeft)
        # self.verticalLayoutCenterTop.addWidget(self.lineEditOldColumnNameInHeaderTitle)
        
        
        # **********************************************************************************************
        # CENTER-MIDDLE-1
        # **********************************************************************************************
        self.verticalLayoutWidgetCenterMiddle1 = QWidget(self.centralWidget)
        self.verticalLayoutWidgetCenterMiddle1.setGeometry(QRect(368, 176, 260, 20))
        
        self.verticalLayoutCenterMiddle1 = QHBoxLayout(self.verticalLayoutWidgetCenterMiddle1)
        self.verticalLayoutCenterMiddle1.setContentsMargins(10, 0, 0, 0)
        # ----------------------------------------------------------------------------------------------
        # CENTER-MIDDLE-1
        # ---------------------------------------------------------------------------------------------
        
        self.radioWidgetOldHeader = QWidget()

        self.radioButtonOldInTopHeader = QRadioButton('Старый в верхнем', self.radioWidgetOldHeader)
        self.radioButtonOldInTopHeader.setChecked(True)
        self.radioButtonOldInTopHeader.setEnabled(False)
        self.verticalLayoutCenterMiddle1.addWidget(self.radioButtonOldInTopHeader)
        self.radioButtonOldInTopHeader.clicked.connect(self.headers_check)     

        self.radioButtonOldInBottomHeader = QRadioButton('Старый в нижнем', self.radioWidgetOldHeader)   
        self.radioButtonOldInBottomHeader.setEnabled(False)
        self.verticalLayoutCenterMiddle1.addWidget(self.radioButtonOldInBottomHeader)        
        self.radioButtonOldInBottomHeader.clicked.connect(self.headers_check)

        self.radioButtonOldInTopHeader.setStyleSheet(
            '''
            QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            '''
            )
        self.radioButtonOldInBottomHeader.setStyleSheet(
            '''
            QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            '''
            )      

        # **********************************************************************************************
        # CENTER-MIDDLE-2
        # **********************************************************************************************
        self.verticalLayoutWidgetCenterMiddle2 = QWidget(self.centralWidget)
        self.verticalLayoutWidgetCenterMiddle2.setGeometry(QRect(368, 191, 320, 60))
        
        self.verticalLayoutCenterMiddle2 = QVBoxLayout(self.verticalLayoutWidgetCenterMiddle2)
        self.verticalLayoutCenterMiddle2.setContentsMargins(10, 0, 0, 0)
        # ---------------------------------------------------------------------------------------------- 
        # CENTER-MIDDLE-2
        # ----------------------------------------------------------------------------------------------
        self.lineEditOldColumnNameInHeader = QLineEdit(self.centralWidget)
        self.lineEditOldColumnNameInHeader.setEnabled(False)
        self.lineEditOldColumnNameInHeader.setAlignment(Qt.AlignLeft)
        self.verticalLayoutCenterMiddle2.addWidget(self.lineEditOldColumnNameInHeader)
        self.lineEditOldColumnNameInHeader.editingFinished.connect(self.headers_check) 
        
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
              
        # self.lineEditNewColumnNameInHeaderTitle = QLineEdit(self.centralWidget)
        # self.lineEditNewColumnNameInHeaderTitle.setEnabled(False)
        # self.lineEditNewColumnNameInHeaderTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); font-weight: 500')
        # self.lineEditNewColumnNameInHeaderTitle.setText("В каком заголовке на что заменяем:")
        # self.lineEditNewColumnNameInHeaderTitle.setFixedHeight(12)
        # self.lineEditNewColumnNameInHeaderTitle.setAlignment(Qt.AlignLeft)
        # self.verticalLayoutCenterMiddle2.addWidget(self.lineEditNewColumnNameInHeaderTitle)
        
        # **********************************************************************************************       
        # CENTER-MIDDLE-3
        # **********************************************************************************************
        self.verticalLayoutWidgetCenterMiddle3 = QWidget(self.centralWidget)
        self.verticalLayoutWidgetCenterMiddle3.setGeometry(QRect(368, 244, 260, 20))
        
        self.verticalLayoutCenterMiddle3 = QHBoxLayout(self.verticalLayoutWidgetCenterMiddle3)
        self.verticalLayoutCenterMiddle3.setContentsMargins(10, 0, 0, 0)
        # ----------------------------------------------------------------------------------------------        
        # CENTER-MIDDLE-3
        # ----------------------------------------------------------------------------------------------
        
        self.radioWidgetNewHeader = QWidget()

        self.radioButtonNewInTopHeader = QRadioButton('Новый в верхнем', self.radioWidgetNewHeader)
        self.radioButtonNewInTopHeader.setChecked(True)
        self.radioButtonNewInTopHeader.setEnabled(False)
        self.verticalLayoutCenterMiddle3.addWidget(self.radioButtonNewInTopHeader)
        self.radioButtonNewInTopHeader.clicked.connect(self.headers_check)     

        self.radioButtonNewInBottomHeader = QRadioButton('Новый в нижнем', self.radioWidgetNewHeader)   
        self.radioButtonNewInBottomHeader.setEnabled(False)
        self.verticalLayoutCenterMiddle3.addWidget(self.radioButtonNewInBottomHeader)        
        self.radioButtonNewInBottomHeader.clicked.connect(self.headers_check)
             
        self.radioButtonNewInTopHeader.setStyleSheet(
            '''
            QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            '''
            )
        self.radioButtonNewInBottomHeader.setStyleSheet(
            '''
            QRadioButton:checked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            QRadioButton:unchecked {background-color: rgba(0, 0, 0, 0.0); color: grey; font-weight: 500;}
            '''
            )            
 

        # **********************************************************************************************
        # CENTER-BOTTOM
        # **********************************************************************************************----
        self.verticalLayoutWidgetCenterBottom = QWidget(self.centralWidget)
        self.verticalLayoutWidgetCenterBottom.setGeometry(QRect(372, 264, 320, 46))

        self.verticalLayoutCenterBottom = QVBoxLayout(self.verticalLayoutWidgetCenterBottom)
        self.verticalLayoutCenterBottom.setContentsMargins(10, 0, 0, 0)        
        # ----------------------------------------------------------------------------------------------
        # CENTER-BOTTOM      
        # ----------------------------------------------------------------------------------------------

        self.lineEditNewColumnNameInHeader = QLineEdit(self.centralWidget)
        self.lineEditNewColumnNameInHeader.setEnabled(False)
        self.lineEditNewColumnNameInHeader.setAlignment(Qt.AlignLeft)
        self.verticalLayoutCenterBottom.addWidget(self.lineEditNewColumnNameInHeader)
        self.lineEditNewColumnNameInHeader.editingFinished.connect(self.headers_check)      




        # **********************************************************************************************
        # RIGHT-TOP
        # **********************************************************************************************
        self.verticalLayoutWidgetRightTop = QWidget(self.centralWidget)
        self.verticalLayoutWidgetRightTop.setGeometry(QRect(730, 44, 320, 158))

        self.verticalLayoutRightTop = QVBoxLayout(self.verticalLayoutWidgetRightTop)
        self.verticalLayoutRightTop.setContentsMargins(10, 0, 0, 0)        
        # ----------------------------------------------------------------------------------------------    


        self.pushButtonChangeRem = QPushButton("Изменить примечание")
        self.pushButtonChangeRem.setEnabled(False)
        self.verticalLayoutRightTop.addWidget(self.pushButtonChangeRem)

        
        self.lineEditOldRemTitle = QLineEdit(self.centralWidget)
        self.lineEditOldRemTitle.setEnabled(False)
        self.lineEditOldRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); font-weight: 500')
        self.lineEditOldRemTitle.setText("Какое примечание нужно заменить:")
        self.lineEditOldRemTitle.setAlignment(Qt.AlignLeft)
        self.verticalLayoutRightTop.addWidget(self.lineEditOldRemTitle)

        self.lineEditOldRem = QLineEdit(self.centralWidget)
        self.lineEditOldRem.setEnabled(False)
        self.lineEditOldRem.setAlignment(Qt.AlignLeft)
        self.verticalLayoutRightTop.addWidget(self.lineEditOldRem)
        self.lineEditOldRem.editingFinished.connect(self.rems_check)
        
        
        self.lineEditNewRemTitle = QLineEdit(self.centralWidget)
        self.lineEditNewRemTitle.setEnabled(False)
        self.lineEditNewRemTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); font-weight: 500')
        self.lineEditNewRemTitle.setText("Новое примечание:")
        self.lineEditNewRemTitle.setAlignment(Qt.AlignLeft)
        self.verticalLayoutRightTop.addWidget(self.lineEditNewRemTitle)

        self.lineEditNewRem = QLineEdit(self.centralWidget)
        self.lineEditNewRem.setEnabled(False)
        self.lineEditNewRem.setAlignment(Qt.AlignLeft)
        self.verticalLayoutRightTop.addWidget(self.lineEditNewRem)
        self.lineEditNewRem.editingFinished.connect(self.rems_check)

        self.lineEditInClipboardTitle = QLineEdit(self.centralWidget)
        self.lineEditInClipboardTitle.setEnabled(False)
        self.lineEditInClipboardTitle.setStyleSheet('border: none; background-color: rgba(0, 0, 0, 0.0); color: green; font-weight: 500')
        # self.lineEditInClipboardTitle.setText("md-файлы и листы для редактирования:")
        self.lineEditInClipboardTitle.setAlignment(Qt.AlignLeft)
        self.verticalLayoutRightTop.addWidget(self.lineEditInClipboardTitle)

        
        # RIGHT-BOTTOM
        # ----------------------------------------------------------------------------------------------
        self.verticalLayoutWidgetRightBottom = QWidget(self.centralWidget)
        self.verticalLayoutWidgetRightBottom.setGeometry(QRect(730, 204, 320, 96))

        self.verticalLayoutRightBottom = QVBoxLayout(self.verticalLayoutWidgetRightBottom)
        self.verticalLayoutRightBottom.setContentsMargins(10, 0, 0, 0)        
        # ----------------------------------------------------------------------------------------------    

        self.tableMDFilesInClipboard = QTableWidget()
        self.tableMDFilesInClipboard.horizontalHeader().hide()
        self.tableMDFilesInClipboard.setColumnWidth(0, 320)
        self.tableMDFilesInClipboard.setFont(QFont("Arial", 7))
        self.tableMDFilesInClipboard.setSelectionMode(QTableWidget.NoSelection)


        self.verticalLayoutRightBottom.addWidget(self.tableMDFilesInClipboard)
        # self.tableMDFilesInClipboard.setVisible(False)
        
        
        # BOTTOM

        self.verticalLayoutWidgetLabels = QWidget(self.centralWidget)
        self.verticalLayoutWidgetLabels.setGeometry(QRect(14, 316, 1366, 56)) #QRect(10, 120, 320, 120)
        self.verticalLayoutLabels = QVBoxLayout(self.verticalLayoutWidgetLabels)
        self.verticalLayoutLabels.setContentsMargins(10, 10, 10, 10)    

        self.project_folder_label = QLabel('Не выбрана папка проекта.')
        self.project_folder_label.setStyleSheet('color: red')      
        self.verticalLayoutLabels.addWidget(self.project_folder_label)

        self.info_label = QLabel('Выберите папу проекта!')
        self.info_label.setStyleSheet('color: red')        
        self.verticalLayoutLabels.addWidget(self.info_label)
